-- MIZAN Stage 0 schema (§6 tables + [proposed] networks). No hypertables in Stage 0.
CREATE EXTENSION IF NOT EXISTS timescaledb;

-- [proposed] benchmark network registry, seeded by scripts/seed_network.py
CREATE TABLE IF NOT EXISTS networks (
    id          BIGSERIAL PRIMARY KEY,
    name        TEXT        NOT NULL UNIQUE,
    inp_sha256  CHAR(64)    NOT NULL,
    node_count  INTEGER     NOT NULL CHECK (node_count >= 0),
    link_count  INTEGER     NOT NULL CHECK (link_count >= 0),
    pump_count  INTEGER     NOT NULL CHECK (pump_count >= 0),
    tank_count  INTEGER     NOT NULL CHECK (tank_count >= 0),
    loaded_at   TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- §6 runs(id, created_at, objective_json, network_id, status, solver, wall_ms)
CREATE TABLE IF NOT EXISTS runs (
    id              BIGSERIAL PRIMARY KEY,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    objective_json  JSONB       NOT NULL,
    network_id      BIGINT      NOT NULL REFERENCES networks(id),
    status          TEXT        NOT NULL DEFAULT 'queued'
                    CHECK (status IN ('queued','solving','verified','infeasible','verification_failed','cancelled','error')),
    solver          TEXT        NOT NULL DEFAULT 'jax'
                    CHECK (solver IN ('jax','surrogate','ga')),
    wall_ms         INTEGER     CHECK (wall_ms IS NULL OR wall_ms >= 0)
);

-- §6 schedules(id, run_id, asset_id, hour, setpoint, mode)
CREATE TABLE IF NOT EXISTS schedules (
    id        BIGSERIAL PRIMARY KEY,
    run_id    BIGINT           NOT NULL REFERENCES runs(id) ON DELETE CASCADE,
    asset_id  TEXT             NOT NULL,
    hour      SMALLINT         NOT NULL CHECK (hour BETWEEN 0 AND 23),
    setpoint  DOUBLE PRECISION NOT NULL,
    mode      TEXT             NOT NULL CHECK (mode IN ('speed','on_off','valve')),
    UNIQUE (run_id, asset_id, hour)
);

-- §6 verification(id, run_id, epanet_feasible, min_pressure, max_violation, energy_kwh)
CREATE TABLE IF NOT EXISTS verification (
    id               BIGSERIAL PRIMARY KEY,
    run_id           BIGINT           NOT NULL REFERENCES runs(id) ON DELETE CASCADE,
    verified_at      TIMESTAMPTZ      NOT NULL DEFAULT now(),
    epanet_feasible  BOOLEAN          NOT NULL,
    min_pressure     DOUBLE PRECISION,
    max_violation    DOUBLE PRECISION,
    energy_kwh       DOUBLE PRECISION
);

-- §6 baselines(id, run_id, method, energy_kwh, wall_ms)
CREATE TABLE IF NOT EXISTS baselines (
    id          BIGSERIAL PRIMARY KEY,
    run_id      BIGINT           NOT NULL REFERENCES runs(id) ON DELETE CASCADE,
    created_at  TIMESTAMPTZ      NOT NULL DEFAULT now(),
    method      TEXT             NOT NULL CHECK (method IN ('gradient','ga','surrogate','heuristic')),
    energy_kwh  DOUBLE PRECISION NOT NULL,
    wall_ms     INTEGER          NOT NULL CHECK (wall_ms >= 0)
);

-- §6 constraint_ledger(id, run_id, constraint, target, achieved, satisfied)
CREATE TABLE IF NOT EXISTS constraint_ledger (
    id          BIGSERIAL PRIMARY KEY,
    run_id      BIGINT           NOT NULL REFERENCES runs(id) ON DELETE CASCADE,
    created_at  TIMESTAMPTZ      NOT NULL DEFAULT now(),
    "constraint" TEXT            NOT NULL,
    target      DOUBLE PRECISION NOT NULL,
    achieved    DOUBLE PRECISION NOT NULL,
    satisfied   BOOLEAN          NOT NULL
);

-- §6 federation_rounds(id, round, client_id, bytes_sent, param_count, epsilon)
CREATE TABLE IF NOT EXISTS federation_rounds (
    id           BIGSERIAL PRIMARY KEY,
    recorded_at  TIMESTAMPTZ      NOT NULL DEFAULT now(),
    round        INTEGER          NOT NULL CHECK (round >= 0),
    client_id    TEXT             NOT NULL,
    bytes_sent   BIGINT           NOT NULL CHECK (bytes_sent >= 0),
    param_count  BIGINT           NOT NULL CHECK (param_count >= 0),
    epsilon      DOUBLE PRECISION,
    UNIQUE (round, client_id)
);

CREATE INDEX IF NOT EXISTS runs_network_id_idx        ON runs (network_id);
CREATE INDEX IF NOT EXISTS runs_created_at_idx        ON runs (created_at DESC);
CREATE INDEX IF NOT EXISTS schedules_run_id_idx       ON schedules (run_id);
CREATE INDEX IF NOT EXISTS verification_run_id_idx    ON verification (run_id);
CREATE INDEX IF NOT EXISTS baselines_run_id_idx       ON baselines (run_id);
CREATE INDEX IF NOT EXISTS constraint_ledger_run_idx  ON constraint_ledger (run_id);
