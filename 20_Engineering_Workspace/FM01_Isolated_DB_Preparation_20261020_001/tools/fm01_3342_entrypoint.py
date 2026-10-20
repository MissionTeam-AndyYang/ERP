"""Concrete fail-closed FM-01 entrypoint.

The CLI only validates and prints a plan. Side-effecting execution requires an
explicitly supplied verifier and target-bound adapters from a separate approved
runtime context; this module never discovers credentials or creates adapters.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from fm01_3342_runner import HoldError, plan


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="FM-01 3342 fail-closed entrypoint")
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--source-dir", required=True)
    parser.add_argument("--datadir", required=True)
    parser.add_argument("--operation", choices=("plan", "status", "start", "safe_stop", "migrate", "backup", "restore", "reset", "fixture"), default="plan")
    return parser


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    try:
        # No trust anchor, credential provider, process adapter or DB adapter is
        # configured in this package. This is deliberate fail-closed behavior.
        result = plan(Path(args.manifest), Path(args.source_dir), args.datadir, lambda _: False)
        print(json.dumps({"status": "HOLD", "reason": "no approved verifier/executor configured", "requested_operation": args.operation, "plan": result}, sort_keys=True))
    except (OSError, json.JSONDecodeError, HoldError) as exc:
        print(str(exc))
    return 10


if __name__ == "__main__":
    raise SystemExit(main())
