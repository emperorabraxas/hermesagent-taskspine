#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
deploy_webhook_receiver.sh

Deploys the HermesAgent GitHub webhook receiver to AWS (HTTP API + Lambda).

It will:
  1) Ensure AWS credentials work (sts get-caller-identity)
  2) Ensure the webhook secret exists in SSM Parameter Store (SecureString)
  3) Deploy/Update the CloudFormation stack
  4) Print the Webhook URL output

Environment:
  AWS_REGION (optional)                 Defaults to AWS CLI config region
  HERMES_GITHUB_WEBHOOK_SECRET (optional)
    - If set, that value is written to SSM (overwrite).
    - If unset, a new random secret is generated and written to SSM.

Notes:
  - This script does not create the GitHub webhook itself. Use scripts/github/create_webhook.sh
EOF
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
TEMPLATE="${ROOT}/aws/webhook-receiver/template.yaml"
STACK_NAME="hermesagent-taskspine-webhook"
SECRET_PARAM_NAME="/hermes-agent/github-webhook/secret"

if ! command -v aws >/dev/null 2>&1; then
  echo "aws CLI is required but not found" >&2
  exit 2
fi

REGION="${AWS_REGION:-}"
if [[ -z "$REGION" ]]; then
  # ask AWS CLI for configured default region (best-effort)
  REGION="$(aws configure get region 2>/dev/null || true)"
fi
if [[ -z "$REGION" ]]; then
  echo "AWS region not set. Set AWS_REGION or configure a default region." >&2
  exit 2
fi

echo "Using region: ${REGION}"

aws sts get-caller-identity --region "${REGION}" >/dev/null

SECRET="${HERMES_GITHUB_WEBHOOK_SECRET:-}"
if [[ -z "$SECRET" ]]; then
  SECRET="$(python3 -c "import secrets; print(secrets.token_hex(32))")"
  echo "Generated new webhook secret (copy this into GitHub webhook settings):"
  echo "${SECRET}"
fi

aws ssm put-parameter \
  --region "${REGION}" \
  --name "${SECRET_PARAM_NAME}" \
  --type SecureString \
  --value "${SECRET}" \
  --overwrite >/dev/null

aws cloudformation deploy \
  --region "${REGION}" \
  --template-file "${TEMPLATE}" \
  --stack-name "${STACK_NAME}" \
  --capabilities CAPABILITY_IAM \
  --parameter-overrides "SecretParamName=${SECRET_PARAM_NAME}" >/dev/null

WEBHOOK_URL="$(aws cloudformation describe-stacks --region "${REGION}" --stack-name "${STACK_NAME}" \
  --query "Stacks[0].Outputs[?OutputKey=='WebhookUrl'].OutputValue" --output text)"

echo "Webhook URL:"
echo "${WEBHOOK_URL}"

