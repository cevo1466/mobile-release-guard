#!/usr/bin/env bash
# Read-only secret-pattern scanner. Prints "TYPE relative/path:line" only; it never prints
# matched text, so secret values cannot reach reports or logs.
#
# Usage: scan_secrets.sh [--strict] <project_dir>
#   default   report mode: always exits 0 (the auditor reads the findings)
#   --strict  exits 1 when a secret-type finding was printed (CI gate); PUBLIC_CLIENT_ID and
#             INFO lines never fail. Exit 2 = bad usage.
#
# This is a regex scanner, not a complete one: it misses unknown token formats and secrets
# without a telling name. A clean result is "not found by this scan", never "no secrets".
set -u
strict=0
if [ "${1:-}" = "--strict" ]; then strict=1; shift; fi
dir="${1:-.}"
case "$dir" in -*) echo "usage: scan_secrets.sh [--strict] <project_dir>" >&2; exit 2;; esac
[ -d "$dir" ] || { echo "usage: scan_secrets.sh [--strict] <project_dir>" >&2; exit 2; }
dir="$(cd "$dir" && pwd)"

EXCL=( --exclude-dir=node_modules --exclude-dir=Pods --exclude-dir=build --exclude-dir=.git
       --exclude-dir=.gradle --exclude-dir=DerivedData --exclude-dir=vendor --exclude-dir=.dart_tool )

scan() {  # $1=type  $2=extended regex
  grep -rInE "${EXCL[@]}" -e "$2" -- "$dir" 2>/dev/null \
    | awk -F: -v t="$1" -v d="$dir/" '{ f=$1; sub(d,"",f); print t, f ":" $2 }'
}

run_scans() {
  scan PRIVATE_KEY      '-----BEGIN ([A-Z]+ )?PRIVATE KEY-----'
  scan AWS_ACCESS_KEY   'AKIA[0-9A-Z]{16}'
  scan LLM_API_KEY      '(sk-ant-[A-Za-z0-9_-]{16,}|sk-[A-Za-z0-9]{20,})'
  scan SLACK_TOKEN      'xox[abprs]-[A-Za-z0-9-]{10,}'
  scan GITHUB_TOKEN     'gh[pousr]_[A-Za-z0-9]{30,}'
  scan STRIPE_KEY       '(sk|rk)_live_[0-9A-Za-z]{16,}'
  scan SENDGRID_KEY     'SG\.[0-9A-Za-z_-]{16,}\.[0-9A-Za-z_-]{16,}'

  # Google API keys: in Firebase client config files they are public client identifiers;
  # anywhere else the key may be a server key, so verify its restrictions.
  grep -rInE "${EXCL[@]}" -e 'AIza[0-9A-Za-z_-]{30,}' -- "$dir" 2>/dev/null \
    | awk -F: -v d="$dir/" '{ f=$1; sub(d,"",f);
        t=(f ~ /(^|\/)(GoogleService-Info\.plist|google-services\.json)$/) ? "PUBLIC_CLIENT_ID" : "GOOGLE_API_KEY";
        print t, f ":" $2 }'

  # Assignments of string literals to secret-looking names. Names containing anon/publishable or
  # NEXT_PUBLIC_/EXPO_PUBLIC_ are public client identifiers: labelled apart, never as secrets.
  grep -rInEi "${EXCL[@]}" \
    -e "[A-Za-z_]*(secret|token|passw(or)?d|credential)[A-Za-z_]*[[:space:]]*[:=][[:space:]]*[\"'][^\"']{8,}[\"']" \
    -e "[A-Za-z_]*key[[:space:]]*[:=][[:space:]]*[\"'][^\"']{8,}[\"']" -- "$dir" 2>/dev/null \
    | awk -F: -v d="$dir/" '{ f=$1; sub(d,"",f); c=tolower(substr($0, length($1)+length($2)+3));
        t=(c ~ /(anon|publishable|next_public_|expo_public_)/) ? "PUBLIC_CLIENT_ID" : "HARDCODED_SECRET";
        print t, f ":" $2 }'

  # Env/credential files present in the tree (names only, never contents).
  find "$dir" \( -name node_modules -o -name Pods -o -name build -o -name .git \) -prune -o \
    -type f \( -name '.env' -o -name '.env.*' -o -name '*.jks' -o -name '*.keystore' \
               -o -name '*.p12' -o -name 'service-account*.json' \) -print 2>/dev/null \
    | sed "s|^$dir/||" | awk '{ print "SENSITIVE_FILE", $0 }'

  # A mature external scanner may be present: mention it, never run or install it.
  for t in gitleaks trufflehog; do
    command -v "$t" >/dev/null 2>&1 && echo "INFO external-scanner-available $t"
  done
}

findings="$(run_scans | sort -u)"
[ -n "$findings" ] && printf '%s\n' "$findings"

if [ "$strict" = 1 ] && printf '%s\n' "$findings" | grep -qE '^(HARDCODED_SECRET|PRIVATE_KEY|AWS_ACCESS_KEY|LLM_API_KEY|SLACK_TOKEN|GITHUB_TOKEN|STRIPE_KEY|SENDGRID_KEY|GOOGLE_API_KEY|SENSITIVE_FILE) '; then
  exit 1
fi
exit 0
