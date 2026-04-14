# Embedded Wallet Pre-Generation
Source: https://docs.cdp.coinbase.com/embedded-wallets/wallet-pre-generation



<Tags />

## Overview

Pre-generate embedded wallets for your users before they sign in, enabling you to fund accounts with assets upfront for a seamless first-time experience.

<Info>
  **Supported authentication methods:** Wallet pre-generation currently supports **email**, **SMS**, and **Custom (JWT) authentication** only. Support for additional authentication methods is coming soon.
</Info>

## Why pre-generate wallets?

* **Pre-load assets**: Fund wallets with loyalty points, gas, or welcome NFTs before users sign in
* **Zero-friction onboarding**: Users see a ready-to-use wallet on first login instead of an empty account
* **Targeted campaigns**: Prepare wallets for specific users (by email, phone, or JWT) before launching marketing campaigns

## Prerequisites

Before pre-generating wallets, ensure you have:

1. **CDP API Key** - Create one in the [CDP Portal → API Keys](https://portal.cdp.coinbase.com/projects/api-keys)
2. **Wallet Secret** - Generate one in the [CDP Portal → Server Wallet → Accounts](https://portal.cdp.coinbase.com/products/server-wallets)
3. **CDP SDK** - Install the [CDP SDK](/sdks) in your project

<Warning>
  **Common mistake:** A standard CDP API key alone is not enough for wallet pre-generation. You must also generate a **Wallet Secret** from the Server Wallet section of the CDP Portal.
</Warning>

### Getting your credentials

<Steps>
  <Step title="Create a CDP API Key">
    1. Go to the [CDP Portal](https://portal.cdp.coinbase.com)
    2. Navigate to **API Keys** in the left sidebar
    3. Click **Create API Key** and save both the **Key ID** and **Key Secret**
  </Step>

  <Step title="Generate a Wallet Secret">
    1. In the CDP Portal, go to **Server Wallet** → **Accounts**
    2. Click **Generate** in the Wallet Secret section
    3. Save the secret securely - you won't be able to view it again
  </Step>

  <Step title="Configure your environment">
    Add both credentials to your `.env` file:

    ```bash theme={null}
    CDP_API_KEY_ID=your-api-key-id
    CDP_API_KEY_SECRET=your-api-key-secret
    CDP_WALLET_SECRET=your-wallet-secret
    ```
  </Step>
</Steps>

For more details, see the [Authentication documentation](/api-reference/v2/authentication) and [Wallet Secret documentation](/server-wallets/v2/introduction/security#wallet-secrets).

## Usage

Use the CDP SDK to create an end user with a specific authentication method. Once created, you can fund the wallet address before the user ever signs in.

### Creating an end user

The `createEndUser` method creates a new end user with an associated wallet. You specify the authentication method (email, SMS, or JWT) that the user will use to sign in later.

#### Email authentication

<Tabs>
  <Tab title="TypeScript">
    ```typescript theme={null}
    import { CdpClient } from "@coinbase/cdp-sdk";
    import "dotenv/config";

    const cdp = new CdpClient();

    try {
      // Create an end user with an email authentication method 
      // and both EVM and Solana accounts.
      const endUser = await cdp.endUser.createEndUser({
        authenticationMethods: [
          { type: "email", email: "user@example.com" }
        ],
        evmAccount: { createSmartAccount: false },
        solanaAccount: { createSmartAccount: false }
      });

      console.log("Created end user:", endUser);

      // The end user's wallet addresses are now available.
      // You can fund these addresses before the user signs in.
      console.log("EVM address:", endUser.evmAccounts?.[0]);
      console.log("Solana address:", endUser.solanaAccounts?.[0]);
    } catch (error) {
      console.error("Error creating end user:", error);
    }
    ```
  </Tab>

  <Tab title="Python">
    ```python theme={null}
    import asyncio

    from cdp import CdpClient
    from cdp.openapi_client.models.authentication_method import AuthenticationMethod
    from cdp.openapi_client.models.create_end_user_request_evm_account import (
        CreateEndUserRequestEvmAccount,
    )
    from cdp.openapi_client.models.create_end_user_request_solana_account import (
        CreateEndUserRequestSolanaAccount,
    )
    from cdp.openapi_client.models.email_authentication import EmailAuthentication
    from dotenv import load_dotenv

    load_dotenv()


    async def main():
        async with CdpClient() as cdp:
            try:
                # Create an end user with an email authentication method
                # and both EVM and Solana accounts.
                end_user = await cdp.end_user.create_end_user(
                    authentication_methods=[
                        AuthenticationMethod(EmailAuthentication(type="email", email="user@example.com"))
                    ],
                    evm_account=CreateEndUserRequestEvmAccount(create_smart_account=False),
                    solana_account=CreateEndUserRequestSolanaAccount(create_smart_account=False),
                )

                print("Created end user:", end_user)

                # The end user's wallet addresses are now available.
                # You can fund these addresses before the user signs in.

            except Exception as e:
                print(f"Error creating end user: {e}")
                raise e


    asyncio.run(main())
    ```
  </Tab>
</Tabs>

#### SMS authentication

<Tabs>
  <Tab title="TypeScript">
    ```typescript theme={null}
    import { CdpClient } from "@coinbase/cdp-sdk";
    import "dotenv/config";

    const cdp = new CdpClient();

    try {
      // Create an end user with an SMS authentication method
      // and both EVM and Solana accounts.
      const endUser = await cdp.endUser.createEndUser({
        authenticationMethods: [
          { type: "sms", phoneNumber: "+12055555555" }
        ],
        evmAccount: { createSmartAccount: false },
        solanaAccount: { createSmartAccount: false }
      });

      console.log("Created end user:", endUser);

      // The end user's wallet addresses are now available.
      // You can fund these addresses before the user signs in.
      console.log("EVM address:", endUser.evmAccounts?.[0]);
      console.log("Solana address:", endUser.solanaAccounts?.[0]);
    } catch (error) {
      console.error("Error creating end user:", error);
    }
    ```
  </Tab>

  <Tab title="Python">
    ```python theme={null}
    import asyncio

    from cdp import CdpClient
    from cdp.openapi_client.models.authentication_method import AuthenticationMethod
    from cdp.openapi_client.models.create_end_user_request_evm_account import (
        CreateEndUserRequestEvmAccount,
    )
    from cdp.openapi_client.models.create_end_user_request_solana_account import (
        CreateEndUserRequestSolanaAccount,
    )
    from cdp.openapi_client.models.sms_authentication import SmsAuthentication
    from dotenv import load_dotenv

    load_dotenv()


    async def main():
        async with CdpClient() as cdp:
            try:
                # Create an end user with an SMS authentication method
                # and both EVM and Solana accounts.
                end_user = await cdp.end_user.create_end_user(
                    authentication_methods=[
                        AuthenticationMethod(SmsAuthentication(type="sms", phone_number="+12055555555"))
                    ],
                    evm_account=CreateEndUserRequestEvmAccount(create_smart_account=False),
                    solana_account=CreateEndUserRequestSolanaAccount(create_smart_account=False),
                )

                print("Created end user:", end_user)

                # The end user's wallet addresses are now available.
                # You can fund these addresses before the user signs in.

            except Exception as e:
                print(f"Error creating end user: {e}")
                raise e


    asyncio.run(main())
    ```
  </Tab>
</Tabs>

#### Custom (JWT) Authentication

<Tabs>
  <Tab title="TypeScript">
    ```typescript theme={null}
    import { CdpClient } from "@coinbase/cdp-sdk";
    import "dotenv/config";

    const cdp = new CdpClient();

    try {
      // Create an end user with a JWT authentication method
      // and both EVM and Solana accounts.
      const endUser = await cdp.endUser.createEndUser({
        authenticationMethods: [
          { type: "jwt", sub: "auth0|69387f18541e0e673845c6b6", kid: "1234567890" }
        ],
        evmAccount: { createSmartAccount: false },
        solanaAccount: { createSmartAccount: false }
      });

      console.log("Created end user:", endUser);

      // The end user's wallet addresses are now available.
      // You can fund these addresses before the user signs in.
      console.log("EVM address:", endUser.evmAccounts?.[0]);
      console.log("Solana address:", endUser.solanaAccounts?.[0]);
    } catch (error) {
      console.error("Error creating end user:", error);
    }
    ```
  </Tab>

  <Tab title="Python">
    ```python theme={null}
    import asyncio

    from cdp import CdpClient
    from cdp.openapi_client.models.authentication_method import AuthenticationMethod
    from cdp.openapi_client.models.create_end_user_request_evm_account import (
        CreateEndUserRequestEvmAccount,
    )
    from cdp.openapi_client.models.create_end_user_request_solana_account import (
        CreateEndUserRequestSolanaAccount,
    )
    from cdp.openapi_client.models.developer_jwt_authentication import DeveloperJWTAuthentication
    from dotenv import load_dotenv

    load_dotenv()


    async def main():
        async with CdpClient() as cdp:
            try:
                # Create an end user with a JWT authentication method
                # and both EVM and Solana accounts.
                end_user = await cdp.end_user.create_end_user(
                    authentication_methods=[
                        AuthenticationMethod(DeveloperJWTAuthentication(type="jwt", sub="auth0|69387f18541e0e673845c6b6", kid="1234567890"))
                    ],
                    evm_account=CreateEndUserRequestEvmAccount(create_smart_account=False),
                    solana_account=CreateEndUserRequestSolanaAccount(create_smart_account=False),
                )

                print("Created end user:", end_user)

                # The end user's wallet addresses are now available.
                # You can fund these addresses before the user signs in.

            except Exception as e:
                print(f"Error creating end user: {e}")
                raise e


    asyncio.run(main())
    ```
  </Tab>
</Tabs>

<Tip>
  The `sub` value you use must match the `sub` claim in the JWTs your identity provider issues for this user.
</Tip>

### Pre-generate wallet with an existing private key

If you already have access to your end users' private keys, you can import them directly into Embedded Wallets. This is useful when migrating users from other wallet solutions—such as [Server Wallets](/server-wallets/v2/introduction/welcome)—to Embedded Wallets.

<Info>
  **When to use import:** Use this method when you have existing private keys for your users and want to preserve their wallet addresses during migration. The import flow is end-to-end encrypted, ensuring keys are never exposed outside of the SDK and the secure enclave.
</Info>

<Note>
  The import API supports both EVM and Solana key types. Set `keyType` to either `"evm"` (hex-encoded private key) or `"solana"` (base58-encoded private key).
</Note>

#### Email authentication

<Tabs>
  <Tab title="TypeScript">
    ```typescript theme={null}
    import { CdpClient } from "@coinbase/cdp-sdk";
    import "dotenv/config";

    const cdp = new CdpClient();

    try {
      // Import an end user with an existing private key.
      // For Solana: use keyType: "solana" with a base58-encoded private key.
      const endUser = await cdp.endUser.importEndUser({
        authenticationMethods: [
          { type: "email", email: "user@example.com" }
        ],
        privateKey: "0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
        keyType: "evm",
      });

      console.log("Imported end user:", endUser);
      console.log("EVM accounts:", endUser.evmAccountObjects);
    } catch (error) {
      console.error("Error importing end user:", error);
    }
    ```
  </Tab>

  <Tab title="Python">
    ```python theme={null}
    import asyncio

    from cdp import CdpClient
    from cdp.openapi_client.models.authentication_method import AuthenticationMethod
    from cdp.openapi_client.models.email_authentication import EmailAuthentication
    from dotenv import load_dotenv

    load_dotenv()


    async def main():
        async with CdpClient() as cdp:
            try:
                # Import an end user with an existing private key.
                # For Solana: use key_type="solana" with a base58-encoded private key.
                end_user = await cdp.end_user.import_end_user(
                    authentication_methods=[
                        AuthenticationMethod(EmailAuthentication(type="email", email="user@example.com"))
                    ],
                    private_key="0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
                    key_type="evm",
                )

                print("Imported end user:", end_user)
                print("EVM accounts:", end_user.evm_account_objects)

            except Exception as e:
                print(f"Error importing end user: {e}")
                raise e


    asyncio.run(main())
    ```
  </Tab>
</Tabs>

#### SMS authentication

<Tabs>
  <Tab title="TypeScript">
    ```typescript theme={null}
    import { CdpClient } from "@coinbase/cdp-sdk";
    import "dotenv/config";

    const cdp = new CdpClient();

    try {
      // Import an end user with an existing private key.
      // For Solana: use keyType: "solana" with a base58-encoded private key.
      const endUser = await cdp.endUser.importEndUser({
        authenticationMethods: [
          { type: "sms", phoneNumber: "+12055555555" }
        ],
        privateKey: "0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
        keyType: "evm",
      });

      console.log("Imported end user:", endUser);
      console.log("EVM accounts:", endUser.evmAccountObjects);
    } catch (error) {
      console.error("Error importing end user:", error);
    }
    ```
  </Tab>

  <Tab title="Python">
    ```python theme={null}
    import asyncio

    from cdp import CdpClient
    from cdp.openapi_client.models.authentication_method import AuthenticationMethod
    from cdp.openapi_client.models.sms_authentication import SmsAuthentication
    from dotenv import load_dotenv

    load_dotenv()


    async def main():
        async with CdpClient() as cdp:
            try:
                # Import an end user with an existing private key.
                # For Solana: use key_type="solana" with a base58-encoded private key.
                end_user = await cdp.end_user.import_end_user(
                    authentication_methods=[
                        AuthenticationMethod(SmsAuthentication(type="sms", phone_number="+12055555555"))
                    ],
                    private_key="0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
                    key_type="evm",
                )

                print("Imported end user:", end_user)
                print("EVM accounts:", end_user.evm_account_objects)

            except Exception as e:
                print(f"Error importing end user: {e}")
                raise e


    asyncio.run(main())
    ```
  </Tab>
</Tabs>

#### Custom (JWT) authentication

<Tabs>
  <Tab title="TypeScript">
    ```typescript theme={null}
    import { CdpClient } from "@coinbase/cdp-sdk";
    import "dotenv/config";

    const cdp = new CdpClient();

    try {
      // Import an end user with an existing private key.
      // For Solana: use keyType: "solana" with a base58-encoded private key.
      const endUser = await cdp.endUser.importEndUser({
        authenticationMethods: [
          { type: "jwt", sub: "auth0|69387f18541e0e673845c6b6", kid: "1234567890" }
        ],
        privateKey: "0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
        keyType: "evm",
      });

      console.log("Imported end user:", endUser);
      console.log("EVM accounts:", endUser.evmAccountObjects);
    } catch (error) {
      console.error("Error importing end user:", error);
    }
    ```
  </Tab>

  <Tab title="Python">
    ```python theme={null}
    import asyncio

    from cdp import CdpClient
    from cdp.openapi_client.models.authentication_method import AuthenticationMethod
    from cdp.openapi_client.models.developer_jwt_authentication import DeveloperJWTAuthentication
    from dotenv import load_dotenv

    load_dotenv()


    async def main():
        async with CdpClient() as cdp:
            try:
                # Import an end user with an existing private key.
                # For Solana: use key_type="solana" with a base58-encoded private key.
                end_user = await cdp.end_user.import_end_user(
                    authentication_methods=[
                        AuthenticationMethod(DeveloperJWTAuthentication(type="jwt", sub="auth0|69387f18541e0e673845c6b6", kid="1234567890"))
                    ],
                    private_key="0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
                    key_type="evm",
                )

                print("Imported end user:", end_user)
                print("EVM accounts:", end_user.evm_account_objects)

            except Exception as e:
                print(f"Error importing end user: {e}")
                raise e


    asyncio.run(main())
    ```
  </Tab>
</Tabs>

<Warning>
  **Security:** Private keys should be handled with extreme care. Ensure you transmit keys securely and never log or expose them in your application. The import flow uses end-to-end encryption to protect keys during transmission.
</Warning>

## Account Configuration

By default, pre-generated wallets are created as EOA (Externally Owned Accounts). You can configure the account type and features using the `evmAccount` and `solanaAccount` parameters.

<Note>
  Smart accounts are only supported for EVM. Solana accounts must have `createSmartAccount` set to `false`.
</Note>

### Smart Accounts

Create an EVM smart account instead of an EOA by setting `createSmartAccount: true`.

<Tabs>
  <Tab title="TypeScript">
    ```typescript theme={null}
    import { CdpClient } from "@coinbase/cdp-sdk";
    import "dotenv/config";

    const cdp = new CdpClient();

    try {
      const endUser = await cdp.endUser.createEndUser({
        authenticationMethods: [
          { type: "email", email: "user@example.com" }
        ],
        evmAccount: { createSmartAccount: true },
        solanaAccount: { createSmartAccount: false }
      });

      console.log("Created end user with smart account:", endUser);
      
      // Access the smart account object
      const smartAccount = endUser.evmSmartAccountObjects?.[0];
      console.log("Smart account address:", smartAccount?.address);
      console.log("Owner addresses:", smartAccount?.ownerAddresses);
      console.log("Solana address:", endUser.solanaAccounts?.[0]);
    } catch (error) {
      console.error("Error creating end user:", error);
    }
    ```
  </Tab>

  <Tab title="Python">
    ```python theme={null}
    import asyncio

    from cdp import CdpClient
    from cdp.openapi_client.models.authentication_method import AuthenticationMethod
    from cdp.openapi_client.models.create_end_user_request_evm_account import (
        CreateEndUserRequestEvmAccount,
    )
    from cdp.openapi_client.models.create_end_user_request_solana_account import (
        CreateEndUserRequestSolanaAccount,
    )
    from cdp.openapi_client.models.email_authentication import EmailAuthentication
    from dotenv import load_dotenv

    load_dotenv()


    async def main():
        async with CdpClient() as cdp:
            try:
                end_user = await cdp.end_user.create_end_user(
                    authentication_methods=[
                        AuthenticationMethod(EmailAuthentication(type="email", email="user@example.com"))
                    ],
                    evm_account=CreateEndUserRequestEvmAccount(create_smart_account=True),
                    solana_account=CreateEndUserRequestSolanaAccount(create_smart_account=False),
                )

                print("Created end user with smart account:", end_user)
                
                smart_account = end_user.evm_smart_account_objects[0]
                print(f"Smart account address: {smart_account.address}")
                print(f"Owner addresses: {smart_account.owner_addresses}")
                print(f"Solana address: {end_user.solana_accounts[0]}")

            except Exception as e:
                print(f"Error creating end user: {e}")
                raise e


    asyncio.run(main())
    ```
  </Tab>
</Tabs>

<Info>
  Spend permissions allow you to grant allowances to specific addresses, enabling delegated transactions without requiring user signatures for each action. Learn more in the [Spend Permissions documentation](/embedded-wallets/evm-features/spend-permissions).
</Info>

### Spend Permissions

Enable spend permissions on an EVM smart account by setting `enableSpendPermissions: true`. This requires `createSmartAccount: true`.

<Tabs>
  <Tab title="TypeScript">
    ```typescript theme={null}
    import { CdpClient } from "@coinbase/cdp-sdk";
    import "dotenv/config";

    const cdp = new CdpClient();

    try {
      const endUser = await cdp.endUser.createEndUser({
        authenticationMethods: [
          { type: "email", email: "user@example.com" }
        ],
        evmAccount: { 
          createSmartAccount: true,
          enableSpendPermissions: true
        },
        solanaAccount: { createSmartAccount: false }
      });

      console.log("Created end user with spend permissions:", endUser);
      
      const smartAccount = endUser.evmSmartAccountObjects?.[0];
      console.log("Smart account address:", smartAccount?.address);
      
      // When spend permissions are enabled, there are 2 owner addresses:
      // 1. User's owner address
      // 2. Spend Permission Manager address
      console.log("Owner addresses:", smartAccount?.ownerAddresses);
      console.log("Solana address:", endUser.solanaAccounts?.[0]);
    } catch (error) {
      console.error("Error creating end user:", error);
    }
    ```
  </Tab>

  <Tab title="Python">
    ```python theme={null}
    import asyncio

    from cdp import CdpClient
    from cdp.openapi_client.models.authentication_method import AuthenticationMethod
    from cdp.openapi_client.models.create_end_user_request_evm_account import (
        CreateEndUserRequestEvmAccount,
    )
    from cdp.openapi_client.models.create_end_user_request_solana_account import (
        CreateEndUserRequestSolanaAccount,
    )
    from cdp.openapi_client.models.email_authentication import EmailAuthentication
    from dotenv import load_dotenv

    load_dotenv()


    async def main():
        async with CdpClient() as cdp:
            try:
                end_user = await cdp.end_user.create_end_user(
                    authentication_methods=[
                        AuthenticationMethod(EmailAuthentication(type="email", email="user@example.com"))
                    ],
                    evm_account=CreateEndUserRequestEvmAccount(
                        create_smart_account=True, 
                        enable_spend_permissions=True
                    ),
                    solana_account=CreateEndUserRequestSolanaAccount(create_smart_account=False),
                )

                print("Created end user with spend permissions:", end_user)
                
                smart_account = end_user.evm_smart_account_objects[0]
                print(f"Smart account address: {smart_account.address}")
                
                # When spend permissions are enabled, there are 2 owner addresses:
                # 1. User's owner address
                # 2. Spend Permission Manager address
                print(f"Owner addresses: {smart_account.owner_addresses}")
                print(f"Solana address: {end_user.solana_accounts[0]}")

            except Exception as e:
                print(f"Error creating end user: {e}")
                raise e


    asyncio.run(main())
    ```
  </Tab>
</Tabs>

## Adding Accounts to Existing End Users

After creating an end user, you can add additional accounts directly on the `EndUser` object. Each end user can have up to 10 EVM EOA accounts, 10 EVM smart accounts, and 10 Solana accounts.

<Tabs>
  <Tab title="TypeScript">
    ```typescript theme={null}
    import { CdpClient } from "@coinbase/cdp-sdk";
    import "dotenv/config";

    const cdp = new CdpClient();

    try {
      // Create an end user
      const endUser = await cdp.endUser.createEndUser({
        authenticationMethods: [
          { type: "email", email: "user@example.com" }
        ]
      });

      // Add an EVM EOA account
      const evmResult = await endUser.addEvmAccount();
      console.log("EVM account address:", evmResult.evmAccount.address);

      // Add an EVM smart account
      const smartResult = await endUser.addEvmSmartAccount({
        enableSpendPermissions: false
      });
      console.log("Smart account address:", smartResult.evmSmartAccount.address);

      // Add a Solana account
      const solanaResult = await endUser.addSolanaAccount();
      console.log("Solana account address:", solanaResult.solanaAccount.address);
    } catch (error) {
      console.error("Error adding accounts:", error);
    }
    ```
  </Tab>

  <Tab title="Python">
    ```python theme={null}
    import asyncio

    from cdp import CdpClient
    from cdp.openapi_client.models.authentication_method import AuthenticationMethod
    from cdp.openapi_client.models.email_authentication import EmailAuthentication
    from dotenv import load_dotenv

    load_dotenv()


    async def main():
        async with CdpClient() as cdp:
            try:
                # Create an end user
                end_user = await cdp.end_user.create_end_user(
                    authentication_methods=[
                        AuthenticationMethod(EmailAuthentication(type="email", email="user@example.com"))
                    ]
                )

                # Add an EVM EOA account
                evm_result = await end_user.add_evm_account()
                print(f"EVM account address: {evm_result.evm_account.address}")

                # Add an EVM smart account
                smart_result = await end_user.add_evm_smart_account(
                    enable_spend_permissions=False
                )
                print(f"Smart account address: {smart_result.evm_smart_account.address}")

                # Add a Solana account
                solana_result = await end_user.add_solana_account()
                print(f"Solana account address: {solana_result.solana_account.address}")

            except Exception as e:
                print(f"Error adding accounts: {e}")
                raise e


    asyncio.run(main())
    ```
  </Tab>
</Tabs>

<Info>
  When adding an EVM smart account, an owner EOA is automatically created to control the smart account.
</Info>

### Using client methods

You can also add accounts using the client methods directly by providing the end user's ID:

<Tabs>
  <Tab title="TypeScript">
    ```typescript theme={null}
    // Add accounts via client methods
    const evmResult = await cdp.endUser.addEndUserEvmAccount({
      userId: endUser.id
    });

    const smartResult = await cdp.endUser.addEndUserEvmSmartAccount({
      userId: endUser.id,
      enableSpendPermissions: false
    });

    const solanaResult = await cdp.endUser.addEndUserSolanaAccount({
      userId: endUser.id
    });
    ```
  </Tab>

  <Tab title="Python">
    ```python theme={null}
    # Add accounts via client methods
    evm_result = await cdp.end_user.add_end_user_evm_account(
        user_id=end_user.id
    )

    smart_result = await cdp.end_user.add_end_user_evm_smart_account(
        user_id=end_user.id,
        enable_spend_permissions=False
    )

    solana_result = await cdp.end_user.add_end_user_solana_account(
        user_id=end_user.id
    )
    ```
  </Tab>
</Tabs>

## What to read next

<CardGroup>
  <Card title="Authentication Methods" icon="key" href="/embedded-wallets/authentication-methods">
    Learn about email OTP, SMS OTP, and social login options
  </Card>

  <Card title="Implementation Guide" icon="code" href="/embedded-wallets/implementation-guide">
    Integrate authentication into your frontend application
  </Card>

  <Card title="Quickstart" icon="rocket" href="/embedded-wallets/quickstart">
    Get started with embedded wallets in your React app
  </Card>

  <Card title="CDP SDK Reference" icon="book" href="/sdks">
    Explore the full SDK documentation
  </Card>
</CardGroup>

