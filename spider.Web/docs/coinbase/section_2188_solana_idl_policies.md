# Solana IDL Policies
Source: https://docs.cdp.coinbase.com/server-wallets/v2/using-the-wallet-api/policies/solana-idl-policies



## Overview

The `solData` criterion provides advanced validation of Solana transaction instruction data using Interface Definition Language (IDL) specifications. This criterion allows you to decode and validate instruction parameters against specific rules, ensuring that transactions meet precise requirements before signing.

A `solData` criterion uses IDL specifications to identify which Solana programs to validate against and defines instruction-specific validation rules including instruction names and parameter constraints.
The `idls` field specifies which programs to validate, while the `conditions` field defines the validation rules.

The `idls` field is a list that can include either:

* [known program names](/server-wallets/v2/using-the-wallet-api/policies/solana-idl-policies#known-program-shortcuts) like "SystemProgram" and "TokenProgram"
* [custom IDL objects](/server-wallets/v2/using-the-wallet-api/policies/solana-idl-policies#custom-idl-objects)

For general policy concepts and setup instructions, see the [Policies Overview](/server-wallets/v2/using-the-wallet-api/policies/overview).

## IDL Specifications

### Anchor IDL Format

IDL specifications must follow Anchor's IDL format v0.30+. This standardized format ensures compatibility and proper instruction decoding.

### Supported Argument Types

The following primitive argument types are currently supported:

* **Boolean**: `bool`
* **String**: `string`
* **Public Key**: `pubkey`
* **Unsigned Integers**: `u8`, `u16`, `u32`, `u64`, `u128`, `u256`
* **Signed Integers**: `i8`, `i16`, `i32`, `i64`, `i128`, `i256`
* **Floating Point**: `f32`, `f64`

### Current Limitations

Complex IDL argument types are not currently supported, including:

* User-defined types
* Arrays
* Vectors
* Optional types

If you need support for any of these features, please reach out to us on our [CDP Discord](https://discord.com/invite/cdp).

### IDL Compatibility

To convert older IDL formats to the required v0.30+ format, use the Anchor CLI:

```bash theme={null}
anchor idl convert internal/policy/fixtures/solana_system_program_idl.json -o internal/policy/fixtures/solana_system_program_idl.json
```

## Instruction Discriminators

Instruction discriminators are unique byte sequences that identify specific instructions within a program. Different program types use different discriminator formats and sizes.

### Discriminator Formats by Program Type

| Program Type         | Discriminator Format                      | Size    | Example                       |
| -------------------- | ----------------------------------------- | ------- | ----------------------------- |
| **SystemProgram**    | 4-byte little-endian u32                  | 4 bytes | Transfer = `[2,0,0,0]`        |
| **SPL Token**        | 1-byte enum index                         | 1 byte  | Transfer = `3`                |
| **Associated Token** | Borsh-encoded enum                        | 1 byte  | Create = `0`                  |
| **Anchor Programs**  | SHA256 hash of "global:instruction\_name" | 8 bytes | transfer = `[163,52,200,...]` |

### Anchor Discriminator Generation

For Anchor programs, the 8-byte discriminator is generated using:

```
SHA256("global:instruction_name")
```

This ensures consistent and unique identification of instructions across Anchor-based programs.

## IDL Configuration

### Known Program Shortcuts

For common Solana programs, you can use predefined program names instead of providing IDL specifications:

* `"SystemProgram"` - Native Solana system program
* `"TokenProgram"` - SPL Token program
* `"AssociatedTokenProgram"` - Associated Token Account program

### Custom IDL Objects

For custom programs or when you need specific instruction definitions, provide IDL objects with:

* **address**: The program's public key address
* **instructions**: Array of instruction definitions containing:
  * **name**: Instruction name
  * **discriminator**: Byte array identifying the instruction
  * **args**: Array of argument definitions with name and type

## Conditions

Conditions in your `solData` criteria allow you to validate specific instruction parameters against defined constraints.

### Condition Evaluation

* If there are **multiple conditions** defined in a solData criterion, they are evaluated with **OR** logic - if any condition matches, the validation passes
* **Parameters within a condition** are evaluated with **AND** logic - all parameters must match for the condition to pass

### Condition Structure

Each condition includes:

* **instruction**: Name matching an instruction in one of the provided IDLs
* **params** (optional): Array of parameter validations, each with:
  * **name**: Parameter name matching the instruction argument
  * **operator**: Comparison operator (`==`, `<=`, `>=`, `<`, `>`, `!=`) for single value comparison, or (`in`, `not in`) for list comparisons
  * **value** or **values**: Expected value or list of values for comparison

## Examples

### Using Known IDLs

This example uses predefined program names for common Solana programs:

<CodeGroup>
  ```typescript TypeScript theme={null}
  import { CdpClient } from "@coinbase/cdp-sdk";
  import {
    LAMPORTS_PER_SOL,
    PublicKey,
    SYSVAR_RECENT_BLOCKHASHES_PUBKEY,
    Transaction,
  } from "@solana/web3.js";
  import "dotenv/config";

  const cdp = new CdpClient();

  const policy = await cdp.policies.createPolicy({
    policy: {
      scope: "account",
      description: "Create solData account policy",
      rules: [
        {
          action: "accept",
          operation: "signSolTransaction",
          criteria: [
            {
              type: "solData",
              idls: ["SystemProgram", "TokenProgram", "AssociatedTokenProgram"],
              conditions: [
                {
                  instruction: "transfer",
                  params: [
                    {
                      name: "lamports",
                      operator: "<=",
                      value: "1000000",
                    },
                  ],
                },
                {
                  instruction: "transfer_checked",
                  params: [
                    {
                      name: "amount",
                      operator: "<=",
                      value: "100000",
                    },
                    {
                      name: "decimals",
                      operator: "==",
                      value: "6",
                    },
                  ],
                },
                {
                  instruction: "create",
                },
              ],
            },
          ],
        },
      ],
    },
  });

  console.log("Created solData policy: ", policy.id);

  // Apply policy to account
  const accountWithSolDataPolicy = await cdp.solana.getOrCreateAccount({
    name: "MyAccount",
  });

  await cdp.solana.updateAccount({
    address: accountWithSolDataPolicy.address,
    update: {
      accountPolicy: policy.id,
    },
  });

  // Test with valid transaction
  const fromPubkey = new PublicKey(accountWithSolDataPolicy.address);
  const goodTransferAmount = BigInt(0.001 * LAMPORTS_PER_SOL);
  const transaction = new Transaction().add(
    createAnchorSystemTransferInstruction(goodTransferAmount),
    createAnchorSPLTransferCheckedInstruction(100000, 6),
    createAnchorAssociatedTokenAccountCreateInstruction()
  );

  transaction.recentBlockhash = SYSVAR_RECENT_BLOCKHASHES_PUBKEY.toBase58();
  transaction.feePayer = fromPubkey;

  const serializedTransaction = transaction.serialize({
    requireAllSignatures: false,
  });

  const base64Transaction = Buffer.from(serializedTransaction).toString("base64");

  try {
    const result = await accountWithSolDataPolicy.signTransaction({
      transaction: base64Transaction,
    });
    console.log("✅ Signed transaction: ", result.signedTransaction);
  } catch (error) {
    console.log("❌ Transaction rejected: ", error);
  }
  ```

  ```python Python theme={null}
  import asyncio
  import base64

  from cdp.update_account_types import UpdateAccountOptions
  from solders.pubkey import Pubkey
  from solders.transaction import Transaction
  from solders.message import Message
  from solders.hash import Hash

  from cdp import CdpClient
  from cdp.policies.types import (
      CreatePolicyOptions,
      SignSolanaTransactionRule,
      SolDataCriterion,
      SolDataCondition,
      SolDataParameterCondition,
  )
  from dotenv import load_dotenv

  load_dotenv()

  async def main():
      """Create a Solana policy with solData criterion using known IDLs."""
      async with CdpClient() as cdp:
          create_options = CreatePolicyOptions(
              scope="account",
              description="Create solData account policy",
              rules=[
                  SignSolanaTransactionRule(
                      action="accept",
                      operation="signSolTransaction",
                      criteria=[
                          SolDataCriterion(
                              type="solData",
                              idls=["SystemProgram", "TokenProgram", "AssociatedTokenProgram"],
                              conditions=[
                                  SolDataCondition(
                                      instruction="transfer",
                                      params=[
                                          SolDataParameterCondition(name="lamports", operator="<=", value="1000000"),
                                      ],
                                  ),
                                  SolDataCondition(
                                      instruction="transfer_checked",
                                      params=[
                                          SolDataParameterCondition(name="amount", operator="<=", value="100000"),
                                          SolDataParameterCondition(name="decimals", operator="==", value="6"),
                                      ],
                                  ),
                                  SolDataCondition(instruction="create"),
                              ],
                          )
                      ],
                  )
              ],
          )
          
          policy = await cdp.policies.create_policy(policy=create_options)
          print(f"Created solData policy: {policy.id}")
          
          # Apply policy to account
          account_with_sol_data_policy = await cdp.solana.get_or_create_account(name="MyAccount")
          await cdp.solana.update_account(
              address=account_with_sol_data_policy.address,
              update=UpdateAccountOptions(account_policy=policy.id),
          )
          
          # Test with valid transaction
          from_pubkey = Pubkey.from_string(account_with_sol_data_policy.address)
          good_transfer_amount = int(0.001 * 10**9)  # 0.001 SOL in lamports
          instructions = [
              create_anchor_system_transfer_instruction(good_transfer_amount),
              create_anchor_spl_transfer_checked_instruction(100000, 6),
              create_anchor_associated_token_account_create_instruction(),
          ]
          placeholder_blockhash = Hash.from_string("SysvarRecentB1ockHashes11111111111111111111")
          message = Message.new_with_blockhash(
              instructions,
              from_pubkey,
              placeholder_blockhash
          )
          transaction = Transaction.new_unsigned(message)
          
          serialized_transaction = bytes(transaction)
          base64_transaction = base64.b64encode(serialized_transaction).decode("utf-8")
          
          try:
              result = await account_with_sol_data_policy.sign_transaction(transaction=base64_transaction)
              print(f"✅ Signed transaction: {result.signed_transaction}")
          except Exception as e:
              print(f"❌ Transaction rejected: {e}")

  asyncio.run(main())
  ```
</CodeGroup>

### Using Custom IDLs

For custom programs, provide IDL specifications:

<CodeGroup>
  ```typescript TypeScript theme={null}
  import { CdpClient } from "@coinbase/cdp-sdk";

  const cdp = new CdpClient();

  const policy = await cdp.policies.createPolicy({
    policy: {
      scope: "account",
      description: "Custom IDL solData policy",
      rules: [
        {
          action: "accept",
          operation: "signSolTransaction",
          criteria: [
            {
              type: "solData",
              idls: [
                {
                  address: "11111111111111111111111111111111",
                  instructions: [
                    {
                      name: "transfer",
                      discriminator: [163, 52, 200, 231, 140, 3, 69, 186],
                      args: [
                        {
                          name: "lamports",
                          type: "u64",
                        },
                      ],
                    },
                  ],
                },
                {
                  address: "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA",
                  instructions: [
                    {
                      name: "transfer_checked",
                      discriminator: [119, 250, 202, 24, 253, 135, 244, 121],
                      args: [
                        {
                          name: "amount",
                          type: "u64",
                        },
                        {
                          name: "decimals",
                          type: "u8",
                        },
                      ],
                    },
                  ],
                },
              ],
              conditions: [
                {
                  instruction: "transfer",
                  params: [
                    {
                      name: "lamports",
                      operator: "<=",
                      value: "1000000",
                    },
                  ],
                },
                {
                  instruction: "transfer_checked",
                  params: [
                    {
                      name: "amount",
                      operator: "<=",
                      value: "100000",
                    },
                    {
                      name: "decimals",
                      operator: "==",
                      value: "6",
                    },
                  ],
                },
              ],
            },
          ],
        },
      ],
    },
  });

  console.log("Created custom IDL solData policy: ", policy.id);
  ```

  ```python Python theme={null}
  import asyncio
  from cdp import CdpClient
  from cdp.openapi_client.models.idl import Idl
  from cdp.policies.types import (
      CreatePolicyOptions,
      SignSolanaTransactionRule,
      SolDataCriterion,
      SolDataCondition,
      SolDataParameterCondition,
  )

  async def main():
      async with CdpClient() as cdp:
          # Define custom IDLs
          system_transfer_idl = Idl(
              address="11111111111111111111111111111111",
              instructions=[{
                  "name": "transfer",
                  "discriminator": [163, 52, 200, 231, 140, 3, 69, 186],
                  "args": [{"name": "lamports", "type": "u64"}]
              }]
          )
          
          token_transfer_idl = Idl(
              address="TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA",
              instructions=[{
                  "name": "transfer_checked",
                  "discriminator": [119, 250, 202, 24, 253, 135, 244, 121],
                  "args": [
                      {"name": "amount", "type": "u64"},
                      {"name": "decimals", "type": "u8"}
                  ]
              }]
          )
          
          create_options = CreatePolicyOptions(
              scope="account",
              description="Custom IDL solData policy",
              rules=[
                  SignSolanaTransactionRule(
                      action="accept",
                      operation="signSolTransaction",
                      criteria=[
                          SolDataCriterion(
                              type="solData",
                              idls=[system_transfer_idl, token_transfer_idl],
                              conditions=[
                                  SolDataCondition(
                                      instruction="transfer",
                                      params=[
                                          SolDataParameterCondition(name="lamports", operator="<=", value="1000000"),
                                      ],
                                  ),
                                  SolDataCondition(
                                      instruction="transfer_checked",
                                      params=[
                                          SolDataParameterCondition(name="amount", operator="<=", value="100000"),
                                          SolDataParameterCondition(name="decimals", operator="==", value="6"),
                                      ],
                                  ),
                              ],
                          )
                      ],
                  )
              ],
          )
          
          policy = await cdp.policies.create_policy(policy=create_options)
          print(f"Created custom IDL solData policy: {policy.id}")

  asyncio.run(main())
  ```
</CodeGroup>

It is critical that instructions are properly formatted with the correct discriminator and parameter encoding for policy validation to work correctly.
The discriminator must match exactly what's defined in the IDL, and parameters must be encoded according to their specified types.

<Accordion title="Anchor-formatted instructions for the above policy examples:">
  <CodeGroup>
    ```typescript TypeScript theme={null}
    import {
      Keypair,
      PublicKey,
      TransactionInstruction,
    } from "@solana/web3.js";
    import { ASSOCIATED_TOKEN_PROGRAM_ID, TOKEN_PROGRAM_ID } from "@solana/spl-token";

    function createAnchorSystemTransferInstruction(
      amount: bigint
    ): TransactionInstruction {
      const testAccount = Keypair.generate().publicKey;
      const transferDiscriminator = Buffer.from([
        163, 52, 200, 231, 140, 3, 69, 186,
      ]);

      const lamportsBuffer = Buffer.alloc(8);
      lamportsBuffer.writeBigUInt64LE(amount, 0);

      const instructionData = Buffer.concat([
        transferDiscriminator,
        lamportsBuffer,
      ]);

      return new TransactionInstruction({
        keys: [
          { pubkey: testAccount, isSigner: true, isWritable: true },
          { pubkey: testAccount, isSigner: false, isWritable: true },
        ],
        programId: new PublicKey("11111111111111111111111111111111"),
        data: instructionData,
      });
    }

    function createAnchorSPLTransferCheckedInstruction(
      amount: number,
      decimals: number
    ): TransactionInstruction {
      const testAccount = Keypair.generate().publicKey;
      const transferCheckedDiscriminator = Buffer.from([119, 250, 202, 24, 253, 135, 244, 121]);

      const amountBuffer = Buffer.alloc(8);
      amountBuffer.writeBigUInt64LE(BigInt(amount), 0);
      const decimalsBuffer = Buffer.alloc(1);
      decimalsBuffer.writeUInt8(decimals, 0);

      const instructionData = Buffer.concat([transferCheckedDiscriminator, amountBuffer, decimalsBuffer]);

      return new TransactionInstruction({
        keys: [
          { pubkey: testAccount, isSigner: false, isWritable: true },
          { pubkey: testAccount, isSigner: false, isWritable: false },
          { pubkey: testAccount, isSigner: false, isWritable: true },
          { pubkey: testAccount, isSigner: true, isWritable: false },
        ],
        programId: TOKEN_PROGRAM_ID,
        data: instructionData
      });
    }

    function createAnchorAssociatedTokenAccountCreateInstruction(): TransactionInstruction {
      const testAccount = Keypair.generate().publicKey;
      const createDiscriminator = Buffer.from([24, 30, 200, 40, 5, 28, 7, 119]);

      return new TransactionInstruction({
        keys: [
          { pubkey: testAccount, isSigner: true, isWritable: true },
          { pubkey: testAccount, isSigner: false, isWritable: true },
          { pubkey: testAccount, isSigner: false, isWritable: false },
          { pubkey: testAccount, isSigner: false, isWritable: false },
          { pubkey: testAccount, isSigner: false, isWritable: false },
          { pubkey: testAccount, isSigner: false, isWritable: false },
        ],
        programId: ASSOCIATED_TOKEN_PROGRAM_ID,
        data: createDiscriminator
      });
    }
    ```

    ```python Python theme={null}
    import struct
    from solders.keypair import Keypair
    from solders.pubkey import Pubkey
    from solders.system_program import ID as SYSTEM_PROGRAM_ID
    from solders.instruction import Instruction, AccountMeta

    def create_anchor_system_transfer_instruction(amount: int) -> Instruction:
        """Create an Anchor-formatted system transfer instruction."""
        test_account = Keypair().pubkey()
        transfer_discriminator = bytes([163, 52, 200, 231, 140, 3, 69, 186])
        
        lamports_buffer = struct.pack("<Q", amount)
        instruction_data = transfer_discriminator + lamports_buffer
        
        return Instruction(
            program_id=SYSTEM_PROGRAM_ID,
            data=instruction_data,
            accounts=[
                AccountMeta(pubkey=test_account, is_signer=True, is_writable=True),
                AccountMeta(pubkey=test_account, is_signer=False, is_writable=True),
            ],
        )

    def create_anchor_spl_transfer_checked_instruction(amount: int, decimals: int) -> Instruction:
        """Create an Anchor-formatted token transfer_checked instruction."""
        test_account = Keypair().pubkey()
        transfer_checked_discriminator = bytes([119, 250, 202, 24, 253, 135, 244, 121])
        
        amount_buffer = struct.pack("<Q", amount)
        decimals_buffer = struct.pack("<B", decimals)
        instruction_data = transfer_checked_discriminator + amount_buffer + decimals_buffer
        
        return Instruction(
            program_id=Pubkey.from_string("TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"),
            data=instruction_data,
            accounts=[
                AccountMeta(pubkey=test_account, is_signer=False, is_writable=True),
                AccountMeta(pubkey=test_account, is_signer=False, is_writable=False),
                AccountMeta(pubkey=test_account, is_signer=False, is_writable=True),
                AccountMeta(pubkey=test_account, is_signer=True, is_writable=False),
            ],
        )

    def create_anchor_associated_token_account_create_instruction() -> Instruction:
        """Create an Anchor-formatted associated token account create instruction."""
        test_account = Keypair().pubkey()
        create_discriminator = bytes([24, 30, 200, 40, 5, 28, 7, 119])
        
        return Instruction(
            program_id=Pubkey.from_string("ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL"),
            data=create_discriminator,
            accounts=[
                AccountMeta(pubkey=test_account, is_signer=True, is_writable=True),
                AccountMeta(pubkey=test_account, is_signer=False, is_writable=True),
                AccountMeta(pubkey=test_account, is_signer=False, is_writable=False),
                AccountMeta(pubkey=test_account, is_signer=False, is_writable=False),
                AccountMeta(pubkey=test_account, is_signer=False, is_writable=False),
                AccountMeta(pubkey=test_account, is_signer=False, is_writable=False),
            ],
        )
    ```
  </CodeGroup>
</Accordion>

<Tip>
  For TypeScript developers working with custom Anchor programs, consider using the [Anchor TypeScript client SDK](https://github.com/solana-foundation/anchor) (`@coral-xyz/anchor`).

  The SDK provides utilities for loading program IDLs, generating type-safe instruction builders, and creating properly formatted transactions, which can simplify the process of working with custom programs in your solData policies.
</Tip>

## Use Cases

The `solData` criterion enables sophisticated policy controls for any Solana program, from native system operations to complex DeFi protocols. By providing custom IDL specifications, you can validate instruction parameters for both your own programs and popular ecosystem protocols.

### Example Ecosystem Program Integration

**DeFi and Trading Protocols:**

* **Jupiter** - Control swap parameters, slippage limits, and route restrictions for decentralized exchanges
* **Raydium** - Set constraints on liquidity provision and farming operations

**Staking and Validation:**

* **Jito** - Govern staking operations, validator selection, and MEV reward distributions
* **Marinade** - Control liquid staking deposits, withdrawals, and stake account management

**NFT and Digital Assets:**

* **Metaplex** - Restrict NFT minting parameters, royalty settings, and marketplace interactions
* **Magic Eden** - Validate NFT marketplace transactions and bid placements

For your own custom programs, `solData` policies provide granular control over inputs to your instruction parameters.

## Key Considerations

### IDL Format Requirements

* Always use Anchor IDL format v0.30+ for compatibility
* Verify IDL structure matches the expected format
* Convert older IDL formats using the Anchor CLI conversion tool
* Ensure discriminator values exactly match the program's instruction identifiers

## What to read next

* [**Policies Overview**](/server-wallets/v2/using-the-wallet-api/policies/overview): Learn about general policy concepts and setup
* [**Solana Policies**](/server-wallets/v2/using-the-wallet-api/policies/solana-policies): Learn about Solana-specific policy examples
* [**v2 Server Wallet Security**](/server-wallets/v2/introduction/security): Learn more about the security features of the CDP v2 Server Wallet
* [**v2 API Reference**](/api-reference/v2/rest-api/policy-engine/list-policies): Explore the API reference for CDP Policies

