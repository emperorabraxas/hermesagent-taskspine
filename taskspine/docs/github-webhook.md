# GitHub Webhook → Hermes Agent (Taskspine)

This repo uses Hermes Agent's built-in **webhook platform adapter** (`gateway/platforms/webhook.py`) to accept GitHub webhooks, validate the `X-Hub-Signature-256` HMAC signature, and trigger an agent run.

## Choose the public HTTPS URL

GitHub requires a public HTTPS endpoint. You can pick any URL you control.

Two common patterns:

1) **Direct to your server / container**
- Example: `https://spiders.wirelash.dev/github/webhook`

2) **Via a managed HTTPS edge (AWS)**
- Example: API Gateway / ALB / CloudFront → your Hermes host

## Hermes configuration

In your Hermes `config.yaml`, enable the webhook platform and define a route called `github`.

Example (snippet):

```yaml
platforms:
  webhook:
    enabled: true
    extra:
      host: 0.0.0.0
      port: 8644
      # Optional: make the endpoint exactly /github/webhook (single route).
      path_template: /github/webhook
      default_route: github
      routes:
        github:
          secret: ${HERMES_GITHUB_WEBHOOK_SECRET}
          events: [push, pull_request, issues, issue_comment]
          prompt: |
            You are HermesAgent. Handle this GitHub webhook:
            event={{event_type}}
            payload={{payload_json}}
```

If you prefer the upstream default routing (multiple routes), omit `path_template` and `default_route` and set the GitHub webhook URL to:

- `https://YOUR_HOST/webhooks/github`

## Local development (HTTP)

Locally, Hermes can listen on HTTP, but GitHub requires HTTPS. Use a tunnel (Cloudflare Tunnel, ngrok, etc.) to terminate HTTPS and forward to your local port.

## Create the GitHub webhook (via `gh`)

Use:

`taskspine/scripts/github/create_webhook.sh`

## Notes

- Hermes validates HMAC using `X-Hub-Signature-256` (`sha256=<hex>`).
- Keep the secret out of git history. Use environment variables or a secret manager.

