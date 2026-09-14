#!/usr/bin/env python3
"""Static package checks for NADER Execution Mode.

Scope: file structure, manifest consistency, and governance invariants.
Out of scope: whether any runtime actually loads or obeys the skill. That
requires the runtime checks in tests/scenarios.md.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "nader-execution-mode"
SKILL = SKILL_DIR / "SKILL.md"
OPENAI_YAML = SKILL_DIR / "agents" / "openai.yaml"
MANIFEST = ROOT / ".codex-plugin" / "plugin.json"
MARKETPLACE = ROOT / ".agents" / "plugins" / "marketplace.json"
README = ROOT / "README.md"

FAILURES: list[str] = []


def require(condition: bool, message: str) -> None:
    if not condition:
        FAILURES.append(message)


def frontmatter(text: str) -> dict:
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not match:
        return {}
    fields = {}
    for line in match.group(1).splitlines():
        if line.startswith(" ") or ":" not in line:
            continue
        key, _, value = line.partition(":")
        fields[key.strip()] = value.strip()
    return fields


def check_files_exist() -> None:
    for path in (SKILL, MANIFEST, MARKETPLACE, README, ROOT / "LICENSE", ROOT / "NOTICE"):
        require(path.is_file(), f"missing required file: {path.relative_to(ROOT)}")


def check_skill(skill: str) -> None:
    require(skill.startswith("---\n"), "SKILL.md must start with YAML frontmatter")
    require("[TODO:" not in skill, "unfinished scaffold placeholder found")

    fields = frontmatter(skill)
    require(bool(fields), "SKILL.md frontmatter could not be parsed")
    name = fields.get("name", "")
    description = fields.get("description", "")

    require(name == "nader-execution-mode", "canonical skill name is missing or wrong")
    require(
        name == SKILL_DIR.name,
        "skill name does not match its folder name",
    )
    require(
        bool(re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name)),
        "skill name must be lowercase kebab-case",
    )
    require(bool(description), "skill description is missing")
    require(len(description) <= 1024, "skill description exceeds the 1024-character limit")

    required_concepts = {
        "acceptance contract": "acceptance governance",
        "Verify with evidence": "evidence gate",
        "Three-Attempt Stop Rule": "failure discipline",
        "Complete:": "complete state",
        "Partial:": "partial state",
        "Blocked:": "blocked state",
        "Failed:": "failed state",
        "System, developer, safety": "instruction precedence",
        "An earlier broad request to delete or overwrite is not this final confirmation": (
            "destructive confirmation boundary"
        ),
    }
    for phrase, label in required_concepts.items():
        require(phrase in skill, f"missing required concept: {label}")


def check_manifest(manifest: dict) -> None:
    require(manifest.get("name") == "nader-execution-mode", "plugin and folder names differ")
    require(manifest.get("skills") == "./skills/", "plugin must expose the skills directory")
    require(
        bool(re.fullmatch(r"\d+\.\d+\.\d+", str(manifest.get("version", "")))),
        "plugin version must be semver",
    )
    for path_field in ("skills", "mcpServers", "apps", "hooks"):
        value = manifest.get(path_field)
        if isinstance(value, str):
            require(
                value.startswith("./"),
                "manifest path " + path_field + " must start with ./",
            )


def check_marketplace(marketplace: dict, manifest: dict) -> None:
    require(
        marketplace.get("name") == "nader-execution-mode",
        "marketplace name must match the documented install command",
    )
    plugins = marketplace.get("plugins") or []
    require(len(plugins) == 1, "marketplace must expose exactly one plugin entry")
    if not plugins:
        return

    entry = plugins[0]
    require(
        entry.get("name") == manifest.get("name"),
        "marketplace plugin entry name must match .codex-plugin/plugin.json",
    )
    require("category" in entry, "marketplace entry must declare a category")

    policy = entry.get("policy") or {}
    require("installation" in policy, "marketplace entry must declare policy.installation")
    require("authentication" in policy, "marketplace entry must declare policy.authentication")

    source = entry.get("source")
    path = source.get("path") if isinstance(source, dict) else source
    require(isinstance(path, str) and path.startswith("./"), "source.path must start with ./")
    if isinstance(path, str):
        target = (ROOT / path).resolve()
        require(target.is_dir(), "source.path does not resolve to a directory")
        require(
            (target / ".codex-plugin" / "plugin.json").is_file(),
            "source.path does not point at a folder containing .codex-plugin/plugin.json",
        )


def check_readme(readme: str, manifest: dict, marketplace: dict) -> None:
    plugin_id = str(manifest.get("name")) + "@" + str(marketplace.get("name"))
    require(plugin_id in readme, "README must document the real plugin id")
    require(
        "codex plugin marketplace add" in readme,
        "README must document the marketplace step before the plugin step",
    )
    require("~/.claude/skills" in readme, "README must document the Claude Code skills path")
    require(
        "~/.copilot/skills" in readme or ".github/skills" in readme,
        "README must document a supported Copilot skills path",
    )
    require(
        "Not verified" in readme,
        "README must state which runtimes are unverified",
    )


def check_openai_yaml() -> None:
    if not OPENAI_YAML.is_file():
        return
    text = OPENAI_YAML.read_text(encoding="utf-8")
    require("interface:" in text, "agents/openai.yaml must declare an interface block")
    for key in ("display_name", "short_description", "default_prompt"):
        require(key in text, "agents/openai.yaml is missing " + key)


def report() -> int:
    if FAILURES:
        print("FAIL: " + str(len(FAILURES)) + " structural problem(s)")
        for failure in FAILURES:
            print("  - " + failure)
        return 1
    print("PASS: package structure and governance invariants validated")
    print("NOTE: structure only. Runtime loading is not proven by this script.")
    return 0


def main() -> int:
    check_files_exist()
    if FAILURES:
        return report()

    skill = SKILL.read_text(encoding="utf-8")
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    marketplace = json.loads(MARKETPLACE.read_text(encoding="utf-8"))
    readme = README.read_text(encoding="utf-8")

    check_skill(skill)
    check_manifest(manifest)
    check_marketplace(marketplace, manifest)
    check_readme(readme, manifest, marketplace)
    check_openai_yaml()

    return report()


if __name__ == "__main__":
    sys.exit(main())
