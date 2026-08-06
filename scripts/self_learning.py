#!/usr/bin/env python3
"""Manage VoxEasy's platform-independent self-learning state and backups."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import sys
import tempfile
import uuid
from datetime import datetime, timezone
from pathlib import Path


SCHEMA_VERSION = 1
MAX_TEXT_LENGTH = 1000
REQUIRED_STATE_FIELDS = {
    "schema_version",
    "usage_count",
    "successful_uses_since_review",
    "last_reviewed_at",
    "observed_failures",
    "user_corrections",
    "candidate_improvements",
    "applied_patches",
    "rejected_learning_items",
    "review_due",
    "review_reasons",
}
SENSITIVE_PATTERNS = (
    re.compile(r"(?i)\b(?:password|passwd|secret|access[_ -]?token|api[_ -]?key)\s*[:=]\s*\S+"),
    re.compile(r"\bsk-[A-Za-z0-9_-]{12,}\b"),
    re.compile(r"(?i)(?:^|[\s\"'])(?:/tmp/|/var/folders/|/Users/|/home/|[A-Za-z]:\\)"),
)


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def timestamp_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def default_state_path() -> Path:
    configured = os.environ.get("VOXEASY_LEARNING_STATE")
    return Path(configured).expanduser() if configured else Path.home() / ".voxeasy" / "learning-state.json"


def empty_state() -> dict:
    return {
        "schema_version": SCHEMA_VERSION,
        "usage_count": 0,
        "successful_uses_since_review": 0,
        "last_reviewed_at": None,
        "observed_failures": [],
        "user_corrections": [],
        "candidate_improvements": [],
        "applied_patches": [],
        "rejected_learning_items": [],
        "review_due": False,
        "review_reasons": [],
    }


def ensure_safe_text(value: str, field: str) -> str:
    value = value.strip()
    if not value:
        raise ValueError(f"{field} must not be empty")
    if len(value) > MAX_TEXT_LENGTH:
        raise ValueError(f"{field} exceeds {MAX_TEXT_LENGTH} characters")
    for pattern in SENSITIVE_PATTERNS:
        if pattern.search(value):
            raise ValueError(f"{field} appears to contain a secret, private value, or machine-specific path")
    return value


def ensure_relative_file(value: str) -> str:
    relative = Path(value)
    if relative.is_absolute() or ".." in relative.parts or not relative.parts:
        raise ValueError(f"modified file must be a safe relative path: {value}")
    return relative.as_posix()


def validate_state(state: object) -> list[str]:
    errors: list[str] = []
    if not isinstance(state, dict):
        return ["state must be a JSON object"]
    missing = sorted(REQUIRED_STATE_FIELDS - state.keys())
    if missing:
        errors.append(f"missing fields: {', '.join(missing)}")
    if state.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"schema_version must be {SCHEMA_VERSION}")
    for field in ("usage_count", "successful_uses_since_review"):
        value = state.get(field)
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            errors.append(f"{field} must be a non-negative integer")
    if state.get("last_reviewed_at") is not None and not isinstance(state.get("last_reviewed_at"), str):
        errors.append("last_reviewed_at must be null or a string")
    for field in (
        "observed_failures",
        "user_corrections",
        "candidate_improvements",
        "applied_patches",
        "rejected_learning_items",
        "review_reasons",
    ):
        if not isinstance(state.get(field), list):
            errors.append(f"{field} must be a list")
    if not isinstance(state.get("review_due"), bool):
        errors.append("review_due must be boolean")
    return errors


def atomic_write(path: Path, data: dict) -> None:
    path = path.expanduser()
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as handle:
        json.dump(data, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
        temporary = Path(handle.name)
    temporary.replace(path)


def load_state(path: Path, create: bool = True) -> dict:
    path = path.expanduser()
    if not path.exists():
        if not create:
            raise FileNotFoundError(path)
        state = empty_state()
        atomic_write(path, state)
        return state
    state = json.loads(path.read_text(encoding="utf-8"))
    errors = validate_state(state)
    if errors:
        raise ValueError("; ".join(errors))
    return state


def add_review_reason(state: dict, reason: str) -> None:
    if reason not in state["review_reasons"]:
        state["review_reasons"].append(reason)
    state["review_due"] = True


def record_success(state: dict) -> dict:
    state["usage_count"] += 1
    state["successful_uses_since_review"] += 1
    if state["successful_uses_since_review"] >= 5:
        add_review_reason(state, "five_successful_uses")
    return state


def record_failure(state: dict, summary: str, evidence: str) -> dict:
    state["usage_count"] += 1
    item = {
        "id": f"failure-{uuid.uuid4().hex[:10]}",
        "observed_at": utc_now(),
        "summary": ensure_safe_text(summary, "summary"),
        "evidence": ensure_safe_text(evidence, "evidence"),
        "review_status": "pending",
    }
    state["observed_failures"].append(item)
    add_review_reason(state, "failure")
    return item


def make_candidate(
    state: dict,
    source_type: str,
    summary: str,
    trigger: str,
    action: str,
    boundary: str,
    evidence: str,
    validation_plan: str,
    reusable: bool,
    source_ids: list[str] | None = None,
) -> dict:
    item = {
        "id": f"candidate-{uuid.uuid4().hex[:10]}",
        "created_at": utc_now(),
        "source_type": ensure_safe_text(source_type, "source_type"),
        "source_ids": source_ids or [],
        "summary": ensure_safe_text(summary, "summary"),
        "trigger": ensure_safe_text(trigger, "trigger"),
        "action": ensure_safe_text(action, "action"),
        "boundary": ensure_safe_text(boundary, "boundary"),
        "evidence": ensure_safe_text(evidence, "evidence"),
        "validation_plan": ensure_safe_text(validation_plan, "validation_plan"),
        "reusable": bool(reusable),
        "scope": "voxeasy",
        "status": "pending_gate_review",
    }
    state["candidate_improvements"].append(item)
    return item


def record_correction(
    state: dict,
    summary: str,
    trigger: str,
    action: str,
    boundary: str,
    evidence: str,
    validation_plan: str,
    reusable: bool,
) -> tuple[dict, dict]:
    correction = {
        "id": f"correction-{uuid.uuid4().hex[:10]}",
        "observed_at": utc_now(),
        "summary": ensure_safe_text(summary, "summary"),
        "evidence": ensure_safe_text(evidence, "evidence"),
        "review_status": "pending",
    }
    state["user_corrections"].append(correction)
    candidate = make_candidate(
        state,
        "user_correction",
        summary,
        trigger,
        action,
        boundary,
        evidence,
        validation_plan,
        reusable,
        [correction["id"]],
    )
    add_review_reason(state, "user_correction")
    return correction, candidate


def review_report(state: dict) -> dict:
    return {
        "review_due": state["review_due"],
        "review_reasons": state["review_reasons"],
        "successful_uses_since_review": state["successful_uses_since_review"],
        "pending_failures": sum(item.get("review_status") == "pending" for item in state["observed_failures"]),
        "pending_corrections": sum(item.get("review_status") == "pending" for item in state["user_corrections"]),
        "pending_candidates": [
            item for item in state["candidate_improvements"] if item.get("status") == "pending_gate_review"
        ],
    }


def complete_review(state: dict) -> None:
    now = utc_now()
    for collection in (state["observed_failures"], state["user_corrections"]):
        for item in collection:
            if item.get("review_status") == "pending":
                item["review_status"] = "reviewed"
                item["reviewed_at"] = now
    state["last_reviewed_at"] = now
    state["successful_uses_since_review"] = 0
    state["review_due"] = False
    state["review_reasons"] = []


def find_candidate(state: dict, candidate_id: str) -> dict:
    for item in state["candidate_improvements"]:
        if item.get("id") == candidate_id:
            return item
    raise ValueError(f"candidate not found: {candidate_id}")


def record_applied(
    state: dict,
    candidate_id: str,
    patch_summary: str,
    files: list[str],
    validation_result: str,
    backup_manifest: Path,
) -> dict:
    candidate = find_candidate(state, candidate_id)
    if candidate.get("status") != "pending_gate_review":
        raise ValueError(f"candidate {candidate_id} is not pending")
    if not candidate.get("reusable"):
        raise ValueError(f"candidate {candidate_id} did not pass the reusable gate")
    for field in ("trigger", "action", "boundary", "evidence", "validation_plan"):
        if not candidate.get(field):
            raise ValueError(f"candidate {candidate_id} is missing {field}")
    backup_manifest = backup_manifest.expanduser().resolve()
    if not backup_manifest.is_file():
        raise ValueError(f"backup manifest does not exist: {backup_manifest}")
    if not files:
        raise ValueError("at least one modified file is required")
    safe_files = [ensure_relative_file(value) for value in files]
    applied = {
        "id": f"patch-{uuid.uuid4().hex[:10]}",
        "candidate_id": candidate_id,
        "applied_at": utc_now(),
        "patch_summary": ensure_safe_text(patch_summary, "patch_summary"),
        "files": safe_files,
        "validation_result": ensure_safe_text(validation_result, "validation_result"),
        "backup_manifest": str(backup_manifest),
    }
    candidate["status"] = "applied"
    candidate["resolved_at"] = applied["applied_at"]
    state["applied_patches"].append(applied)
    return applied


def reject_candidate(state: dict, candidate_id: str, reason: str) -> dict:
    candidate = find_candidate(state, candidate_id)
    if candidate.get("status") != "pending_gate_review":
        raise ValueError(f"candidate {candidate_id} is not pending")
    rejected = {
        "candidate_id": candidate_id,
        "rejected_at": utc_now(),
        "reason": ensure_safe_text(reason, "reason"),
    }
    candidate["status"] = "rejected"
    candidate["resolved_at"] = rejected["rejected_at"]
    state["rejected_learning_items"].append(rejected)
    return rejected


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def backup_files(
    skill_root: Path,
    relative_files: list[str],
    reason: str,
    backup_root: Path | None = None,
    timestamp: str | None = None,
) -> Path:
    skill_root = skill_root.expanduser().resolve()
    if not skill_root.is_dir():
        raise ValueError(f"skill root is not a directory: {skill_root}")
    if not relative_files:
        raise ValueError("at least one --file is required")
    reason = ensure_safe_text(reason, "reason")
    timestamp = timestamp or timestamp_now()
    backup_root = (backup_root or (Path.home() / ".voxeasy" / "backups")).expanduser().resolve()
    sources: list[tuple[Path, Path]] = []
    for relative_text in relative_files:
        relative = Path(relative_text)
        if relative.is_absolute() or ".." in relative.parts:
            raise ValueError(f"backup file must be a safe relative path: {relative_text}")
        source = (skill_root / relative).resolve()
        try:
            source.relative_to(skill_root)
        except ValueError as exc:
            raise ValueError(f"backup file escapes skill root: {relative_text}") from exc
        if not source.is_file():
            raise ValueError(f"backup source is not a file: {source}")
        sources.append((relative, source))

    backup_dir = backup_root / skill_root.name / timestamp
    if backup_dir.exists():
        raise FileExistsError(f"backup directory already exists: {backup_dir}")
    backup_dir.mkdir(parents=True)

    entries = []
    for relative, source in sources:
        backup_name = f"{str(relative).replace(os.sep, '__')}.{timestamp}.bak"
        destination = backup_dir / backup_name
        if destination.exists():
            raise FileExistsError(f"refusing to overwrite backup: {destination}")
        shutil.copy2(source, destination)
        entries.append(
            {
                "original": str(source),
                "backup": str(destination),
                "reason": reason,
                "timestamp": timestamp,
                "original_sha256": sha256(source),
                "backup_sha256": sha256(destination),
            }
        )

    manifest = backup_dir / "backup-manifest.json"
    manifest.write_text(
        json.dumps(
            {
                "skill_root": str(skill_root),
                "created_at": timestamp,
                "backup_policy": "no-overwrite",
                "entries": entries,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return manifest


def print_json(value: object) -> None:
    print(json.dumps(value, ensure_ascii=False, indent=2))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state", type=Path, default=default_state_path(), help="Learning state JSON path")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("init")
    subparsers.add_parser("status")
    subparsers.add_parser("validate")
    subparsers.add_parser("record-success")

    failure = subparsers.add_parser("record-failure")
    failure.add_argument("--summary", required=True)
    failure.add_argument("--evidence", required=True)

    correction = subparsers.add_parser("record-correction")
    for name in ("summary", "trigger", "action", "boundary", "evidence", "validation-plan"):
        correction.add_argument(f"--{name}", required=True)
    correction.add_argument("--reusable", action="store_true")

    candidate = subparsers.add_parser("propose-candidate")
    candidate.add_argument("--source-type", choices=("failure_review", "success_batch_review"), required=True)
    for name in ("summary", "trigger", "action", "boundary", "evidence", "validation-plan"):
        candidate.add_argument(f"--{name}", required=True)
    candidate.add_argument("--source-id", action="append", default=[])
    candidate.add_argument("--reusable", action="store_true")

    review = subparsers.add_parser("review")
    review.add_argument("--complete", action="store_true")

    applied = subparsers.add_parser("record-applied")
    applied.add_argument("--candidate-id", required=True)
    applied.add_argument("--patch-summary", required=True)
    applied.add_argument("--file", action="append", default=[])
    applied.add_argument("--validation-result", required=True)
    applied.add_argument("--backup-manifest", type=Path, required=True)

    rejected = subparsers.add_parser("reject")
    rejected.add_argument("--candidate-id", required=True)
    rejected.add_argument("--reason", required=True)

    backup = subparsers.add_parser("backup")
    backup.add_argument("--skill-root", type=Path, required=True)
    backup.add_argument("--file", action="append", default=[])
    backup.add_argument("--reason", required=True)
    backup.add_argument("--backup-root", type=Path)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        if args.command == "backup":
            manifest = backup_files(args.skill_root, args.file, args.reason, args.backup_root)
            print_json({"ok": True, "backup_manifest": str(manifest)})
            return 0

        if args.command == "validate":
            state = load_state(args.state, create=False)
            errors = validate_state(state)
            print_json({"ok": not errors, "state": str(args.state.expanduser()), "errors": errors})
            return 0 if not errors else 1

        state = load_state(args.state, create=True)
        result: object = state
        changed = False

        if args.command == "init":
            result = {"ok": True, "state": str(args.state.expanduser())}
        elif args.command == "status":
            result = {"state": str(args.state.expanduser()), **review_report(state)}
        elif args.command == "record-success":
            record_success(state)
            changed = True
            result = review_report(state)
        elif args.command == "record-failure":
            item = record_failure(state, args.summary, args.evidence)
            changed = True
            result = {"recorded": item, **review_report(state)}
        elif args.command == "record-correction":
            correction, candidate = record_correction(
                state,
                args.summary,
                args.trigger,
                args.action,
                args.boundary,
                args.evidence,
                args.validation_plan,
                args.reusable,
            )
            changed = True
            result = {"correction": correction, "candidate": candidate, **review_report(state)}
        elif args.command == "propose-candidate":
            candidate = make_candidate(
                state,
                args.source_type,
                args.summary,
                args.trigger,
                args.action,
                args.boundary,
                args.evidence,
                args.validation_plan,
                args.reusable,
                args.source_id,
            )
            add_review_reason(state, args.source_type)
            changed = True
            result = {"candidate": candidate, **review_report(state)}
        elif args.command == "review":
            result = review_report(state)
            if args.complete:
                complete_review(state)
                changed = True
                result = {"completed": True, **review_report(state), "last_reviewed_at": state["last_reviewed_at"]}
        elif args.command == "record-applied":
            item = record_applied(
                state,
                args.candidate_id,
                args.patch_summary,
                args.file,
                args.validation_result,
                args.backup_manifest,
            )
            changed = True
            result = {"applied": item}
        elif args.command == "reject":
            item = reject_candidate(state, args.candidate_id, args.reason)
            changed = True
            result = {"rejected": item}

        errors = validate_state(state)
        if errors:
            raise ValueError("; ".join(errors))
        if changed:
            atomic_write(args.state, state)
        print_json(result)
        return 0
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print_json({"ok": False, "error": str(exc)})
        return 2


if __name__ == "__main__":
    sys.exit(main())
