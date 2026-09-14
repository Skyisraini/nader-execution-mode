# Changelog

## 0.1.1

Fixed:

- Added `.agents/plugins/marketplace.json`. Without it, `codex plugin marketplace add` failed with `marketplace root does not contain a supported manifest`, so the documented Codex install in 0.1.0 could not succeed. Reproduced and fixed against Codex CLI 0.154.0.
- Corrected the README Codex section to state that the marketplace step and the plugin step are both required, and to give a local-clone fallback for private repositories.
- Added per-runtime verification commands for Codex, Claude Code, and GitHub Copilot.
- Added a verification status table separating structural checks from unproven runtime behavior.

Changed:

- `.codex-plugin/plugin.json` now carries `repository`, `license`, and `keywords`, and `interface.defaultPrompt` uses the documented array form.
- `tests/validate_package.py` now validates the marketplace manifest, cross-file name consistency, `source.path` resolution, semver, skill-name-to-folder match, description length, and README drift. It reports all failures instead of aborting on the first.
- `tests/scenarios.md` now separates runtime load checks from behavioral scenarios and carries a result log.
- `AGENTS.md` documents the manifest pair and the evidence rules.

## 0.1.0

Initial package.
