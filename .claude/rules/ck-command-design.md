# Command design rules

Design rules for slash commands under `.claude/commands/`.

> Claude Code doesn't auto-attach rule files by glob the way Cursor's `.mdc` rules do. This doc isn't loaded automatically — reference it (`@.claude/rules/ck-command-design.md`) when creating or reviewing a command, or point the `skill-creator` skill at it.

- **Commands orchestrate only.** No review checklists, fix logic, or business rules — those belong in agents or skills.
- **Readable top-to-bottom in under a minute.** If it is not, extract to agents.
- **Shared multi-step logic goes in an agent, not copy-pasted.** If a new command is a flag variation, make it a `--flag` on the existing one.
- **Every command ends with a verifiable outcome** — a report, a file, a test result, a commit hash. "Done" is not verifiable.
- **Challenge before adding.** Does this duplicate an existing command? Could it be a flag instead?
