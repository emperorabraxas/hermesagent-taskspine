# Integrating Dedicated ETH Staking
Source: https://docs.cdp.coinbase.com/staking/staking-api/protocols/dedicated-eth/usage



<Note>
  Ethereum Pectra support is now live on **Mainnet** and **Hoodi testnet** via the Coinbase Staking API. Try them out and share feedback on [Discord](https://discord.com/invite/cdp).
</Note>

Coinbase Staking API supports **Dedicated ETH Staking** with full mainnet support for Ethereum’s latest upgrade *Pectra*.

This guide covers how to stake, unstake, consolidate, top-up and manage validators — including both pre and post Pectra flows.

### What's New with Pectra

* Stake validators with up to **2048 ETH** (previously 32 ETH max)
* Automatically **compound rewards** for high-balance validators
* Unstake directly via the **execution layer** (partial or full exits)
* **Consolidate** smaller legacy validators into fewer large ones

SDK Availability:

* **Go SDK**: Pectra features available starting version [v0.0.27](https://github.com/coinbase/coinbase-sdk-go/releases/tag/v0.0.27)
* **Node.js SDK**: Pectra features available starting version [v0.24.0](https://github.com/coinbase/coinbase-sdk-nodejs/releases/tag/v0.23.0)

<Info>
  New to Staking API? Start with the [Quickstart Guide](/staking/staking-api/introduction/quickstart.mdx) to learn basic setup and terminology.
</Info>

***

### Stake (Pre & Post Pectra)

You can stake to either **pre-Pectra (0x01)** or **post-Pectra (0x02)** validators by selecting the appropriate withdrawal credential type.

* **Minimum stake:** 32 ETH
* **Maximum (post-Pectra only):** 2048 ETH
* Ensure your external address has enough ETH to cover the stake **plus gas fees**.

The example below illustrates how to perform dedicated ETH staking.

<Note>
  Dedicated ETH Staking can take up to 5 minutes to generate a staking transaction,
  as it involves provisioning dedicated backend infrastructure.
  Until it's ready, the `Transaction` field in the `StakeOperation` will remain empty.
</Note>

<CodeGroup>
  ```typescript Typescript [expandable] theme={null}
  import { Coinbase, ExternalAddress, StakeOptionsMode } from "@coinbase/coinbase-sdk";

  // Create a new external address on the ethereum-hoodi testnet network.
  let address = new ExternalAddress(
      Coinbase.networks.EthereumHoodi,
      "YOUR_WALLET_ADDRESS",
  );

  // Find out how much ETH is available to stake.
  let stakeableBalance = await address.stakeableBalance(
      Coinbase.assets.Eth,
      StakeOptionsMode.NATIVE,
  );

  console.log("Stakeable balance: %s", stakeableBalance)

  // Build a stake operation for 100 ETH.
  // Set withdrawal_credential_type to:
  // - "0x01" for pre-Pectra
  // - "0x02" for post-Pectra (required for balances > 32 ETH)
  let stakingOperation = await address.buildStakeOperation(
      100,
      Coinbase.assets.Eth,
      StakeOptionsMode.NATIVE,
      {"withdrawal_credential_type": "0x02"},
  );

  console.log("Staking Operation ID: %s", stakingOperation.getID())

  // Wait for staking infrastructure to be provisioned and transaction created.
  await stakingOperation.wait();
  ```

  Once the stake operation has been built, relay the transactions to your end-user for signing and broadcasting. Refer to the [Signing and Broadcasting Transactions](/staking/staking-api/protocols/dedicated-eth/usage#signing-and-broadcasting-transactions) section for an example using Ethers.js.

  ```go Go [expandable] theme={null}
  // Create a new external address on the ethereum-hoodi testnet network.
  address := coinbase.NewExternalAddress(coinbase.EthereumHoodi, "YOUR_WALLET_ADDRESS")

  // Find out how much ETH is available to stake.
  stakeableBalance, err := client.GetStakeableBalance(
      ctx,
      coinbase.Eth,
      address,
      coinbase.WithNativeStakingBalanceMode(),
  )
  if err != nil {
      log.Fatal(err)
  }

  log.Printf("Stakeable balance: %s\n", stakeableBalance.Amount().Text('f', 18))

  // Set withdrawal_credential_type to:
  // - "0x01" for pre-Pectra
  // - "0x02" for post-Pectra (required for balances > 32 ETH)
  options := []coinbase.StakingOperationOption{
      coinbase.WithNativeStakingOperationMode(),
      coinbase.With0x02WithdrawalCredentialType(),
  }

  // Build a stake operation for 100 ETH.
  stakingOperation, err := client.BuildStakeOperation(
      ctx,
      big.NewFloat(100),
      coinbase.Eth,
      address,
      options...,
  )
  if err != nil {
      log.Fatalf("error building staking operation: %v", err)
  }

  log.Printf("Staking Operation ID: %s\n", stakingOperation.ID())

  // Wait for staking infrastructure to be provisioned and transaction created.
  if err := client.Wait(
      ctx,
      stakingOperation,
      coinbase.WithWaitTimeoutSeconds(600),
  ); err != nil {
      log.Fatalf("error waiting for staking operation: %v", err)
  }
  ```

  Once the stake operation has been built, relay the transactions to your end-user for signing and broadcasting. Refer to the [Signing and Broadcasting Transactions](/staking/staking-api/protocols/dedicated-eth/usage#signing-and-broadcasting-transactions) section for an example using go-ethereum.
</CodeGroup>

### Unstake (via Execution Layer)

Post-Pectra validators can now be unstaked directly from the **execution layer** using the withdrawal address.
This bypasses the consensus-layer exit process entirely.

Supports both:

* **Partial withdrawals**: Withdraw a portion of a validator’s balance
* **Full exits**: Exit the validator completely and withdraw all funds

#### Partial Withdrawals

<CodeGroup>
  ```typescript Typescript [expandable] theme={null}
  import {
      Coinbase,
      ExternalAddress,
      StakeOptionsMode,
      ExecutionLayerWithdrawalOptionsBuilder,
  } from "@coinbase/coinbase-sdk";
  import Decimal from "decimal.js";

  // Create a new external address on the ethereum-hoodi testnet network
  // corresponding to the withdrawal address of the validators you want
  // to partially withdraw from.
  let withdrawAddr = new ExternalAddress(
      Coinbase.networks.EthereumHoodi,
      "YOUR_WITHDRAWAL_ADDRESS",
  );

  // Configure partial withdrawals for two post-Pectra validators.
  let buildr = new ExecutionLayerWithdrawalOptionsBuilder(withdrawAddr.getNetworkId());
  buildr.addValidatorWithdrawal("YOUR_VALIDATOR_PUBKEY_1", new Decimal("1"));
  buildr.addValidatorWithdrawal("YOUR_VALIDATOR_PUBKEY_2", new Decimal("2"));

  let options = await buildr.build();

  let stakingOperation = await withdrawAddr.buildUnstakeOperation(
      0, // Amount here doesn't matter.
      Coinbase.assets.Eth,
      StakeOptionsMode.NATIVE,
      options,
  );

  console.log("Staking Operation ID: %s", stakingOperation.getID())

  // Wait for the partial withdrawal transactions to be built.
  await stakingOperation.wait();
  ```

  Once the partial withdrawal staking operation has been built, relay the transactions to your end-user for signing and broadcasting. Refer to the [Signing and Broadcasting Transactions](/staking/staking-api/protocols/dedicated-eth/usage#signing-and-broadcasting-transactions) section for an example using Ethers.js.

  ```go Go [expandable] theme={null}
  // Create a new external address on the ethereum-hoodi testnet network
  // corresponding to the withdrawal address of the validators you want
  // to partially withdraw from.
  withdrawAddr := coinbase.NewExternalAddress(
      coinbase.EthereumHoodi,
      "YOUR_WITHDRAWAL_ADDRESS",
  )

  // Configure partial withdrawals for two post-Pectra validators.
  builder, err := coinbase.NewExecutionLayerWithdrawalsOptionBuilder(
      ctx,
      client,
      withdrawAddr,
  )
  if err != nil {
      log.Fatalf("error creating execution layer withdrawals option builder: %v", err)
  }

  // Add a validator withdrawal to the builder.
  err = builder.AddValidatorWithdrawal("YOUR_VALIDATOR_PUBKEY_1", big.NewFloat(1.0))
  if err != nil {
      log.Fatalf("error adding validator withdrawal: %v", err)
  }

  // Add a validator withdrawal to the builder.
  err = builder.AddValidatorWithdrawal("YOUR_VALIDATOR_PUBKEY_2", big.NewFloat(2.0))
  if err != nil {
      log.Fatalf("error adding validator withdrawal: %v", err)
  }

  options := []coinbase.StakingOperationOption{
      coinbase.WithNativeStakingOperationMode(),
      coinbase.WithExecutionLayerWithdrawals(builder),
  }

  stakingOperation, err := client.BuildUnstakeOperation(
      ctx,
      big.NewFloat(0), // Amount here doesn't matter.
      coinbase.Eth,
      withdrawAddr,
      options...,
  )
  if err != nil {
      log.Fatalf("error building staking operation: %v", err)
  }

  log.Printf("Staking Operation ID: %s\n", stakingOperation.ID())

  // Wait for the partial withdrawal transactions to be built.
  if err := client.Wait(
      ctx,
      stakingOperation,
      coinbase.WithWaitTimeoutSeconds(600),
  ); err != nil {
      log.Fatalf("error waiting for staking operation: %v", err)
  }
  ```

  Once the partial withdrawal staking operation has been built, relay the transactions to your end-user for signing and broadcasting. Refer to the [Signing and Broadcasting Transactions](/staking/staking-api/protocols/dedicated-eth/usage#signing-and-broadcasting-transactions) section for an example using go-ethereum.
</CodeGroup>

#### Full Exits

<CodeGroup>
  ```typescript Typescript [expandable] theme={null}
  import {
      Coinbase,
      ExternalAddress,
      StakeOptionsMode,
      ExecutionLayerWithdrawalOptionsBuilder,
  } from "@coinbase/coinbase-sdk";
  import Decimal from "decimal.js";

  // Create a new external address on the ethereum-hoodi testnet network
  // corresponding to the withdrawal address of the validators you want
  // to fully exit.
  let withdrawAddr = new ExternalAddress(
      Coinbase.networks.EthereumHoodi,
      "YOUR_WITHDRAWAL_ADDRESS",
  );

  // Build a full exit staking operation to exit 2 different post Pectra validators.

  let buildr = new ExecutionLayerWithdrawalOptionsBuilder(withdrawAddr.getNetworkId());
  buildr.addValidatorWithdrawal("YOUR_VALIDATOR_PUBKEY_1", new Decimal("0"));
  buildr.addValidatorWithdrawal("YOUR_VALIDATOR_PUBKEY_2", new Decimal("0"));

  let options = await buildr.build();

  let stakingOperation = await withdrawAddr.buildUnstakeOperation(
      0, // Amount here doesn't matter.
      Coinbase.assets.Eth,
      StakeOptionsMode.NATIVE,
      options,
  );

  console.log("Staking Operation ID: %s", stakingOperation.getID())

  // Wait for the full exit transactions to be built.
  await stakingOperation.wait();
  ```

  Once the full exit staking operation has been built, relay the transactions to your end-user for signing and broadcasting. Refer to the [Signing and Broadcasting Transactions](/staking/staking-api/protocols/dedicated-eth/usage#signing-and-broadcasting-transactions) section for an example using Ethers.js.

  ```go Go [expandable] theme={null}
  // Create a new external address on the ethereum-hoodi testnet network
  // corresponding to the withdrawal address of the validators you want
  // to fully exit.
  withdrawAddr := coinbase.NewExternalAddress(
      coinbase.EthereumHoodi,
      "YOUR_WITHDRAWAL_ADDRESS",
  )

  // Build a full exit staking operation to exit 2 different post Pectra validators.

  builder, err := coinbase.NewExecutionLayerWithdrawalsOptionBuilder(
      ctx,
      client,
      withdrawAddr,
  )
  if err != nil {
      log.Fatalf("error creating execution layer withdrawals option builder: %v", err)
  }

  // Add a validator withdrawal to the builder.
  err = builder.AddValidatorWithdrawal("YOUR_VALIDATOR_PUBKEY_1", big.NewFloat(0))
  if err != nil {
      log.Fatalf("error adding validator withdrawal: %v", err)
  }

  // Add a validator withdrawal to the builder.
  err = builder.AddValidatorWithdrawal("YOUR_VALIDATOR_PUBKEY_2", big.NewFloat(0))
  if err != nil {
      log.Fatalf("error adding validator withdrawal: %v", err)
  }

  options := []coinbase.StakingOperationOption{
      coinbase.WithNativeStakingOperationMode(),
      coinbase.WithExecutionLayerWithdrawals(builder),
  }

  stakingOperation, err := client.BuildUnstakeOperation(
      ctx,
      big.NewFloat(0), // Amount here doesn't matter.
      coinbase.Eth,
      withdrawAddr,
      options...,
  )
  if err != nil {
      log.Fatalf("error building staking operation: %v", err)
  }

  log.Printf("Staking Operation ID: %s\n", stakingOperation.ID())

  // Wait for the full exit transactions to be built.
  if err := client.Wait(
      ctx,
      stakingOperation,
      coinbase.WithWaitTimeoutSeconds(600),
  ); err != nil {
      log.Fatalf("error waiting for staking operation: %v", err)
  }
  ```

  Once the full exit staking operation has been built, relay the transactions to your end-user for signing and broadcasting. Refer to the [Signing and Broadcasting Transactions](/staking/staking-api/protocols/dedicated-eth/usage#signing-and-broadcasting-transactions) section for an example using go-ethereum.
</CodeGroup>

### Unstake (via Consensus Layer)

The consensus-layer unstaking process is still supported post-Pectra and works for both **pre-** and **post-Pectra** validators.

To initiate a consensus-layer exit, a [voluntary exit message](https://github.com/ethereum/consensus-specs/blob/dev/specs/phase0/beacon-chain.md#signedvoluntaryexit) must be signed by the validator and broadcast to the Ethereum network.

You have two options when unstaking from external addresses:

* **[Coinbase managed unstake](#coinbase-managed-unstake)** *(recommended)* : Coinbase signs and broadcasts the exit message on your behalf.

* **[User managed unstake](#user-managed-unstake)**: Coinbase provides a pre-signed message, and **you** are responsible for [broadcasting](#broadcasting-exit-messages) it to the consensus layer.

#### Coinbase Managed Unstake

There are two options to build the coinbase managed unstake operation.

##### By Amount

<Note>
  Coinbase managed unstake by amount currently only supports selection of pre Pectra validators for unstaking.
</Note>

For 0x01 validators, this amount should be in multiples of 32. If amount = 64 ETH, we pick 2 0x01 validators and exit them.
This behind the scenes will identify validators to be exited, generate a voluntary exit message per validator, sign it with the
validator's private key and broadcast them for you.

<CodeGroup>
  ```typescript Typescript [expandable] theme={null}
  import { Coinbase, ExternalAddress, StakeOptionsMode } from "@coinbase/coinbase-sdk";

  // Create a new external address on the ethereum-hoodi testnet network.
  let address = new ExternalAddress(
      Coinbase.networks.EthereumHoodi,
      "YOUR_WALLET_ADDRESS",
  );

  // To know how much ETH balance is available for unstaking, use `unstakeableBalance`.
  // Unstakeable balance depends on your CDP account validators, not your address.
  // It's surfaced on the address object for simplicity.
  // Set `withdrawal_credential_type` to 0x01 or 0x02 to query specific validators.
  // By default, it returns the unstakeable balance for 0x01 validators.
  let unstakeableBalance = await address.unstakeableBalance(
      Coinbase.assets.Eth,
      StakeOptionsMode.NATIVE,
      );

  console.log("Unstakeable balance: %s", unstakeableBalance)

  // Build unstake operation for amount = 32 ETH.
  let stakingOperation = await address.buildUnstakeOperation(
      32,
      Coinbase.assets.Eth,
      StakeOptionsMode.NATIVE,
      {"immediate": "true"},
  );

  console.log("Staking Operation ID: %s", stakingOperation.getID())

  // Immediate native eth unstaking is completely handled by the API
  // with no user action needed.
  // Example of polling the unstake operation status until it reaches
  // a terminal state using the SDK.
  await stakingOperation.wait();
  ```

  ```go Go [expandable] theme={null}
  // Create a new external address on the ethereum-hoodi testnet network.
  address := coinbase.NewExternalAddress(coinbase.EthereumHoodi, "YOUR_WALLET_ADDRESS")

  // To know how much ETH balance is available for unstaking, use `unstakeableBalance`.
  // Unstakeable balance depends on your CDP account validators, not your address.
  // It's surfaced on the address object for simplicity.
  // Set `withdrawal_credential_type` to 0x01 or 0x02 to query specific validators.
  // By default, it returns the unstakeable balance for 0x01 validators.
  unstakeableBalance, err := client.GetUnstakeableBalance(
      ctx,
      coinbase.Eth,
      address,
      coinbase.WithNativeStakingBalanceMode(),
  )
  if err != nil {
      log.Fatal(err)
  }

  log.Printf("Unstakeable balance: %s\n", unstakeableBalance.Amount().Text('f', 18))

  // Build unstake operation for amount = 64 ETH.
  stakingOperation, err := client.BuildUnstakeOperation(
      ctx,
      big.NewFloat(64.0),
      coinbase.Eth,
      address,
      coinbase.WithNativeStakingOperationMode(),
      coinbase.WithImmediateUnstake(),
  )
  if err != nil {
      log.Fatalf("error building unstaking operation: %v", err)
  }

  log.Printf("Staking Operation ID: %s\n", stakingOperation.ID())

  // Immediate native eth unstaking is completely handled by the API
  // with no user action needed.
  // Example of polling the unstake operation status until it reaches
  // a terminal state using the SDK.
  if err := client.Wait(
      ctx,
      stakingOperation,
      coinbase.WithWaitTimeoutSeconds(600),
  ); err != nil {
      log.Fatalf("error waiting for staking operation: %v", err)
  }
  ```
</CodeGroup>

##### By Validator

We support unstaking of both pre & post Pectra validators by validator pub keys. The amount is ignored in this case.

<CodeGroup>
  ```typescript Typescript [expandable] theme={null}
  import {
      Coinbase,
      ExternalAddress,
      StakeOptionsMode,
      ConsensusLayerExitOptionBuilder,
  } from "@coinbase/coinbase-sdk";

  // Create a new external address on the ethereum-hoodi testnet network.
  let address = new ExternalAddress(
      Coinbase.networks.EthereumHoodi,
      "YOUR_WALLET_ADDRESS",
  );

  let options: { [key: string]: string } = { immediate: "true" };

  const builder = new ConsensusLayerExitOptionBuilder();
  builder.addValidator("YOUR_VALIDATOR_PUBKEY_1");
  builder.addValidator("YOUR_VALIDATOR_PUBKEY_2");
  options = await builder.build(options);

  let stakingOperation = await address.buildUnstakeOperation(
      0, // Amount here doesn't matter.
      "eth",
      StakeOptionsMode.NATIVE,
      options,
  );

  console.log("Staking Operation ID: %s", stakingOperation.getID())

  // Immediate native eth unstaking is completely handled by the API
  // with no user action needed.
  // Example of polling the unstake operation status until it reaches
  // a terminal state using the SDK.
  await stakingOperation.wait();
  ```

  ```go Go [expandable] theme={null}
  // Create a new external address on the ethereum-hoodi testnet network.
  address := coinbase.NewExternalAddress(coinbase.EthereumHoodi, "YOUR_WALLET_ADDRESS")

  builder := coinbase.NewConsensusLayerExitOptionBuilder()
  builder.AddValidator("YOUR_VALIDATOR_PUBKEY_1")
  builder.AddValidator("YOUR_VALIDATOR_PUBKEY_2")

  options := []coinbase.StakingOperationOption{
      coinbase.WithNativeStakingOperationMode(),
      coinbase.WithConsensusLayerExit(builder),
      coinbase.WithImmediateUnstake(),
  }

  stakingOperation, err := client.BuildUnstakeOperation(
      ctx,
      big.NewFloat(0), // Amount here doesn't matter.
      coinbase.Eth,
      address,
      options...,
  )
  if err != nil {
      log.Fatalf("error building staking operation: %v", err)
  }

  log.Printf("Staking Operation ID: %s\n", stakingOperation.ID())

  // Immediate native eth unstaking is completely handled by the API
  // with no user action needed.
  // Example of polling the unstake operation status until it reaches
  // a terminal state using the SDK.
  if err := client.Wait(
      ctx,
      stakingOperation,
      coinbase.WithWaitTimeoutSeconds(600),
  ); err != nil {
      log.Fatalf("error waiting for staking operation: %v", err)
  }
  ```
</CodeGroup>

Once the unstake operation has completed successfully, congrats you've just exited a validator.

Refer to the [View Validator Information](#view-validator-information) section to monitor your validator status.
When it changes to `WITHDRAWAL_COMPLETE`, your funds should be available in the `withdrawal_address` set during staking.

#### User Managed Unstake

There are 2 options to build the coinbase managed unstake operation.

##### By Amount

<Note>
  User managed unstake by amount currently only supports selection of pre Pectra validators for unstaking.
  If you want to be able to unstake both pre & post Pectra validators, use the "Unstake by Validator" option.
</Note>

For 0x01 validators this amount should be in multiples of 32. If amount = 64 ETH, we pick 2 0x01 validators and exit them.
This behind the scenes will identify validators to be exited, generate a voluntary exit message per validator, sign it with the
validator's private key and broadcast them for you.

<CodeGroup>
  ```typescript Typescript [expandable] theme={null}
  import { Coinbase, ExternalAddress, StakeOptionsMode } from "@coinbase/coinbase-sdk";

  // Create a new external address on the ethereum-hoodi testnet network.
  let address = new ExternalAddress(
      Coinbase.networks.EthereumHoodi,
      "YOUR_WALLET_ADDRESS",
  );

  // To know how much ETH balance is available for unstaking, use `unstakeableBalance`.
  // Unstakeable balance depends on your CDP account validators, not your address.
  // It's surfaced on the address object for simplicity.
  // Set `withdrawal_credential_type` to 0x01 or 0x02 to query specific validators.
  // By default, it returns the unstakeable balance for 0x01 validators.
  let unstakeableBalance = await address.unstakeableBalance(
      Coinbase.assets.Eth,
      StakeOptionsMode.NATIVE,
  );

  console.log("Unstakeable balance: %s", unstakeableBalance)

  // Build unstake operation for amount = 32 ETH.
  let stakingOperation = await address.buildUnstakeOperation(
      32,
      Coinbase.assets.Eth,
      StakeOptionsMode.NATIVE,
  );

  console.log("Staking Operation ID: %s", stakingOperation.getID())

  // Native eth unstaking can take some time as we build the voluntary exit message
  // and have it signed by the validator.
  // Example of polling the unstake operation status until it reaches
  // a terminal state using the SDK.
  await stakingOperation.wait();
  ```

  After unstaking, voluntary exit messages can be read and stored on your end and broadcasted to the network whenever you want to initiate the unstaking process. Refer to the [Broadcasting Exit Messages](#broadcasting-exit-messages) section for an example.

  ```go Go [expandable] theme={null}
  // Create a new external address on the ethereum-hoodi testnet network.
  address := coinbase.NewExternalAddress(coinbase.EthereumHoodi, "YOUR_WALLET_ADDRESS")

  // To know how much ETH balance is available for unstaking, use `unstakeableBalance`.
  // Unstakeable balance depends on your CDP account validators, not your address.
  // It's surfaced on the address object for simplicity.
  // Set `withdrawal_credential_type` to 0x01 or 0x02 to query specific validators.
  // By default, it returns the unstakeable balance for 0x01 validators.
  unstakeableBalance, err := client.GetUnstakeableBalance(
      ctx,
      coinbase.Eth,
      address,
      coinbase.WithNativeStakingBalanceMode(),
  )
  if err != nil {
      log.Fatal(err)
  }

  log.Printf("Unstakeable balance: %s\n", unstakeableBalance.Amount().Text('f', 18))

  // Build unstake operation for amount = 64 ETH.
  stakingOperation, err := client.BuildUnstakeOperation(
      ctx,
      big.NewFloat(64.0),
      coinbase.Eth,
      address,
      coinbase.WithNativeStakingOperationMode(),
  )
  if err != nil {
      log.Fatalf("error building unstaking operation: %v", err)
  }

  log.Printf("Staking Operation ID: %s\n", stakingOperation.ID())

  // Native eth unstaking can take some time as we build the voluntary exit message
  // and have it signed by the validator.
  // Example of polling the unstake operation status until it reaches
  // a terminal state using the SDK.
  if err := client.Wait(
      ctx,
      stakingOperation,
      coinbase.WithWaitTimeoutSeconds(600),
  ); err != nil {
      log.Fatalf("error waiting for staking operation: %v", err)
  }
  ```

  After unstaking, voluntary exit messages can be read and stored on your end and broadcasted to the network whenever you want to initiate the unstaking process. Refer to the [Broadcasting Exit Messages](#broadcasting-exit-messages) section for an example.
</CodeGroup>

##### By Validator

We support unstaking of both pre & post Pectra validators by validator pub keys. The amount is ignored in this case.

<CodeGroup>
  ```typescript Typescript [expandable] theme={null}
  import {
      Coinbase,
      ExternalAddress,
      StakeOptionsMode,
      ConsensusLayerExitOptionBuilder,
  } from "@coinbase/coinbase-sdk";

  // Create a new external address on the ethereum-hoodi testnet network.
  let address = new ExternalAddress(
      Coinbase.networks.EthereumHoodi,
      "YOUR_WALLET_ADDRESS",
  );

  const builder = new ConsensusLayerExitOptionBuilder();
  builder.addValidator("YOUR_VALIDATOR_PUBKEY_1");
  builder.addValidator("YOUR_VALIDATOR_PUBKEY_2");
  let options = await builder.build();

  let stakingOperation = await address.buildUnstakeOperation(
      0, // Amount here doesn't matter.
      "eth",
      StakeOptionsMode.NATIVE,
      options,
  );

  console.log("Staking Operation ID: %s", stakingOperation.getID())

  // Native eth unstaking can take some time as we build the voluntary exit message
  // and have it signed by the validator.
  // Example of polling the unstake operation status until it reaches
  // a terminal state using the SDK.
  await stakingOperation.wait();
  ```

  After unstaking, voluntary exit messages can be read and stored on your end and broadcasted to the network whenever you want to initiate the unstaking process. Refer to the [Broadcasting Exit Messages](#broadcasting-exit-messages) section for an example.

  ```go Go [expandable] theme={null}
  // Create a new external address on the ethereum-hoodi testnet network.
  address := coinbase.NewExternalAddress(coinbase.EthereumHoodi, "YOUR_WALLET_ADDRESS")

  builder := coinbase.NewConsensusLayerExitOptionBuilder()
  builder.AddValidator("YOUR_VALIDATOR_PUBKEY_1")
  builder.AddValidator("YOUR_VALIDATOR_PUBKEY_2")

  options := []coinbase.StakingOperationOption{
  coinbase.WithNativeStakingOperationMode(),
  coinbase.WithConsensusLayerExit(builder),
  }

  stakingOperation, err := client.BuildUnstakeOperation(
      ctx,
      big.NewFloat(0), // Amount here doesn't matter.
      coinbase.Eth,
      address,
      options...,
  )
  if err != nil {
      log.Fatalf("error building staking operation: %v", err)
  }

  log.Printf("Staking Operation ID: %s\n", stakingOperation.ID())

  // Native eth unstaking can take some time as we build the voluntary exit message
  // and have it signed by the validator.
  // Example of polling the unstake operation status until it reaches
  // a terminal state using the SDK.
  if err := client.Wait(
      ctx,
      stakingOperation,
      coinbase.WithWaitTimeoutSeconds(600),
  ); err != nil {
      log.Fatalf("error waiting for staking operation: %v", err)
  }
  ```

  After unstaking, voluntary exit messages can be read and stored on your end and broadcasted to the network whenever you want to initiate the unstaking process. Refer to the [Broadcasting Exit Messages](#broadcasting-exit-messages) section for an example.
</CodeGroup>

### Validator Consolidation

You can consolidate smaller **pre-Pectra (0x01)** validators into larger **post-Pectra (0x02)** validators, without manually unstaking and re-staking.

This reduces the number of active validators you manage and enables **auto-compounding rewards**.

Two modes:

* **Self-consolidation**: Convert a validator from 0x01 → 0x02 by setting the same pubkey as both source and target.
* **Merge**: Consolidate a single 0x01 validator under an existing 0x02 validator.

<CodeGroup>
  ```typescript Typescript [expandable] theme={null}
  import { Coinbase, ExternalAddress } from "@coinbase/coinbase-sdk";

  // Create a new external address on the ethereum-hoodi testnet network.
  let withdrawAddr = new ExternalAddress(
      Coinbase.networks.EthereumHoodi,
      "YOUR_WALLET_ADDRESS",
  );

  // Build a validator consolidate operation.
  // To perform self consolidation, set the source and target validator public
  // keys to the same value. This converts existing 0x01 validators to 0x02.
  // To perform consolidation, set the source and target validator public keys
  // to different values. This consolidates existing 0x01 validators under an
  // existing 0x02 validator.
  let stakingOperation = await withdrawAddr.buildValidatorConsolidationOperation({
      "source_validator_pubkey": "YOUR_SOURCE_VALIDATOR_PUBKEY",
      "target_validator_pubkey": "YOUR_TARGET_VALIDATOR_PUBKEY"
  });

  console.log("Staking Operation ID: %s", stakingOperation.getID())

  await stakingOperation.wait();
  ```

  Once the stake operation has been built, relay the transactions to your end-user for signing and broadcasting. Refer to the [Signing and Broadcasting Transactions](/staking/staking-api/protocols/dedicated-eth/usage#signing-and-broadcasting-transactions) section for an example using Ethers.js.

  ```go Go [expandable] theme={null}
  // Create a new external address on the ethereum-hoodi testnet network.
  withdrawAddr := coinbase.NewExternalAddress(
      coinbase.EthereumHoodi,
      "YOUR_WALLET_ADDRESS",
  )

  // Set source and target validator public keys that need to be consolidated.
  options := []coinbase.StakingOperationOption{
      coinbase.WithSourceValidatorPublicKey("YOUR_SOURCE_VALIDATOR_PUBKEY"),
      coinbase.WithTargetValidatorPublicKey("YOUR_TARGET_VALIDATOR_PUBKEY"),
  }

  // Build a validator consolidate operation.
  // To perform self consolidation, set the source and target validator public
  // keys to the same value. This converts existing 0x01 validators to 0x02.
  // To perform consolidation, set the source and target validator public keys
  // to different values. This consolidates existing 0x01 validators under an
  // existing 0x02 validator.
  stakingOperation, err := client.BuildValidatorConsolidationOperation(
      ctx,
      address,
      options...,
  )
  if err != nil {
      log.Fatalf("error building staking operation: %v", err)
  }

  log.Printf("Staking Operation ID: %s\n", stakingOperation.ID())

  if err := client.Wait(
      ctx,
      stakingOperation,
      coinbase.WithWaitTimeoutSeconds(600),
  ); err != nil {
      log.Fatalf("error waiting for staking operation: %v", err)
  }
  ```

  Once the stake operation has been built, relay the transactions to your end-user for signing and broadcasting. Refer to the [Signing and Broadcasting Transactions](/staking/staking-api/protocols/dedicated-eth/usage#signing-and-broadcasting-transactions) section for an example using go-ethereum.
</CodeGroup>

### Validator Top-Ups

Validator top-ups allow you to add more ETH to an existing validator. This is useful for increasing the validator's effective balance and rewards.

<CodeGroup>
  ```typescript Typescript [expandable] theme={null}
  import { Coinbase, ExternalAddress, StakeOptionsMode } from "@coinbase/coinbase-sdk";

  // Create a new external address on the ethereum-hoodi testnet network.
  let address = new ExternalAddress(
      Coinbase.networks.EthereumHoodi,
      "YOUR_WALLET_ADDRESS",
  );

  // Build a top-up stake operation.
  // This is similar to a normal stake operation, but the amount is topped-up on an
  // existing validator provided by the `top_up_validator_pubkey` option instead of
  // creating a new validator.
  let stakingOperation = await address.buildStakeOperation(
      2, // Amount to top-up.
      Coinbase.assets.Eth,
      StakeOptionsMode.NATIVE,
      {"top_up_validator_pubkey": "YOUR_VALIDATOR_PUBKEY"},
  );

  console.log("Staking Operation ID: %s", stakingOperation.getID())

  await stakingOperation.wait();
  ```

  Once the top-up stake operation has been built, relay the transactions to your end-user for signing and broadcasting. Refer to the [Signing and Broadcasting Transactions](/staking/staking-api/protocols/dedicated-eth/usage#signing-and-broadcasting-transactions) section for an example using Ethers.js.

  ```go Go [expandable] theme={null}
  // Create a new external address on the ethereum-hoodi testnet network.
  address := coinbase.NewExternalAddress(coinbase.EthereumHoodi, "YOUR_WALLET_ADDRESS")

  // Set the validator public key that needs to be topped up.
  options := []coinbase.StakingOperationOption{
      coinbase.WithNativeStakingOperationMode(),
      coinbase.WithTopUpValidatorPublicKey("YOUR_VALIDATOR_PUBKEY"),
  }

  // Build a top-up stake operation.
  // This is similar to a normal stake operation, but the amount is topped-up on an
  // existing validator provided by the `top_up_validator_pubkey` option instead of
  // creating a new validator.
  stakingOperation, err := client.BuildStakeOperation(
      ctx,
      big.NewFloat(2), // Amount to top-up.
      coinbase.Eth,
      address,
      options...,
  )
  if err != nil {
      log.Fatalf("error building staking operation: %v", err)
  }

  log.Printf("Staking Operation ID: %s\n", stakingOperation.ID())

  if err := client.Wait(
      ctx,
      stakingOperation,
      coinbase.WithWaitTimeoutSeconds(600),
  ); err != nil {
      log.Fatalf("error waiting for staking operation: %v", err)
  }
  ```

  Once the top-up stake operation has been built, relay the transactions to your end-user for signing and broadcasting. Refer to the [Signing and Broadcasting Transactions](/staking/staking-api/protocols/dedicated-eth/usage#signing-and-broadcasting-transactions) section for an example using go-ethereum.
</CodeGroup>

### View Staking Rewards

You can view historical staking rewards by validator address. This helps you track earnings over time, including USD-converted value and conversion rates.
Refer to the [StakingReward docs](https://coinbase.github.io/coinbase-sdk-nodejs/classes/coinbase_staking_reward.StakingReward.html) for a full list of supported methods.

Look up staking rewards for a list of addresses.

<CodeGroup>
  ```typescript Typescript [expandable] theme={null}
  import { Coinbase, StakingReward } from "@coinbase/coinbase-sdk";

  let now = new Date();
  let tenDaysAgo = new Date();
  tenDaysAgo.setDate(now.getDate() - 10);

  let rewards = await StakingReward.list(
      Coinbase.networks.EthereumMainnet, Coinbase.assets.Eth,
      ["VALIDATOR_ADDRESS1", "VALIDATOR_ADDRESS2"],
      tenDaysAgo.toISOString(), now.toISOString(),
  );

  // Loop through the rewards and print each staking reward
  rewards.forEach(reward => console.log(reward.toString()));
  ```

  View the USD value of rewards including conversion price and time.

  ```typescript theme={null}
  // Loop through the rewards and print each staking reward's USD conversion information
  rewards.forEach(reward => {
      console.log(
          `USD value: ${reward.usdValue()},
          Conversion price: ${reward.conversionPrice().toString()},
          Conversion time: ${reward.conversionTime().toISOString()}`,
      );
  });
  ```

  ```go Go [expandable] theme={null}
  rewards, err := client.ListStakingRewards(
      context.Background(),
      coinbase.Eth,
      []coinbase.Address{*validator1, *validator2},
      time.Now().Add(-10*24*time.Hour),
      time.Now(),
      api.STAKINGREWARDFORMAT_USD,
  )
  if err != nil {
      log.Fatal(err)
  }

  // Loop through the rewards and print each staking reward.
  for _, reward := range rewards {
      log.Printf("Staking reward: %s", reward.ToString())
  }
  ```
</CodeGroup>

### View Historical Staking Balances

Detailed information about the historical staking balances for given validator address, including bonded and unbonded stakes.

* **Bonded Stakes**: The total amount of stake that is actively earning rewards to this address. Pending active stake is not included.
* **Unbonded Balance**: This amount includes any ETH balance that is under the control of the wallet address but is not actively staked.
  Refer to the [StakingBalance docs](https://coinbase.github.io/coinbase-sdk-nodejs/classes/coinbase_staking_balance.StakingBalance.html) for a full list of supported methods.

  Look up staking balances for an address.

<CodeGroup>
  ```typescript Typescript [expandable] theme={null}
  import { Coinbase, StakingBalance } from "@coinbase/coinbase-sdk";

  let now = new Date();
  let tenDaysAgo = new Date();
  tenDaysAgo.setDate(now.getDate() - 10);

  let stakingBalances = await StakingBalance.list(
      Coinbase.networks.EthereumMainnet, Coinbase.assets.Eth,
      "VALIDATOR_ADDRESS",
      tenDaysAgo.toISOString(), now.toISOString(),
  );

  // Loop through the historical staking balances and print each balance
  stakingBalances.forEach(stakingBalance => console.log(stakingBalance.toString()));
  ```

  Look up staking balances for an address.

  Refer to the [ListHistoricalStakingBalances documentation](https://pkg.go.dev/github.com/coinbase/coinbase-sdk-go/pkg/coinbase#Client.ListHistoricalStakingRewards) for a full list of supported methods.

  Look up historical staking balances for an address.

  ```go Go [expandable] theme={null}
  address = coinbase.NewExternalAddress(
    coinbase.EthereumMainnet,
    "VALIDATOR_ADDRESS",
  )
  stakingBalances, err := client.ListHistoricalStakingBalances(
    ctx,
    coinbase.Eth,
    address,
    time.Now().Add(-10*24*time.Hour),
    time.Now(),
  )
  if err != nil {
    log.Fatalf("error listing staking balances: %v", err)
  }

  // Loop through the staking balances and print
  for _, stakingBalance := range stakingBalances {
    fmt.Println(stakingBalance.String())
  }
  ```
</CodeGroup>

## Validator Information

### View Validator Information

Detailed information is available for any validators that you've created. The validator status (i.e. `provisioned`, `active`, etc.) is available in the response and is printed to stdout in the example below.
The Validator object documentation is available [here](https://coinbase.github.io/coinbase-sdk-nodejs/classes/coinbase_validator.Validator.html) and the ListValidators documentation is available [here](https://pkg.go.dev/github.com/coinbase/coinbase-sdk-go/pkg/coinbase#Client.ListValidators)

<CodeGroup>
  ```typescript Typescript  theme={null}
  // Get the validators that you've provisioned for staking.
  const validators = await Validator.list(Coinbase.networks.EthereumHoodi, Coinbase.assets.Eth);

  // Loop through the validators and print each validator
  validators.forEach(validator => {
      console.log(validator.toString());
  });
  ```

  ```go Go  theme={null}
  // Get the validators that you've provisioned for staking.
  validators := client.ListValidator(ctx, coinbase.EthereumHoodi, coinbase.Eth)

  // Loop through the validators and print each validator
  for _, validator := range validators {
    fmt.Println(validator.String())
  }
  ```
</CodeGroup>

<Accordion title="Example output">
  Your validators will be listed with their respective statuses.

  ```text wrap theme={null}
  Id: 0x984209f61e2507de65de2b0b08ca9cb02c66fb5deab5eb780bfe298b4870e5babd942624c9028cb7820577a6f52ac2d2, Status: provisioned
  Id: 0xa3fc791b5abb4b83fe0e9fe2f6bc5a2728f967c5e845dd353cfac6d9ed4677ad39aa32ee25a1dbdaad8248d71ee1e3a4, Status: active
  Id: 0xadc25472f45a72446d0b5f7b5ec5760db14b198a21a8b0ad40ec673365c54ba1688ad0913f171135a94d4ce1f0ee684f, Status: active
  Id: 0x8071b39b9cfaefc094aff22c76a30f41709ed18f00b36efd63c7c64c644b3482bdfad5018fa32246af1a6c96943c750c, Status: active
  Id: 0x881eb088e400920706bf3281fcabd23bbea081d818c8a60f91faa1f2a1f2c8170b5a89f355ef832d05d8d1685c3e7a52, Status: unavailable
  ```
</Accordion>

### Validator Statuses

A validator can have the following statuses, provided in the `status` field of the response:

| Status               | Description                                                                                                                                                                             | Onchain State Equivalent                 | Action Required                                     |
| -------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------- | --------------------------------------------------- |
| Provisioning         | Validator is being created by Coinbase                                                                                                                                                  | :no\_entry\_sign: (Coinbase Only Status) | Wait :hourglass\_flowing\_sand:                     |
| Provisioned          | Validator has been created by Coinbase and is ready for a deposit                                                                                                                       | :no\_entry\_sign: (Coinbase Only Status) | Sign and broadcast the provided deposit transaction |
| Deposited            | Deposit transaction has been signed, broadcasted, and finalized on the Ethereum network                                                                                                 | :no\_entry\_sign: (Coinbase Only Status) | Wait :hourglass\_flowing\_sand:                     |
| Pending              | Validator is in the activation queue. This means the Ethereum network has successfully executed the deposit transaction                                                                 | `pending_queued`                         | Wait :hourglass\_flowing\_sand:                     |
| Active               | Validator is active and earning rewards                                                                                                                                                 | `active_ongoing`                         | None                                                |
| Exiting              | Validator is in the exit queue. The validator is still earning rewards                                                                                                                  | `active_exiting`                         | Wait :hourglass\_flowing\_sand:                     |
| Exited               | Validator is waiting to enter the withdrawal queue. This means the validator has exited the active set and rewards are no longer being earned.                                          | `exited_unslashed`                       | Wait :hourglass\_flowing\_sand:                     |
| Withdrawal Available | Validator is in the withdrawal queue. The network will sweep available funds to the `withdrawal_address` on a predetermined schedule                                                    | `withdrawal_possible`                    | Wait :hourglass\_flowing\_sand:                     |
| Withdrawal Complete  | Validator has completed its lifecycle. It no longer has any validating responsibilities and the available funds (rewards and initial stake) have been swept to the `withdrawal_address` | `withdrawal_done`                        | None                                                |
| Unavailable          | Validator was provisioned, but a deposit transaction was never broadcasted. Coinbase has spun down the provisioned validator                                                            | :no\_entry\_sign: (Coinbase Only Status) | None                                                |
| Active Slashed       | Validator has been slashed in a previous epoch. The validator is still in the active set, but rewards cannot be earned and a voluntary exit cannot be performed                         | `active_slashed`                         | Wait :hourglass\_flowing\_sand:                     |
| Exited Slashed       | Validator has been slashed in a previous epoch. The validator has exited the active set                                                                                                 | `exited_slashed`                         | None                                                |

### Filtering By Validator Statuses

You can filter the list of validators to view all validators with a specific status.

<CodeGroup>
  ```typescript Typescript  theme={null}
  // Show all your validators with an active status.
  const validators = await Validator.list(
      Coinbase.networks.EthereumHoodi,
      Coinbase.assets.Eth,
      ValidatorStatus.ACTIVE,
  );
  ```

  ```go Go  theme={null}
  // Get the validators that you've provisioned for staking.
  validators := client.ListValidator(
    ctx,
    coinbase.EthereumHoodi,
    coinbase.Eth,
    coinbase.WithListValidatorsStatusOption(coinbase.ValidatorStatusActive),
  )
  ```
</CodeGroup>

<Accordion title="Example output">
  Your validators will be listed only if the status is active.

  ```text wrap theme={null}
  Id: 0xa3fc791b5abb4b83fe0e9fe2f6bc5a2728f967c5e845dd353cfac6d9ed4677ad39aa32ee25a1dbdaad8248d71ee1e3a4, Status: active
  Id: 0xadc25472f45a72446d0b5f7b5ec5760db14b198a21a8b0ad40ec673365c54ba1688ad0913f171135a94d4ce1f0ee684f, Status: active
  Id: 0x8071b39b9cfaefc094aff22c76a30f41709ed18f00b36efd63c7c64c644b3482bdfad5018fa32246af1a6c96943c750c, Status: active
  ```
</Accordion>

## Broadcasting Exit Messages

The example below broadcasts pre-signed voluntary exit messages surfaced during an unstake process. Ethereum validator exit messages are special transaction types which are pre-signed by the validator keys and must be broadcast directly to the consensus layer.

<CodeGroup>
  ```typescript Typescript  theme={null}
  // For Hoodi, publicly available RPC URL's can be
  // found here https://chainlist.org/chain/560048
  stakingOperation.getSignedVoluntaryExitMessages().forEach(async signedVoluntaryExitMessage => {
      let resp = await axios.post("HOODI_RPC_URL/eth/v1/beacon/pool/voluntary_exits", signedVoluntaryExitMessage)
      console.log(resp.status);
  });
  ```

  ```go Go  theme={null}
  exitMessages, err := stakingOperation.GetSignedVoluntaryExitMessages()
  if err != nil {
      log.Fatalf("error getting signed voluntary exit messages: %v", err)
  }

  for _, exitMessage := range exitMessages {
  // For Hoodi, publicly available RPC URL's can be
  // found here https://chainlist.org/chain/560048
  url := fmt.Sprintf("%s/eth/v1/beacon/pool/voluntary_exits", rpcURL)

  resp, err := http.Post(url, "application/json", bytes.NewBuffer([]byte(exitMessage)))
  if err != nil {
      log.Fatalf("error sending exit message: %v", err)
  }
  defer resp.Body.Close()

  log.Printf("Response status: %s\n", resp.Status)
  }
  ```
</CodeGroup>

## Signing and Broadcasting Transactions

The example below signs and broadcasts transactions surfaced via the staking operation resource.
These are standard execution-layer EIP-1159 transactions and follow the normal Ethereum signing flow.

<CodeGroup>
  ```typescript Typescript  theme={null}
  // Load your wallet's private key from which you initiated the above stake operation.
  const wallet = new ethers.Wallet("YOUR_WALLET_PRIVATE_KEY");

  // Sign the transactions within staking operation resource with your wallet.
  await stakingOperation.sign(wallet);

  // For Hoodi, publicly available RPC URL's can be
  // found here https://chainlist.org/chain/560048
  const provider = new ethers.JsonRpcProvider("HOODI_RPC_URL");

  // Broadcast each of the signed transactions to the network.
  stakingOperation.getTransactions().forEach(async tx => {
  let resp = await provider.broadcastTransaction(tx.getSignedPayload()!);
      console.log(resp);
  });
  ```

  ```go Go  theme={null}
  // Load your wallet's private key from which you initiated the above stake operation.
  key, err := crypto.HexToECDSA("YOUR_WALLET_PRIVATE_KEY")
  if err != nil {
      log.Fatal(err)
  }

  // Sign the transactions within staking operation resource with your private key.
  err = stakingOperation.Sign(key)
  if err != nil {
      log.Fatal(err)
  }

  // For Hoodi, publicly available RPC URL's can be
  // found here https://chainlist.org/chain/560048
  ethClient, err := ethclient.Dial("HOODI_RPC_URL")
  if err != nil {
      log.Fatal(err)
  }

  // Broadcast each of the signed transactions to the network.
  for _, transaction := range stakeOperation.Transactions() {
      rawTx, ok := transaction.Raw().(*types.Transaction)
      if !ok {
          log.Fatal("Failed to cast to *types.Transaction")
      }
      if err := ethClient.SendTransaction(context.Background(), rawTx); err != nil {
          log.Fatal(err)
      }
      println(fmt.Sprintf("Broadcasted transaction hash: %s", rawTx.Hash().Hex()))
  }
  ```
</CodeGroup>

