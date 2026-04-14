#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
deploy_webhook_receiver.sh

Deploys the Taskspine GitHub webhook receiver to AWS (HTTP API + Lambda).

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
  - This script does not create the GitHub webhook itself.
    Use taskspine/scripts/github/create_webhook.sh
EOF
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi

if ! command -v aws >/dev/null 2>&1; then
  echo "aws CLI is required but not found" >&2
  exit 2
fi

REGION="${AWS_REGION:-}"
if [[ -z "$REGION" ]]; then
  REGION="$(aws configure get region || true)"
fi
if [[ -z "$REGION" ]]; then
  echo "AWS_REGION not set and AWS CLI has no configured region" >&2
  exit 2
fi

STACK_NAME="hermesagent-taskspine-webhook"
TEMPLATE="taskspine/infra/aws/webhook-receiver/template.yaml"
SECRET_PARAM_NAME="/hermes-agent/github-webhook/secret"

aws --region "$REGION" sts get-caller-identity >/dev/null

SECRET="${HERMES_GITHUB_WEBHOOK_SECRET:-}"
if [[ -z "$SECRET" ]]; then
  if command -v python3 >/dev/null 2>&1; then
    SECRET="$(python3 -c "import secrets; print(secrets.token_hex(32))")"
  else
    echo "python3 required to generate secret (or set HERMES_GITHUB_WEBHOOK_SECRET)" >&2
    exit 2
  fi
fi

aws --region "$REGION" ssm put-parameter \
  --name "$SECRET_PARAM_NAME" \
  --type SecureString \
  --value "$SECRET" \
  --overwrite \
  >/dev/null

aws --region "$REGION" cloudformation deploy \
  --stack-name "$STACK_NAME" \
  --template-file "$TEMPLATE" \
  --capabilities CAPABILITY_NAMED_IAM \
  --parameter-overrides "SecretParamName=$SECRET_PARAM_NAME" \
  >/dev/null

WEBHOOK_URL="$(aws --region "$REGION" cloudformation describe-stacks --stack-name "$STACK_NAME" --query "Stacks[0].Outputs[?OutputKey=='WebhookUrl'].OutputValue" --output text)"

echo "Webhook URL: ${WEBHOOK_URL}"
echo "SSM secret param: ${SECRET_PARAM_NAME}"
echo "Secret (paste into GitHub webhook settings): ${SECRET}"

