# Then start the development server
pnpm dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser.

## Tech Stack

The Mini App example uses:

* **Frontend**: Next.js 16, React 19, Tailwind CSS 4
* **Wallet**: OnchainKit 1.1.2, Wagmi
* **Payments**: x402 v2 SDK (`@x402/next`, `@x402/fetch`, `@x402/evm`)
* **Farcaster**: Mini App SDK for Mini App detection

## Environment Configuration

Create a `.env` file with the following variables:

```env theme={null}