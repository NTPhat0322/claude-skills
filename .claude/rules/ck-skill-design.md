# Skill design rules

Design rules for skills under `.claude/skills/`.

> Claude Code doesn't auto-attach rule files by glob the way Cursor's `.mdc` rules do. This doc isn't loaded automatically — reference it (`@.claude/rules/ck-skill-design.md`) when creating or reviewing a skill, or point the `skill-creator` skill at it.

- **Behavioral guidance only, not documentation.** If removing a section would not change the agent output, remove it.
- **Under 500 lines. Under 300 is better.** Approaching the limit means the skill is doing too much — extract to `references/` or split.
- **description frontmatter = trigger. Body = behavior.** Do not restate the trigger in the body. Do not duplicate guidance already in `CLAUDE.md` or rules.
- **Output skills define correct output.** Include a concrete example or success criteria — not just "produce a report".
- **Challenge overlap.** Is this a patch for a broken existing skill? Does it overlap with another skill domain?
