"""S0: Net3 parses with WNTR, a 24 h EPANET run completes, and junction pressures are finite."""

from __future__ import annotations

import os
import tempfile

import numpy as np
import wntr


def test_net3_parses(net3_path):
    wn = wntr.network.WaterNetworkModel(str(net3_path))
    assert wn.num_nodes > 0 and wn.num_links > 0
    assert wn.num_pumps >= 1 and wn.num_tanks >= 1


def test_net3_24h_epanet_run_pressures_finite(net3_path):
    wn = wntr.network.WaterNetworkModel(str(net3_path))
    wn.options.time.duration = 24 * 3600
    with tempfile.TemporaryDirectory() as tmp:
        results = wntr.sim.EpanetSimulator(wn).run_sim(file_prefix=os.path.join(tmp, "t"))
    pressure = results.node["pressure"].loc[:, wn.junction_name_list].to_numpy()
    assert pressure.shape[0] >= 24
    assert np.isfinite(pressure).all()
