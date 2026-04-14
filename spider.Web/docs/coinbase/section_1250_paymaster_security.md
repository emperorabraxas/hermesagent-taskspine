# Paymaster Security
Source: https://docs.cdp.coinbase.com/paymaster/reference-troubleshooting/security



## Protecting Your Paymaster Endpoint

Your Paymaster endpoint URL includes your **Client API Key** (not a Secret API Key). While the Client API Key is less sensitive than a secret - it cannot access your wallets or signing capabilities - it still grants access to sponsor transactions on your behalf. **Anyone with this URL can send requests that consume your gas credits.**

<Note>
  The Client API Key in your Paymaster URL is different from the Secret API Key used for Server Wallets. Exposing your Paymaster URL won't compromise your wallet security, but it can lead to unauthorized gas sponsorship.
</Note>

### The Risk

If your Paymaster URL is exposed in client-side code (JavaScript bundles, network requests visible in browser DevTools), malicious actors can:

1. **Drain your gas credits** by sending sponsored transactions
2. **Abuse your allowlisted contracts** if your policy is too permissive
3. **Exceed your billing limits** unexpectedly

### Mitigation Strategies

<Steps>
  <Step title="Use built-in CDP Paymaster integration">
    The simplest and most secure approach is to use CDP's built-in Paymaster integration, which handles the endpoint securely without exposing it client-side:

    * **CDP Embedded Wallets** — Use `useCdpPaymaster: true` with `useSendUserOperation`
    * **CDP Server Wallets** — Use [Managed Mode](/server-wallets/v2/evm-features/managed-mode#paymaster-integration) which automatically integrates Paymaster
  </Step>

  <Step title="Set up a contract allowlist">
    Always configure a contract allowlist in the [Paymaster Configuration](https://portal.cdp.coinbase.com/products/bundler-and-paymaster). This limits sponsorship to only the contracts your application needs.

    Without an allowlist, any transaction to any contract could be sponsored.
  </Step>

  <Step title="Create a Paymaster proxy (if not using CDP Wallets)">
    If you're integrating with other wallet solutions (Wagmi, viem, etc.), route all Paymaster requests through your backend instead of calling the endpoint directly from the frontend.

    See the [Paymaster Proxy Guide](/paymaster/guides/paymaster-proxy) for implementation details.
  </Step>

  <Step title="Configure spend limits">
    Set limits to protect against unexpected usage:

    * **Per-userOperation limit** — Maximum USD per single operation
    * **Per-address limit** — Maximum sponsorship per sender address
    * **Global limit** — Maximum total USD sponsorship
  </Step>
</Steps>

## Paymaster Proxy

Creating a backend API to proxy Paymaster requests is critical for production applications.

### Benefits

* **Protect your Client API key** — The Paymaster URL never leaves your server
* **Add custom validation** — Implement rate limiting, user auth, or business logic
* **Audit requests** — Log and monitor all sponsorship requests

### Basic Implementation

```typescript title="api/paymaster-proxy.ts" theme={null}
// Example: Next.js API route
import { NextRequest, NextResponse } from "next/server";

const PAYMASTER_URL = process.env.CDP_PAYMASTER_URL!;

export async function POST(request: NextRequest) {
  // Optional: Add authentication
  const session = await getSession(request);
  if (!session) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }
  
  // Optional: Add rate limiting
  const rateLimitOk = await checkRateLimit(session.userId);
  if (!rateLimitOk) {
    return NextResponse.json({ error: "Rate limited" }, { status: 429 });
  }
  
  const body = await request.json();
  
  // Forward to Paymaster
  const response = await fetch(PAYMASTER_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  
  const data = await response.json();
  return NextResponse.json(data);
}
```

<Tip>
  For local development, you can use the Paymaster URL directly in your frontend. Always use a proxy in production.
</Tip>

***

## EIP-7702 Security

EIP-7702 introduces new security considerations for wallet upgrades. CDP Wallets do not yet support EIP-7702 upgrades directly, but CDP Paymaster can sponsor transactions for EOAs that have been upgraded using other tools.

### The Risk: Front-Running Attacks

When upgrading an EOA to a smart account, there's a risk of **initialization front-running**:

1. User signs an authorization to delegate to a smart account implementation
2. Attacker sees the pending transaction and front-runs it
3. Attacker calls the wallet's `initialize` function first, setting themselves as the owner
4. User's transaction completes, but the attacker now controls the wallet

### Mitigation: Use EIP7702Proxy

Never delegate directly to a wallet implementation. Instead, delegate to the **EIP7702Proxy** contract which makes the upgrade atomic:

1. Delegate your EOA to `EIP7702Proxy` (not the wallet implementation)
2. In the same transaction, call `setImplementation` with your desired wallet implementation and initialization data
3. The proxy validates a signature and uses a nonce tracker to prevent replay attacks
4. Implementation and initialization happen atomically — no window for front-running

### Contract Addresses

See [EIP7702Proxy releases](https://github.com/base/eip-7702-proxy/releases/tag/v1.0.0) for the canonical deployment addresses.

### Best Practices for 7702

* **Use only trusted delegate contracts** — Verify implementations are legitimate and audited
* **Verify addresses on block explorers** — Double-check contract addresses match expected implementations
* **Use EIP7702Proxy** — Never delegate directly to a wallet implementation
* **Validate in your application** — Check that delegate addresses match known safe implementations

### Learn More

* [Securing EIP-7702 Upgrades](https://blog.base.dev/securing-eip-7702-upgrades) — Blog post on the security model
* [EIP7702Proxy repository](https://github.com/base/eip-7702-proxy) — Contracts and deployments
* [Demo app](https://eip7702-viem-demo.vercel.app/) — Reference implementation on Base Sepolia

