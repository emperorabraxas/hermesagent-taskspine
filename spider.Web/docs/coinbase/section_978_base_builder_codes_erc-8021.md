# Base Builder Codes (ERC-8021)
Source: https://docs.cdp.coinbase.com/embedded-wallets/evm-features/builder-codes



## Overview

[Base Builder Codes](https://docs.base.org/base-chain/builder-codes/builder-codes) are unique identifiers that attribute onchain activity, such as transactions and user operations, back to your app. They're built on [ERC-8021](https://eip.tools/eip/8021), a standard for appending a small attribution suffix to transaction calldata. Indexers on Base read the suffix to credit your app with the activity it generates.

CDP Embedded Wallets support Builder Codes natively via the `dataSuffix` parameter on `sendUserOperation`. No contract changes are needed; the suffix is appended to the `callData` of each user operation and is invisible to smart contract execution.

<Tip>
  If you're new to Embedded Wallets, start with the [Quickstart](/embedded-wallets/quickstart) and [React Hooks](/embedded-wallets/react-hooks) first.
</Tip>

## Benefits

* **Rewards:** Builder Codes let Base automatically attribute onchain usage back to your app, unlocking rewards as the program expands.
* **Analytics:** Track onchain activity, user acquisition, and conversion metrics at [base.dev](https://base.dev).
* **Visibility:** Apps with Builder Codes can appear in discovery surfaces like App Leaderboards, the Base App store, and ecosystem spotlights.

## Prerequisites

* A Builder Code from [base.dev](https://base.dev/) (register, then find your code under **Settings → Builder Code**)
* `@coinbase/cdp-core`, `@coinbase/cdp-hooks`, and `ox` installed

```bash theme={null}
npm install @coinbase/cdp-core @coinbase/cdp-hooks ox
```

## Generate your attribution suffix

Use the `ox/erc8021` package to convert your Builder Code into the hex-encoded suffix that gets appended to transactions. Do this once at module level, and reuse it across all your calls.

```ts theme={null}
import { Attribution } from "ox/erc8021";

// Replace with your code from base.dev > Settings > Builder Code
const DATA_SUFFIX = Attribution.toDataSuffix({
  codes: ["YOUR-BUILDER-CODE"],
});
```

## Add Builder Codes to user operations

Pass `dataSuffix` to `sendUserOperation` (or `useSendUserOperation`). The SDK appends the suffix to the user operation's `callData` before it's signed and submitted.

### React hook

```tsx theme={null}
import { Attribution } from "ox/erc8021";
import { useSendUserOperation, useCurrentUser } from "@coinbase/cdp-hooks";

const DATA_SUFFIX = Attribution.toDataSuffix({
  codes: ["YOUR-BUILDER-CODE"],
});

function SendWithAttribution() {
  const { sendUserOperation, data, isError, error } = useSendUserOperation();
  const { currentUser } = useCurrentUser();

  const handleSend = async () => {
    const smartAccount = currentUser?.evmSmartAccounts?.[0];
    if (!smartAccount) return;

    await sendUserOperation({
      evmAccount: smartAccount,
      network: "base",
      calls: [
        {
          to: "0xYourContractAddress",
          value: "0x0",
          data: "0xYourCalldata",
        },
      ],
      dataSuffix: DATA_SUFFIX,
    });
  };

  return (
    <div>
      {isError && <p>Error: {error?.message}</p>}
      {data && <p>Transaction hash: {data.transactionHash}</p>}
      <button onClick={handleSend}>Send</button>
    </div>
  );
}
```

### Core SDK (non-React)

```ts theme={null}
import { Attribution } from "ox/erc8021";
import { sendUserOperation } from "@coinbase/cdp-core";

const DATA_SUFFIX = Attribution.toDataSuffix({
  codes: ["YOUR-BUILDER-CODE"],
});

const result = await sendUserOperation({
  evmAccount: smartAccount,
  network: "base",
  calls: [
    {
      to: "0xYourContractAddress",
      value: "0x0",
      data: "0xYourCalldata",
    },
  ],
  dataSuffix: DATA_SUFFIX,
});

console.log("User operation hash:", result.userOperationHash);
```

### Parameters

| Parameter    | Type          | Description                                                                                                                           |
| ------------ | ------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| `dataSuffix` | `0x${string}` | Hex-encoded ERC-8021 attribution suffix generated from your Builder Code. Generate with `Attribution.toDataSuffix` from `ox/erc8021`. |

## Full end-to-end example

<Accordion title="Complete example with wallet setup">
  ```tsx theme={null}
  import { Attribution } from "ox/erc8021";
  import {
    useSendUserOperation,
    useCurrentUser,
    useCreateEvmSmartAccount,
  } from "@coinbase/cdp-hooks";

  const DATA_SUFFIX = Attribution.toDataSuffix({
    codes: ["YOUR-BUILDER-CODE"],
  });

  function App() {
    const { currentUser } = useCurrentUser();
    const { createEvmSmartAccount } = useCreateEvmSmartAccount();
    const { sendUserOperation, data, isError, error } = useSendUserOperation();

    const handleSend = async () => {
      // Ensure the user has a smart account
      let smartAccount = currentUser?.evmSmartAccounts?.[0];
      if (!smartAccount) {
        smartAccount = await createEvmSmartAccount({ network: "base" });
      }

      await sendUserOperation({
        evmAccount: smartAccount,
        network: "base",
        calls: [
          {
            to: "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
            value: "0x0",
            data: "0x",
          },
        ],
        dataSuffix: DATA_SUFFIX,
      });
    };

    return (
      <div>
        {isError && <p>Error: {error?.message}</p>}
        {data && (
          <div>
            <p>Attributed successfully!</p>
            <p>Transaction hash: {data.transactionHash}</p>
          </div>
        )}
        <button onClick={handleSend}>Send attributed transaction</button>
      </div>
    );
  }
  ```
</Accordion>

## Verify attribution

After sending a transaction, confirm your Builder Code is being attributed correctly using any of the following methods.

**1. Check base.dev**

* Visit [base.dev](https://base.dev)
* Select **Onchain** from the transaction type dropdown
* Attribution counts increment as transactions with your code are processed

**2. Use a block explorer (Basescan, Etherscan)**

* Find your transaction hash
* View the input data field
* Verify the last 16 bytes contain the `8021` repeating pattern
* Decode the suffix to confirm your Builder Code is present

**3. Open source validation tool**

* Use the [Builder Code Validation Tool](https://builder-code-checker.vercel.app/)
* Select transaction type and enter the transaction or UserOperation hash
* Click **Check Attribution**

## FAQ

### Do I need to modify my smart contracts?

**No.** The attribution suffix is appended to the end of `callData`. Smart contracts execute normally and ignore the extra bytes. Attribution is extracted by offchain indexers after the fact. Any existing contract automatically supports ERC-8021 with no upgrades or re-deployments required.

### How much additional gas do Builder Codes cost?

The ERC-8021 suffix adds a negligible amount of gas (16 gas per non-zero byte appended).

### Does this work with EOAs too?

**Yes.** ERC-8021 works with both EOAs and smart contract wallets. For EOA transactions (not user operations), the suffix is appended to `tx.data` instead of `userOp.callData`. See the [For App Developers](https://docs.base.org/base-chain/builder-codes/app-developers) guide on Base docs for EOA-specific setup using Wagmi or Viem.

### Will Builder Codes expose my users' identities?

**No.** Builder Codes associate transactions with your application only; they don't expose any wallet information that isn't already public onchain.

## Additional resources

* [Base Builder Codes overview](https://docs.base.org/base-chain/builder-codes/builder-codes) — full program details, rewards, and FAQ
* [ERC-8021 specification](https://eip.tools/eip/8021)
* [Builder Code Validation Tool](https://builder-code-checker.vercel.app/)
* [ox/erc8021 package docs](https://oxlib.sh/api/erc8021/Attribution)
* [Register for a Builder Code](https://base.dev/)

<Note>
  Have questions or feedback? Join the discussion in the [Coinbase Developer Discord](https://discord.com/invite/cdp).
</Note>

