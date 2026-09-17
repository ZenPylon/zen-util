# Agent Directives

## Tooling & Scripting Preferences
- **Ad-hoc Scripts:** Any temporary or utility scripts written during an agent session **should be written in Python with explicit type annotations** (e.g., `def parse_data(raw: str) -> dict:`). Avoid using bash/shell, Perl, or untyped JS/Node for inline scripting unless striclty necessary.

## Formatting & Output Rules
- **Numbered Lists:** Always use `1.` prefix for every item in ordered lists to maximize git diff and edit efficiency (e.g., `1. first`, `1. second`)
- For git commits, use the structure: <type>[optional scope]: <description>
  - Types: feat, fix, docs, style, refactor, perf, test, build, ci, chore, revert
  - Example: feat(auth): add OAuth2 refresh token handling

## Vendored Skills

`skills/grilling`, `skills/retro`, `skills/to-tickets` are locally patched forks of [mattpocock/skills](https://github.com/mattpocock/skills), symlinked into `~/.agents/skills/` and absent from `.skill-lock.json` so the `skills` CLI never overwrites them.

To check for upstream changes: `python3 scripts/upstream-sync.py`. On `DRIFT`, merge upstream `SKILL.md` with the local copy, then `python3 scripts/upstream-sync.py --update` to re-baseline. Provenance: `skills/.upstream.json`.
