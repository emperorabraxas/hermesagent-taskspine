# Policy Engine
Source: https://docs.cdp.coinbase.com/policy-engine/overview



The CDP Policy Engine is a shared enforcement layer that governs signing operations across CDP wallet products.

Each **policy** is a collection of rules. Each rule specifies an `operation` (the signing action to govern), `criteria` (conditions that must all match), and an `action` (`accept` or `reject`).

Rules are evaluated in order before any signing operation executes. If no rule matches, the request is **rejected** by default.

## Policy structure

A policy defines a set of rules that govern specific signing operations. Each policy contains:

| Field         | Description                                  | Valid values                                            |
| ------------- | -------------------------------------------- | ------------------------------------------------------- |
| `scope`       | The level at which the policy is applied     | `project` (embedded wallets only support project scope) |
| `description` | A human-readable description of the policy   | Any string                                              |
| `rules`       | A list of rules that govern signing behavior | An array of rules                                       |

Each rule contains:

| Field       | Description                                            | Valid values                                            |
| ----------- | ------------------------------------------------------ | ------------------------------------------------------- |
| `action`    | The action to take when a rule matches                 | `accept` or `reject`                                    |
| `operation` | The signing operation this rule applies to             | See [Supported operations](#supported-operations) below |
| `criteria`  | Conditions that must all be true for the rule to match | An array of criteria (logical AND)                      |

## Scope

Policies apply at the **project** or **account** level. Project-level policies cover all accounts in a CDP project; account-level policies apply to a single account. A single account can have at most one of each.

<Note>
  Embedded Wallets only support **project-level** policies.
</Note>

## Operations by product

The `operation` field in each rule determines which signing action and product surface the rule applies to.

Use this table to find the right operation name for your wallet type.

<Note>
  Network-based criteria (`evmNetwork`, `solNetwork`) only apply to **send** operations, not sign-only operations.
</Note>

### EVM

|          | Action                  | Server Wallet          | Embedded Wallet             |
| -------- | ----------------------- | ---------------------- | --------------------------- |
| **Sign** | Transaction             | `signEvmTransaction`   | `signEndUserEvmTransaction` |
|          | Message (EIP-191)       | `signEvmMessage`       | `signEndUserEvmMessage`     |
|          | Typed data (EIP-712)    | `signEvmTypedData`     | `signEndUserEvmTypedData`   |
|          | Hash                    | `signEvmHash`          | —                           |
| **Send** | Transaction             | `sendEvmTransaction`   | `sendEndUserEvmTransaction` |
|          | Smart account (prepare) | `prepareUserOperation` | —                           |
|          | Smart account (send)    | `sendUserOperation`    | —                           |

### Solana

|          | Action      | Server Wallet        | Embedded Wallet             |
| -------- | ----------- | -------------------- | --------------------------- |
| **Sign** | Transaction | `signSolTransaction` | `signEndUserSolTransaction` |
|          | Message     | `signSolMessage`     | `signEndUserSolMessage`     |
| **Send** | Transaction | `sendSolTransaction` | `sendEndUserSolTransaction` |

## Policies by product

<CardGroup>
  <Card title="Server Wallets" icon="server" href="/server-wallets/v2/using-the-wallet-api/policies/overview">
    Govern developer-controlled EVM and Solana account signing, including smart account user operations. Supports both project-level and account-level scope.
  </Card>

  <Card title="Embedded Wallets" icon="mobile" href="/embedded-wallets/policies/overview">
    Govern end-user signing operations in your app. Supports project-level scope only.
  </Card>

  <Card title="API Reference" icon="code" href="/api-reference/v2/rest-api/policy-engine/list-policies">
    Full Policy Engine REST API reference including all criteria types and request schemas.
  </Card>
</CardGroup>

