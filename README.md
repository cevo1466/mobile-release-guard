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

## Status and verification

Verified by running them:
- `python3 skills/mobile-release-guard/scripts/validate_skill.py skills/mobile-release-guard` (frontmatter, links, all SEC/APP IDs)
- `cd skills/mobile-release-guard && python3 -m unittest discover -s tests` (30 tests: spec coverage, script behavior, secret redaction, stack detection on 7 fixtures)
- `curl | bash` installer, tested into a temporary directory

Not verified, be aware:
- The 16 behavioral evals (`evals/evals.json`, 6 scenarios + 10 negative cases) are checked by a **static trace** (`tests/test_eval_mechanisms.py`: each expected behavior must be backed by a rule in the skill or a script that runs). They have **not** been run as live end-to-end model sessions.
- App Store and Google Play rules were written from existing knowledge, not re-checked against the live policy pages; OWASP/CWE mappings are not web-verified. The skill itself tells the auditor to verify policies at run time and to report `UNVERIFIED` when it cannot.
- Not tried on a real production app yet.

## Uninstall

```bash
rm -rf ~/.claude/skills/mobile-release-guard
```

MIT licensed.
