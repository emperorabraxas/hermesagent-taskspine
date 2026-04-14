# Importing Accounts
Source: https://docs.cdp.coinbase.com/server-wallets/v2/using-the-wallet-api/import-accounts



## Overview

The CDP Server Wallet offers a secure method for creating EVM and Solana Accounts from imported private keys.

The import flow is end-to-end encrypted between the CDP SDK and the [TEE](/server-wallets/v2/introduction/security#tee-architecture), ensuring that keys are never exposed outside of the secure enclave during the request.
Encrypted by the SDK in a way that only the TEE can decrypt the keys, this process enables seamless and secure import of your keys.

## EVM Accounts: Import from external wallet providers

You can import private keys from other wallet providers by exporting them as raw, hex-encoded 32-byte strings.

To complete the import, use `importAccount` in TypeScript or `import_account` in the Python CDP SDK.
Only private key import is supported. To import an HD Wallet, derive individual private keys from the seed and import them one by one.

<CodeGroup>
  ```ts TypeScript lines wrap theme={null}
      import { CdpClient } from "@coinbase/cdp-sdk";
      import dotenv from "dotenv";

      dotenv.config();

      const cdp = new CdpClient();
      const account = await cdp.evm.importAccount({
          privateKey: "0x0123456789abcdef...",
          name: "ExternalWalletImportedAccount",
      });
      console.log("Imported account: ", account.address);
  ```

  ```python Python lines wrap theme={null}
      import asyncio
      from cdp import CdpClient
      from dotenv import load_dotenv

      load_dotenv()

      async def main():
          async with CdpClient() as cdp:
              account = await cdp.evm.import_account(
                  private_key="0x0123456789abcdef...",
                  name="ExternalWalletImportedAccount",
              )
              print("Imported account: ", account.address)

      asyncio.run(main())
  ```
</CodeGroup>

## Solana Accounts: Import from external wallet providers

Here's an example of how to import a Solana account with a base58-encoded private key from a wallet provider like Phantom.

<CodeGroup>
  ```ts TypeScript lines wrap theme={null}
      import { CdpClient } from "@coinbase/cdp-sdk";
      import dotenv from "dotenv";

      dotenv.config();

      const cdp = new CdpClient();
      const account = await cdp.solana.importAccount({
          privateKey: "4YFq9y5f5hi77Bq8kDCE6VgqoAq...",
          name: "ExternalWalletImportedAccount",
      });
      console.log("Imported account: ", account.address);
  ```

  ```python Python lines wrap theme={null}
      import asyncio
      from cdp import CdpClient
      from dotenv import load_dotenv

      load_dotenv()

      async def main():
          async with CdpClient() as cdp:
              account = await cdp.solana.import_account(
                  private_key="4YFq9y5f5hi77Bq8kDCE6VgqoAq...",
                  name="ExternalWalletImportedAccount",
              )
              print("Imported account: ", account.address)

      asyncio.run(main())
  ```
</CodeGroup>

You can also import a Solana account using the raw 32-byte private key array.

<CodeGroup>
  ```ts TypeScript lines wrap theme={null}
      import { CdpClient } from "@coinbase/cdp-sdk";
      import dotenv from "dotenv";

      dotenv.config();

      const keypair = Keypair.generate();
      const privateKeyBytes32 = keypair.secretKey.subarray(0, 32);

      const account = await cdp.solana.importAccount({
          privateKey: privateKeyBytes32,
          name: "BytesAccount32",
      });
      console.log("Imported account: ", account.address);
  ```

  ```python Python lines wrap theme={null}
      import asyncio
      from cdp import CdpClient
      from dotenv import load_dotenv

      load_dotenv()

      async def main():
          async with CdpClient() as cdp:
              keypair = Keypair.generate()
              private_key_bytes32 = keypair.secret_key[:32]

              account = await cdp.solana.import_account(
                  private_key=private_key_bytes32,
                  name="BytesAccount32",
              )
              print("Imported account: ", account.address)

      asyncio.run(main())
  ```
</CodeGroup>

## Video: Watch and learn

**Watch this video for a walkthrough of importing keys:**

<Frame>
  <iframe title="Importing Keys Walkthrough" />
</Frame>

## What to read next

* [**v2 Server Wallet Security**](/server-wallets/v2/introduction/security): Learn more about the security features of the CDP v2 Server Wallet.
* [**Policies**](/server-wallets/v2/using-the-wallet-api/policies/overview): Learn more about governing behavior of v2 accounts.
* [**Exporting Accounts**](/server-wallets/v2/using-the-wallet-api/export-accounts): Learn more about exporting EVM and Solana accounts.

