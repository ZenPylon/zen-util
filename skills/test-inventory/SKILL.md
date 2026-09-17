---
name: test-inventory
description: >
  Enumerate, review, and sign off the unit/integration tests for a feature
  BEFORE any test code is written. Takes a spec plus agreed seams (the output
  of to-spec); produces a reviewable inventory document, then hands it to tdd
  as ordered slices. Use when the user says "list the tests", "what tests
  should we write", "test enumeration", or after seams are confirmed but
  before TDD starts. Not for: writing the tests themselves (use tdd), QA
  sprint/release test plans (use a test-planning skill), or reviewing
  finished test code.
---

# Test Inventory

Produce the complete list of tests a feature needs, get the user's sign-off on
it, and only then hand it to the `tdd` skill as an ordered set of slices. The
inventory is a **design artifact, not test code**. It fills the gap between
"seams confirmed" (end of `to-spec`) and "first failing test written" (start of
`tdd`).

Two failure modes guard everything below:

1. **Fabrication** — a test for behavior no upstream declares is a defect, not
   coverage. Every inventory row traces to the spec, an acceptance criterion,
   or an error the interface can actually produce. Never invent error cases
   the interface cannot produce because they "seem thorough".
2. **Combinatorial blow-up** — depth follows risk. A 10-switch module does not
   get 1,024 rows; it gets risk-selected boundaries, negatives, and a few
   pairwise combinations. Trivial areas get happy-path-only. Row count is not
   coverage: blow-up is a defect in both directions (unmaintainable, and it
   hides which behaviors are actually risky).

## Inputs

1. The spec (from `to-spec`, an issue, or prose). If no spec exists, stop
   and send the user to `grilling` first — an inventory built on an
   unchallenged plan inherits its blind spots.
2. The **agreed seams**. If seams are not yet agreed, propose them first
   (highest seam possible, fewest overall — see `tdd`/`codebase-design`), and
   confirm with the user before enumerating anything.

## Workflow

### Step 1: Enumerate behaviors per seam

For each seam, walk every category and list candidate tests as one-line rows:

> `seam · behavior · input/state · expected observable result · source (spec section)`

Categories (skip any that don't apply to the seam, and say so):

- **Happy path** — primary success flow.
- **Validation** — required fields empty, format violations, boundary values.
- **Error conditions** — every error the interface can return: rejected
  input, dependency failure, timeout.
- **Edge cases** — unicode, empty collections, oversized payloads, zero/one/many,
  unsupported formats.
- **Concurrency / sequencing** — double-submit, retry-after-timeout, two
  writers on the same record. The most-missed category; justify skipping it.
- **Integration points** — behavior across each boundary the seam crosses.

While enumerating, read the actual code around each seam if it exists — the
spec omits real error paths, and rows sourced from code are often the most
valuable. A row sourced from code rather than spec is legal but must be marked
`source: code` so the user can confirm it's a behavior worth pinning.

### Step 2: Risk-weight the inventory

Mark each row HIGH / MEDIUM / LOW risk (likelihood × impact of the behavior
breaking). Depth follows risk:

- HIGH: full coverage across applicable categories.
- MEDIUM: happy path + the two or three most dangerous negatives.
- LOW: happy path only, or drop the row entirely.

Cut padding: if two rows assert the same observable result at the same seam,
keep one.

### Step 3: Grill in rounds

Format the inventory as a reviewable document and work it through `grilling`
rounds: present the rows grouped by seam with your risk calls and
recommendations, ask the whole open frontier in one round (numbered questions,
recommended answers), wait, and reshape. Typical frontier questions:

- Which of these behaviors are actually in scope?
- Is this concurrency case real for this system, or hypothetical?
- This row's expected result comes from code, not the spec — keep or cut?
- Which seams deserve depth; which are LOW-risk happy-path-only?

The session is done when every row is either accepted or cut and nothing is
silently assumed.

### Step 4: Emit the inventory document

Write the final inventory to `docs/test-inventories/<feature>.md` (create the
directory if needed). Structure:

1. **Seams** — one line each, as confirmed.
2. **Inventory table** — `id · seam · behavior · expected result · risk ·
   source`. IDs stable (`T-01`, `T-02`, …) so tickets and tests can reference
   rows.
3. **Explicitly dropped** — candidate rows cut in review, each with a
   one-line reason. This makes the not-testing decision visible instead of
   silent.
4. **Assumptions** — anything the inventory relies on that no upstream
   declares.

Then get explicit user sign-off on the document.

### Step 5: Hand off to tdd

On sign-off, the inventory's HIGH-risk rows (first) order the `tdd` slices:
one row = one red → green cycle, at that row's seam. The inventory is a
checklist, not a commitment: when a cycle teaches you something — the seam is
wrong, a behavior is impossible, a row is redundant — amend the inventory
document and note the amendment, then continue. Do not write test files from
the inventory in bulk; that is horizontal slicing and it fails (see `tdd`).

## Rules

**Hard rules:**

1. **No test code before sign-off.** This skill produces a document; `tdd`
   produces code, one slice at a time.
2. **No unconfirmed seams.** Confirm seams first; enumerate second.
3. **Dropped rows are recorded, not deleted silently.**

**Preferences:**

1. Order rounds by seam; within a seam, happy path → validation → errors →
   edges → concurrency.
2. Keep each row to one line in rounds; the document can expand expected
   results where the observable output needs precision (exact message, error
   code).

## Related

1. `to-spec` — produces the spec and the confirmed seams this skill consumes.
2. `tdd` — consumes the signed-off inventory as an ordered slice list;
   owns the good-test bar (tests verify behavior through public interfaces) and
   the anti-patterns this skill's rows are pre-checked against.
3. `grilling` — the interview format used in Step 3.