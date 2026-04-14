# Govern behavior using Policies
Source: https://docs.cdp.coinbase.com/server-wallets/v2/using-the-wallet-api/policies/overview



## Overview

CDP Wallets support **Policies** that enable developers to govern account and project behavior. Policies provide flexible configuration for enforcing controls based on transaction parameters such as destination address and transaction value.

### Use cases

* **Wallet transaction filtering:** Prevent transfers to known malicious or restricted addresses
* **Allowlisted access to project features:** Restrict access only to approved addresses to interact with a smart contract or mint a token
* **Transaction limits per address:** Limit financial risk by capping transaction values
* **Prevent signing of fraudulent messages:** Ensure compromised clients cannot prove control of your accounts
* **USD Spend Limits:** Restrict the amount in USD that can be sent, or approved, in a single transaction.

### Policy field definitions

A policy is defined by the following fields:

| Field       | Description                                                                                                              | Valid values                                                                                                                                                                                                                                                                                                                                                                                                   |
| ----------- | ------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `scope`     | The level at which a policy gets applied                                                                                 | `project` or `account`                                                                                                                                                                                                                                                                                                                                                                                         |
| `rules`     | A list of rules that are used to govern the behavior of accounts                                                         | An array of rules                                                                                                                                                                                                                                                                                                                                                                                              |
| `action`    | The action to take when a policy is applied                                                                              | `accept` or `reject`                                                                                                                                                                                                                                                                                                                                                                                           |
| `operation` | The operation to perform when a policy is applied                                                                        | `signEvmTransaction`, `sendEvmTransaction`, `signEvmMessage`, `signEvmHash`, `signEvmTypedData`, `signSolTransaction`, `sendSolTransaction`, `signSolMessage`, `prepareUserOperation`, `sendUserOperation`, `signEndUserEvmTransaction`, `sendEndUserEvmTransaction`, `signEndUserEvmMessage`, `signEndUserEvmTypedData`, `signEndUserSolTransaction`, `sendEndUserSolTransaction`, or `signEndUserSolMessage` |
| `criteria`  | The list of logical expressions that are evaluated to a transaction to determine whether a rule should be applied or not | An array of criteria. See [API Reference](/api-reference/v2/rest-api/policy-engine/list-policies) for more details.                                                                                                                                                                                                                                                                                            |

### Evaluation process

A `project`-level policy will be evaluated first, followed by any `account`-level policies. Read more technical details on policy evaluation in the [API Reference documentation](/api-reference/v2/rest-api/policy-engine/list-policies).

```json project-policy.json [expandable] lines wrap theme={null}
{
  "description": "An example project level policy",
  "scope": "project",
  "rules": [
    {
      "action": "accept",
      "operation": "signEvmTransaction",
      "criteria": [
        {
          "type": "ethValue",
          "ethValue": "1000000000000000000",
          "operator": "<="
        }
      ]
    },
    {
      "action": "accept",
      "operation": "signEvmTransaction",
      "criteria": [
        {
          "type": "ethValue",
          "ethValue": "2000000000000000000",
          "operator": "<="
        },
        {
          "type": "evmAddress",
          "addresses": [
            "0x123"
          ],
          "operator": "in"
        }
      ]
    }
  ]
}
```

<Accordion title="How would this policy be evaluated?">
  In this example, the policy has two rules. An incoming transaction would be processed against each rule as follows:

  1. Accept any transaction with a value less than or equal to 1 ETH (expressed in Wei).
  2. Accept any transaction with a value less than or equal to 2 ETH, and an address in the allowlist.

  Assume we have two transaction requests to the same address, 0x123:

  1. Transaction A with a value of 0.5 ETH
  2. Transaction B with a value of 2 ETH

  * **Transaction A** would be accepted on the first rule, and the policy engine would stop evaluation against this policy.
  * **Transaction B** would be processed against both rules. It would be rejected on the first rule, but accepted once processed against the second rule.
</Accordion>

### Supported operations

Each rule defines the behavior of a certain `operation`. The `operation` corresponds to a CDP v2 API. Currently, the following operations are supported:

**EVM Operations:**

* `signEvmTransaction`: To identify incoming signing transactions on an EVM compatible network
* `sendEvmTransaction`: To identify incoming signing transactions that are then sent to a supported network
* `signEvmTypedData`: To identify incoming typed data to be signed by an account
* `signEvmMessage`: To identify incoming messages to be signed by an account
* `signEvmHash`: To identify incoming hash to be signed by an account
* `prepareUserOperation`: For preparing user operations on a smart account
* `sendUserOperation`: For sending user operations using a smart account

**Solana Operations:**

* `signSolTransaction`: To identify incoming signing transactions on the Solana network
* `sendSolTransaction`: To identify incoming signing transactions that are then sent to the Solana mainnet or devnet network.
* `signSolMessage`: To identify incoming messages to be signed by a Solana account

The Policy Engine also supports end-user signing operations for Embedded Wallets. See the [Policy Engine overview](/policy-engine/overview) for a full list of operations across all wallet products.

You can find more details in the [API reference documentation](/api-reference/v2/rest-api/policy-engine/list-policies).

### API Key Configuration

In order to securely manage Policies via API or SDK, you'll need to manually configure an API key with a specific scope.

This scope is required to perform the following API operations:

* Create Policy
* Update Policy
* Delete Policy
* Account Policy assignment

When you're creating a new API Key, first expand the **API restrictions** panel then scroll down to the **API-specific restrictions** section.

Ensure that **Manage (modify policies)** is checked before key creation as seen in the following screenshot.

<Frame>
  <img alt="Policies Scope" />
</Frame>

## Define a policy

Policies can be defined via CDP Portal UI or via the CDP SDK.

<Note>
  You may only create one project-level policy per project.
</Note>

### UI (CDP Portal)

1. Navigate to [Policies](https://portal.cdp.coinbase.com/products/server-wallets/policies) in the CDP Portal.
   <Frame>
     <img alt="Policies UI" />
   </Frame>

2. Click the **Create new policy** button to access the JSON editor. The modal will contain a sample policy that you can edit, but you can also use some of the examples in our [EVM Policies](/server-wallets/v2/using-the-wallet-api/policies/evm-policies) or [Solana Policies](/server-wallets/v2/using-the-wallet-api/policies/solana-policies) documentation.

   <Frame>
     <img alt="JSON Editor" />
   </Frame>

3. Define the policy and click the **Create** button. If successful, you should see a "Policy created" message.

4. Refresh the page to see the new policy listed in the Policies dashboard:

   <Frame>
     <img alt="Policy Engine dashboard" />
   </Frame>

   Click the **View** button to edit or delete the policy.

5. Account level policies should be added to the account programmatically via the SDK.

<CodeGroup>
  ```ts TypeScript lines wrap theme={null}
      import { CdpClient } from "@coinbase/cdp-sdk";
      import dotenv from "dotenv";

      dotenv.config();

      const cdp = new CdpClient();

      const account = await cdp.evm.createAccount();

      const policyId = "" // Paste the policy ID created on portal.

      // Update the account to add the account policy.
      const updatedAccount = await cdp.evm.updateAccount({
        address: account.address,
        update: {
          accountPolicy: policyId,
        }
      })

      console.log("Updated account %s with policy: %s", updatedAccount.address, updatedAccount.policies);
  ```

  ```python Python lines wrap theme={null}
          import asyncio

          from cdp import CdpClient
          from dotenv import load_dotenv
          from cdp.update_account_types import UpdateAccountOptions

          load_dotenv()

          async def main():
              async with CdpClient() as cdp:
                  account = await cdp.evm.create_account()

                  policy_id = "" # Paste the policy ID created on portal.

                  updatedAccount = await cdp.evm.update_account(
                                           address=account.address,
                                           update=UpdateAccountOptions(
                                             account_policy=policy_id,
                                           ),
                                         )

                  print(f"Updated account {account.address} with policy {updatedAccount.policies}")

          asyncio.run(main())
  ```
</CodeGroup>

### Programmatically

<Note>
  In order to manage Policies via SDK or API, you need to have an API Key with [Policy management enabled](#api-key-configuration)
</Note>

To create a policy programmatically, you can use the CDP SDK. The code below demonstrates basic policy creation and management:

1. Create an EVM account named `PolicyAccount`
2. Create an account-level policy that only allows transactions less than or equal to 1 ETH to the address `0x000000000000000000000000000000000000dEaD`
3. Apply the policy to the account we created
4. Create another account named `OtherPolicyAccount` which has the above policy applied during creation
5. Create a project-level policy that only allows transactions less than or equal to 5 ETH to the address `0x000000000000000000000000000000000000dEaD`

<Note>
  A project-level policy is automatically applied to all accounts in the project on creation.

  An account-level policy may be applied to an account in 2 ways: *during* account creation, or *after* account creation by updating the account.
</Note>

<CodeGroup>
  ```ts TypeScript [expandable] lines wrap theme={null}
      import { CdpClient } from "@coinbase/cdp-sdk";

      const cdp = new CdpClient();

      const account = await cdp.evm.getOrCreateAccount({
        name: "PolicyAccount"
      });
      console.log("Account address:", account.address);

      // Create policy
      const policy = await cdp.policies.createPolicy({
        policy: {
          scope: "account",
          description: "Account Allowlist Example",
          rules: [
            {
              action: "accept",
              operation: "signEvmTransaction",
              criteria: [
                {
                  type: "ethValue",
                  ethValue: "1000000000000000000", // 1 ETH in wei
                  operator: "<=",
                },
                {
                  type: "evmAddress",
                  addresses: ["0x000000000000000000000000000000000000dEaD"],
                  operator: "in",
                },
              ],
            },
          ],
        },
      });
      console.log("Created policy:", policy.id);

      // Apply policy to the account
      const updatedAccount = await cdp.evm.updateAccount({
        address: account.address,
        update: {
          accountPolicy: policy.id
        }
      });
      console.log("Applied policy to account:", updatedAccount.address);

      // Create another account with policy immediately applied to it
      const otherAccount = await cdp.evm.createAccount({
        name: "OtherPolicyAccount",
        accountPolicy: policy.id
      });
      console.log("Other account address:", otherAccount.address);

      // Create project policy example
      const projectPolicy = await cdp.policies.createPolicy({
        policy: {
          scope: "project",
          description: "Project Transaction Limit Example",
          rules: [
            {
              action: "accept",
              operation: "signEvmTransaction",
              criteria: [
                {
                  type: "ethValue",
                  ethValue: "5000000000000000000", // 5 ETH in wei
                  operator: "<=",
                },
                {
                  type: "evmAddress",
                  addresses: ["0x000000000000000000000000000000000000dEaD"],
                  operator: "in",
                },
              ],
            },
          ],
        },
      });
      console.log("Created project policy:", projectPolicy.id);
  ```

  ```python Python lines wrap [expandable] theme={null}
      import asyncio
      from cdp import CdpClient
      from dotenv import load_dotenv
      from cdp.policies.types import CreatePolicyOptions, EthValueCriterion, EvmAddressCriterion, SignEvmTransactionRule
      from cdp.update_account_types import UpdateAccountOptions

      load_dotenv()

      async def main():
          cdp = CdpClient()

          account = await cdp.evm.get_or_create_account(name="PolicyAccount")
          print(f"Account address: {account.address}")

          # Create policy
          policy = await cdp.policies.create_policy(
              policy=CreatePolicyOptions(
                  scope="account",
                  description="Account Allowlist Example",
                  rules=[
                      SignEvmTransactionRule(
                          action="accept",
                          criteria=[
                              EthValueCriterion(
                                  ethValue="1000000000000000000", # 1 ETH in wei
                                  operator="<=",
                              ),
                              EvmAddressCriterion(
                                  addresses=["0x000000000000000000000000000000000000dEaD"],
                                  operator="in",
                              ),
                          ],
                      )
                  ],
              )
          )
          print(f"Created policy: {policy.id}")

          # Apply policy to the account
          updated_account = await cdp.evm.update_account(
              address=account.address,
              update=UpdateAccountOptions(
                  account_policy=policy.id
              ),
          )
          print(f"Applied policy to account: {updated_account.address}")

          # Create another account with policy immediately applied to it
          other_account = await cdp.evm.create_account(
            name="OtherPolicyAccount",
            account_policy=policy.id,
          )
          print(f"Other account address: {other_account.address}");

          # Create project policy example
          project_policy = await cdp.policies.create_policy(
              policy=CreatePolicyOptions(
                  scope="project",
                  description="Project Transaction Limit Example",
                  rules=[
                      SignEvmTransactionRule(
                          action="accept",
                          criteria=[
                              EthValueCriterion(
                                  ethValue="5000000000000000000", # 5 ETH in wei
                                  operator="<=",
                              ),
                              EvmAddressCriterion(
                                  addresses=["0x000000000000000000000000000000000000dEaD"],
                                  operator="in",
                              ),
                          ],
                      )
                  ],
              )
          )
          print(f"Created project policy: {project_policy.id}")

          await cdp.close()


      asyncio.run(main())
  ```
</CodeGroup>

<Note>
  A project-level policy is automatically applied to all accounts in the project on creation.

  An account-level policy may be applied to an account in 2 ways: *during* account creation, or *after* account creation by updating the account.
</Note>

For more detailed examples and specific policy configurations, see:

* [**EVM Policies**](/server-wallets/v2/using-the-wallet-api/policies/evm-policies): Comprehensive examples for EVM-based transactions
* [**Solana Policies**](/server-wallets/v2/using-the-wallet-api/policies/solana-policies): Examples for Solana network transactions

## Video: Watch and learn

Watch the video to learn how to implement and manage policies with CDP Server Wallet, which covers:

* An overview of policy engine setup and configuration
* How to create project-level and account-level policies
* Best practices for implementing transaction controls and security measures

<Frame>
  <iframe title="How to implement policies with CDP Server Wallet" />
</Frame>

## What to read next

* [**EVM Policies**](/server-wallets/v2/using-the-wallet-api/policies/evm-policies): Learn about EVM-specific policy examples and implementations
* [**Solana Policies**](/server-wallets/v2/using-the-wallet-api/policies/solana-policies): Learn about Solana-specific policy examples and implementations
* [**Embedded Wallet Policies**](/embedded-wallets/policies/overview): Learn about policies for embedded wallet end-user operations
* [**v2 Server Wallet Security**](/server-wallets/v2/introduction/security): Learn more about the security features of the CDP v2 Server Wallet
* [**v2 API Reference**](/api-reference/v2/rest-api/policy-engine/list-policies): Explore the API reference for CDP Policies

