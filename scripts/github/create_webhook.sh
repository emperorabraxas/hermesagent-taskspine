#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
create_webhook.sh --repo OWNER/REPO --url https://... --secret HEX

Creates a GitHub webhook using the GitHub CLI (gh).

Requirements:
  - gh installed and authenticated: gh auth status
  - repo admin permission

Notes:
  - This script is safe-by-default: it only creates a webhook.
  - It does not store secrets on disk.
EOF
}

REPO=""
URL=""
SECRET=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --repo) REPO="${2:-}"; shift 2 ;;
    --url) URL="${2:-}"; shift 2 ;;
    --secret) SECRET="${2:-}"; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown arg: $1" >&2; usage; exit 2 ;;
  esac
done

if [[ -z "$REPO" || -z "$URL" || -z "$SECRET" ]]; then
  echo "Missing required args" >&2
  usage
  exit 2
fi

if ! command -v gh >/dev/null 2>&1; then
  echo "gh is required but not found" >&2
  exit 2
fi

gh api "repos/${REPO}/hooks" \
  --method POST \
  -f "name=web" \
  -f "active=true" \
  -f "events[]=push" \
  -f "events[]=pull_request" \
  -f "events[]=issues" \
  -f "events[]=issue_comment" \
  -f "config[url]=${URL}" \
  -f "config[content_type]=json" \
  -f "config[insecure_ssl]=0" \
  -f "config[secret]=${SECRET}" \
  >/dev/null

echo "Created webhook on ${REPO} -> ${URL}"
