"""Stage 0 `make verify`: run inside the twin container against the live stack.

Checks: pytest (unit + integration), ruff check + format, api /health, n8n /healthz.
Prints one PASS/FAIL line per check and a summary; exits non-zero if any check fails.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import urllib.request

API_URL = os.environ.get("API_URL", "http://localhost:8000")
N8N_URL = os.environ.get("N8N_URL", "http://localhost:5678")


def run(cmd: list[str]) -> tuple[bool, str]:
    proc = subprocess.run(cmd, capture_output=True, text=True)
    out = (proc.stdout + proc.stderr).strip().splitlines()
    return proc.returncode == 0, "\n".join(out[-15:])


def check_pytest() -> tuple[bool, str]:
    return run([sys.executable, "-m", "pytest", "-q", "tests"])


def check_ruff() -> tuple[bool, str]:
    ok1, out1 = run(["ruff", "check", "."])
    ok2, out2 = run(["ruff", "format", "--check", "."])
    return ok1 and ok2, out1 + "\n" + out2


def check_api_health() -> tuple[bool, str]:
    try:
        with urllib.request.urlopen(f"{API_URL}/health", timeout=5) as r:
            body = json.load(r)
    except Exception as exc:  # noqa: BLE001 - report any failure mode
        return False, f"{exc!r}"
    net = body.get("network") or {}
    ok = (
        body.get("db") == "ok"
        and net.get("node_count", 0) > 0
        and net.get("link_count", 0) > 0
        and bool(body.get("versions", {}).get("jax"))
        and bool(body.get("versions", {}).get("wntr"))
    )
    return ok, json.dumps(body)


def check_n8n_health() -> tuple[bool, str]:
    try:
        with urllib.request.urlopen(f"{N8N_URL}/healthz", timeout=5) as r:
            return r.status == 200, r.read().decode().strip()
    except Exception as exc:  # noqa: BLE001
        return False, f"{exc!r}"


CHECKS = [
    ("pytest", check_pytest),
    ("ruff", check_ruff),
    ("api /health", check_api_health),
    ("n8n /healthz", check_n8n_health),
]


def main() -> int:
    failed = 0
    for name, fn in CHECKS:
        ok, detail = fn()
        failed += not ok
        last = detail.strip().splitlines()[-1] if detail.strip() else ""
        print(f"{'PASS' if ok else 'FAIL'} {name}: {last}")
        if not ok and detail:
            print(detail)
    verdict = "PASS" if failed == 0 else "FAIL"
    print(f"{verdict} verify: {len(CHECKS) - failed}/{len(CHECKS)} checks green")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
