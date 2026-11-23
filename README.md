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
- `python3 skills/mobile-release-guard/scripts/validate_skill.py skills/mobile-release-guard`: frontmatter, links, and every control family (SEC, APP, GP, EXT, AI), report sections A-L, the 17 official source URLs, eval case folders, executable scripts.
- `cd skills/mobile-release-guard && python3 -m unittest discover -s tests`: 63 tests (spec coverage, validator, secret scanner patterns and exit codes, stack detection on synthetic layouts incl. `.xcodeproj` directories and monorepos).
- `curl | bash` installer, tested into a temporary directory.

Secret scanner (`scripts/scan_secrets.sh [--strict] <dir>`): prints only type and `file:line`, never the matched text. Default exits 0; `--strict` exits 1 on secret-type findings (CI gate), while `PUBLIC_CLIENT_ID` (anon/publishable keys, Firebase client config) never fails. It is a regex scanner: a clean result means "not found by this scan", not "no secrets".

Policy checks: store and OWASP references were checked against official pages on 2026-11-23 and carry a dated `Son doğrulama` line with the source URL. Anything that could not be confirmed is marked `Doğrulanamadı` (for example the exact Sign in with Apple 4.8 equivalence criteria). Volatile numbers (API levels, Billing Library versions, fees) are deliberately not copied; the auditor must read the current page. The verification used search summaries, not full page reads.

Evals (`skills/mobile-release-guard/evals/`, 16 skill-creator case folders: 6 scenarios + 10 negative cases):
- Run **inline by the skill's author in one session, without subagents or a baseline**, then graded (84/84). Mechanical assertions (files unchanged by sha256, seeded fake secrets never printed, no guarantee wording, no invented version numbers) are real checks. The judged ones rest on the author's own reports, so the score is a self-consistency check, not independent proof.
- For real, independent runs with and without the skill, use Claude Code's runner from the skill directory (billed model runs): `claude plugin eval . --allow-tools Write,Edit,Bash --scaffold`.

Not verified, be aware:
- Not tried on a real production app yet.
- No independent (separate-session or other-model) evaluation yet.
- Stack detection is marker based (file names and fixed strings) and has documented blind spots.
- skill-creator's `quick_validate` rejects `argument-hint` and `disable-model-invocation`: its schema targets Claude.ai `.skill` packages. Both fields are valid in Claude Code and are needed here (manual-only invocation).

## Uninstall

```bash
rm -rf ~/.claude/skills/mobile-release-guard
```

MIT licensed.
