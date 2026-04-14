# Building a Paymaster Proxy
Source: https://docs.cdp.coinbase.com/paymaster/guides/paymaster-proxy



This guide shows how to build a backend proxy for your CDP Paymaster endpoint. A proxy keeps your API key secure while allowing you to add custom validation logic for sponsored transactions.

## Why Use a Proxy?

Your CDP Paymaster endpoint URL contains your **Client API Key** (not a Secret API Key). While this isn't as sensitive as a secret key, exposing it in client-side code allows anyone to use your Paymaster endpoint to sponsor transactions—potentially draining your gas credits or abusing your allowlisted contracts.

A proxy solves this by:

1. **Keeping your API key server-side** — The Paymaster URL never reaches the browser
2. **Enabling custom validation** — Add rate limiting, user authentication, or business logic
3. **Providing an audit trail** — Log all sponsorship requests for monitoring

For a deeper dive into security considerations, see the [Security](/paymaster/reference-troubleshooting/security) page.

<Note>
  **When is a proxy optional?**

  If you're using CDP Embedded Wallets with `useCdpPaymaster: true`, the SDK handles paymaster communication securely. A custom proxy is only needed if you want additional validation beyond CDP's built-in contract allowlists.
</Note>

## Basic Proxy Implementation

Here's a minimal Next.js API route that proxies requests to your CDP Paymaster:

```typescript title="app/api/paymaster/route.ts" theme={null}
import { NextRequest, NextResponse } from "next/server";

const PAYMASTER_URL = process.env.CDP_PAYMASTER_URL!;

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();

    const response = await fetch(PAYMASTER_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });

    const data = await response.json();
    return NextResponse.json(data, { status: response.status });
  } catch (error) {
    console.error("Paymaster proxy error:", error);
    return NextResponse.json(
      { error: "Internal server error" },
      { status: 500 }
    );
  }
}
```

Store your Paymaster URL in an environment variable (server-side only):

```bash title=".env" theme={null}