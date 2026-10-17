"""Deterministic, read-only CF-01 validation for the existing FM-02 records.

The validator intentionally uses only the Python standard library. It reads the
existing docs/fm02 records and never writes to the repository, database, or
external service.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


CANONICAL_INDEX_REFERENCE = (
    "Canonical_ERP2.0_Monorepo/01_Foundation/repository_knowledge/"
    "Repository-Knowledge-Index-20261010-001.md"
)


def read_text(repo_root: Path, relative_path: str) -> str:
    path = repo_root / relative_path
    if not path.is_file():
        raise AssertionError(f"missing source record: {relative_path}")
    return path.read_text(encoding="utf-8")


def assert_contains(text: str, needle: str, label: str) -> None:
    if needle not in text:
        raise AssertionError(f"{label}: missing {needle!r}")


def assert_row_contains(text: str, row_label: str, needles: tuple[str, ...]) -> None:
    row_prefix = f"| {row_label}"
    row = next(
        (
            line
            for line in text.splitlines()
            if line.lstrip().startswith(row_prefix)
            and (len(line) == len(row_prefix) or line[len(row_prefix)] in " |-")
        ),
        None,
    )
    if row is None:
        raise AssertionError(f"missing matrix row: {row_label}")
    for needle in needles:
        if needle.lower() not in row.lower():
            raise AssertionError(f"{row_label}: missing row text {needle!r}")


def validate(repo_root: Path) -> list[str]:
    matrix_path = "docs/fm02/FM02_SPRINT01_TRACEABILITY_MATRIX_20261016.md"
    completion_path = "docs/fm02/FM02_SPRINT01_DOCUMENT_COMPLETION_MATRIX_20261016_104.md"
    relay_path = "docs/fm02/FM02_SPRINT01_REPOSITORY_KNOWLEDGE_REGISTRATION_RELAY_20261016_105A.md"

    matrix = read_text(repo_root, matrix_path)
    completion = read_text(repo_root, completion_path)
    relay = read_text(repo_root, relay_path)

    for decision_id in ("B01", "B02", "B03", "B04", "B05", "B06"):
        assert_row_contains(matrix, decision_id, (decision_id,))
    for requirement_id in (f"FR-{number:02d}" for number in range(1, 21)):
        assert_row_contains(matrix, requirement_id, (requirement_id,))

    assert_row_contains(
        matrix,
        "B02",
        (
            "Item is separate from Product/SKU",
            "cardinality",
            "source of truth",
            "CONTROLLED_DEFERRED",
            "no unapproved schema",
        ),
    )
    assert_row_contains(
        matrix,
        "FR-13",
        (
            "Product/SKU relationship",
            "no relationship/schema",
            "controlled-deferred",
        ),
    )

    for document_id in ("D01", "D02", "D03", "D05", "D06", "D09"):
        assert_contains(completion, document_id, "B02 completion coverage")

    assert_contains(relay, CANONICAL_INDEX_REFERENCE, "canonical Repository Knowledge Index reuse")
    assert_contains(relay, "not a competing knowledge index", "non-duplication custody rule")
    assert_contains(
        relay,
        "REPOSITORY_KNOWLEDGE_READBACK=HOLD",
        "Repository Office readback limitation",
    )
    assert_contains(relay, "placeholders until", "Repository Office readback limitation")

    mechanism_dir = Path(__file__).resolve().parent
    local_index_names = list(mechanism_dir.rglob("*Repository-Knowledge-Index*"))
    if local_index_names:
        raise AssertionError(
            "competing local Repository Knowledge Index detected: "
            + ", ".join(str(path.relative_to(mechanism_dir)) for path in local_index_names)
        )

    return [
        "CF01_VALIDATION=PASS",
        "B02_BOUNDARY=PASS",
        "B01_B06_COVERAGE=6/6",
        "FR_COVERAGE=20/20",
        "REPOSITORY_KNOWLEDGE_REUSE=PASS",
        "READ_ONLY_SCOPE=PASS",
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path(__file__).resolve().parents[3],
        help="FM-02 repository root; defaults to the repository containing this mechanism",
    )
    args = parser.parse_args()
    try:
        for line in validate(args.repo_root.resolve()):
            print(line)
    except (AssertionError, OSError, UnicodeError) as exc:
        print(f"CF01_VALIDATION=FAIL: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
