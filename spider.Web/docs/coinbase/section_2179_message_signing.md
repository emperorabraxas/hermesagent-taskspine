# Message Signing
Source: https://docs.cdp.coinbase.com/server-wallets/v2/solana-features/message-signing



## Overview

Message signing allows you to apply a unique cryptographic signature to messages, ensuring authenticity and integrity.
This is particularly useful for verifying ownership of accounts or authorizing actions without sending a transaction.

Using the [CDP-SDK](https://github.com/coinbase/cdp-sdk), developers can sign messages for Solana.

In this guide, you will learn how to:

* Sign a message using the CDP v2 Server Wallet

## Prerequisites

It is assumed you have already completed the [Quickstart](/server-wallets/v2/introduction/quickstart) guide.

## Sign message

Input a message to sign. The CDP v2 Server Wallet will return a signature that can be used to verify the message.

<CodeGroup>
  ```typescript TypeScript theme={null}
  import { CdpClient } from "@coinbase/cdp-sdk";
  import "dotenv/config";

  const cdp = new CdpClient();

  const account = await cdp.solana.getOrCreateAccount({ name: "MyAccount" });
  const { signature } = await account.signMessage({
    message: "Hello, world!",
  });

  console.log(
    `Signed message: ${signature}`
  );
  ```

  ```python Python theme={null}
  import asyncio
  from cdp import CdpClient
  from dotenv import load_dotenv

  load_dotenv()


  async def main():
      async with CdpClient() as cdp:
          account = await cdp.solana.create_account()
          response = await account.sign_message(message="Hello, world!")
          print(response)


  asyncio.run(main())
  ```
</CodeGroup>

