# Exporting Accounts
Source: https://docs.cdp.coinbase.com/server-wallets/v2/using-the-wallet-api/export-accounts



## Overview

The CDP Server Wallet offers a secure method for exporting private keys of EVM and Solana accounts, that are compatible with all major wallet providers, such as Coinbase Wallet and Metamask.

The export API is end-to-end encrypted between the CDP SDK and the [TEE](/server-wallets/v2/introduction/security#tee-architecture), ensuring that keys are never exposed outside of the secure enclave while exporting. The private key is encrypted within the TEE by a single-use encryption key generated within the SDK.

<Warning>
  Exporting is a sensitive operation that puts your account's security and private keys at risk if not handled securely. It is important to store the private key in a secure place after it's exported.
</Warning>

## Exporting EVM accounts

Export private keys from your EVM accounts using either the account address or name.

<CodeGroup>
  ```typescript TypeScript theme={null}
  import { CdpClient } from "@coinbase/cdp-sdk";
  import dotenv from "dotenv";

  dotenv.config();

  const cdp = new CdpClient();
  const account = await cdp.evm.createAccount({
    name: "ExportEvmAccount",
  });
  console.log("Account to export:", account.address);

  // Export account with its address.
  let privateKey = await cdp.evm.exportAccount({
    address: account.address
  })

  // Export account with its name.
  privateKey = await cdp.evm.exportAccount({
    name: account.name
  })
  ```

  ```python Python theme={null}
  import asyncio
  from cdp import CdpClient
  from dotenv import load_dotenv

  load_dotenv()


  async def main():
      async with CdpClient() as cdp:
          account = await cdp.evm.create_account(
              name="ExportEvmAccount"
          )
          print("Account to export: ", account.address)

          # Export account with its address.
          private_key = await cdp.evm.export_account(
              address=account.address
          )

          # Export account with its name.
          private_key = await cdp.evm.export_account(
              name=account.name
          )

  asyncio.run(main())
  ```
</CodeGroup>

## Exporting Solana accounts

Export private keys from your Solana accounts using either the account address or name.

<CodeGroup>
  ```typescript TypeScript theme={null}
  import { CdpClient } from "@coinbase/cdp-sdk";
  import dotenv from "dotenv";

  dotenv.config();

  const cdp = new CdpClient();
  const account = await cdp.solana.createAccount({
    name: "ExportSolanaAccount",
  });
  console.log("Account to export: ", account.address);

  // Export account with its address.
  let privateKey = await cdp.solana.exportAccount({
    address: account.address
  })

  // Export account with its name.
  privateKey = await cdp.solana.exportAccount({
    name: account.name
  })
  ```

  ```python Python theme={null}
  import asyncio
  from cdp import CdpClient
  from dotenv import load_dotenv

  load_dotenv()


  async def main():
      async with CdpClient() as cdp:
          account = await cdp.solana.create_account(
              name="ExportSolanaAccount"
          )
          print("Account to export: ", account.address)

          # Export account with its address.
          private_key = await cdp.solana.export_account(
              address=account.address
          )

          # Export account with its name.
          private_key = await cdp.solana.export_account(
              name=account.name
          )

  asyncio.run(main())
  ```
</CodeGroup>

## API Key Configuration for Private Key Export

In order to programmatically export account private keys, you'll need to manually configure an API key with a specific scope.

When you're creating a new API Key, first expand the **API restrictions** panel then scroll down to the **API-specific restrictions** section.

Ensure that **Export (export private key)** is checked before key creation as seen in the following screenshot.

<Frame>
  <img alt="Export Scope" />
</Frame>

## What to read next

* [**v2 Wallet Security**](/server-wallets/v2/introduction/security): Learn more about the security features of the CDP v2 Server Wallet.
* [**Policies**](/server-wallets/v2/using-the-wallet-api/policies/overview): Learn more about governing behavior of v2 accounts.
* [**Importing Accounts**](/server-wallets/v2/using-the-wallet-api/import-accounts): Learn more about importing EVM accounts.

