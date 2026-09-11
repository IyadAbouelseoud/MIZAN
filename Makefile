# MIZAN Stage 0. `make up` is THE one command.
SHELL := /bin/sh
COMPOSE ?= docker compose
API_PORT ?= 8000
N8N_PORT ?= 5678
PY_IN_TWIN = $(COMPOSE) exec -T twin python

.PHONY: up verify test lint logs down clean wait seed

## Build, start, wait until healthy, seed the benchmark network. Non-zero exit on any failure.
up:
	$(COMPOSE) build --quiet
	$(COMPOSE) up -d --wait --wait-timeout 180
	$(MAKE) --no-print-directory seed
	@echo "OK MIZAN stack up: api http://localhost:$(API_PORT)/health  n8n http://localhost:$(N8N_PORT)"

seed:
	$(PY_IN_TWIN) scripts/seed_network.py

## Full verification against the live stack, run inside the twin container:
## pytest (incl. integration), ruff, api /health, n8n /healthz, then a PASS/FAIL summary.
verify:
	$(COMPOSE) exec -T twin python scripts/verify_stack.py

## Unit tests only (no running stack needed), executed on the host Python env.
test:
	python -m pytest -q -m "not integration" tests

lint:
	ruff check . && ruff format --check .

logs:
	$(COMPOSE) logs -f --tail=100

down:
	$(COMPOSE) down --remove-orphans

## Remove this project's containers, networks AND named volumes (db_data, n8n_data).
clean:
	$(COMPOSE) down -v --remove-orphans
