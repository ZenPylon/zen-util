#!/usr/bin/env python3
"""Check vendored skills against their upstream sources.

Reads skills/.upstream.json, fetches the current upstream tree hash for each
skill via `gh api` (same mechanism the `skills` CLI uses), and reports which
vendored skills have upstream changes.

Usage:
    python3 scripts/upstream-sync.py           # report drift only
    python3 scripts/upstream-sync.py --update  # also update the recorded hashes

Exit codes: 0 = in sync, 1 = upstream changed (or error).
"""

import json
import os
import subprocess
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST = os.path.join(REPO_ROOT, "skills", ".upstream.json")


class UpstreamEntry(dict):
    """One entry in .upstream.json: source repo + last-seen upstream tree hash."""


def read_manifest() -> dict[str, UpstreamEntry]:
    with open(MANIFEST) as f:
        return json.load(f)


def write_manifest(data: dict[str, UpstreamEntry]) -> None:
    with open(MANIFEST, "w") as f:
        json.dump(data, f, indent=2, sort_keys=True)
        f.write("\n")


def _gh_api(endpoint: str) -> dict:
    """GET a GitHub API endpoint via `gh api` (uses gh's TLS + credentials)."""
    result = subprocess.run(
        ["gh", "api", endpoint], capture_output=True, text=True
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip())
    return json.loads(result.stdout)


def upstream_tree_sha(source: str, skill_path: str) -> str:
    """Fetch the current git tree SHA of `skill_path` in `source` (owner/repo)."""
    branch = _gh_api(f"repos/{source}")["default_branch"]
    tree = _gh_api(f"repos/{source}/git/trees/{branch}?recursive=1")

    prefix = skill_path.removesuffix("SKILL.md").rstrip("/")
    for entry in tree["tree"]:
        if entry["path"] == prefix:
            return entry["sha"]
    raise LookupError(f"path {prefix!r} not found in {source}@{branch}")


def main() -> int:
    manifest = read_manifest()
    apply = "--update" in sys.argv[1:]
    drifted = []

    for name, meta in sorted(manifest.items()):
        try:
            current = upstream_tree_sha(meta["source"], meta["skillPath"])
        except Exception as e:
            print(f"ERROR  {name}: {e}")
            drifted.append(name)
            continue

        if current == meta["skillFolderHash"]:
            print(f"ok     {name} (in sync with {meta['source']})")
            continue

        print(f"DRIFT  {name}: upstream {meta['source']} changed")
        print(f"         last-seen hash: {meta['skillFolderHash']}")
        print(f"         current  hash: {current}")
        print(
            f"         next: clone {meta['sourceUrl']}, 3-way-merge"
            f" {meta['skillPath']} with skills/{name}/SKILL.md"
        )
        drifted.append(name)
        if apply:
            meta["skillFolderHash"] = current
            print(f"         recorded new hash (patch re-application is manual)")

    if apply and drifted:
        write_manifest(manifest)
        print("manifest updated")
    return 1 if drifted else 0


if __name__ == "__main__":
    sys.exit(main())