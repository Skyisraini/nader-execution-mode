# NADER Execution Mode

Execution governance for AI coding agents. It turns substantial requests into a compact acceptance contract, executes within authorization, verifies outcomes, repairs in-scope failures, and reports evidence without false completion claims.

## What it adds

- Acceptance criteria before substantial work
- Action-first autonomous execution
- Bounded progress and tangent control
- Evidence-based completion and repair
- A three-attempt stop rule for debug loops
- Clear Complete, Partial, Blocked, and Failed states

[`skills/nader-execution-mode/SKILL.md`](skills/nader-execution-mode/SKILL.md) is canonical for NADER behavior. Documentation in the target project remains canonical for that project's facts and rules.

## Repository layout

```
.agents/plugins/marketplace.json   Codex marketplace catalog (points at this repo root)
.codex-plugin/plugin.json          Codex plugin manifest
skills/nader-execution-mode/       The portable skill; canonical behavior
  SKILL.md
  agents/openai.yaml               Optional Codex/ChatGPT presentation metadata
tests/                             Structural validator and behavioral scenarios
```

This repo is both a Codex marketplace and the plugin it publishes. The marketplace entry's `source.path` is `./`, so the repository root is the plugin root.

## Install

### Codex

Adding the marketplace does not install the plugin. Both commands are required.

```bash
codex plugin marketplace add Skyisraini/nader-execution-mode --ref main
codex plugin add nader-execution-mode@nader-execution-mode
```

Verify, then start a new Codex session so the skill loads:

```bash
codex plugin list      # expect: nader-execution-mode@nader-execution-mode  installed, enabled
```

Invoke with `$nader-execution-mode`, or run `/skills` inside a session to confirm it is listed.

Private repositories require git credentials that Codex can use for the clone. If the repo is private and your machine cannot authenticate to it, use the local install instead:

```bash
git clone https://github.com/Skyisraini/nader-execution-mode.git
codex plugin marketplace add ./nader-execution-mode
codex plugin add nader-execution-mode@nader-execution-mode
```

To skip plugins entirely, copy the skill into a Codex skills directory:

```bash
mkdir -p ~/.agents/skills
cp -R nader-execution-mode/skills/nader-execution-mode ~/.agents/skills/
```

### Claude Code

```bash
git clone https://github.com/Skyisraini/nader-execution-mode.git
mkdir -p ~/.claude/skills
cp -R nader-execution-mode/skills/nader-execution-mode ~/.claude/skills/
```

Verify with `/skills` inside a Claude Code session; the skill should appear with a personal scope. Invoke it by name, or with `/nader-execution-mode` where slash invocation is supported.

For a single repository, copy it to `<repo>/.claude/skills/nader-execution-mode/` instead.

### GitHub Copilot

```bash
git clone https://github.com/Skyisraini/nader-execution-mode.git
mkdir -p ~/.copilot/skills
cp -R nader-execution-mode/skills/nader-execution-mode ~/.copilot/skills/
```

For a single repository, copy it to `.github/skills/nader-execution-mode/` instead. In Copilot CLI, run `/skills reload` in an open session, or start a new session, then confirm the skill is listed.

## Verify

```bash
python3 tests/validate_package.py
```

That script checks structure and manifest consistency only. Behavioral scenarios are in [`tests/scenarios.md`](tests/scenarios.md) and must be run by a human inside each runtime.

## Verification status

| Claim | Status |
| --- | --- |
| Package structure and manifest consistency | Verified by `tests/validate_package.py` |
| `codex plugin marketplace add` + `codex plugin add` succeed and report `installed, enabled` | Verified on Codex CLI 0.154.0 against a local and a git-cloned copy of this repo |
| Codex install from the GitHub shorthand `Skyisraini/nader-execution-mode` | Not verified. Requires the published repo and working git credentials. |
| Claude Code loads and invokes the skill | Not verified in an authenticated session |
| GitHub Copilot loads and invokes the skill | Not verified in an authenticated session |
| The five behavioral scenarios pass in any runtime | Not verified. These need a live model session. |

Treat every "Not verified" row as unproven until someone runs the matching check in `tests/scenarios.md` and records the result.

## License and attribution

MIT licensed. The action-first and tangent-control concepts were inspired by Ayoub Ghriss's MIT-licensed [`i-have-adhd`](https://github.com/ayghri/i-have-adhd). NADER Execution Mode adds acceptance governance, autonomous execution, evidence gates, completion states, and repair discipline.
