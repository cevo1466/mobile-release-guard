# mobile-release-guard

A Claude Code skill that audits mobile apps (iOS, Android, Flutter, React Native, Expo, Capacitor, KMP) for security and App Store / Google Play release readiness. Reports are in Turkish and every finding cites file and line.

## Install (one command)

```bash
curl -fsSL https://raw.githubusercontent.com/cevo1466/mobile-release-guard/main/install.sh | bash
```

This copies the skill to `~/.claude/skills/mobile-release-guard/` (an existing install is backed up). Restart Claude Code afterwards. Read `install.sh` first if you prefer; it only downloads this repo and copies one folder.

### Install through your AI assistant

Paste this into Claude Code (or any assistant that can run shell commands):

> Install the mobile-release-guard skill by running `curl -fsSL https://raw.githubusercontent.com/cevo1466/mobile-release-guard/main/install.sh | bash`, then tell me to restart.

To use another skills directory, set `CLAUDE_SKILLS_DIR` (the installer copies the folder to `$CLAUDE_SKILLS_DIR/mobile-release-guard`); only the default `~/.claude/skills` is tested.

## Use

| Command | What it does |
|---|---|
| `/mobile-release-guard` or `audit` | Read-only audit of the current project |
| `audit ios\|android\|all\|security\|appstore\|googleplay\|subscriptions` | Scoped audit |
| `plan` | P0-P3 remediation plan, no file changes |
| `fix [critical]` | Applies verified, narrow fixes; asks before payments, production or external accounts |
| `verify` | Re-checks earlier fixes and reruns tests |

The skill is manual-only (`disable-model-invocation: true`).

## What it covers

26 security controls (SEC-01..26), 24 App Store controls (APP-01..24), 25 Google Play controls (GP-01..25) and OWASP-based extras. Checks only run when the matching technology is detected; unverifiable items (backend, store consoles, devices) are reported as `UNVERIFIED`, never `PASS`.

## Status and verification

Verified by running them:
- `python3 skills/mobile-release-guard/scripts/validate_skill.py skills/mobile-release-guard` (frontmatter, links, all SEC/APP IDs)
- `cd skills/mobile-release-guard && python3 -m unittest discover -s tests` (31 tests: spec coverage, script behavior, secret redaction and public-ID separation, stack detection on 7 fixtures)
- `curl | bash` installer, tested into a temporary directory

Evals (`skills/mobile-release-guard/evals/`, 16 cases in the skill-creator folder format: 6 scenarios + 10 negative cases):
- They were run **inline by the skill's author in one session, without subagents or a baseline**, then graded (84/84 assertions). Mechanical assertions (files unchanged by sha256, seeded fake secrets never printed, no guarantee wording, no invented version numbers) are real checks. The judged ones rest on the author's own reports, so the score is a self-consistency check, not independent proof.
- Building them found and fixed real defects (scanner missed names ending in `_KEY`, no "no mobile project" rule, missing NOT_APPLICABLE conditions for APP-09/10/11/13/14).
- For real, independent runs with and without the skill, use Claude Code's own runner from the skill directory (billed model runs): `claude plugin eval . --allow-tools Write,Edit,Bash --scaffold`.

Not verified, be aware:
- App Store and Google Play rules were written from existing knowledge, not re-checked against the live policy pages; OWASP/CWE mappings are not web-verified. The skill tells the auditor to verify policies at run time and report `UNVERIFIED` when it cannot.
- Not tried on a real production app yet.
- skill-creator's `quick_validate` rejects `argument-hint` and `disable-model-invocation`: its schema targets Claude.ai `.skill` packages. Both fields are valid in Claude Code and are needed here (manual-only invocation).

## Uninstall

```bash
rm -rf ~/.claude/skills/mobile-release-guard
```

MIT licensed.
