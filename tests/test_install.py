"""Tests for install.py (AGENT-STD-001 Korak 3).

Everything runs against tmp_path. Never touches the real home directory.
Exercises the Target/plan_for/do_install/do_check/do_uninstall functions
directly (constructed against tmp_path files) rather than through main(),
so no monkeypatching of Path.home()/CODEX_HOME is needed.
"""

from __future__ import annotations

import hashlib
import importlib.util
import sys
from pathlib import Path

import pytest

_REPO_ROOT = Path(__file__).resolve().parents[1]
_SPEC = importlib.util.spec_from_file_location("install", _REPO_ROOT / "install.py")
install = importlib.util.module_from_spec(_SPEC)
sys.modules["install"] = install
_SPEC.loader.exec_module(install)  # type: ignore[union-attr]


ROUTER_TEXT = "# Router\n\nSome routing content.\n"
ROUTER_HASH = hashlib.sha256(ROUTER_TEXT.encode("utf-8")).hexdigest()
BLOCK = install._build_block(ROUTER_TEXT, ROUTER_HASH)


def _target(path: Path) -> "install.Target":
    return install.Target("test-agent", path, verified=True)


# --- new file -----------------------------------------------------------


def test_create_when_file_does_not_exist(tmp_path: Path) -> None:
    path = tmp_path / "subdir" / "AGENTS.md"
    msg = install.do_install(_target(path), BLOCK, dry_run=False)
    assert "CREATED" in msg
    assert path.read_text(encoding="utf-8") == BLOCK + "\n"


def test_dry_run_does_not_create_file(tmp_path: Path) -> None:
    path = tmp_path / "AGENTS.md"
    msg = install.do_install(_target(path), BLOCK, dry_run=True)
    assert "[dry-run]" in msg
    assert not path.exists()


# --- existing file, no block ---------------------------------------------


def test_prepend_block_keeps_existing_content_byte_identical(tmp_path: Path) -> None:
    path = tmp_path / "CLAUDE.md"
    original = "# Moje lične preferencije\n\nNešto što sam ručno napisao.\n"
    path.write_text(original, encoding="utf-8")

    install.do_install(_target(path), BLOCK, dry_run=False)

    new_text = path.read_text(encoding="utf-8")
    assert new_text.startswith(BLOCK)
    # The entire original content must survive byte-for-byte after the block.
    assert new_text.endswith(original)
    # A .bak-<timestamp> file must exist before the file was changed.
    backups = list(tmp_path.glob("CLAUDE.md.bak-*"))
    assert len(backups) == 1
    assert backups[0].read_text(encoding="utf-8") == original


def test_dry_run_does_not_modify_existing_file(tmp_path: Path) -> None:
    path = tmp_path / "CLAUDE.md"
    original = "# original\n"
    path.write_text(original, encoding="utf-8")

    install.do_install(_target(path), BLOCK, dry_run=True)

    assert path.read_text(encoding="utf-8") == original
    assert not list(tmp_path.glob("CLAUDE.md.bak-*"))


# --- existing file, old block already present -----------------------------


def test_replace_block_keeps_surrounding_content_byte_identical(
    tmp_path: Path,
) -> None:
    path = tmp_path / "AGENTS.md"
    old_router_text = "# Old router\n\nStale content.\n"
    old_hash = hashlib.sha256(old_router_text.encode("utf-8")).hexdigest()
    old_block = install._build_block(old_router_text, old_hash)
    before = "# Before the block\nSome prose.\n\n"
    after = "\n\n# After the block\nMore prose that must survive.\n"
    path.write_text(before + old_block + after, encoding="utf-8")

    install.do_install(_target(path), BLOCK, dry_run=False)

    new_text = path.read_text(encoding="utf-8")
    assert before in new_text
    assert after in new_text
    assert old_block not in new_text
    assert BLOCK in new_text
    # Content strictly before/after the markers is untouched.
    assert new_text.startswith(before)
    assert new_text.endswith(after)


def test_replace_is_idempotent(tmp_path: Path) -> None:
    path = tmp_path / "AGENTS.md"
    path.write_text("prefix\n" + BLOCK + "\nsuffix\n", encoding="utf-8")
    install.do_install(_target(path), BLOCK, dry_run=False)
    install.do_install(_target(path), BLOCK, dry_run=False)
    text = path.read_text(encoding="utf-8")
    assert text.count("AGENT-STANDARD:BEGIN") == 1


# --- --check ----------------------------------------------------------


def test_check_exit_ok_when_hash_matches(tmp_path: Path) -> None:
    path = tmp_path / "AGENTS.md"
    path.write_text(BLOCK + "\n", encoding="utf-8")
    ok, msg = install.do_check(_target(path), ROUTER_HASH)
    assert ok is True
    assert msg.startswith("OK")


def test_check_reports_drift_on_hash_mismatch(tmp_path: Path) -> None:
    path = tmp_path / "AGENTS.md"
    stale_block = install._build_block("# stale\n", "0" * 64)
    path.write_text(stale_block + "\n", encoding="utf-8")
    ok, msg = install.do_check(_target(path), ROUTER_HASH)
    assert ok is False
    assert "DRIFT" in msg


def test_check_reports_missing_block(tmp_path: Path) -> None:
    path = tmp_path / "AGENTS.md"
    path.write_text("no block here\n", encoding="utf-8")
    ok, msg = install.do_check(_target(path), ROUTER_HASH)
    assert ok is False
    assert "NO BLOCK" in msg


def test_check_reports_missing_file(tmp_path: Path) -> None:
    path = tmp_path / "does-not-exist.md"
    ok, msg = install.do_check(_target(path), ROUTER_HASH)
    assert ok is False
    assert "MISSING" in msg


# --- --uninstall --------------------------------------------------------


def test_uninstall_removes_only_the_block(tmp_path: Path) -> None:
    path = tmp_path / "AGENTS.md"
    before = "# Before\nprose\n\n"
    after = "\n\n# After\nmore prose\n"
    path.write_text(before + BLOCK + after, encoding="utf-8")

    install.do_uninstall(_target(path), dry_run=False)

    text = path.read_text(encoding="utf-8")
    assert "AGENT-STANDARD:BEGIN" not in text
    assert "AGENT-STANDARD:END" not in text
    assert before.strip("\n") in text
    assert after.strip("\n") in text


def test_uninstall_is_noop_when_no_block(tmp_path: Path) -> None:
    path = tmp_path / "AGENTS.md"
    original = "# nothing to remove\n"
    path.write_text(original, encoding="utf-8")
    msg = install.do_uninstall(_target(path), dry_run=False)
    assert "SKIP" in msg
    assert path.read_text(encoding="utf-8") == original


def test_uninstall_is_noop_when_file_missing(tmp_path: Path) -> None:
    path = tmp_path / "missing.md"
    msg = install.do_uninstall(_target(path), dry_run=False)
    assert "SKIP" in msg


# --- edge cases: CRLF, BOM, ambiguous markers -----------------------------


def test_preserves_crlf_line_endings(tmp_path: Path) -> None:
    path = tmp_path / "AGENTS.md"
    original = "line one\r\nline two\r\n"
    path.write_bytes(original.encode("utf-8"))

    install.do_install(_target(path), BLOCK, dry_run=False)

    raw = path.read_bytes()
    assert b"\r\n" in raw
    # The original CRLF content must still be present with CRLF intact.
    assert b"line one\r\nline two\r\n" in raw


def test_preserves_utf8_bom(tmp_path: Path) -> None:
    path = tmp_path / "AGENTS.md"
    original = "﻿# has a BOM\n"
    path.write_bytes(original.encode("utf-8"))

    install.do_install(_target(path), BLOCK, dry_run=False)

    raw = path.read_bytes()
    assert raw.startswith(b"\xef\xbb\xbf")


def test_two_begin_markers_refuses_to_guess(tmp_path: Path) -> None:
    path = tmp_path / "AGENTS.md"
    path.write_text(BLOCK + "\n" + BLOCK + "\n", encoding="utf-8")
    with pytest.raises(install.AmbiguousBlockError):
        install.do_install(_target(path), BLOCK, dry_run=False)


def test_begin_without_end_refuses_to_guess(tmp_path: Path) -> None:
    path = tmp_path / "AGENTS.md"
    begin_only = BLOCK.split(install._END_MARKER)[0]
    path.write_text(begin_only + "\n", encoding="utf-8")
    with pytest.raises(install.AmbiguousBlockError):
        install.do_install(_target(path), BLOCK, dry_run=False)
