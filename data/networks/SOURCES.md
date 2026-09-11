# Benchmark network sources

| File | Source | Retrieved | sha256 |
|---|---|---|---|
| `Net3.inp` | Bundled copy in the installed `wntr==1.5.0` package: `wntr/library/networks/Net3.inp` (upstream: USEPA/WNTR GitHub repository, `examples/networks/Net3.inp`, https://github.com/USEPA/WNTR/tree/main/examples/networks) | 2026-09-11 | `ea3e825c4fef0b5cba47fb06301bc85253f18b6364dc96c44d9fb492c40faa52` |

Net3 is the EPANET example network 3 (published benchmark; §4 S0). It is the Stage 0–2 network.
L-Town / BattLeDIM are added later for realism (§4 S0) and will be listed here with their own hashes.

Verify: `sha256sum data/networks/Net3.inp`
