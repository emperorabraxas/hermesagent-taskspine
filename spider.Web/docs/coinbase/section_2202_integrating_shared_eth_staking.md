# Integrating Shared ETH Staking
Source: https://docs.cdp.coinbase.com/staking/staking-api/protocols/shared-eth/usage



Shared ETH Staking enables users to stake with any amount of ETH.

See the [quickstart](/staking/staking-api/introduction/quickstart) to familiarize yourself with Coinbase Staking API and basic usage.

<Info>
  Currently, Shared ETH staking only supports addresses used with the Coinbase Staking API specifically.

  Coinbase App addresses and Coinbase Prime addresses are not supported.
</Info>

The supported staking model uses an address model where the private keys are **not** managed by the Coinbase SDK, referred to as `External Address` in the CDP SDK. Developers are responsible for managing their own wallets. All signing operations must be completed off-platform.

## Stake

To stake, **ensure that the external address contains enough ETH on the network you are using** to cover the stake amount and network transaction fees. To fund your Hoodi testnet address with ETH, the SDK provides a faucet method.

<CodeGroup>
  ```typescript Typescript theme={null}
  import { Coinbase, ExternalAddress, StakeOptionsMode } from "@coinbase/coinbase-sdk";

  // Create a new external address on the ethereum-hoodi testnet network.
  let address = new ExternalAddress(Coinbase.networks.EthereumHoodi, "YOUR_WALLET_ADDRESS");

  // Find out how much ETH is available to stake.
  let stakeableBalance = await address.stakeableBalance(Coinbase.assets.Eth, StakeOptionsMode.PARTIAL);

  // Build a stake operation for an amount <= stakeableBalance, in this case 0.005 ETH.
  let stakeOperation = await address.buildStakeOperation(0.005, Coinbase.assets.Eth, StakeOptionsMode.PARTIAL);
  ```

  ```go Go theme={null}
  // Create a new external address on the `ethereum-hoodi` testnet network.
  address := coinbase.NewExternalAddress(coinbase.EthereumHoodi, "YOUR_WALLET_ADDRESS")

  // Get the amount of ETH available to stake.
  stakeableBalance, err := client.GetStakeableBalance(ctx, coinbase.Eth, address, coinbase.WithStakingBalanceMode(coinbase.StakingOperationModePartial))
  if err != nil {
      log.Fatal(err)
  }

  // Build a stake operation for an amount <= stakeableBalance, in this case 0.005 ETH.
  stakeOperation, err := client.BuildStakeOperation(
      context.Background(),
      big.NewFloat(0.005),
      coinbase.Eth,
      address,
      coinbase.WithStakingOperationMode(coinbase.StakingOperationModePartial),
  )
  if err != nil {
      log.Fatal(err)
  }
  ```
</CodeGroup>

Once the stake operation has been built, relay the transactions to your end-user for signing and broadcasting. Refer to the [Signing and Broadcasting Transactions](#signing-and-broadcasting-transactions) section for an Ethers.js example.

Refer to the [ExternalAddress documentation](https://coinbase.github.io/coinbase-sdk-nodejs/classes/coinbase_address_external_address.ExternalAddress.html) for a full list of supported methods.

## Unstake

Unstake is the first part of a two-step process to withdraw your staked assets. This step involves submitting an exit request to the network. **Processing time varies** based on the unstake request volume on the shared ETH staking pool. In periods of high demand, wait times follow the native Ethereum validator exit queue — check [validatorqueue.com (see Exit Queue Wait)](https://validatorqueue.com) for current estimates.

<CodeGroup>
  ```typescript Typescript theme={null}
  import { Coinbase, ExternalAddress, StakeOptionsMode } from "@coinbase/coinbase-sdk";

  // Create a new external address on the ethereum-hoodi testnet network.
  let address = new ExternalAddress(Coinbase.networks.EthereumHoodi, "YOUR_WALLET_ADDRESS");

  // Since the time you first staked, it is possible that the amount of staked ETH has increased.
  // To determine the amount of ETH available to unstake, use the `unstakeableBalance` method as shown below.
  let unstakeableBalance = await address.unstakeableBalance(Coinbase.assets.Eth, StakeOptionsMode.PARTIAL);

  // Build an unstake operation for an amount <= unstakeableBalance, in this case 0.005 ETH.
  let unstakeOperation = await address.buildUnstakeOperation(0.005, Coinbase.assets.Eth, StakeOptionsMode.PARTIAL);
  ```

  ```go Go theme={null}
  // Create a new external address on the `ethereum-hoodi` testnet network.
  address := coinbase.NewExternalAddress(coinbase.EthereumHoodi, "YOUR_WALLET_ADDRESS")

  // Since the time you first staked, it is possible that the amount of staked ETH has increased.
  // To determine the amount of ETH available to unstake, use the `unstakeableBalance` method as shown below:
  unstakeableBalance, err := client.GetUnstakeableBalance(ctx, coinbase.Eth, address, coinbase.WithStakingBalanceMode(coinbase.StakingOperationModePartial))
  if err != nil {
      log.Fatal(err)
  }

  // Build an unstake operation for an amount <= unstakeableBalance, in this case 0.005 ETH.
  unstakeOperation, err := client.BuildUnstakeOperation(
      context.Background(),
      big.NewFloat(0.005),
      coinbase.Eth,
      address,
      coinbase.WithStakingOperationMode(coinbase.StakingOperationModePartial),
  )
  if err != nil {
      log.Fatal(err)
  }
  ```
</CodeGroup>

Once the unstake operation has been built, relay the transactions to your end-user for signing and broadcasting. Refer to the [Signing and Broadcasting Transactions](#signing-and-broadcasting-transactions) section for an Ethers.js example.

Refer to the [ExternalAddress documentation](https://coinbase.github.io/coinbase-sdk-nodejs/classes/coinbase_address_external_address.ExternalAddress.html) for a full list of supported methods.

## Claim Stake

Once your exit request has been processed by the network you may proceed with the Claim Stake method below.

<CodeGroup>
  ```typescript Typescript theme={null}
  import { Coinbase, ExternalAddress, StakeOptionsMode } from "@coinbase/coinbase-sdk";

  // Create a new external address on the ethereum-hoodi testnet network.
  let address = new ExternalAddress(Coinbase.networks.EthereumHoodi, "YOUR_WALLET_ADDRESS");

  // Check if there is any staked balance available to claim.
  let claimableBalance = await address.claimableBalance(Coinbase.assets.Eth, StakeOptionsMode.PARTIAL);

  // Build a claim_stake operation for an amount = claimableBalance.
  // The claim stake operation aims to claim all the exitable ETH available at that point in time,
  // which may have been requested from multiple previous unstake attempts.
  let claimStakeOperation = await address.buildClaimStakeOperation(claimableBalance, Coinbase.assets.Eth, StakeOptionsMode.PARTIAL);
  ```

  ```go Go theme={null}
  // Create a new external address on the `ethereum-hoodi` testnet network.
  address := coinbase.NewExternalAddress(coinbase.EthereumHoodi, "YOUR_WALLET_ADDRESS")

  // Check if there is any staked balance available to claim.
  claimableBalance, err := client.GetClaimableBalance(ctx, coinbase.Eth, address, coinbase.WithStakingBalanceMode(coinbase.StakingOperationModePartial))
  if err != nil {
      log.Fatal(err)
  }

  // Build a claim_stake operation for an amount = claimableBalance.
  // The claim stake operation aims to claim all the exitable ETH available at that point in time,
  // which may have been requested from multiple previous unstake attempts.
  claimStakeOperation, err := client.BuildClaimStakeOperation(
      context.Background(),
      claimableBalance.Amount(),
      coinbase.Eth,
      address,
      coinbase.WithStakingOperationMode(coinbase.StakingOperationModePartial),
  )
  if err != nil {
      log.Fatal(err)
  }
  ```
</CodeGroup>

Once the claim stake operation has been built, relay the transactions to your end-user for signing and broadcasting. Refer to the [Signing and Broadcasting Transactions](#signing-and-broadcasting-transactions) section for an Ethers.js example.
Refer to the [ExternalAddress documentation](https://coinbase.github.io/coinbase-sdk-nodejs/classes/coinbase_address_external_address.ExternalAddress.html) for a full list of supported methods.

## View Staking Rewards

After staking your ETH, reward will begin to accrue on your address. These rewards can be listed via the `stakingRewards` call.
Refer to the [StakingRewards documentation](https://coinbase.github.io/coinbase-sdk-nodejs/classes/coinbase_address_external_address.ExternalAddress.html#stakingRewards) for an explanation of the method's parameters.

Look up staking rewards for a specific address.

<CodeGroup>
  ```typescript Typescript theme={null}
  import { Coinbase, ExternalAddress } from "@coinbase/coinbase-sdk";

  // Create a new external address on the ethereum-mainnet network for which you want to view staking rewards.
  let address = new ExternalAddress(Coinbase.networks.EthereumMainnet, "YOUR_WALLET_ADDRESS");

  // Get the rewards earned from staking in the last 1 week (default window).
  // Note that it can take upto a day for new rewards to show up.
  let rewards = await address.stakingRewards(Coinbase.assets.Eth);

  // Loop through the rewards and print each staking reward.
  rewards.forEach(reward => console.log(reward.toString()));
  ```

  Look up staking rewards for a list of addresses.

  ```typescript theme={null}
  import { Coinbase, StakingReward } from "@coinbase/coinbase-sdk";

  let rewards = await StakingReward.list(
      Coinbase.networks.EthereumMainnet, Coinbase.assets.Eth,
      ["ADDRESS1", "ADDRESS2"],
      tenDaysAgo.toISOString(), now.toISOString(),
  );

  // Loop through the rewards and print each staking reward.
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

  ```go Go theme={null}
  // Create a new external address on the `ethereum-hoodi` network for which you want to view staking rewards.
  address := coinbase.NewExternalAddress(coinbase.EthereumHoodi, "YOUR_WALLET_ADDRESS")

  // Get the rewards earned from staking in the last 10 days.
  // Note that it can take upto a day for new rewards to show up.
  rewards, err := client.ListStakingRewards(
      context.Background(),
      coinbase.Eth,
      []coinbase.Address{*address},
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

  Look up staking rewards for a list of addresses.

  ```go theme={null}
  rewards, err := client.ListStakingRewards(
      context.Background(),
      coinbase.Eth,
      []coinbase.Address{*address1, *address2},
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

## Signing and Broadcasting Transactions

Here's an example of how to sign and broadcast transactions surfaced via the staking operation resource.

<CodeGroup>
  ```typescript Typescript theme={null}
  // Load your wallet's private key from which you initiated the above stake operation.
  const wallet = new ethers.Wallet("YOUR_WALLET_PRIVATE_KEY");

  // Sign the transactions within staking operation resource with your wallet.
  await stakingOperation.sign(wallet);

  // For Hoodi, publicly available RPC URL's can be found here https://chainlist.org/chain/560048
  const provider = new ethers.JsonRpcProvider("HOODI_RPC_URL");

  // Broadcast each of the signed transactions to the network.
  stakingOperation.getTransactions().forEach(async tx => {
      let resp = await provider.broadcastTransaction(tx.getSignedPayload()!);
      console.log(resp);
  });
  ```

  ```go Go theme={null}
  // Load your wallet's private key from which you initiated the above stake operation.
  key, err := crypto.HexToECDSA("YOUR_WALLET_PRIVATE_KEY")
  if err != nil {
      log.Fatal(err)
  }

  // Sign the transactions within staking operation resource with your private key.
  err = stakeOperation.Sign(key)
  if err != nil {
      log.Fatal(err)
  }

  // For Hoodi, publicly available RPC URL's can be found here https://chainlist.org/chain/560048
  ethClient, err := ethclient.Dial("HOODI_RPC_URL")
  if err != nil {
      log.Fatal(err)
  }

  // Broadcast each of the signed transactions to the network.
  for _, transaction := range stakeOperation.Transactions() {
      rawTx, ok := transaction.Raw().(*types.Transaction)
      if !ok {
          log.Fatal("Failed to convert transaction to *types.Transaction")
      }
      if err := ethClient.SendTransaction(context.Background(), rawTx); err != nil {
          log.Fatal(err)
      }
      println(fmt.Sprintf("Broadcasted transaction hash: %s", rawTx.Hash().Hex()))
  }
  ```
</CodeGroup>

