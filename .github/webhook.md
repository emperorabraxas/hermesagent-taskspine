# GitHub Webhook (HermesAgent)

HermesAgent can be driven by GitHub webhooks (push/PR/issue events) if you run a receiver service.

HermesAgent **does not** automatically create webhooks (no assumptions). This file gives the exact config + commands.

## 1) Choose receiver URL

Set the public HTTPS endpoint that will receive GitHub webhook POSTs (must be reachable from GitHub), e.g.:

- `https://YOUR_DOMAIN/hermes/github/webhook`

If you're running the receiver locally, you typically expose it via a tunnel (Cloudflare Tunnel, ngrok, etc.)
and point the webhook URL at the tunnel hostname.

HermesAgent's built-in receiver listens at:

- `http://127.0.0.1:8787/github/webhook` (default)

## AWS (recommended if you don't want a tunnel)

HermesAgent includes an AWS deploy template that gives you a stable HTTPS URL:

- `https://<apiId>.execute-api.<region>.amazonaws.com/github/webhook`

Deploy it:

```bash
./scripts/aws/deploy_webhook_receiver.sh
```

This prints:

- the generated webhook secret (copy into GitHub webhook settings)
- the webhook URL (paste into GitHub webhook URL field)

## 2) Generate a secret

```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

Store it somewhere safe (example):

- GitHub webhook secret field
- `HERMES_GITHUB_WEBHOOK_SECRET` on your receiver service

## 3) Create the webhook (recommended via `gh`)

Prereqs:

- `gh auth login`
- Repo admin permissions

```bash
./scripts/github/create_webhook.sh \
  --repo "emperorabraxas/hermesagent-taskspine" \
  --url "https://YOUR_DOMAIN/hermes/github/webhook" \
  --secret "PASTE_SECRET"
```

## 3.5) Run the receiver

```bash
export HERMES_GITHUB_WEBHOOK_SECRET="PASTE_SECRET"
hermes webhook serve --host 127.0.0.1 --port 8787 --path /github/webhook
```

## 4) Suggested events

This script registers these events:

- `push`
- `pull_request`
- `issues`
- `issue_comment`

If you only want CI-style triggers, remove `issues`/`issue_comment`.
