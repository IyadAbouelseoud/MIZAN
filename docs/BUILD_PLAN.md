# MIZAN — Build Plan, Stages 0–6

Source of truth: "MIZAN — Master Build & Defense File" (compiled 10 Sep 2026). Section numbers (§) below cite it. Anything this plan adds that the Master File does not specify is tagged **[proposed]** and listed in the Appendix.

Plan date: 11 Sep 2026 (Week 1). Final: 14–16 Dec 2026, Jeddah.

---

## 1. Header

### 1.1 Scope lock (§0.2)

Build **three pillars only**:

1. The differentiable twin (JAX hydraulic core + optimizer + surrogate) — S1, S2, S3
2. The federated layer — S4
3. The n8n / EPANET MVP (orchestration, API, console) — S5

**Roadmap only — never build** (§0.2):

- QUBO / tensor-network layer
- Structural causal / counterfactual engine
- Agentic Arabic operator copilot
- Giga-project simulation marketplace

Any new pillar proposed after **1 Nov** goes to the roadmap automatically.

### 1.2 Claims → stage that satisfies them (§0.1)

| Claim | Statement (§0.1) | Satisfied by | Evidence artifact |
|---|---|---|---|
| C1 | Differentiable neural program → JAX hydraulic model with gradients verified against finite differences | **S1** | `notebooks/02_gradient_fd_check.ipynb`, `tests/test_gradients.py` |
| C2 | Operator states a target → optimal pump/valve schedules, end to end, live | **S2** (optimizer) + **S5** (console → API → schedule) | `runs`, `schedules` tables; live demo |
| C3 | Physics-verified → every schedule replayed in EPANET and reported feasible | **S2** (repair pass) + **S5** (feasibility gate, Constraint Ledger screen) | `verification` table; EPANET verification block |
| C4 | FNO, thousands of times faster → trained surrogate with a measured speedup and an error bound | **S3** | `notebooks/07_s3_gate.ipynb` (speedup + error bound) |
| C5 | Backpropagation outputs the control policy → gradient optimizer beats a GA baseline | **S2** | `baselines` table; `notebooks/04_s2_gate.ipynb` |
| C6 | Federated learning (gradients, not raw SCADA) → 2-client federated training plus a byte-level privacy ledger | **S4** | `federation_rounds` table; Federation & Privacy screen |
| C7 | n8n pipeline connecting EPANET to a local Python twin → working orchestration, triggered live | **S5** (foundation in **S0**: n8n service + `./n8n` mount) | `n8n/*.json`, live trigger |
| C8 | SCADA integration design → architecture doc plus a mocked OPC-UA/historian adapter | **S5** | `docs/SCADA_INTEGRATION.md`, `packages/api/scada_mock.py` |

All eight must exist by 14 Dec; they are contractual.

### 1.3 Gate-before-next-stage rule (§4)

A stage is **done only when its gate passes**. No stage starts before its predecessor's gate is green. Overlapping windows in §5 (S3 starts W6 while S2 runs to W7; S5 starts W9 while S4 runs to W10) are allowed only because the overlapping stage depends on a *different* predecessor: S3 depends on S1 (solver + datagen), S5's UI/n8n work depends on S0 and S2's API contract. Where a hard dependency exists (S2 ← S1, S4 ← S3 surrogate, S6 ← S5) the rule is strict.

### 1.4 Feature freeze — 18 Nov (§0.2, §5)

After **18 Nov 2026**, only bug fixes, tests, and demo polish. No new screens, services, models, or objective terms.

Forbidden phrasing anywhere in code, docs, deck, or demo: claims of a global optimum, guaranteed savings, or full autonomy. The optimizer produces *a feasible, EPANET-verified, lower-cost schedule than the GA baseline* — nothing stronger.

---

## 2. Calendar — §5 weeks merged with the programme calendar

| Wk | Dates | §5 milestone | Programme event | Collision |
|---|---|---|---|---|
| W1 | Sep 10–16 | repo, Docker, network (S0) | **Digital camp 13–17 Sep** | ⚠ K1 |
| W2 | Sep 17–23 | JAX residual matches EPANET on one scenario | Digital camp (to 17 Sep) | ⚠ K1 |
| W3 | Sep 24–30 | Newton + implicit diff (passes FD check) | — | |
| W4 | Oct 1–7 | pumps, tanks, energy; launch datagen → **S1 gate** | **Riyadh camp 6–8 Oct** | ⚠ K2 |
| W5 | Oct 8–14 | objective and optimizer (first feasible schedule) | S1 slip trigger **8 Oct**; **Rabigh camp 13–15 Oct** | ⚠ K2, K3 |
| W6 | Oct 15–21 | GA baseline and benchmark harness | Prototyping sprint starts (~16 Oct) | ⚠ K4 |
| W7 | Oct 22–28 | relaxation + repair → **S2 gate** | Prototyping sprint | ⚠ K4 |
| W8 | Oct 29–Nov 4 | DeepONet (< 5% error) | Prototyping sprint; second reviewer per component due | |
| W9 | Nov 5–11 | Graph-FNO attempt, Flower up → **FNO go/no-go** | Prototyping sprint | |
| W10 | Nov 12–18 | DP + privacy ledger, UI starts → **S4 gate**; **freeze 18 Nov** | Prototyping sprint ends (~20 Nov): lab-tested prototype due | ⚠ K4, K5 |
| W11 | Nov 19–25 | UI, n8n, end-to-end run unattended | — | ⚠ K5 |
| W12 | Nov 26–Dec 2 | fixes, demo dataset, rehearsal → **S5 gate** | — | |
| W13 | Dec 3–9 | 3 clean run-throughs, recorded backup, final deck | — | |
| W14 | Dec 10–13 | travel and venue setup | — | |
| — | Dec 14–16 | **Final, Jeddah** | Final 14–16 Dec | |

### Collisions

**K1 — Digital camp (13–17 Sep) overlaps W1–W2.**
Impact: mandatory attendance removes ~5 working days from the S0 gate week and from the start of the W2 JAX residual work; the physics lead's W1 JAX/optimistix study (§13) is squeezed.
[proposed] Mitigation: S0 is executed and gated on 11–12 Sep (this session), before camp. The physics lead's W1 study moves to camp evenings using `notebooks/00_jax_warmup.ipynb`. The W2 target (residual matches EPANET on one scenario) keeps its 23 Sep date; W2 work starts 18 Sep with a 5-day, not 7-day, budget. No slip into W3.

**K2 — Riyadh camp (6–8 Oct) collides with the S1 gate (end W4, 7 Oct) and the S1 slip trigger (8 Oct).**
Impact: the team is travelling exactly when the highest-risk gate must be judged and the smaller-network fallback decided.
[proposed] Mitigation: internal S1 gate moved forward to **Sun 4 Oct**; the gate notebooks run unattended via `make gate-s1` [proposed] so evidence exists before travel. The 8 Oct go/no-go is a 30-minute decision meeting held at camp, using the 4 Oct evidence. Datagen launch (W4) is scripted so it starts on 5 Oct and runs during camp.

**K3 — Rabigh camp (13–15 Oct) falls inside W5 (Oct 8–14) / start of W6.**
Impact: W5 (objective + optimizer, first feasible schedule) loses its last two days; W6 GA baseline starts a day late.
[proposed] Mitigation: W5 target "first feasible schedule" is due **12 Oct**. GA baseline design (parameter ranges, fitness = same J as §3) is written as a doc during camp travel; coding starts 16 Oct.

**K4 — 5-week prototyping sprint (≈16 Oct – 20 Nov) deliverable "lab-tested prototype" vs the S1/S2 gates.**
Impact: the programme's deliverable date does not match any single §4 gate; it spans S2 gate (28 Oct), S3 (11 Nov) and S4 gate (18 Nov).
[proposed] Mitigation: define the lab-tested prototype as **S2 gate output + S3 DeepONet baseline + S4 partial demo**: the 20-scenario benchmark harness with EPANET verification (`notebooks/04_s2_gate.ipynb`), the DeepONet held-out error report, and the Flower 2-client run with ledger. The 18 Nov freeze is treated as the sprint deadline. Nothing later than S4 is promised to the programme.

**K5 — Feature freeze 18 Nov (W10) precedes the S5 build weeks W11–W12 (UI, n8n, end-to-end run).**
Impact: read literally, the console and n8n workflows would be "new features" after the freeze.
[proposed] Mitigation: all six S5 screens and all n8n workflows are **scoped, stubbed and routed by 18 Nov** (empty/solving/infeasible/verification-failed states render with fixture data). W11–W12 work completes those already-scoped screens and is classed as demo polish; no new screen, endpoint, workflow, or table is added after 18 Nov.

---

## 3. Roles for 4 people [proposed]

§13 is written for 5 people. Mapping onto 4:

| Person | Primary role (§13) | Secondary | Critical weeks |
|---|---|---|---|
| **P1** | Physics lead — JAX core, implicit diff, validation. Sole, dedicated owner from W1. | **Pitch lead** (W11–14; a builder, satisfies §13) | W1–7, W11–14 |
| **P2** | ML lead — datagen, DeepONet, Graph-FNO, federation | Second reviewer of physics core (reads the code by W4) | W4–10 |
| **P3** | Backend/infra — FastAPI, Postgres, Docker, n8n, integration | Second reviewer of optimizer and federation | W1, W9–12 |
| **P4** | Front-end/design — console, design system, charts | n8n workflow authoring with P3 (team strength); second reviewer of API/DB | W9–12 |

Rationale: the physics lead is free after W7 and knows the core best, so they carry the Q&A-heavy pitch. P3 and P4 split the two integration roles, matching the team's stated strengths (Python, PostgreSQL, Docker, Git, n8n). The team's JAX / neural-operator gap is closed by P1 (W1 JAX + optimistix study) and P2 (W1–3 DeepONet/FNO study alongside S0/S1 support).

Second reviewer per component (all named by W8, per §12):

| Component | Owner | Second reviewer |
|---|---|---|
| `packages/physics/*` | P1 | P2 |
| `packages/optimize/*` | P1 | P3 |
| `packages/surrogate/*` | P2 | P1 |
| `packages/federated/*` | P2 | P3 |
| `packages/api/*`, `db/`, `docker-compose.yml`, `n8n/` | P3 | P4 |
| `apps/console/*` | P4 | P3 |
| Pitch, deck, run of show | P1 | P4 |

---

## 4. Stages

### S0 — Foundation

**Objective & claims served:** monorepo, Docker Compose environment, EPANET benchmark network loaded, CI running (§4 S0). Foundation for C7 (n8n service, `./n8n` mount) and the persistence layer for C2/C3/C5/C6 (§6 tables). Serves no claim directly.
**Window:** W1, Sep 10–16 (executed 11 Sep).
**Owner / reviewer:** P3 / P4.

**Entry criteria**
- Host has Docker with Compose v2, git, Python 3.11+.
- Working directory is empty or a fresh `git init`.
- `git config user.name` / `user.email` set to a human team member.

**Task breakdown** (this is exactly what Part B of the 11 Sep session builds)
- [ ] S0.1 Preflight: `docker compose version`, `git --version`, `ls -A`; `git init -b main` if not a repo. Stop if Compose v2 missing or a non-MIZAN project is present. (no files)
- [ ] S0.2 Skeleton per §6: `docker-compose.yml`; `packages/physics/{residual,solve,pumps,validate}.py`; `packages/optimize/{objective,gradient,baseline_ga}.py`; `packages/surrogate/{datagen,models}.py`; `packages/federated/README.md`; `packages/api/`; `apps/console/README.md`; `n8n/`; `notebooks/README.md`. Stage 1+ modules are docstring-only. Root: `README.md`, `.gitignore`, `.env.example`, single `pyproject.toml` (Python 3.11; runtime `jax[cpu]`, `wntr`, `fastapi`, `uvicorn`, `pydantic`, `psycopg[binary]`; dev `pytest`, `ruff`, `httpx`; exact pins).
- [ ] S0.3 Benchmark network: `data/networks/Net3.inp` from the USEPA/WNTR GitHub `examples/networks` or the installed wntr package copy; `data/networks/SOURCES.md` (URL/path, retrieval date, sha256); `scripts/seed_network.py` (loads Net3 with WNTR, 24 h EpanetSimulator, idempotent upsert into `networks`).
- [ ] S0.4 Database: `db/init/001_schema.sql` — timescaledb extension; [proposed] `networks` table (id, name, inp_sha256, node_count, link_count, pump_count, tank_count, loaded_at); the six §6 tables with `network_id → networks`, `run_id → runs`, timestamptz columns. No hypertables in S0.
- [ ] S0.5 Compose: services `db` (postgres 16 + timescaledb), `twin`, `api`, `n8n`; healthchecks on db/api/n8n; pinned image tags; named volumes; host ports configurable with defaults (db 5433, api 8000, n8n 5678); `api` exposes `GET /health` (db status, loaded network name + node/link counts, jax and wntr versions); `./n8n` mounted; `twin`/`api` share `Dockerfile` with dependency layer cached; `flower` and `console` are commented placeholders naming S4 / S5.
- [ ] S0.6 `Makefile`: `up` (build, start, wait healthy, seed; non-zero on failure), `verify`, `test`, `lint`, `logs`, `down`, `clean` (`down -v`, this project only).
- [ ] S0.7 Tests: `tests/test_network.py` (Net3 parses, 24 h run completes, pressures finite); `tests/test_jax_env.py` (x64 on, `jax.grad` matches analytic derivative to 1e-12); `tests/test_health.py` (integration, hits `/health`). `make verify` = pytest in `twin` against the live stack + `/health` + n8n `/healthz` + PASS/FAIL summary; ruff clean.
- [ ] S0.8 CI: `.github/workflows/ci.yml` on push + PR; job `lint-test` (Python 3.11, pip cache, ruff, non-integration pytest); job `stack` (`make up` → `make verify` → `make down`). YAML validated with a Python yaml load; equivalent commands run locally.
- [ ] S0.9 Commit `stage-0: foundation + build plan` as the human git identity. No push.

**Exit gate** (§4 S0, verbatim): *"any team member clones the repo and gets a working environment with one command."*

| Metric | Exact proof | Evidence stored |
|---|---|---|
| Fresh clone → `make up` exits 0, all services healthy | `git clone <repo> /tmp/x && cd /tmp/x && make up` (no `.env`) | CI job `stack`; session Part C log |
| `/health` reports db ok, Net3 loaded with node/link counts | `curl -s localhost:8000/health` | `networks` table row |
| n8n answers | `curl -s localhost:5678/healthz` | `make verify` summary |
| pytest green, ruff clean | `make verify` | CI job `lint-test` + `stack` |
| CI YAML valid, jobs mirror local commands | `python -c "import yaml; yaml.safe_load(open('.github/workflows/ci.yml'))"` | `.github/workflows/ci.yml` |
| Only human authors, no AI attribution | `git log --format='%an <%ae>%n%b' \| grep -iE "claude\|anthropic\|co-authored"` → empty | git history |

**Risks & cut trigger**
- Net3.inp unobtainable from the named sources → stop and report (no substitute network without team sign-off).
- Docker/Compose v2 unavailable on a member's laptop → that member develops via `pip install -e .[dev]` on host for S1 only; the gate still requires Compose. Fallback: none — S0 is a hard prerequisite for everything.
- Cut trigger: if S0 is not green by **16 Sep**, S1 starts anyway on the host Python env and S0 is finished by P3 during the digital camp evenings (K1).

**Demo/defense artifacts**
- `README.md` quick start (one command) — shown to judges as reproducibility evidence.
- `docs/BUILD_PLAN.md` (this file).
- `data/networks/SOURCES.md` — provenance of the benchmark network.
- `/health` JSON — first slide of the "it runs" story.

---

### S1 — Differentiable physics core

**Objective & claims served:** JAX steady-state solver with implicit-differentiation gradients (§4 S1). Serves **C1** fully; is the substrate for C2, C3, C5.
**Window:** W2–W4, Sep 17 – Oct 7 (internal gate 4 Oct, K2).
**Owner / reviewer:** P1 (sole, dedicated) / P2 (reads the code by W4).

**Entry criteria**
- S0 gate green.
- P1 has completed the W1 JAX autodiff + optimistix study (`notebooks/00_jax_warmup.ipynb` [proposed]).
- Net3 in `networks` table; `tests/test_network.py` green.

**Task breakdown**
- [ ] S1.1 Network → arrays: parse Net3 with WNTR into JAX arrays (incidence matrix, pipe R from Hazen-Williams with α=1.852, node demands, fixed heads for reservoirs). Creates `packages/physics/network.py` [proposed], `tests/test_topology.py` [proposed].
- [ ] S1.2 Residual F(x,u,d): continuity at each node (inflow − outflow = demand) and headloss h_i − h_j = R·q^α (§3). Creates `packages/physics/residual.py` (implementation), `tests/test_residual.py` [proposed].
- [ ] S1.3 W2 checkpoint: residual evaluated at EPANET's solution is ≈ 0 on one scenario. Creates `notebooks/01_residual_check.ipynb`.
- [ ] S1.4 Newton-Raphson solve with line search / damping; `jax.lax.custom_root` for the implicit gradient (§3). Never unroll Newton. Creates `packages/physics/solve.py` (implementation).
- [ ] S1.5 Gradient check: ∂heads/∂demand and ∂heads/∂(pipe R) vs central finite differences at x64. Creates `notebooks/02_gradient_fd_check.ipynb`, `tests/test_gradients.py`.
- [ ] S1.6 Pump model H(q,s) = s²A − B·q^C·s^(2−C); power P = ρgqH/η(q) with the efficiency **curve** (flat efficiency forbidden, §3). Creates `packages/physics/pumps.py` (implementation), `tests/test_pumps.py` [proposed].
- [ ] S1.7 Tanks and 24 h stepping: sequence of steady-state solves with tank levels integrated between hours (quasi-steady) [proposed detail]; energy per hour. Changes `packages/physics/solve.py`.
- [ ] S1.8 Validator: heads/flows vs EPANET (WNTR) on random demand scenarios, relative L2; convergence sweep. Creates `packages/physics/validate.py` (implementation), `tests/test_validate.py`.
- [ ] S1.9 Gate notebook and `make gate-s1` [proposed]: runs S1.8 on 100 scenarios (accuracy) and 1,000 scenarios (convergence), writes a JSON report. Creates `notebooks/03_s1_gate.ipynb`, changes `Makefile`.
- [ ] S1.10 (W4, P2) Datagen launch: LHS over demand multipliers, tariffs, schedules; parallel EPANET runs, 50k–200k target (§4 S3). Creates `packages/surrogate/datagen.py` (implementation), `scripts/run_datagen.py` [proposed].
- [ ] S1.11 Second-reviewer read-through by P2 (by W4) with written notes. Creates `docs/reviews/S1_review.md` [proposed].

**Exit gate** (§4 S1, verbatim — all must pass)

| Metric (verbatim) | Exact proof | Evidence stored |
|---|---|---|
| heads/flows vs EPANET < 0.5% relative L2 on 100 random demand scenarios | `pytest tests/test_validate.py -k accuracy`; `notebooks/03_s1_gate.ipynb` | notebook outputs; `data/reports/s1_gate.json` [proposed] |
| gradients vs central finite differences < 1e-4 relative error | `pytest tests/test_gradients.py`; `notebooks/02_gradient_fd_check.ipynb` | notebook outputs |
| 1,000 random scenarios converge with 0 failures | `pytest tests/test_validate.py -k convergence` | `data/reports/s1_gate.json` [proposed] |

**Risks & cut trigger** (§12)
- Highest-risk stage. Trigger: **S1 slips past 8 Oct** → cut S3, ship differentiable physics only (still covers C1, C2, C3, C5), simplify to a smaller network (§4 S1, §12). [proposed] the smaller network is a Net3 sub-zone or WNTR's `Net1`, decided by P1 on 8 Oct at the Riyadh camp.
- Newton non-convergence on some scenarios → damping / continuation on demand multiplier before invoking the fallback.
- P1 unavailable → P2 is the named reviewer and takes over with the review notes.

**Demo/defense artifacts**
- `notebooks/02_gradient_fd_check.ipynb` — C1 evidence (gradient vs FD table).
- `notebooks/03_s1_gate.ipynb` — accuracy histogram and convergence count.
- One slide: "EPANET is the referee, never the model" (§2).

---

### S2 — Optimizer & objective

**Objective & claims served:** gradient schedule optimizer with full constraint handling plus an honestly tuned GA baseline (§4 S2). Serves **C5** fully, **C2** (schedule production) and **C3** (repair pass + EPANET replay).
**Window:** W5–W7, Oct 8–28 (first feasible schedule due 12 Oct, K3).
**Owner / reviewer:** P1 / P3.

**Entry criteria**
- S1 gate green (all three metrics) or the 8 Oct fallback decision recorded.
- Pump efficiency curves for Net3 pumps loaded (S1.6).
- `runs`, `schedules`, `verification`, `baselines`, `constraint_ledger` tables exist (S0).

**Task breakdown**
- [ ] S2.1 Objective J = Σ tariff·P·Δt + λ_p·ΣΣ relu(h_min − h)² + λ_v·Σ(tank_end − tank_start)² + λ_s·Σ switches² (§3). Written justification per λ. Creates `packages/optimize/objective.py` (implementation), `docs/OBJECTIVE_LAMBDAS.md` [proposed].
- [ ] S2.2 Control vector: pump speeds × hours; JSON objective/constraints → loss + control vector compiler (§2 step 2). Creates `packages/optimize/compile.py` [proposed], `tests/test_objective.py` [proposed].
- [ ] S2.3 Gradient descent through the JAX core (optax Adam / L-BFGS [proposed choice]); loss curve logging; cancel hook. Creates `packages/optimize/gradient.py` (implementation).
- [ ] S2.4 W5 checkpoint: first feasible schedule on Net3 replayed in EPANET. Creates `notebooks/04a_first_schedule.ipynb` [proposed].
- [ ] S2.5 GA baseline, honestly tuned (population, generations, mutation searched on the same J, same time budget reported). Creates `packages/optimize/baseline_ga.py` (implementation), `docs/GA_TUNING.md` [proposed].
- [ ] S2.6 Benchmark harness: 20 randomized scenarios; records energy cost, constraint satisfaction, wall-clock for both methods into `baselines` and `constraint_ledger`. Creates `scripts/benchmark_s2.py` [proposed], `tests/test_benchmark.py` [proposed].
- [ ] S2.7 Discrete pumps: sigmoid relaxation to [0,1], temperature annealing, rounding (§3). Changes `packages/optimize/gradient.py`.
- [ ] S2.8 EPANET repair pass after rounding and post-rounding optimality gap report (§3). Creates `packages/optimize/repair.py` [proposed]; writes `verification` rows.
- [ ] S2.9 Gate notebook `notebooks/04_s2_gate.ipynb`: 20-scenario table (gradient vs GA: cost, constraints, wall-clock ratio).
- [ ] S2.10 Second-reviewer read-through by P3. Creates `docs/reviews/S2_review.md` [proposed].

**Exit gate** (§4 S2, verbatim): *"matches or beats the GA on energy cost, satisfies all constraints, and uses ≥ 50× less wall-clock, across 20 randomized scenarios."*

| Metric | Exact proof | Evidence stored |
|---|---|---|
| matches or beats the GA on energy cost (20 scenarios) | `python scripts/benchmark_s2.py --scenarios 20`; `notebooks/04_s2_gate.ipynb` | `baselines` (method ∈ {gradient, ga}, energy_kwh) |
| satisfies all constraints | same harness; every `constraint_ledger.satisfied = true`; `verification.epanet_feasible = true` | `constraint_ledger`, `verification` |
| ≥ 50× less wall-clock | `baselines.wall_ms` ratio per scenario, min over 20 ≥ 50 | `baselines`, `runs.wall_ms` |

**Risks & cut trigger**
- Gradient optimizer stuck in poor local minima vs GA → multi-start from GA's best individual [proposed]; report honestly if GA wins on any scenario.
- Wall-clock ratio < 50× → JIT the full 24 h solve; if still short, report the measured ratio and do not claim 50×.
- Trigger: S2 not green by **28 Oct** → freeze scope to the 20-scenario harness as-is, carry the gap into the prototyping sprint report (K4), and start S3 regardless (S3 depends on S1 only).

**Demo/defense artifacts**
- `notebooks/04_s2_gate.ipynb` — C5 table (gradient vs GA).
- Post-rounding optimality gap figure — pre-empts the "you relaxed discrete pumps" question.
- `docs/OBJECTIVE_LAMBDAS.md`, `docs/GA_TUNING.md` — "honestly tuned" defense.

---

### S3 — Neural operator surrogate

**Objective & claims served:** surrogate mapping (demand, schedule) → (heads, flows) (§4 S3). Serves **C4**; the surrogate fast path in §2 step 3.
**Window:** W6–W9, Oct 15 – Nov 11 (FNO go/no-go W9).
**Owner / reviewer:** P2 / P1.

**Entry criteria**
- S1 gate green; datagen (S1.10) launched in W4 and ≥ 50k runs landed.
- S2 objective available so gradient agreement can be measured on the real J.

**Task breakdown**
- [ ] S3.1 Dataset assembly: LHS samples → (demand multipliers, tariffs, schedules) → EPANET heads/flows; train/val/held-out split by scenario. Changes `packages/surrogate/datagen.py`; creates `data/surrogate/README.md` [proposed] (data lives outside git).
- [ ] S3.2 DeepONet baseline (branch: demand + schedule; trunk: node/link id + hour). Creates `packages/surrogate/models.py` (DeepONet class), `scripts/train_surrogate.py` [proposed].
- [ ] S3.3 W8 checkpoint: DeepONet < 5% held-out relative L2. Creates `notebooks/05_deeponet.ipynb`.
- [ ] S3.4 Graph-FNO: GNN encoder over Net3 topology, FNO along the 24 h axis. Changes `packages/surrogate/models.py`.
- [ ] S3.5 Graph-FNO training and comparison vs DeepONet on the same split. Creates `notebooks/06_graph_fno.ipynb`.
- [ ] S3.6 Speedup measurement vs the JAX core (same batch, same hardware, warm JIT). Creates `scripts/bench_surrogate.py` [proposed].
- [ ] S3.7 Gradient agreement: optimize J through the surrogate, replay through JAX core + EPANET, compare final cost. Creates `notebooks/07_s3_gate.ipynb`.
- [ ] S3.8 W9 go/no-go record: FNO vs DeepONet decision, signed by P2 + P1. Creates `docs/decisions/FNO_GO_NO_GO.md` [proposed].
- [ ] S3.9 Second-reviewer read-through by P1. Creates `docs/reviews/S3_review.md` [proposed].

**Exit gate** (§4 S3, verbatim): *"< 2% relative L2 on held-out data, a measured speedup vs the JAX core, and gradient agreement good enough for optimization to reach comparable cost."*

| Metric | Exact proof | Evidence stored |
|---|---|---|
| < 2% relative L2 on held-out data | `python scripts/train_surrogate.py --eval held_out`; `notebooks/07_s3_gate.ipynb` | notebook outputs; `data/reports/s3_gate.json` [proposed] |
| a measured speedup vs the JAX core | `python scripts/bench_surrogate.py` | `data/reports/s3_gate.json` |
| gradient agreement good enough for optimization to reach comparable cost | `notebooks/07_s3_gate.ipynb` (surrogate-optimized schedule cost vs core-optimized, both EPANET-replayed) | `runs.solver ∈ {jax, surrogate}`, `verification.energy_kwh` |

**Risks & cut trigger** (§12)
- Trigger: **Graph-FNO underperforms at W9 go/no-go** → ship the DeepONet and never call it an FNO (§3). All C4 wording then says "neural operator surrogate (DeepONet)".
- Datagen too slow → cap at 50k runs (lower bound of §4 S3).
- Surrogate gradients disagree → optimizer uses the surrogate only as a warm start, then finishes on the JAX core; speedup reported for the warm-start phase only.

**Demo/defense artifacts**
- Held-out error histogram, speedup bar (single axis), cost-comparison table.
- `docs/decisions/FNO_GO_NO_GO.md` — shows the team applied its own kill criterion.

---

### S4 — Federated layer

**Objective & claims served:** 2 Flower clients on disjoint partitions, FedAvg with DP-SGD, secure aggregation with a stated epsilon, byte-level privacy ledger (§4 S4). Serves **C6**.
**Window:** W8–W10, Oct 29 – Nov 18 (timebox 2 weeks of active work; Flower up in W9).
**Owner / reviewer:** P2 / P3.

**Entry criteria**
- A surrogate model class (DeepONet at minimum) trains centrally (S3.3).
- `federation_rounds` table exists (S0).
- Surrogate dataset partitionable into disjoint scenario sets.

**Task breakdown**
- [ ] S4.1 Disjoint partitions for Client A (Ministry) and Client B (NWC) (§2). Creates `packages/federated/partition.py` [proposed].
- [ ] S4.2 Flower server with FedAvg. Creates `packages/federated/server.py` [proposed]; uncomments `flower` in `docker-compose.yml`.
- [ ] S4.3 Flower client wrapping the surrogate training step; gradients/weights only leave the client. Creates `packages/federated/client.py` [proposed].
- [ ] S4.4 DP-SGD (clip + noise) with a stated ε and δ; justification doc. Creates `packages/federated/dp.py` [proposed], `docs/PRIVACY_BUDGET.md` [proposed].
- [ ] S4.5 Secure aggregation (Flower SecAgg+ [proposed]). Changes `server.py`, `client.py`.
- [ ] S4.6 Byte-level privacy ledger: per round, per client: bytes_sent, param_count, epsilon, and a hash of every payload; asserts no raw record type crosses. Creates `packages/federated/ledger.py` [proposed]; writes `federation_rounds`.
- [ ] S4.7 Central-vs-federated accuracy comparison on the same held-out set. Creates `notebooks/08_s4_gate.ipynb`.
- [ ] S4.8 Second-reviewer read-through by P3. Creates `docs/reviews/S4_review.md` [proposed].

**Exit gate** (§4 S4, verbatim): *"within 5% of centrally trained accuracy, and the ledger shows only gradient tensors crossed the boundary."*

| Metric | Exact proof | Evidence stored |
|---|---|---|
| within 5% of centrally trained accuracy | `notebooks/08_s4_gate.ipynb`: held-out L2 (federated) ≤ 1.05 × held-out L2 (central) | notebook outputs |
| the ledger shows only gradient tensors crossed the boundary | `pytest tests/test_ledger.py` [proposed]: every `federation_rounds` row has `bytes_sent == param_count × dtype_bytes` and payload type = tensor; "raw records transmitted: 0" | `federation_rounds` |

**Risks & cut trigger** (§12)
- Trigger: **not working by 18 Nov** → present the architecture plus a partial demo (§4 S4). Partial demo = 2 clients, FedAvg without DP or SecAgg, ledger still live.
- DP noise destroys accuracy → raise ε, state it; accuracy gap reported honestly.
- Timebox strictly 2 weeks; P2 returns to S3 polish if the box expires.

**Demo/defense artifacts**
- Federation & Privacy screen data: "gradient tensors transmitted: N" beside "raw records transmitted: 0".
- `docs/PRIVACY_BUDGET.md` with ε, δ.
- Ledger CSV export.

---

### S5 — Orchestration & interface

**Objective & claims served:** n8n workflows, FastAPI, web console (§4 S5). Serves **C2** (end to end, live), **C3** (verification block), **C7**, **C8**; surfaces C5 and C6.
**Window:** W9–W12, Nov 5 – Dec 2 (screens stubbed by 18 Nov, K5).
**Owner / reviewer:** P3 (API, n8n, SCADA) + P4 (console) / P4 ↔ P3 cross-review.

**Entry criteria**
- S0 stack green; S2 gate green (real schedules exist to display).
- S3 surrogate available or explicitly cut (fast path toggle).
- S4 ledger rows exist or partial demo declared.

**Task breakdown**
- [ ] S5.1 API schemas: objective + constraints JSON (§2 step 1). Creates `packages/api/schemas.py` [proposed], `tests/test_schemas.py` [proposed].
- [ ] S5.2 `POST /runs`: compile → optimize (core or surrogate) → EPANET replay → persist `runs`, `schedules`, `verification`, `baselines`, `constraint_ledger` (§2 steps 2–5). Creates `packages/api/runs.py` [proposed], `packages/api/db.py` [proposed]; changes `packages/api/main.py`.
- [ ] S5.3 `GET /runs/{id}`, `GET /runs`, `POST /runs/{id}/cancel`, loss-curve streaming (SSE [proposed]). Changes `packages/api/runs.py`.
- [ ] S5.4 n8n workflow "on run complete": operator notification, mocked SCADA write payload, audit log (§2 step 6). Creates `n8n/run_complete.json`, `n8n/README.md`.
- [ ] S5.5 n8n workflow "trigger run" (webhook → API → EPANET → result) for the live C7 trigger. Creates `n8n/trigger_run.json`.
- [ ] S5.6 Mocked OPC-UA / historian adapter (reads tags from a fixture, accepts write payloads, logs them). Creates `packages/api/scada_mock.py`, `tests/test_scada_mock.py` [proposed].
- [ ] S5.7 SCADA integration doc (C8): architecture, tag mapping, write-back safety interlocks, historian read path. Creates `docs/SCADA_INTEGRATION.md`.
- [ ] S5.8 Console scaffold: Next.js 14 + Tailwind + shadcn/ui + Radix, dark tokens, RTL via CSS logical properties, IBM Plex Sans Arabic, Western numerals. Creates `apps/console/` (app, `tailwind.config.ts`, `components/ui/*`); uncomments `console` in `docker-compose.yml`.
- [ ] S5.9 Objective Console (home, build first) with the four required states: empty (pre-filled default), solving (loss curve, iteration count, cancel), infeasible (which constraint, by how much), verification failed (always shown). Creates `apps/console/app/page.tsx`, `apps/console/components/objective/*`.
- [ ] S5.10 Schedule & Comparison screen (single-axis charts only; no dual-axis). Creates `apps/console/app/runs/[id]/page.tsx`, `components/charts/*`.
- [ ] S5.11 Constraint Ledger screen with the EPANET verification block. Creates `apps/console/app/runs/[id]/ledger/page.tsx`.
- [ ] S5.12 Federation & Privacy screen ("gradient tensors transmitted" next to "raw records transmitted: 0"). Creates `apps/console/app/federation/page.tsx`.
- [ ] S5.13 Network Canvas (Net3 topology, pressure colouring). Creates `apps/console/app/network/page.tsx`.
- [ ] S5.14 Run History. Creates `apps/console/app/runs/page.tsx`.
- [ ] S5.15 End-to-end unattended run (W11): n8n webhook → API → schedule → EPANET → DB → n8n dispatch, scripted. Creates `scripts/e2e_run.py` [proposed], `tests/test_e2e.py` [proposed] (integration).
- [ ] S5.16 Outsider test protocol and log (W12). Creates `docs/OUTSIDER_TEST.md` [proposed].

**Exit gate** (§4 S5, verbatim): *"an outsider with no instructions states an objective and receives a verified schedule."*

| Metric | Exact proof | Evidence stored |
|---|---|---|
| Outsider states an objective, receives a verified schedule, no instructions | Protocol in `docs/OUTSIDER_TEST.md`: 3 outsiders, each timed; success = a `runs` row with `verification.epanet_feasible = true` shown on the Constraint Ledger screen | `runs`, `verification`; `docs/OUTSIDER_TEST.md` log |
| All four required states reachable | fixture routes `/dev/states/*` [proposed]; screenshot per state | `docs/screens/*.png` [proposed] |
| n8n triggered live | `curl -X POST localhost:5678/webhook/trigger-run` → run completes → dispatch fires | n8n execution log; audit row |

**Risks & cut trigger** (§12)
- Trigger: **UI incomplete at W12** → ship one screen (Objective Console) done well; other screens become API-only JSON views.
- n8n auth / webhook drift across versions → version pinned in compose since S0; workflow JSON versioned in `n8n/`.
- Cross-review load on P3/P4 → S5.13 and S5.14 are the first to be cut.

**Demo/defense artifacts**
- Live path: Objective Console → schedule → Constraint Ledger with EPANET block.
- `docs/SCADA_INTEGRATION.md` + `scada_mock.py` (C8).
- n8n workflow JSON files (C7).
- Screenshots of all four required states.

---

### S6 — Hardening & defense

**Objective & claims served:** frozen build, recorded demo backup, rehearsed pitch, drilled Q&A (§4 S6). Protects all of C1–C8 at the final.
**Window:** W12–W14, Nov 26 – Dec 13; final 14 Dec.
**Owner / reviewer:** P1 (pitch lead) / P4; P3 owns the frozen build.

**Entry criteria**
- Feature freeze in force since 18 Nov.
- S5 gate green (or one-screen fallback declared).
- Two presentation laptops identified.

**Task breakdown**
- [ ] S6.1 Freeze tag `v1.0-final-candidate`; lock `pyproject.toml` and compose pins; CI green on the tag. Changes `docker-compose.yml` (no tag changes after this), creates git tag.
- [ ] S6.2 Seeded offline demo dataset: fixed scenarios, pre-computed fallback result set. Creates `data/demo/*.json` [proposed], `scripts/seed_demo.py` [proposed].
- [ ] S6.3 Cached fallback wiring: console can render the fallback result set with the network down. Changes `apps/console/lib/fallback.ts` [proposed].
- [ ] S6.4 Recorded demo backup, full path, copied to 2 laptops. Recording stored on the laptops (not in git); path documented in `docs/RUN_OF_SHOW.md` [proposed].
- [ ] S6.5 Run of show + 8-second cut-to-recording drill. Creates `docs/RUN_OF_SHOW.md` [proposed].
- [ ] S6.6 Q&A bank drilled: per claim C1–C8, the hardest question and the honest answer (including every cut that was taken). Creates `docs/QA_BANK.md` [proposed].
- [ ] S6.7 Final deck. Creates `docs/deck/` [proposed].
- [ ] S6.8 Three full run-throughs on the actual presentation hardware, logged. Creates `docs/RUNTHROUGH_LOG.md` [proposed].
- [ ] S6.9 Venue setup checklist (W14). Creates `docs/VENUE_CHECKLIST.md` [proposed].

**Exit gate** (§4 S6, verbatim): *"three full run-throughs on the actual presentation hardware with no intervention."*

| Metric | Exact proof | Evidence stored |
|---|---|---|
| Three full run-throughs, actual hardware, no intervention | `docs/RUNTHROUGH_LOG.md`: date, laptop id, duration, interventions = 0, signed by a non-presenter | `docs/RUNTHROUGH_LOG.md` |
| Recording on 2 laptops, cut within 8 s | Timed drill in `docs/RUN_OF_SHOW.md` | `docs/RUN_OF_SHOW.md` |
| Offline: `make up` with network disabled succeeds from cached images | run-through 3 performed with Wi-Fi off | `docs/RUNTHROUGH_LOG.md` |

**Risks & cut trigger** (§12)
- Trigger: **live demo fails** → cut to the recording within 8 s.
- A run-through has an intervention → it does not count; fix, re-run; three consecutive clean runs required.
- Presentation hardware differs from dev machines → images pulled and cached on both laptops by 9 Dec.

**Demo/defense artifacts**
- Recorded demo (2 copies), cached fallback result set, final deck, Q&A bank, run of show.

---

## 5. Appendix — every [proposed] decision

| # | Decision | Where |
|---|---|---|
| P1 | K1 mitigation: S0 finished 11–12 Sep before camp; W2 residual keeps 23 Sep with a 5-day budget | §2 |
| P2 | K2 mitigation: internal S1 gate on Sun 4 Oct; `make gate-s1` target; datagen scripted to start 5 Oct | §2, S1.9 |
| P3 | K3 mitigation: first feasible schedule due 12 Oct; GA design doc written during Rabigh travel | §2 |
| P4 | K4 mitigation: lab-tested prototype ≡ S2 gate output + S3 DeepONet + S4 partial demo; 18 Nov = sprint deadline | §2 |
| P5 | K5 mitigation: all S5 screens and workflows scoped/stubbed by 18 Nov; W11–12 = completion of scoped screens only | §2 |
| P6 | 4-person role map: P1 physics + pitch, P2 ML, P3 backend/infra, P4 front-end (+ n8n); reviewer table | §3 |
| P7 | `networks` table (id, name, inp_sha256, node_count, link_count, pump_count, tank_count, loaded_at) | S0.4 |
| P8 | Host port defaults db 5433 / api 8000 / n8n 5678 | S0.5 |
| P9 | `notebooks/00_jax_warmup.ipynb` for the W1 JAX/optimistix study | S1 entry |
| P10 | `packages/physics/network.py` + `tests/test_topology.py`, `tests/test_residual.py`, `tests/test_pumps.py` | S1.1, S1.2, S1.6 |
| P11 | Quasi-steady 24 h stepping (sequence of steady-state solves with tank level integration) | S1.7 |
| P12 | `data/reports/*.json` gate reports; `scripts/run_datagen.py` | S1.9, S1.10 |
| P13 | `docs/reviews/S{1..4}_review.md` second-reviewer notes | S1.11, S2.10, S3.9, S4.8 |
| P14 | Smaller-network fallback candidate: Net3 sub-zone or WNTR `Net1`, chosen 8 Oct | S1 risks |
| P15 | `docs/OBJECTIVE_LAMBDAS.md`, `docs/GA_TUNING.md`; `packages/optimize/{compile,repair}.py`; `scripts/benchmark_s2.py`; `tests/test_objective.py`, `tests/test_benchmark.py`; `notebooks/04a_first_schedule.ipynb` | S2 |
| P16 | optax Adam / L-BFGS as the gradient optimizer; multi-start from GA best on hard scenarios | S2.3, S2 risks |
| P17 | `scripts/train_surrogate.py`, `scripts/bench_surrogate.py`, `data/surrogate/README.md`, `docs/decisions/FNO_GO_NO_GO.md` | S3 |
| P18 | `packages/federated/{partition,server,client,dp,ledger}.py`; `docs/PRIVACY_BUDGET.md`; Flower SecAgg+; `tests/test_ledger.py` | S4 |
| P19 | `packages/api/{schemas,runs,db}.py`; SSE for loss-curve streaming; `tests/test_schemas.py`, `tests/test_scada_mock.py` | S5 |
| P20 | `scripts/e2e_run.py`, `tests/test_e2e.py`, `docs/OUTSIDER_TEST.md`, fixture routes `/dev/states/*`, `docs/screens/*.png` | S5 |
| P21 | `data/demo/*.json`, `scripts/seed_demo.py`, `apps/console/lib/fallback.ts`, `docs/{RUN_OF_SHOW,QA_BANK,RUNTHROUGH_LOG,VENUE_CHECKLIST}.md`, `docs/deck/`, recording path | S6 |
