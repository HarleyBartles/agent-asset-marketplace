---
name: skill-installer
description: Orchestrate GPT skill installation handoff from source to a valid installable package. Use when Harley asks to install, prepare, package, or update a GPT skill here, especially phrases like "install @skill", "using asset-market", "present for installation", "latest version", or "get this skill landed". Owns the source-to-handoff stack across skill-creator, skill-validator, skill-packager, and skill-handoff. Does not claim GPT self-installs skills; completion requires a visible skill.zip handoff and Harley's landed confirmation.
---

# Skill Installer

## Owned decision

Drive a skill from an authorized source path to a valid installable `skill.zip` handoff and track the path to Harley's `landed` confirmation.

This skill composes the existing skill stack. It does not replace source acquisition, semantic authorship, validation, packaging, or handoff cadence rules.

## Anti-use rule for repo-resident generated zips

If the work is repo-backed generation of `skill.zip` artifacts and Harley says he will install the generated zips directly in GPT, do not route into the GPT handoff lifecycle. Do not create a separate GPT handoff queue, install-handoff Linear issue, or `landed` requirement as worker DOD for that repo-backed case. The repo worker should return generated zip paths, package/projection validation evidence, and direct install notes instead.

Preserve `skill-installer` for explicit GPT install/present/package handoff requests, recovery from broken package handoff, handoff cadence management, or landed-confirmation tracking.

## Input routes

### Marketplace route

When the user says to install the latest version from the asset marketplace repo, or says `using asset-market`, invoke `asset-market` first. Continue only from a green `asset_market_source_packet` with a staged source path.

### Authorship route

When the user asks to create, update, rename, repair, or deliberately change skill content, invoke `skill-creator` first and require its structured authorship object for the staged source path.

### Uploaded zip route

When the user provides a zip and asks to install or prepare it, follow the skill-creator uploaded-zip intake first. Continue only after the zip has been inspected as a single-skill package or unpacked into a single staged source path.

## Stack order

Use this order for every installable handoff:

```text
source route -> skill-creator when content changed -> skill-validator -> skill-packager -> skill-handoff -> Harley landed
```

Do not skip a step because the source looks simple, because a package exists, or because a prior chat message says it passed.

## Required state objects

Require concrete objects for the same `target_skill` and `staged_source_path`:

```yaml
authored_by_skill_creator:
  target_skill: <skill-name>
  staged_source_path: <path>
  authored_by_skill_creator: true
  next_required_step: skill-validator
```

```yaml
validated_by_skill_validator:
  target_skill: <skill-name>
  staged_source_path: <same path>
  decision: pass
  handoff_allowed: true
  next_required_step: skill-packager
```

```yaml
packaged_by_skill_packager:
  target_skill: <skill-name>
  staged_source_path: <same path>
  package_path: <exact path ending /skill.zip>
  exact_file_exists: true
  exact_file_nonzero: true
  top_level_folder_matches_skill: true
  next_required_step: skill-handoff
```

If any object is missing, stale, path-mismatched, skill-name-mismatched, or prose-only, stop with `hard_red_stack_incomplete`.

## Handoff rules

Invoke `skill-handoff` before presenting an installable package link. The handoff must emit exactly one normal assistant-message link to a file whose basename is `skill.zip` and whose machine package evidence matches the exact archive.

Do not present multiple installable `skill.zip` links in one assistant message. For multiple skills, use the lifecycle selected by `skill-handoff`.

## Completion state

A package is not installed because GPT created it. Use these states:

- `packaged`: archive exists and passed packager verification.
- `presented`: valid `skill.zip` was handed off in a normal assistant message.
- `landed`: Harley confirms installation or acceptance.
- `repo_ready`: Harley saved the installed zip/source package for the worker child.

Only `landed` satisfies the install side of the issue DOD.

## Anti-false-green rules

Do not claim installation, repo update, marketplace publication, or user acceptance from package creation alone.

Do not treat `asset-market` source acquisition as validation. Do not treat `skill-validator` pass as package identity. Do not treat package evidence as a lawful visible handoff. Do not treat a visible handoff as `landed` until Harley says so.

## Stop rule

After presenting one installable package, stop and wait for `landed`, unless `skill-handoff` has explicitly selected a valid batch cursor. Do not mutate the repo from this skill.
