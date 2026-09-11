# MIZAN

Differentiable hydraulic twin + federated surrogate + n8n/EPANET MVP. Miyahthon 2026, Track 4 finalist.
Plan, gates and calendar: **[docs/BUILD_PLAN.md](docs/BUILD_PLAN.md)**.

## Quick start (one command)

Requires Docker with Compose v2, GNU make, git. No `.env` needed (see `.env.example` to override).

```sh
make up
```

Builds the images, starts the stack, waits until every service is healthy, and seeds the Net3 benchmark
network into Postgres. Exits non-zero on any failure.

## Services and ports (host defaults)

| Service | Image | Host port | Purpose |
|---|---|---|---|
| `db` | `timescale/timescaledb:2.21.1-pg16` | 5433 | PostgreSQL 16 + TimescaleDB, schema in `db/init/` |
| `api` | `mizan/twin` (this repo's `Dockerfile`) | 8000 | FastAPI — `GET /health` |
| `twin` | `mizan/twin` | — | Python 3.11 + JAX (CPU) + WNTR; tests and seeding run here |
| `n8n` | `n8nio/n8n:1.110.1` | 5678 | Orchestration; `./n8n` mounted at `/home/node/workflows` |
| `flower` | — | — | Stage 4 placeholder (commented in `docker-compose.yml`) |
| `console` | — | — | Stage 5 placeholder (commented in `docker-compose.yml`) |

## Verify

```sh
make verify     # pytest (unit + integration) + ruff inside twin, api /health, n8n /healthz → PASS/FAIL summary
curl -s localhost:8000/health
```

Other targets: `make test` (host, unit only), `make lint`, `make logs`, `make down`, `make clean` (also drops volumes).

## Layout (§6)

```
docker-compose.yml  Dockerfile  Makefile  pyproject.toml
packages/physics/     residual, solve, pumps, validate   (S1)
packages/optimize/    objective, gradient, baseline_ga   (S2)
packages/surrogate/   datagen, models                    (S3)
packages/federated/   Flower server/clients, ledger      (S4)
packages/api/         FastAPI                            (S0 /health, S5 runs)
apps/console/         Next.js operator console           (S5)
n8n/                  versioned workflow JSON            (S5)
notebooks/            validation evidence                (S1+)
data/networks/        Net3.inp + SOURCES.md
db/init/              001_schema.sql
scripts/              seed_network.py, verify_stack.py
tests/                test_network, test_jax_env, test_health (integration)
docs/                 BUILD_PLAN.md
```
