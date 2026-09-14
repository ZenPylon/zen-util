# Agent Directives

## Tooling & Scripting Preferences
- **Ad-hoc Scripts:** Any temporary or utility scripts written during an agent session **should be written in Python with explicit type annotations** (e.g., `def parse_data(raw: str) -> dict:`). Avoid using bash/shell, Perl, or untyped JS/Node for inline scripting unless striclty necessary.

## Formatting & Output Rules
- **Numbered Lists:** Always use `1.` prefix for every item in ordered lists to maximize git diff and edit efficiency (e.g., `1. first`, `1. second`)
