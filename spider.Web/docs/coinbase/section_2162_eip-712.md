# EIP-712
Source: https://docs.cdp.coinbase.com/server-wallets/v2/evm-features/eip-712-signing



## Overview

EIP-712 message signing allows you to sign structured data using a human-readable format.

Using the [CDP-SDK](https://github.com/coinbase/cdp-sdk), developers can enable signing while presenting clear, meaningful messages to users, rather than unintelligible raw hexadecimal hashes.

In this guide, you will learn how to:

* Create an EVM account
* Sign an EIP-712 message

## Prerequisites

It is assumed you have already completed the [Quickstart](/server-wallets/v2/introduction/quickstart) guide.

## 1. Create an account

To create an account, see below:

<CodeGroup>
  ```ts main.ts lines wrap  theme={null}
  import { CdpClient } from "@coinbase/cdp-sdk";  
  import "dotenv/config";  
    
  const cdp = new CdpClient();  
    
  const account = await cdp.evm.createAccount();  
    
  console.log("Successfully created account: ", account.address);  
  ```

  ```python main.py lines wrap  theme={null}
  import asyncio
  from cdp import CdpClient
  import dotenv
    
  dotenv.load_dotenv()
    
  async def main():
      cdp = CdpClient()
    
      account = await cdp.evm.create_account()
      print(f"Successfully created account: {account.address}")
    
      await cdp.close()
    
    
  asyncio.run(main())
  ```
</CodeGroup>

After running the above snippet, you should see output similar to the following:

```
Successfully created account: 0x6aAEc7535706ce8B36ea184B2236D53702c1F06A
```

## 2. Sign message

The v2 Server Wallet supports [EIP-712](/api-reference/v2/rest-api/evm-accounts/sign-eip-712-typed-data) for typed structured data hashing and signing, providing a way to create human-readable messages that can be signed and verified onchain.

<Accordion title="Expand to learn more about EIP-712 components">
  ### Domain Separator

  The domain separator is a unique identifier for the application or protocol. It helps prevent signature collisions between different applications.

  It typically includes:

  * `name`: the name of the application (e.g., "MyApp")
  * `chainId`: the network ID where the signature will be verified (e.g., 1 for Ethereum mainnet)
  * `verifyingContract`: the address of the contract that will verify the signature

  ### Type Definitions

  Type definitions describe the structure of your message. They include the required `EIP712Domain` type and your custom types. Each custom type is defined as an array of fields, where each field has a name and type.

  * EIP712Domain: required base type that defines the domain structure
    * `name` (string)
    * `version` (string)
    * `chainId` (uint256)
    * `verifyingContract` (address)
    * `salt` (bytes32)
  * Custom Types: your application-specific types (e.g., "Person")
    * Each field has a name and type
    * Can include nested types
    * Must be properly defined before use

  ### Primary Type

  The primary type is the main type of the message you're signing. It should be one of the types defined in your type definitions.

  ### Message

  The message contains the actual data you want to sign. It must match the structure defined by your primary type.
</Accordion>

Here is a complete example showing how to sign EIP-712 typed data:

<CodeGroup>
  ```ts main.ts lines wrap [expandable] theme={null}
  import { CdpClient } from "@coinbase/cdp-sdk";
  import "dotenv/config";
    
  const cdp = new CdpClient();
    
  const account = await cdp.evm.createAccount();
  console.log("Created account:", account.address);
    
  const signature = await cdp.evm.signTypedData({
    address: account.address,
    domain: {
      name: "MyApp",
      chainId: 1,
      verifyingContract: "0x0000000000000000000000000000000000000000",
    },
    types: {
      EIP712Domain: [
        { name: "name", type: "string" },
        { name: "chainId", type: "uint256" },
        { name: "verifyingContract", type: "address" },
      ],
      Person: [
        { name: "name", type: "string" },
        { name: "age", type: "uint256" }
      ]
    },
    primaryType: "Person",
    message: {
      name: "Alice",
      age: 25
    },
  });

  console.log("Signature:", signature);  
  ```

  ```python main.py lines wrap [expandable] theme={null}
  import asyncio
    
  from cdp import CdpClient
  from cdp.evm_message_types import EIP712Domain
    
  from dotenv import load_dotenv
    
  load_dotenv()
    
  async def main():
      cdp = CdpClient()
    
      account = await cdp.evm.create_account()
      print(f"Created account: {account.address}")
    
      signature = await cdp.evm.sign_typed_data(
          address=account.address,
          domain=EIP712Domain(
              name="EIP712Domain",
              chain_id=1,
              verifying_contract="0x0000000000000000000000000000000000000000",
          ).as_dict(),
          types={
              "EIP712Domain": [
                  {"name": "name", "type": "string"},
                  {"name": "chainId", "type": "uint256"},
                  {"name": "verifyingContract", "type": "address"},
              ],
              "Person": [
                  {"name": "name", "type": "string"},
                  {"name": "age", "type": "uint256"}
              ]
          },
          primary_type="Person",
          message={
            "name": "Alice",
            "age": 25
          },
      )
      print("Signature: ", signature)
    
      await cdp.close()
    
    
  asyncio.run(main())
  ```
</CodeGroup>

After running the above snippet, you should see output similar to the following:

```
Created account: 0x2Ae896e791c9596c7beDeCC3E06Fa6DA9aE2B193  
Signature:  0xa8fdc11edcf120b116d34131159ca356af52b90732425ebec48cac125a449e7d2151d97ca8232bff43568da9ee2249cf1bc187c392f1d1e53c72fc0b5937f5b31b    
```

To summarize, in the example above, we:

* Created an EVM account
* Signed a message using EIP-712 structured data, which includes: a domain separator, type definitions, primary type, and a message payload (a person named Alice who is 25 years old)

The EIP-712 structured data was used to create a human-readable message which we successfully signed cryptographically.

## Video: Watch and learn

**Watch this video for a walkthrough of EIP-712 message signing:**

<Frame>
  <iframe title="EIP-712 Message Signing Walkthrough" />
</Frame>

## What to read next

* [**v2 Security**](/server-wallets/v2/introduction/security): Learn about the security features of v2 Server Wallet.
* [**API Reference**](/api-reference/v2/introduction): Explore the complete API reference for v2 Server Wallet.

