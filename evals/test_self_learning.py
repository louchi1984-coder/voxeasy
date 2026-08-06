#!/usr/bin/env python3
"""Regression tests for VoxEasy's platform-independent self-learning loop."""

from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "self_learning.py"
SPEC = importlib.util.spec_from_file_location("voxeasy_self_learning", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class SelfLearningTests(unittest.TestCase):
    def test_empty_state_schema_is_valid(self) -> None:
        state = MODULE.empty_state()
        self.assertEqual([], MODULE.validate_state(state))

    def test_five_successes_schedule_batch_review(self) -> None:
        state = MODULE.empty_state()
        for _ in range(5):
            MODULE.record_success(state)
        self.assertEqual(5, state["usage_count"])
        self.assertEqual(5, state["successful_uses_since_review"])
        self.assertTrue(state["review_due"])
        self.assertIn("five_successful_uses", state["review_reasons"])

    def test_failure_requires_immediate_review_without_auto_candidate(self) -> None:
        state = MODULE.empty_state()
        MODULE.record_failure(state, "Generated duration did not match the confirmed bucket", "Real Flow run returned a different duration")
        self.assertTrue(state["review_due"])
        self.assertIn("failure", state["review_reasons"])
        self.assertEqual([], state["candidate_improvements"])

    def test_user_correction_creates_candidate(self) -> None:
        state = MODULE.empty_state()
        correction, candidate = MODULE.record_correction(
            state,
            "User corrected an unnecessary metaphor",
            "When the sentence names a directly visible real process",
            "Prefer direct depiction before considering a metaphor",
            "Use a metaphor only for summaries, abstractions, or content without a real visual carrier",
            "Observed during a real VoxEasy visual-confirmation step",
            "Run one direct-scene case and one abstract-summary case, then inspect the routing decision",
            True,
        )
        self.assertEqual(correction["id"], candidate["source_ids"][0])
        self.assertEqual("pending_gate_review", candidate["status"])
        self.assertTrue(state["review_due"])

    def test_applied_patch_requires_reusable_candidate_and_manifest(self) -> None:
        state = MODULE.empty_state()
        _, candidate = MODULE.record_correction(
            state,
            "User corrected a repeatable timing rule",
            "When an SRT contains a leading blank",
            "Keep the blank inside the first Shot interval",
            "Only apply when the original media timeline is known",
            "Observed in a real SRT task",
            "Run the existing leading-blank timeline fixture",
            True,
        )
        with tempfile.TemporaryDirectory() as directory:
            manifest = Path(directory) / "backup-manifest.json"
            manifest.write_text("{}\n", encoding="utf-8")
            applied = MODULE.record_applied(
                state,
                candidate["id"],
                "Clarified the leading-blank rule",
                ["references/timeline-rules.md"],
                "Timeline fixture and validator passed",
                manifest,
            )
        self.assertEqual(candidate["id"], applied["candidate_id"])
        self.assertEqual("applied", candidate["status"])

    def test_backup_manifest_and_no_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "voxeasy"
            root.mkdir()
            (root / "SKILL.md").write_text("test\n", encoding="utf-8")
            backup_root = Path(directory) / "backups"
            manifest = MODULE.backup_files(
                root,
                ["SKILL.md"],
                "Test backup",
                backup_root,
                "20260806T000000Z",
            )
            data = json.loads(manifest.read_text(encoding="utf-8"))
            self.assertEqual(data["entries"][0]["original_sha256"], data["entries"][0]["backup_sha256"])
            with self.assertRaises(FileExistsError):
                MODULE.backup_files(
                    root,
                    ["SKILL.md"],
                    "Test backup",
                    backup_root,
                    "20260806T000000Z",
                )

    def test_machine_specific_path_is_rejected_from_learning_evidence(self) -> None:
        with self.assertRaises(ValueError):
            MODULE.ensure_safe_text("failure at /tmp/private-file", "evidence")

    def test_applied_patch_rejects_absolute_file_path(self) -> None:
        state = MODULE.empty_state()
        _, candidate = MODULE.record_correction(
            state,
            "User corrected a repeatable visual rule",
            "When a concrete object is directly visible",
            "Keep the concrete object as the scene anchor",
            "Do not apply to abstract summaries",
            "Observed in a real visual-confirmation step",
            "Run one concrete case and one abstract case",
            True,
        )
        with tempfile.TemporaryDirectory() as directory:
            manifest = Path(directory) / "backup-manifest.json"
            manifest.write_text("{}\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                MODULE.record_applied(
                    state,
                    candidate["id"],
                    "Clarified scene anchoring",
                    ["/tmp/private-file"],
                    "Example cases passed",
                    manifest,
                )


if __name__ == "__main__":
    unittest.main()
