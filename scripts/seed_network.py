"""Stage 0 seed: load the benchmark network with WNTR, run a 24 h EPANET simulation,
and upsert its counts into the `networks` table. Idempotent (ON CONFLICT on name).

Usage: python scripts/seed_network.py  (env: DATABASE_URL, NETWORK_NAME, NETWORK_INP)
"""

from __future__ import annotations

import hashlib
import os
import sys
import tempfile
from pathlib import Path

import numpy as np
import psycopg
import wntr

ROOT = Path(__file__).resolve().parents[1]

UPSERT = """
INSERT INTO networks (name, inp_sha256, node_count, link_count, pump_count, tank_count, loaded_at)
VALUES (%(name)s, %(sha)s, %(nodes)s, %(links)s, %(pumps)s, %(tanks)s, now())
ON CONFLICT (name) DO UPDATE SET
  inp_sha256 = EXCLUDED.inp_sha256,
  node_count = EXCLUDED.node_count,
  link_count = EXCLUDED.link_count,
  pump_count = EXCLUDED.pump_count,
  tank_count = EXCLUDED.tank_count,
  loaded_at  = now()
RETURNING id
"""


def simulate_24h(inp_path: Path) -> tuple[wntr.network.WaterNetworkModel, float]:
    """Load the .inp, run a 24 h EpanetSimulator in a scratch dir, return (model, min pressure)."""
    wn = wntr.network.WaterNetworkModel(str(inp_path))
    wn.options.time.duration = 24 * 3600
    with tempfile.TemporaryDirectory() as tmp:
        results = wntr.sim.EpanetSimulator(wn).run_sim(file_prefix=os.path.join(tmp, "seed"))
    pressure = results.node["pressure"].loc[:, wn.junction_name_list].to_numpy()
    if not np.isfinite(pressure).all():
        raise RuntimeError("EPANET 24 h run produced non-finite junction pressures")
    return wn, float(pressure.min())


def main() -> int:
    name = os.environ.get("NETWORK_NAME", "Net3")
    inp = ROOT / os.environ.get("NETWORK_INP", "data/networks/Net3.inp")
    dsn = os.environ.get("DATABASE_URL")
    if not dsn:
        raise SystemExit("DATABASE_URL is not set (the twin container sets it; see .env.example)")

    sha = hashlib.sha256(inp.read_bytes()).hexdigest()
    wn, p_min = simulate_24h(inp)
    row = {
        "name": name,
        "sha": sha,
        "nodes": wn.num_nodes,
        "links": wn.num_links,
        "pumps": wn.num_pumps,
        "tanks": wn.num_tanks,
    }
    with psycopg.connect(dsn) as conn, conn.cursor() as cur:
        cur.execute(UPSERT, row)
        (network_id,) = cur.fetchone()
    print(
        f"seeded {name} id={network_id} nodes={row['nodes']} links={row['links']} "
        f"pumps={row['pumps']} tanks={row['tanks']} min_pressure_24h={p_min:.2f} sha256={sha[:12]}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
