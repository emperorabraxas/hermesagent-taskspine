# Spend Permissions
Source: https://docs.cdp.coinbase.com/server-wallets/v2/evm-features/spend-permissions



## Overview

Spend Permissions let you designate a trusted spender that can spend tokens on behalf of your [Smart Account](/server-wallets/v2/evm-features/smart-accounts). After you sign the permission, the spender can initiate token spending within the limits you define. You can define limits based on token, time period and amount.

<Warning>
  Smart Accounts must have spend permissions enabled at the time of creation. You cannot create spend permissions on accounts that were created without spend permissions enabled.
</Warning>

Spend Permissions utilize the [Spend Permission Manager contract](https://github.com/coinbase/spend-permissions) deployed on Base and [other networks](/server-wallets/v2/evm-features/spend-permissions#supported-networks).

Some use cases this feature enables:

* **Subscription payments** - Enable recurring payments for SaaS, content subscriptions, or membership fees
* **Agentic payments** - Control your agent's spending limits for autonomous operations
* **Algorithmic trading** - Allow trading bots to execute trades within predefined limits
* **Automated payouts** - Schedule regular distributions or reward payments
* **Allowance management** - Give team members or family controlled access to funds
* **Dollar-cost averaging** - Automate periodic investment purchases

## How Spend Permissions Work

There are two parties involved in a Spend Permission:

* **Account** - The smart account that creates the Spend Permission and approves it onchain.
* **Spender** - The entity that can spend tokens on behalf of the account within the limits defined by a Spend Permission. Can be a Smart Account or a regular account.

The [CDP SDK](https://github.com/coinbase/cdp-sdk) makes it easy to work with Spend Permissions as either the Account or Spender, offering methods to create and manage Spend Permissions, as well as methods to use Spend Permissions.

## Anatomy of a Spend Permission

These are the main components of a Spend Permission:

* **Spender** - The entity that can spend tokens on behalf of the account.
* **Token** - The token that the Spend Permission is for, and the amount of that token that the Spender is allowed to spend.
* **Time Period** - The time period for which the Spend Permission is valid.
* **Salt** - A random value used to differentiate between Spend Permissions with the same parameters. The SDK will generate a random salt for you, but you can also specify your own.
* **Extra Data** - Arbitrary data that can be used to store additional information about the Spend Permission.

See the following sections for more details on the main components.

### Spender

The spender is specified in the `spender` field of the Spend Permission. It can be the address of any account, whether it's a Smart Account or a regular account.

### Token

The token is specified in the `token` field of the Spend Permission, and the amount allowed to spend is specified in the `allowance` field.

Spend Permissions support both native tokens and ERC-20 tokens. When using the CDP SDK, you have two options for specifying tokens:

1. **Convenient shortcuts** - Use `"eth"` for native ETH or `"usdc"` for USDC, and the SDK will handle the conversion to the correct token address. This shortcut is only supported on Base or Base Sepolia.
2. **ERC-20 contract addresses** - For other tokens, specify the token contract address as a string (e.g., `"0x4200000000000000000000000000000000000006"` for WETH).

The amount allowed to spend is specified in the `allowance` field, using the smallest unit of the token. For example, if the token is ETH, the allowance is specified in wei, and if the token is USDC, the allowance is specified in the smallest unit of USDC (6 decimals).

### Time Period

The time period is specified using the `periodInDays` field for simple day-based periods, or the `period`, `start` and `end` fields for more complex time controls.

The `periodInDays` field provides a convenient way to specify common time periods (e.g., `periodInDays: 1` for daily limits, `periodInDays: 7` for weekly limits).

For more advanced control, the `start` and `end` fields specify when the Spend Permission is valid. This means that the Spender can spend the amount specified in the `allowance` field after the `start` time and before the `end` time; attempting to spend outside of this time range will fail.

<Info>
  The `period` field specifies a rolling window of time in seconds in which the Spender can spend the amount specified in the `allowance` field. This allows you specify things like "the Spender can spend up to 0.00001 ETH per day" or "the Spender can spend up to 100 USDC per week".
</Info>

## Creating a Spend Permission

Here's how to create a spend permission that allows a spender to withdraw up to 0.01 USDC per day:

<Warning>
  Creating Spend Permissions is currently only supported on CDP Smart Accounts owned by CDP Server Wallets.
</Warning>

<CodeGroup>
  ```typescript TypeScript theme={null}
  import {
    CdpClient,
    parseUnits,
    type SpendPermissionInput,
  } from "@coinbase/cdp-sdk";
  import "dotenv/config";

  const cdp = new CdpClient();

  const smartAccount = await cdp.evm.getOrCreateSmartAccount({
    name: "SmartAccount",
    owner: await cdp.evm.getOrCreateAccount({
      name: "Owner",
    }),
    enableSpendPermissions: true, // NOTE: Smart Accounts must have spend permissions enabled at the time of creation.
  });

  const spender = await cdp.evm.getOrCreateSmartAccount({
    name: "Spender",
    owner: await cdp.evm.getOrCreateAccount({
      name: "Spender-Owner",
    }),
  });

  const spendPermission: SpendPermissionInput = {
    account: smartAccount.address,
    spender: spender.address,
    token: "usdc",
    allowance: parseUnits("0.01", 6),
    periodInDays: 1,
  };

  const { userOpHash } = await cdp.evm.createSpendPermission({
    network: "base-sepolia",
    spendPermission,
  });

  const userOperationResult = await smartAccount.waitForUserOperation({
    userOpHash,
  });

  console.log("Spend permission created:", userOperationResult);
  ```

  ```python Python theme={null}
  from cdp import CdpClient, SpendPermission
  from web3 import Web3

  async def main():
    async with CdpClient(
      api_key_id=os.environ.get("CDP_API_KEY_ID"),
      api_key_secret=os.environ.get("CDP_API_KEY_SECRET"),
      wallet_secret=os.environ.get("CDP_WALLET_SECRET"),
    ) as cdp:
      smart_account = await cdp.evm.get_or_create_smart_account(
        name="SmartAccount",
        owner=await cdp.evm.get_or_create_account(name="Owner"),
        enable_spend_permissions=True,
      )

      spender = await cdp.evm.get_or_create_account(name="Spender")

      result = await cdp.evm.create_spend_permission(
        network="base-sepolia",
        spend_permission=SpendPermission(
          account=smart_account.address,
          spender=spender.address,
          token="eth",
          allowance=parse_ether("0.00001"),
          period_in_days=1,
        ),
      )
      user_operation_result = await cdp.evm.wait_for_user_operation(
        smart_account_address=smart_account.address,
        user_op_hash=result.user_op_hash,
      )
      print(f"Spend permission created: {user_operation_result}")

  if __name__ == "__main__":
    asyncio.run(main())
  ```
</CodeGroup>

### ERC-20 Token Permissions

To create spend permissions for ERC-20 tokens other than USDC, specify the token contract address:

```typescript theme={null}
const wethSpendPermission: SpendPermissionInput = {
  account: smartAccount.address,
  spender: spender.address,
  token: "0x4200000000000000000000000000000000000006", // WETH on Base Sepolia
  allowance: parseEther("0.00001"), // 0.00001 WETH
  periodInDays: 1, // Daily limit
};
```

## Using a Spend Permission

Once a spend permission is created, the designated spender can spend tokens on behalf of the account within the defined limits:

<CodeGroup>
  ```typescript TypeScript theme={null}
  // List spend permissions to get the actual resolved permission
  const allPermissions = await cdp.evm.listSpendPermissions({
    address: smartAccount.address,
  });
  const permissions = allPermissions.spendPermissions.filter(
    (p) => p.permission.spender.toLowerCase() === spender.address.toLowerCase()
  );

  if (permissions.length === 0) {
    console.log("No spend permissions found for this spender");
    process.exit(1);
  }

  const spend = await spender.useSpendPermission({
    spendPermission: permissions[0].permission,
    value: parseUnits("0.005", 6),
    network: "base-sepolia",
  });

  const spendReceipt = await spender.waitForUserOperation(spend);

  const spendUserOp = await spender.getUserOperation({
    userOpHash: spendReceipt.userOpHash,
  });

  console.log(
    "Spend completed!",
    `https://sepolia.basescan.org/tx/${spendUserOp.transactionHash}`
  );
  ```

  ```python Python theme={null}
  all_permissions = cdp.evm.list_spend_permissions(
    address=smart_account.address,
  )
  permissions = [permission for permission in all_permissions if permission.spender.lower() == spender.address.lower()]

  if len(permissions) == 0:
    print("No spend permissions found for this spender")
    exit(1)

  spend = spender.use_spend_permission(
      spend_permission=permissions[0].permission,
      value=parse_units("0.005", 6),
      network="base-sepolia"
  )

  spend_receipt = spender.wait_for_user_operation(spend)

  print(f"Spend completed! https://sepolia.basescan.org/tx/{spend_receipt.transaction_hash}")
  ```
</CodeGroup>

## Check Remaining Allowance

To check how much of a spend permission's allowance remains in the current period, query the `getCurrentPeriod` function on the Spend Permission Manager contract. This returns the period start/end timestamps and the amount already spent.

<Accordion title="Example: Calculate remaining spend allowance">
  <CodeGroup>
    ```typescript TypeScript theme={null}
    import { createPublicClient, http, type Address } from "viem";
    import { baseSepolia } from "viem/chains";

    const SPEND_PERMISSION_MANAGER_ADDRESS = "0xf85210B21cC50302F477BA56686d2019dC9b67Ad";

    const SPEND_PERMISSION_MANAGER_ABI = [
      {
        inputs: [
          {
            components: [
              { name: "account", type: "address" },
              { name: "spender", type: "address" },
              { name: "token", type: "address" },
              { name: "allowance", type: "uint160" },
              { name: "period", type: "uint48" },
              { name: "start", type: "uint48" },
              { name: "end", type: "uint48" },
              { name: "salt", type: "uint256" },
              { name: "extraData", type: "bytes" },
            ],
            name: "spendPermission",
            type: "tuple",
          },
        ],
        name: "getCurrentPeriod",
        outputs: [
          { name: "start", type: "uint48" },
          { name: "end", type: "uint48" },
          { name: "spend", type: "uint160" },
        ],
        stateMutability: "view",
        type: "function",
      },
    ] as const;

    async function getRemainingAllowance(permission: {
      account: Address;
      spender: Address;
      token: Address;
      allowance: bigint;
      period: number;
      start: number;
      end: number;
      salt: bigint;
      extraData: `0x${string}`;
    }) {
      const client = createPublicClient({
        chain: baseSepolia,
        transport: http(),
      });

      const [periodStart, periodEnd, amountSpent] = await client.readContract({
        address: SPEND_PERMISSION_MANAGER_ADDRESS,
        abi: SPEND_PERMISSION_MANAGER_ABI,
        functionName: "getCurrentPeriod",
        args: [permission],
      });

      const remaining = BigInt(permission.allowance) - amountSpent;

      return { periodStart, periodEnd, spent: amountSpent, remaining };
    }

    // Usage with a permission from listSpendPermissions
    const permissions = await cdp.evm.listSpendPermissions({ address: smartAccount.address });
    const permission = permissions.spendPermissions[0].permission;

    const result = await getRemainingAllowance(permission);
    console.log(`Spent: ${result.spent}, Remaining: ${result.remaining}`);
    ```

    ```python Python theme={null}
    from web3 import Web3

    SPEND_PERMISSION_MANAGER_ADDRESS = "0xf85210B21cC50302F477BA56686d2019dC9b67Ad"

    # Spend Permission Manager ABI (getCurrentPeriod function)
    SPEND_PERMISSION_MANAGER_ABI = [
        {
            "inputs": [
                {
                    "components": [
                        {"name": "account", "type": "address"},
                        {"name": "spender", "type": "address"},
                        {"name": "token", "type": "address"},
                        {"name": "allowance", "type": "uint160"},
                        {"name": "period", "type": "uint48"},
                        {"name": "start", "type": "uint48"},
                        {"name": "end", "type": "uint48"},
                        {"name": "salt", "type": "uint256"},
                        {"name": "extraData", "type": "bytes"},
                    ],
                    "name": "spendPermission",
                    "type": "tuple",
                }
            ],
            "name": "getCurrentPeriod",
            "outputs": [
                {"name": "start", "type": "uint48"},
                {"name": "end", "type": "uint48"},
                {"name": "spend", "type": "uint160"},
            ],
            "stateMutability": "view",
            "type": "function",
        }
    ]

    def get_remaining_allowance(permission, rpc_url="https://sepolia.base.org"):
        """Calculate remaining spend allowance for the current period."""
        w3 = Web3(Web3.HTTPProvider(rpc_url))
        contract = w3.eth.contract(
            address=Web3.to_checksum_address(SPEND_PERMISSION_MANAGER_ADDRESS),
            abi=SPEND_PERMISSION_MANAGER_ABI,
        )

        # Convert permission to tuple format
        permission_tuple = (
            Web3.to_checksum_address(permission.account),
            Web3.to_checksum_address(permission.spender),
            Web3.to_checksum_address(permission.token),
            int(permission.allowance),
            int(permission.period),
            int(permission.start),
            int(permission.end),
            int(permission.salt),
            bytes.fromhex(permission.extra_data[2:]) if permission.extra_data.startswith("0x") else bytes.fromhex(permission.extra_data),
        )

        result = contract.functions.getCurrentPeriod(permission_tuple).call()
        period_start, period_end, amount_spent = result[0], result[1], result[2]

        remaining = int(permission.allowance) - amount_spent
        return {
            "period_start": period_start,
            "period_end": period_end,
            "spent": amount_spent,
            "remaining": remaining,
        }

    # Usage with a permission from listSpendPermissions
    permissions = await cdp.evm.list_spend_permissions(address=smart_account.address)
    permission = permissions.spend_permissions[0].permission

    result = get_remaining_allowance(permission)
    print(f"Spent: {result['spent']}, Remaining: {result['remaining']}")
    ```
  </CodeGroup>
</Accordion>

## Managing Spend Permissions

### Listing Spend Permissions

The `listSpendPermissions` method works differently depending on whether you're querying as the Account or as the Spender:

#### As the Account

When listing as the Account, you see all spend permissions you've granted to various spenders:

<CodeGroup>
  ```typescript TypeScript theme={null}
  const permissions = await cdp.evm.listSpendPermissions({
    address: smartAccount.address,
  });

  console.log("Spend permissions granted by this account:", permissions);
  ```

  ```python Python theme={null}
  permissions = cdp.evm.list_spend_permissions(
    address=smart_account.address,
  )

  print("Spend permissions granted by this account:", permissions)
  ```
</CodeGroup>

#### As the Spender

When listing as the Spender, you must query spend permissions granted by the account whose tokens you want to spend. You can then filter the results to find the spend permission you want to use.

<CodeGroup>
  ```typescript TypeScript theme={null}
  const allPermissions = await cdp.evm.listSpendPermissions({
    address: "0xDeF2Bd558190d2DE7E4b26F452C9c10A175B1f45", // Account that is known to have designated this spender
  });

  const permissions = allPermissions.spendPermissions.filter(
    (p) => p.permission.spender.toLowerCase() === spender.address.toLowerCase()
  );

  console.log("Spend permissions available to this spender:", permissions);
  ```

  ```python Python theme={null}
  all_permissions = cdp.evm.list_spend_permissions(
    address="0xDeF2Bd558190d2DE7E4b26F452C9c10A175B1f45", # Account that is known to have designated this spender
  )

  permissions = [permission for permission in all_permissions if permission.spender.lower() == spender.address.lower()]

  print("Spend permissions available to this spender:", permissions)
  ```
</CodeGroup>

### Revoking Spend Permissions

You can revoke a Spend Permission using the `revokeSpendPermission` method:

<CodeGroup>
  ```typescript TypeScript theme={null}
  // First, get the permission hash of the permission to revoke
  const permissions = await cdp.evm.listSpendPermissions({
    address: account.address,
  });
  const permissionHash = permissions.spendPermissions[0].permissionHash;

  await cdp.evm.revokeSpendPermission({
    address: account.address,
    permissionHash,
    network: "base-sepolia",
  });

  const revokeResult = await cdp.evm.waitForUserOperation({
    smartAccountAddress: account.address,
    userOpHash: revokeUserOpHash,
  });

  console.log("Revoke result:", revokeResult);
  ```

  ```python Python theme={null}
  # First, get the permission hash of the permission to revoke
  all_permissions = cdp.evm.list_spend_permissions(
    address=account.address,
  )
  permission_hash = all_permissions[0].permission_hash

  cdp.evm.revoke_spend_permission(
    address=account.address,
    permission_hash=permission_hash,
  )

  revoke_result = cdp.evm.wait_for_user_operation(
    smart_account_address=account.address,
    user_op_hash=revoke_user_op_hash,
  )

  print("Revoke result:", revoke_result)
  ```
</CodeGroup>

## Spend Permissions vs. Policies

At its core, a Spend Permission enables a spender to spend tokens on behalf of an account within a specified time period and amount. The tokens can be native ETH or an ERC-20 token.

This section explores the differences between Spend Permissions and [CDP Policies](/server-wallets/v2/using-the-wallet-api/policies/overview).

|                            | Spend Permissions                                                                               | Policies                                                                                                       |
| -------------------------- | ----------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| **Evaluation Environment** | Evaluated entirely onchain through smart contracts, providing transparency and decentralization | Evaluated within Coinbase's trusted infrastructure using TEE technology, providing secure off-chain evaluation |
| **Scope and Flexibility**  | Specifically designed for spending assets on EVM chains                                         | Can be applied to any arbitrary transaction type, giving full control over allowed transactions                |
| **Platform Support**       | Only available on EVM chains                                                                    | Available on both EVM chains and Solana                                                                        |
| **Account Scope**          | Can grant permissions to any account onchain, including accounts outside your CDP project       | Govern accounts within your CDP project only                                                                   |

## Best Practices

1. **Set Reasonable Limits** - Use the minimum allowance necessary for your use case
2. **Define Time Boundaries** - Set appropriate start and end times to limit exposure
3. **Monitor Usage** - Track spending activity to detect any unusual behavior
4. **Revoke When Necessary** - Implement logic to revoke permissions when no longer needed

## Supported Networks

Spend Permissions are currently supported on:

Testnets:

* Base Sepolia
* Ethereum Sepolia

Mainnets:

* Base
* Ethereum
* Optimism
* Arbitrum
* Polygon
* Avalanche

<Info>
  The Spend Permission Manager contract is deployed at `0xf85210B21cC50302F477BA56686d2019dC9b67Ad` on all supported networks.
</Info>

## What to read next

* [**Smart Accounts**](/server-wallets/v2/evm-features/smart-accounts): Learn more about ERC-4337 Smart Accounts
* [**Gas Sponsorship**](/server-wallets/v2/evm-features/gas-sponsorship): Sponsor gas fees for your users' transactions

