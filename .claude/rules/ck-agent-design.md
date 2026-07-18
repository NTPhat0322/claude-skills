# Agent design rules

Design rules for agent definitions under `.claude/agents/`.

> Claude Code doesn't auto-attach rule files by glob the way Cursor's `.mdc` rules do. This doc isn't loaded automatically — reference it (`@.claude/rules/ck-agent-design.md`) when creating or reviewing an agent, or point the `skill-creator` skill at it.

- **One job per agent.** If the description needs "and also", split or simplify.
- **Tool list = what it actually uses.** No `Write` if it never writes. No shell if it only reads.
- **Check before creating.** The finalize trio (project-manager, docs-manager, git-manager) and code-reviewer are shared — never duplicate them.
- **Model tiering:** use cheaper models for bookkeeping (scout, git-manager, docs-manager, project-manager); stronger models for reasoning (debugger, tester, code-reviewer, planner, plan-reviewer).
- **Every output agent defines pass/fail.** Tests report results. Commits confirm staged files. Reviews state verdict explicitly.
- **Challenge existence.** Can the main agent handle it inline? What is the blast radius if it fails mid-pipeline?
