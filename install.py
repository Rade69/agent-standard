#!/usr/bin/env python3
"""Install/update the AGENT-STANDARD marker block in global agent config
files (AGENT-STD-001, Standard rada sa AI agentima v1.2, §3.1/§3.2).

Only the standard library. Works unmodified on Windows and Fedora. Respects
CODEX_HOME. Never touches content outside the marker block.

Marker block::

    <!-- AGENT-STANDARD:BEGIN version=1.2 sha256=<hash of GLOBAL_ROUTER.md> -->
    ...contents of GLOBAL_ROUTER.md...
    <!-- AGENT-STANDARD:END -->

Rules (§3.1):
  - File does not exist      -> create it containing only the block.
  - File exists, no block    -> backup (.bak-<timestamp>), block prepended
                                 at the very top; rest of the file is kept
                                 byte-identical, unchanged, after the block.
  - File exists, has a block -> backup, ONLY the text between (and
                                 including) the markers is replaced; every
                                 byte outside the markers is left untouched.

Modes::

    python install.py --dry-run     show what would change, touch nothing
    python install.py --install     write/update the block + backup
    python install.py --check       exit 0 if every target's block matches
                                     GLOBAL_ROUTER.md's hash; exit 1 + diff
                                     list of drift otherwise
    python install.py --uninstall   remove only the block, rest untouched
"""

from __future__ import annotations

import argparse
import hashlib
import os
import re
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent
ROUTER_PATH = REPO_ROOT / "GLOBAL_ROUTER.md"
STANDARD_VERSION = "1.2"

_BEGIN_RE = re.compile(
    r"<!-- AGENT-STANDARD:BEGIN version=(?P<version>[^\s]+) "
    r"sha256=(?P<hash>[0-9a-f]{64}) -->"
)
_END_MARKER = "<!-- AGENT-STANDARD:END -->"
# Full-block regex: BEGIN marker .. END marker, inclusive, across lines.
_BLOCK_RE = re.compile(
    r"<!-- AGENT-STANDARD:BEGIN version=[^\s]+ sha256=[0-9a-f]{64} -->"
    r".*?"
    r"<!-- AGENT-STANDARD:END -->",
    re.DOTALL,
)


@dataclass(frozen=True)
class Target:
    """One global config file this installer manages."""

    name: str
    path: Path
    verified: bool  # False = path is a best-effort guess, not confirmed
    note: str = ""


def _codex_home() -> Path:
    env = os.environ.get("CODEX_HOME")
    return Path(env) if env else (Path.home() / ".codex")


def targets() -> list[Target]:
    """Phase-1 targets (AGENT-STD-001 Korak 0c): Claude Code, Codex, Pi,
    Crush, OpenCode. Cursor is intentionally NOT a target — its global
    "User Rules" are not a plain-text file on this machine (searched
    ~/.cursor/** and AppData/Roaming/Cursor/User/settings.json, found
    nothing resembling a rules path); the marker-block mechanism does not
    apply to it. MiniMax is out of scope for phase 1 (Korak 0d)."""
    home = Path.home()
    return [
        Target("claude-code", home / ".claude" / "CLAUDE.md", verified=True),
        Target(
            "codex",
            _codex_home() / "AGENTS.md",
            verified=True,
            note="path resolved via CODEX_HOME env var, not the ~/.codex default",
        ),
        Target(
            "pi",
            home / ".pi" / "agent" / "APPEND_SYSTEM.md",
            verified=True,
            note="contract assumed AGENTS.md; the real file is APPEND_SYSTEM.md",
        ),
        Target(
            "crush",
            home / ".config" / "crush" / "CRUSH.md",
            verified=True,
            note="contract also listed ~/.config/AGENTS.md (generic); that "
            "file does not exist on this machine and is not used",
        ),
        Target(
            "opencode",
            home / ".config" / "opencode" / "instructions.md",
            verified=True,
            note="not in the original contract table; added as a phase-1 "
            "target per Korak 0c",
        ),
    ]


def _router_text() -> str:
    return ROUTER_PATH.read_text(encoding="utf-8")


def _router_hash() -> str:
    return hashlib.sha256(_router_text().encode("utf-8")).hexdigest()


def _build_block(router_text: str, router_hash: str) -> str:
    body = router_text.rstrip("\n")
    return (
        f"<!-- AGENT-STANDARD:BEGIN version={STANDARD_VERSION} "
        f"sha256={router_hash} -->\n"
        f"{body}\n"
        f"{_END_MARKER}"
    )


def _read_raw(path: Path) -> bytes:
    return path.read_bytes()


def _detect_bom_and_eol(raw: bytes) -> tuple[bytes, str]:
    """Return (bom_bytes, eol) where bom_bytes is b'' if absent and eol is
    '\\r\\n' or '\\n', detected from the file's own content so we never
    change either."""
    bom = b"\xef\xbb\xbf" if raw.startswith(b"\xef\xbb\xbf") else b""
    body = raw[len(bom) :]
    eol = "\r\n" if b"\r\n" in body else "\n"
    return bom, eol


def _decode(raw: bytes) -> tuple[str, bytes, str]:
    bom, eol = _detect_bom_and_eol(raw)
    text = raw[len(bom) :].decode("utf-8")
    if eol == "\r\n":
        text = text.replace("\r\n", "\n")
    return text, bom, eol


def _encode(text: str, bom: bytes, eol: str) -> bytes:
    if eol == "\r\n":
        text = text.replace("\n", "\r\n")
    return bom + text.encode("utf-8")


def _backup(path: Path) -> Path:
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_path = path.with_name(f"{path.name}.bak-{stamp}")
    backup_path.write_bytes(path.read_bytes())
    return backup_path


class AmbiguousBlockError(RuntimeError):
    pass


def _count_begin_markers(text: str) -> int:
    return len(_BEGIN_RE.findall(text))


def plan_for(target: Target, block: str) -> dict:
    """Read-only: compute what --install would do, without writing
    anything. Used by both --dry-run and --install (install just also
    executes the write)."""
    path = target.path
    if not path.exists():
        return {"action": "create", "path": path, "backup": None}

    raw = _read_raw(path)
    text, bom, eol = _decode(raw)
    begin_count = _count_begin_markers(text)
    has_end = _END_MARKER in text

    if begin_count > 1:
        raise AmbiguousBlockError(
            f"{path}: {begin_count} BEGIN markers found — refusing to guess "
            "which one to replace. Fix manually, then re-run."
        )
    if begin_count == 1 and not has_end:
        raise AmbiguousBlockError(
            f"{path}: BEGIN marker present without a matching END marker — "
            "refusing to touch a malformed block. Fix manually, then re-run."
        )

    if begin_count == 1 and has_end:
        new_text = _BLOCK_RE.sub(block, text, count=1)
        action = "replace-block"
    else:
        new_text = block + "\n\n" + text if text else block + "\n"
        action = "prepend-block"

    return {
        "action": action,
        "path": path,
        "backup": "will create .bak-<timestamp>",
        "old_text": text,
        "new_text": new_text,
        "bom": bom,
        "eol": eol,
    }


def do_install(target: Target, block: str, *, dry_run: bool) -> str:
    plan = plan_for(target, block)
    path = plan["path"]

    if plan["action"] == "create":
        if dry_run:
            return f"[dry-run] CREATE {path}"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(_encode(block + "\n", b"", "\n"))
        return f"CREATED {path}"

    if dry_run:
        return f"[dry-run] {plan['action'].upper()} {path} (backup first)"

    backup_path = _backup(path)
    path.write_bytes(_encode(plan["new_text"], plan["bom"], plan["eol"]))
    return f"{plan['action'].upper()} {path} (backup: {backup_path.name})"


def do_uninstall(target: Target, *, dry_run: bool) -> str:
    path = target.path
    if not path.exists():
        return f"SKIP {path} (does not exist)"
    raw = _read_raw(path)
    text, bom, eol = _decode(raw)
    begin_count = _count_begin_markers(text)
    if begin_count == 0:
        return f"SKIP {path} (no block present)"
    if begin_count > 1 or _END_MARKER not in text:
        raise AmbiguousBlockError(
            f"{path}: malformed/multiple blocks — refusing to uninstall "
            "automatically. Fix manually."
        )
    new_text = _BLOCK_RE.sub("", text, count=1)
    # Collapse the blank-line gap the removed block leaves behind, but only
    # at the very start of the file (prepend-mode leftover) to avoid
    # reshaping unrelated whitespace the user may have had.
    new_text = new_text.lstrip("\n")
    if dry_run:
        return f"[dry-run] REMOVE block from {path} (backup first)"
    backup_path = _backup(path)
    path.write_bytes(_encode(new_text, bom, eol))
    return f"REMOVED block from {path} (backup: {backup_path.name})"


def do_check(target: Target, expected_hash: str) -> tuple[bool, str]:
    path = target.path
    if not path.exists():
        return False, f"MISSING {path}"
    text, _bom, _eol = _decode(_read_raw(path))
    match = _BEGIN_RE.search(text)
    if match is None:
        return False, f"NO BLOCK {path}"
    if match.group("hash") != expected_hash:
        return False, (
            f"DRIFT {path} (installed sha256={match.group('hash')[:12]}…, "
            f"router sha256={expected_hash[:12]}…)"
        )
    if _END_MARKER not in text:
        return False, f"MALFORMED {path} (BEGIN without END)"
    return True, f"OK {path}"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--dry-run", action="store_true")
    group.add_argument("--install", action="store_true")
    group.add_argument("--check", action="store_true")
    group.add_argument("--uninstall", action="store_true")
    args = parser.parse_args(argv)

    router_text = _router_text()
    router_hash = hashlib.sha256(router_text.encode("utf-8")).hexdigest()
    block = _build_block(router_text, router_hash)

    all_ok = True
    for t in targets():
        verified_tag = "" if t.verified else " [UNVERIFIED]"
        note_tag = f" — {t.note}" if t.note else ""
        try:
            if args.check:
                ok, msg = do_check(t, router_hash)
                all_ok = all_ok and ok
                print(f"{t.name}{verified_tag}: {msg}{note_tag}")
            elif args.uninstall:
                msg = do_uninstall(t, dry_run=False)
                print(f"{t.name}{verified_tag}: {msg}{note_tag}")
            else:
                msg = do_install(t, block, dry_run=args.dry_run)
                print(f"{t.name}{verified_tag}: {msg}{note_tag}")
        except AmbiguousBlockError as exc:
            all_ok = False
            print(f"{t.name}{verified_tag}: ERROR {exc}{note_tag}")

    if args.check:
        return 0 if all_ok else 1
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
