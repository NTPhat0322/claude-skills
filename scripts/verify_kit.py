#!/usr/bin/env python3
"""
Verify claude-skills kit: agents/commands presence + frontmatter, hooks py_compile + smoke stdin.

Run from repo root:
  python3 scripts/verify_kit.py

Exit 0 if no hard failures; still prints WARN for path / doc mismatches.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CLAUDE = REPO / ".claude"
HOOKS = CLAUDE / "hooks"
AGENTS = CLAUDE / "agents"
COMMANDS = CLAUDE / "commands"
SKILLS = CLAUDE / "skills"


def eprint(*a: object) -> None:
    print(*a, file=sys.stderr)


def check_agents() -> list[str]:
    issues: list[str] = []
    for f in sorted(AGENTS.glob("*.md")):
        text = f.read_text(encoding="utf-8", errors="replace")
        if len(text.strip()) < 80:
            issues.append(f"WARN agent thin content: {f.name} ({len(text)} chars)")
        if not text.lstrip().startswith("---"):
            issues.append(f"WARN agent missing YAML frontmatter: {f.name}")
        if 'tools: [' in text:
            issues.append(f"FAIL agent tools field uses JSON-array syntax, not Claude Code comma list: {f.name}")
    if not list(AGENTS.glob("*.md")):
        issues.append("FAIL no agents/*.md")
    return issues


def check_commands() -> list[str]:
    issues: list[str] = []
    for f in sorted(COMMANDS.rglob("*.md")):
        text = f.read_text(encoding="utf-8", errors="replace")
        if not text.lstrip().startswith("---"):
            issues.append(f"FAIL command missing YAML frontmatter: {f.relative_to(CLAUDE)}")
        if ".cursor/" in text:
            issues.append(f"WARN command still references .cursor/: {f.relative_to(CLAUDE)}")
    if not list(COMMANDS.rglob("*.md")):
        issues.append("FAIL no commands")
    return issues


def check_skills() -> list[str]:
    issues: list[str] = []
    for f in sorted(SKILLS.rglob("SKILL.md")):
        rel = f.relative_to(SKILLS)
        text = f.read_text(encoding="utf-8", errors="replace")
        if not text.lstrip().startswith("---"):
            issues.append(f"FAIL skill missing frontmatter: {rel}")
    if not list(SKILLS.rglob("SKILL.md")):
        issues.append("FAIL no SKILL.md under skills/")
    return issues


def py_compile_hooks() -> list[str]:
    import ast

    issues: list[str] = []
    for f in sorted(HOOKS.rglob("*.py")):
        try:
            ast.parse(f.read_text(encoding="utf-8", errors="replace"), filename=str(f))
        except SyntaxError as e:
            issues.append(f"FAIL syntax {f.relative_to(REPO)}: {e}")
    return issues


def smoke_hook(path: Path, stdin: str, env: dict | None = None) -> tuple[int, str, str]:
    r = subprocess.run(
        [sys.executable, str(path)],
        input=stdin,
        text=True,
        capture_output=True,
        cwd=str(REPO),
        env={**dict(**__import__("os").environ), **(env or {})},
        timeout=30,
    )
    return r.returncode, r.stdout, r.stderr


def check_hooks_runtime() -> list[str]:
    issues: list[str] = []
    tests: list[tuple[str, Path, str]] = [
        ("dev_rules_reminder", HOOKS / "dev_rules_reminder.py", '{"message":"/ck:cook test"}'),
        ("privacy_block", HOOKS / "privacy_block.py", "{}"),
        ("session_end", HOOKS / "session_end.py", "{}"),
        ("pre_compact", HOOKS / "pre_compact.py", "{}"),
        ("subagent_init", HOOKS / "subagent_init.py", "{}"),
        ("caveman_watch", HOOKS / "caveman_watch.py", '{"message":"be brief"}'),
        ("artifact_fold", HOOKS / "artifact_fold.py", "{}"),
        ("session_init", HOOKS / "session_init.py", "{}"),
        ("build_check", HOOKS / "build_check.py", "{}"),
        ("simplify_gate", HOOKS / "simplify_gate.py", "{}"),
        ("session_state", HOOKS / "session_state.py", "{}"),
    ]
    for name, script, stdin in tests:
        if not script.exists():
            issues.append(f"FAIL missing hook {name}")
            continue
        code, out, err = smoke_hook(script, stdin)
        if code not in (0, 2):
            issues.append(f"FAIL hook {name} exit={code} stderr={err[:500]!r}")
        elif code == 2:
            issues.append(f"INFO hook {name} exit=2 (deny) stderr={err[:200]!r}")

    # suggest_compact: no __main__, executed as script body
    sc = HOOKS / "suggest_compact.py"
    if sc.exists():
        code, out, err = smoke_hook(sc, "")
        if code != 0:
            issues.append(f"FAIL suggest_compact exit={code}")

    return issues


def check_settings_json() -> list[str]:
    """settings.json must exist and register every hook script under some event."""
    import json

    issues: list[str] = []
    settings_path = CLAUDE / "settings.json"
    if not settings_path.exists():
        issues.append("FAIL .claude/settings.json missing — hooks will not run")
        return issues
    try:
        cfg = json.loads(settings_path.read_text(encoding="utf-8-sig"))
    except Exception as e:
        issues.append(f"FAIL .claude/settings.json invalid JSON: {e}")
        return issues

    registered = set()
    for event_entries in cfg.get("hooks", {}).values():
        for matcher_block in event_entries:
            for h in matcher_block.get("hooks", []):
                cmd = h.get("command", "")
                registered.add(Path(cmd.split('"')[-2] if '"' in cmd else cmd).name)

    core_hooks = {
        "session_init.py", "subagent_init.py", "session_end.py", "pre_compact.py",
        "dev_rules_reminder.py", "caveman_watch.py", "privacy_block.py",
        "suggest_compact.py", "artifact_fold.py",
    }
    missing = core_hooks - registered
    if missing:
        issues.append(f"WARN hooks not registered in settings.json: {', '.join(sorted(missing))}")
    return issues


def check_repo_claude_only() -> list[str]:
    """claude-skills ships the Claude Code kit only — no leftover .cursor/ tree in this repo."""
    issues: list[str] = []
    cursor_dir = REPO / ".cursor"
    if cursor_dir.exists():
        issues.append(
            "WARN .cursor/ exists in this repo — claude-skills should only ship .claude/"
        )
    return issues


def main() -> int:
    if not CLAUDE.is_dir():
        eprint("Run from claude-skills repo root (.claude/ missing)")
        return 2

    all_issues: list[str] = []
    all_issues += check_agents()
    all_issues += check_commands()
    all_issues += check_skills()
    all_issues += py_compile_hooks()
    all_issues += check_hooks_runtime()
    all_issues += check_settings_json()
    all_issues += check_repo_claude_only()

    fails = [x for x in all_issues if x.startswith("FAIL")]
    warns = [x for x in all_issues if x.startswith("WARN")]
    infos = [x for x in all_issues if x.startswith("INFO")]

    print("=== verify_kit.py ===")
    print(f"Repo: {REPO}")
    print(f"Agents: {len(list(AGENTS.glob('*.md')))} md")
    print(f"Commands: {len(list(COMMANDS.rglob('*.md')))} md")
    print(f"Skills: {len(list(SKILLS.rglob('SKILL.md')))} SKILL.md (all levels)")
    print(f"Hooks py: {len(list(HOOKS.rglob('*.py')))} files")
    print()
    for row in fails + warns + infos:
        print(row)

    print()
    if fails:
        print(f"Result: {len(fails)} FAIL, {len(warns)} WARN")
        return 1
    print(f"Result: OK ({len(warns)} WARN)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
