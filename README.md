# mobile-release-guard

A Claude Code skill that audits mobile apps (iOS, Android, Flutter, React Native, Expo, Capacitor, KMP) for security and App Store / Google Play release readiness. Reports are in Turkish and every finding cites file and line.

## Install (one command)

```bash
curl -fsSL https://raw.githubusercontent.com/cevo1466/mobile-release-guard/main/install.sh | bash
```

This copies the skill to `~/.claude/skills/mobile-release-guard/` (an existing install is backed up). Restart Claude Code afterwards. Read `install.sh` first if you prefer; it only downloads this repo and copies one folder.

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

## Status

Structural validation (`python3 skills/mobile-release-guard/scripts/validate_skill.py skills/mobile-release-guard`) and unit tests pass. Behavioral evals are defined in `skills/mobile-release-guard/evals/evals.json` (6 scenarios, 10 negative cases) but have not been run end-to-end yet.

## Uninstall

```bash
rm -rf ~/.claude/skills/mobile-release-guard
```

MIT licensed.
