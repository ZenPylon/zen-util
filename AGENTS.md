# Agent Directives

## Tooling & Scripting Preferences
- **Ad-hoc Scripts:** Any temporary or utility scripts written during an agent session **should be written in Python with explicit type annotations** (e.g., `def parse_data(raw: str) -> dict:`). Avoid using bash/shell, Perl, or untyped JS/Node for inline scripting unless striclty necessary.

## Formatting & Output Rules
- **Numbered Lists:** Always use `1.` prefix for every item in ordered lists to maximize git diff and edit efficiency (e.g., `1. first`, `1. second`)
- For git commits, use the structure: <type>[optional scope]: <description>
  - Types: feat, fix, docs, style, refactor, perf, test, build, ci, chore, revert
  - Example: feat(auth): add OAuth2 refresh token handling

## Vendored Skills

`skills/` holds agent skills. Some are local originals (`test-inventory`); others are **vendored forks** of upstream skills with local patches (`grilling`, `retro`, `to-tickets` — originally from [mattpocock/skills](https://github.com/mattpocock/skills)). They are installed into `~/.agents/skills/` by symlink, so edits here take effect immediately.

**Why vendored instead of manager-installed:** the `skills` CLI (`npx skills update`) reinstalls changed skills wholesale and would clobber local patches. Vendored skills have no entry in `~/.agents/.skill-lock.json`, so the CLI never touches them.

**Upstream drift check:** run `python3 scripts/upstream-sync.py`. `ok` = nothing to do; `DRIFT` = upstream changed — clone the source, 3-way-merge `SKILL.md` with the vendored copy, re-apply or drop the local patch, then run `python3 scripts/upstream-sync.py --update` to re-baseline the recorded hash. Provenance (source repo, path, last-seen hash) lives in `skills/.upstream.json`.

**To vendor another skill:** copy it into `skills/<name>/`, apply patches, remove its entry from `~/.agents/.skill-lock.json`, replace `~/.agents/skills/<name>` with a symlink to `skills/<name>`, and add its provenance to `skills/.upstream.json` (hash from the lock entry before removal).
