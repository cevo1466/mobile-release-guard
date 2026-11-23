#!/usr/bin/env bash
# Read-only mobile stack detector. Prints one tag per line.
# Looks at file names and greps for fixed marker strings only; never executes
# project code and never prints file contents.
set -u
dir="${1:-.}"
[ -d "$dir" ] || { echo "usage: detect_stack.sh <project_dir>" >&2; exit 2; }

PRUNE=( -name node_modules -o -name Pods -o -name build -o -name .git -o -name .gradle -o -name DerivedData -o -name vendor -o -name .dart_tool )
tags=()
add() { tags+=("$1"); }

has_file() { find "$dir" \( "${PRUNE[@]}" \) -prune -o -name "$1" -print -quit 2>/dev/null | grep -q .; }
has_ext()  { find "$dir" \( "${PRUNE[@]}" \) -prune -o -name "*.$1" -print -quit 2>/dev/null | grep -q .; }
# $1 = fixed string, remaining = file name globs
has_text() {
  local needle="$1"; shift
  local args=()
  for g in "$@"; do args+=( --include="$g" ); done
  grep -rIlF "${args[@]}" --exclude-dir=node_modules --exclude-dir=Pods --exclude-dir=build \
    --exclude-dir=.git --exclude-dir=.gradle --exclude-dir=DerivedData --exclude-dir=vendor \
    -- "$needle" "$dir" 2>/dev/null | head -1 | grep -q .
}

# Apple
has_ext swift && add swift
has_text "import SwiftUI" "*.swift" && add swiftui
has_text "import UIKit" "*.swift" && add uikit
has_ext m && add objective-c
{ has_file Package.swift || has_file Package.resolved; } && add swiftpm
has_file Podfile && add cocoapods
{ has_ext xcodeproj || has_ext xcworkspace; } && add xcode
has_text "import StoreKit" "*.swift" "*.m" && add storekit
# Android
has_ext kt && add kotlin
has_ext java && add java
{ has_file build.gradle || has_file build.gradle.kts; } && add gradle
has_file AndroidManifest.xml && add android
has_text "androidx.compose" "*.kt" "*.kts" "*.gradle" && add compose
has_text "com.android.billingclient" "*.kt" "*.java" "*.kts" "*.gradle" && add play-billing
# Cross-platform
has_file pubspec.yaml && { add flutter; add dart; }
if has_file package.json; then
  add node
  has_text '"react-native"' package.json && add react-native
  has_text '"expo"' package.json && add expo
  has_text '"@capacitor/core"' package.json && add capacitor
  has_text '"@ionic/' package.json && add ionic
fi
has_file capacitor.config.json && add capacitor
has_text "kotlin(\"multiplatform\")" "*.kts" && add kotlin-multiplatform
# Backend / services
{ has_file GoogleService-Info.plist || has_file google-services.json || has_file firebase.json || has_file firestore.rules; } && add firebase
has_file firestore.rules && add firestore-rules
{ has_file config.toml && [ -d "$dir/supabase" ]; } && add supabase
has_text "supabase" "package.json" "pubspec.yaml" "*.swift" "*.kt" && add supabase
has_text "ENABLE ROW LEVEL SECURITY" "*.sql" && add supabase-rls
has_text "RevenueCat" "*.swift" "*.kt" "package.json" "pubspec.yaml" "Podfile" "*.gradle" "*.kts" && add revenuecat
has_text "openai" "package.json" "*.py" "*.swift" "*.kt" "pubspec.yaml" && add llm-api
has_text "anthropic" "package.json" "*.py" "*.swift" "*.kt" "pubspec.yaml" && add llm-api
has_text "generativelanguage" "*.swift" "*.kt" "*.py" "*.js" "*.ts" && add llm-api
has_file wrangler.toml && add cloudflare-workers
{ has_file composer.json && has_text laravel composer.json; } && add laravel
has_file .github && add github-actions
[ -d "$dir/.github/workflows" ] && add github-actions

printf '%s\n' "${tags[@]}" | sort -u
