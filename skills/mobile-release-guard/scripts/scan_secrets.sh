#!/usr/bin/env bash
# Read-only secret-pattern scanner. Prints "TYPE relative/path:line" only.
# It never prints matched text, so secret values cannot reach reports or logs.
# Usage: scan_secrets.sh <project_dir>
set -u
dir="${1:-.}"
[ -d "$dir" ] || { echo "usage: scan_secrets.sh <project_dir>" >&2; exit 2; }
dir="$(cd "$dir" && pwd)"

EXCL=( --exclude-dir=node_modules --exclude-dir=Pods --exclude-dir=build --exclude-dir=.git
       --exclude-dir=.gradle --exclude-dir=DerivedData --exclude-dir=vendor --exclude-dir=.dart_tool )

scan() {  # $1=type  $2=extended regex (case-insensitive when $3=i)
  local flags="-rInE"; [ "${3:-}" = "i" ] && flags="-rInEi"
  grep $flags "${EXCL[@]}" -e "$2" -- "$dir" 2>/dev/null \
    | awk -F: -v t="$1" -v d="$dir/" '{ f=$1; sub(d,"",f); print t, f ":" $2 }'
}

scan PRIVATE_KEY      '-----BEGIN ([A-Z]+ )?PRIVATE KEY-----'
scan AWS_ACCESS_KEY   'AKIA[0-9A-Z]{16}'
scan LLM_API_KEY      '(sk-ant-[A-Za-z0-9_-]{16,}|sk-[A-Za-z0-9]{20,})'
scan SLACK_TOKEN      'xox[abprs]-[A-Za-z0-9-]{10,}'
scan GITHUB_TOKEN     'gh[pousr]_[A-Za-z0-9]{30,}'
# Assignments of string literals to secret-looking names. Names that contain anon/publishable or
# NEXT_PUBLIC_/EXPO_PUBLIC_ are public client identifiers: labelled apart, never as secrets.
grep -rInEi "${EXCL[@]}" -e "[A-Za-z_]*(secret|token|passw(or)?d|credential)[A-Za-z_]*[[:space:]]*[:=][[:space:]]*[\"'][^\"']{8,}[\"']" \
  -e "[A-Za-z_]*key[[:space:]]*[:=][[:space:]]*[\"'][^\"']{8,}[\"']" -- "$dir" 2>/dev/null \
  | awk -F: -v d="$dir/" '{ f=$1; sub(d,"",f); c=tolower(substr($0, length($1)+length($2)+3));
      t=(c ~ /(anon|publishable|next_public_|expo_public_)/) ? "PUBLIC_CLIENT_ID" : "HARDCODED_SECRET";
      print t, f ":" $2 }'

# Env/credential files present in the tree (names only, never contents).
find "$dir" \( -name node_modules -o -name Pods -o -name build -o -name .git \) -prune -o \
  -type f \( -name '.env' -o -name '.env.*' -o -name '*.jks' -o -name '*.keystore' \
             -o -name '*.p12' -o -name 'service-account*.json' \) -print 2>/dev/null \
  | sed "s|^$dir/||" | awk '{ print "SENSITIVE_FILE", $0 }'

exit 0
