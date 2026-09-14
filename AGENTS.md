# Repository Instructions

## Source of truth

`skills/nader-execution-mode/SKILL.md` is the only canonical behavior specification. Runtime installation instructions may point to or copy that folder, but must not define divergent behavior.

## Manifest pair

Two manifests must stay in sync and neither is optional:

- `.codex-plugin/plugin.json` defines the plugin.
- `.agents/plugins/marketplace.json` defines the marketplace that publishes it.

The plugin `name` in both files and the marketplace `name` together form the install id `nader-execution-mode@nader-execution-mode`. Changing any of them breaks the documented install command, so change the README in the same commit.

## Change gate

Before merging a behavior change:

1. Update the canonical skill.
2. Add or revise a scenario when the behavior changes.
3. Run `python3 tests/validate_package.py`.
4. Bump `version` in `.codex-plugin/plugin.json` and add a `CHANGELOG.md` entry.
5. Re-run the Part A load check in `tests/scenarios.md` for any runtime whose install path changed, and update the result log with what was observed.
6. Confirm the README, the manifest pair, and the verification status table still describe the implemented behavior.

## Evidence rules

Do not mark a runtime as working in the README table or the scenario log unless that runtime itself reported the skill as loaded. Structural validation is not a substitute. Leave unproven rows as "Not verified" rather than removing them.

Do not store project-specific facts or credentials in this repository.
