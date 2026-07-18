# Using this `.claude/` kit

This directory is the **Claude Code project kit**: skills, slash commands, sub-agents, hooks, contexts, coding levels, and design-rule references. In **claude-skills** the tree already lives here; in another repo it is the same tree at `<workspace>/.claude/`.

For a **step-by-step setup in Vietnamese**, see **[`README.md`](../README.md)** in the repo root.

---

## Open the right workspace

Claude Code reads **`.claude/**` from the folder you launch it in** (`claude` CLI, desktop app, or IDE extension). That root must **directly** contain this `.claude/` directory — not a parent folder that only has the project in a subfolder without `.claude/`.

---

## Skills (`skills/`)

Each subfolder with a **`SKILL.md`** is a skill. Claude Code discovers them under **`.claude/skills/`** and triggers them automatically based on the `description` in each skill's frontmatter.

| How you use them | What to do |
|------------------|------------|
| **Automatic** | Claude reads `description` frontmatter across all skills and activates the matching one when your request fits — no invocation needed. |
| **Slash / explicit** | A project command can point at a skill (e.g. **`/ck:cook`** reads `.claude/skills/ck-cook/SKILL.md`), or ask Claude directly to follow the workflow in a given `SKILL.md`. |
| **Direct reference** | `@`-mention the file, e.g. **`.claude/skills/ck-plan/SKILL.md`**, so the model loads that spec explicitly. |
| **Browse** | Open **`skills/`** and read `SKILL.md` + any `references/` next to it. |

---

## Commands (`commands/**/*.md`)

Slash commands live under **`commands/`**. A file's path (relative to `commands/`, minus `.md`) is its invocation, with `/` replaced by `:` — e.g. **`commands/ck/cook.md`** → **`/ck:cook`**. This kit namespaces everything under `ck/` so all its commands read as `/ck:<name>`.

Each file is a prompt template (YAML frontmatter + body). Frontmatter supports `description`, `argument-hint`, `allowed-tools`, `model`. Use `$ARGUMENTS` in the body to receive whatever the user typed after the command name.

---

## Agents (`agents/*.md`)

Markdown sub-agent definitions under **`agents/`** — planner, researcher, scout, debugger, tester, code-reviewer, plan-reviewer, project-manager, docs-manager, git-manager, playwright-capture. Frontmatter: `name`, `description` (used to decide when Claude spawns it), `tools` (comma-separated list), `model`. Spawn them explicitly ("use the `scout` agent to…") or let a command orchestrate them.

---

## Hooks (`hooks/`)

Python scripts implementing real **Claude Code** hook events (`SessionStart`, `UserPromptSubmit`, `PreToolUse`, `PostToolUse`, `Stop`, `SubagentStop`, `PreCompact`). They are wired up in **[`settings.json`](settings.json)**, which ships with this kit — copying `.claude/` in is enough, no extra configuration step. Details and the full event/matcher table: **[`hooks/README.md`](hooks/README.md)**.

Most hook behavior (thresholds, enabled flags, allow-lists) is tunable per-project via a `.ck.json` file at the repo root — see `/ck:init` and `/ck:coding-level`.

---

## Rules (`rules/*.md`)

Design-guidance docs for creating new agents, commands, and skills consistent with this kit's conventions. Unlike Cursor's `.mdc` rules, Claude Code has no glob-based auto-attach mechanism — these are plain reference docs. `@`-mention them (e.g. `@.claude/rules/ck-skill-design.md`) when authoring, or point the `skill-creator` skill at them.

---

## Contexts (`contexts/*.md`)

Markdown "modes" (dev / research / review) injected by the `dev_rules_reminder.py` hook based on which `/ck:*` command was invoked, or read by hand. Paths are always under **`.claude/contexts/`**.

---

## Coding levels (`coding-levels/*.md`)

Style / explanation-depth presets loaded by `session_init.py` from `.ck.json`'s `codingLevel` field. Set via `/ck:coding-level`.

---

## Layout reference

```text
.claude/
  skills/           # one folder per skill → SKILL.md
  commands/
    ck/*.md         # namespaced slash commands → /ck:<name>
  agents/*.md       # sub-agent definitions
  hooks/            # Python hooks (Claude Code hook events) + lib/
  contexts/
  coding-levels/
  rules/*.md        # design-rule reference docs (not auto-loaded)
  settings.json     # hook registrations, ignorePatterns, env
```
