# Hooks in this kit

When you copy this **`.claude/`** tree into another repository, **skills, commands, agents, contexts, and rules** work from that repo's workspace root without extra configuration.

The **Python files** in this folder implement **Claude Code** hook events (`SessionStart`, `UserPromptSubmit`, `PreToolUse`, `PostToolUse`, `Stop`, `PreCompact`, …). They read and write **under the project's `.claude/` tree** (for example `.claude/session-data`, `.claude/contexts`, `.claude/coding-levels`) and are wired up in **[`settings.json`](../settings.json)**.

Claude Code does **not** run scripts under `hooks/` automatically just because the files exist — each script must be registered under the `hooks` key in `.claude/settings.json` (or `settings.local.json`), with an event name, an optional tool-name `matcher`, and a `command` pointing at the script. This kit's `settings.json` already registers every script below; copy it along with `.claude/` and the hooks are active immediately.

## What each hook does

| Script | Event | Matcher | Purpose |
|---|---|---|---|
| `session_init.py` | `SessionStart` | `startup\|resume\|clear\|compact` | Loads coding level + previous session state into context (skips for subagents) |
| `subagent_init.py` | `SessionStart` | `startup\|resume\|clear\|compact` | Injects ~200-token context into subagent sessions only |
| `session_end.py` | `Stop` | — | Persists session state (`session_state.py`) after each response |
| `pre_compact.py` | `PreCompact` | — | Saves state and purges outdated session files before `/compact` |
| `dev_rules_reminder.py` | `UserPromptSubmit` | — | Injects the active context (`dev`/`research`/`review`) and any active plan |
| `caveman_watch.py` | `UserPromptSubmit` | — | Watches tool-call count thresholds, triggers/releases terse "caveman" mode |
| `privacy_block.py` | `PreToolUse` | `Read\|Write\|Edit\|Bash` | Blocks access to secrets/credentials unless allow-listed in `.ck.json` |
| `build_check.py` | `PostToolUse` | `Write\|Edit` | Runs the relevant build/type-check and surfaces compiler errors |
| `simplify_gate.py` | `PostToolUse` | `Write\|Edit` | Tracks edit volume, triggers the `simplify` skill past threshold |
| `artifact_fold.py` | `PostToolUse` | `Read\|Grep\|Bash` | Flags oversized tool output to be saved under `.claude/artifacts/` |
| `suggest_compact.py` | `PreToolUse` | `Write\|Edit\|Bash\|Agent` | Counts tool calls, suggests `/compact` at checkpoints |

Shared helpers live in `hooks/lib/` (`ck_config_utils.py` for `.ck.json` + project-root resolution, `session_utils.py`, `project_detector.py`, `privacy_checker.py`, `config_counter.py`, `hook_logger.py`).

## Configuration

Most behavior is tunable per-project via a `.ck.json` file at the repo root (thresholds, enabled flags, allow-lists). Hooks fall back to sane defaults when it's absent.

## Python interpreter

`settings.json` invokes hooks with `python`. If your PATH only has `python3` (common on Linux/Mac), replace `python` with `python3` in `.claude/settings.json` — or symlink one to the other. On Windows, watch out for the `python3`/`python` App Execution Alias stub that prints an install prompt instead of running Python; `python` is usually the safe choice there.
