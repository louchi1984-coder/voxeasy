#!/usr/bin/env python3
"""Validate a VoxEasy SRT shot plan without making semantic decisions."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


TIME_RE = re.compile(r"^(?:(\d+):)?(\d{1,2}):(\d{2})(?:[,.](\d{1,3}))?$")
EPSILON = 0.002


def parse_time(value: object) -> float:
    if isinstance(value, (int, float)):
        return float(value)
    if not isinstance(value, str):
        raise ValueError(f"unsupported time value: {value!r}")
    match = TIME_RE.match(value.strip())
    if not match:
        raise ValueError(f"invalid time format: {value!r}")
    hours = int(match.group(1) or 0)
    minutes = int(match.group(2))
    seconds = int(match.group(3))
    millis = int((match.group(4) or "0").ljust(3, "0"))
    if minutes >= 60 or seconds >= 60:
        raise ValueError(f"invalid time value: {value!r}")
    return hours * 3600 + minutes * 60 + seconds + millis / 1000


def snap_duration(actual: float) -> int | None:
    for duration in (4, 6, 8, 10):
        if actual <= duration + EPSILON:
            return duration
    return None


def close(left: float, right: float) -> bool:
    return abs(left - right) <= EPSILON


def validate(data: dict) -> dict:
    errors: list[str] = []
    warnings: list[str] = []
    cues = data.get("cues", [])
    shots = data.get("shots", [])

    if not cues:
        errors.append("cues must contain at least one subtitle cue")
    if not shots:
        errors.append("shots must contain at least one shot")

    parsed_cues: list[tuple[float, float]] = []
    for index, cue in enumerate(cues):
        try:
            start = parse_time(cue["start"])
            end = parse_time(cue["end"])
        except (KeyError, ValueError) as exc:
            errors.append(f"cue {index}: {exc}")
            continue
        if end <= start:
            errors.append(f"cue {index}: end must be later than start")
        if parsed_cues and start < parsed_cues[-1][1] - EPSILON:
            errors.append(f"cue {index}: overlaps the previous cue")
        parsed_cues.append((start, end))

    assigned: dict[int, str] = {}
    previous_end: float | None = None
    computed_shots: list[dict] = []

    for index, shot in enumerate(shots):
        shot_id = str(shot.get("shot_id", index + 1))
        try:
            start = parse_time(shot["start"])
            end = parse_time(shot["end"])
        except (KeyError, ValueError) as exc:
            errors.append(f"shot {shot_id}: {exc}")
            continue

        actual = end - start
        if actual <= 0:
            errors.append(f"shot {shot_id}: end must be later than start")
        if index == 0 and not close(start, 0.0):
            errors.append(f"shot {shot_id}: first shot must start at 00:00.000 to preserve opening blank")
        if previous_end is not None and not close(start, previous_end):
            errors.append(f"shot {shot_id}: starts at {start:.3f}s but previous shot ends at {previous_end:.3f}s")
        previous_end = end

        expected = snap_duration(actual)
        declared_duration = shot.get("duration_seconds")
        if expected is None:
            errors.append(f"shot {shot_id}: actual duration {actual:.3f}s exceeds 10 seconds")
        elif declared_duration != expected:
            errors.append(f"shot {shot_id}: duration_seconds must be {expected}, got {declared_duration!r}")

        declared_actual = shot.get("actual_duration_seconds")
        if declared_actual is not None and not close(float(declared_actual), actual):
            errors.append(f"shot {shot_id}: actual_duration_seconds must be {actual:.3f}")

        cue_indices = shot.get("cue_indices")
        if not isinstance(cue_indices, list) or not cue_indices:
            errors.append(f"shot {shot_id}: cue_indices must be a non-empty list")
            cue_indices = []

        spoken = 0.0
        for cue_index in cue_indices:
            if not isinstance(cue_index, int) or cue_index < 0 or cue_index >= len(parsed_cues):
                errors.append(f"shot {shot_id}: invalid cue index {cue_index!r}")
                continue
            if cue_index in assigned:
                errors.append(f"cue {cue_index}: assigned to both {assigned[cue_index]} and {shot_id}")
            assigned[cue_index] = shot_id
            cue_start, cue_end = parsed_cues[cue_index]
            if cue_start < start - EPSILON or cue_end > end + EPSILON:
                errors.append(f"shot {shot_id}: cue {cue_index} lies outside the shot interval")
            spoken += cue_end - cue_start

        blank = max(0.0, actual - spoken)
        declared_blank = shot.get("included_blank_seconds")
        if declared_blank is not None and not close(float(declared_blank), blank):
            errors.append(f"shot {shot_id}: included_blank_seconds must be {blank:.3f}")

        computed_shots.append(
            {
                "shot_id": shot_id,
                "actual_duration_seconds": round(actual, 3),
                "duration_seconds": expected,
                "included_blank_seconds": round(blank, 3),
            }
        )

    for cue_index in range(len(parsed_cues)):
        if cue_index not in assigned:
            errors.append(f"cue {cue_index}: not assigned to any shot")

    if previous_end is not None and data.get("media_end") is not None:
        try:
            media_end = parse_time(data["media_end"])
            if not close(previous_end, media_end):
                errors.append(f"last shot ends at {previous_end:.3f}s but media_end is {media_end:.3f}s")
        except ValueError as exc:
            errors.append(f"media_end: {exc}")
    elif previous_end is not None:
        warnings.append("media_end missing; trailing blank cannot be verified")

    return {"ok": not errors, "errors": errors, "warnings": warnings, "computed_shots": computed_shots}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan", type=Path, help="JSON file containing cues, shots, and optional media_end")
    args = parser.parse_args()
    try:
        data = json.loads(args.plan.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"ok": False, "errors": [str(exc)]}, ensure_ascii=False, indent=2))
        return 2
    result = validate(data)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
