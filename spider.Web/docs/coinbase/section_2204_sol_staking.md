# SOL Staking
Source: https://docs.cdp.coinbase.com/staking/staking-api/protocols/sol/usage



The Coinbase Staking API enables users to stake or unstake any amount of SOL. A user only needs to specify a wallet and a stake amount, and the API will handle the rest.

See the [quickstart](/staking/staking-api/introduction/quickstart) to familiarize yourself with Coinbase Staking API and basic usage.

The API automatically creates and manages the underlying Solana [stake accounts](https://solana.com/docs/references/staking/stake-accounts) on your behalf. The staking rewards automatically accrue on the derives stake accounts, which can be claimed in the two-step process of [unstaking](#unstake) and [claiming rewards](#claim-rewards).

## Stake

Before staking, **ensure that your address contains enough SOL** to cover the stake amount and network fees. For devnet funds, you can use [this faucet](https://faucet.solana.com).

The amount of SOL that is ultimately staked will be the user input subtracted by the [rent reserve](https://solana.com/docs/core/fees#rent) amount. The rent reserve amount is a Solana-mandated account minimum. So if the user input is 1 SOL and the rent reserve is 0.02 SOL, the amount that will ultimately be staked is \~0.98 SOL. Without this rent adjustment, the stake wouldn't become active.

We currently only support delegating to the Coinbase public validator [`6D2jqw9hyVCpppZexquxa74Fn33rJzzBx38T58VucHx9`](https://solanabeach.io/validator/6D2jqw9hyVCpppZexquxa74Fn33rJzzBx38T58VucHx9). This validator is operated by Coinbase and is located in Ireland.

### Step 1. Create a Stake Operation

<CodeGroup>
  ```typescript Typescript  theme={null}
  import { Coinbase, ExternalAddress } from "@coinbase/coinbase-sdk";

  // Create a new external address on the solana-devnet testnet network.
  let address = new ExternalAddress(Coinbase.networks.SolanaDevnet, "YOUR_WALLET_ADDRESS");

  // Find out how much SOL is available to stake.
  let stakeableBalance = await address.stakeableBalance(Coinbase.assets.Sol);

  // Build a stake operation for an amount <= stakeableBalance, in this case 0.1 SOL.
  let stakingOperation = await address.buildStakeOperation(0.1, Coinbase.assets.Sol);
  ```

  Refer to the [ExternalAddress docs](https://coinbase.github.io/coinbase-sdk-nodejs/classes/coinbase_address_external_address.ExternalAddress.html) for a full list of supported methods.

  ```go Go  theme={null}
  // Code assumes you've already created a CDP client as shown in the quickstart guide.

  // Create a new external address on the solana-devnet testnet network.
  address := coinbase.NewExternalAddress(coinbase.SolanaDevnet, "YOUR_WALLET_ADDRESS")

  // Get the amount of SOL available to stake.
  stakeableBalance, err := client.GetStakeableBalance(ctx, coinbase.Sol, address)
  if err != nil {
      return err
  }

  // Build a stake operation for an amount <= stakeableBalance, in this case 0.1 SOL.
  stakingOperation, err := client.BuildStakeOperation(
      context.Background(),
      big.NewFloat(0.1),
      coinbase.Sol,
      address,
  )
  if err != nil {
      return err
  }
  ```

  Refer to the [ExternalAddress](https://pkg.go.dev/github.com/coinbase/coinbase-sdk-go/pkg/coinbase#NewExternalAddress), [GetStakeableBalance](https://pkg.go.dev/github.com/coinbase/coinbase-sdk-go/pkg/coinbase#Client.GetStakeableBalance) and [BuildStakeOperation](https://pkg.go.dev/github.com/coinbase/coinbase-sdk-go/pkg/coinbase#Client.BuildStakeOperation) functions for more details.
</CodeGroup>

### Step 2. Sign and Broadcast

Once the unstake operation has been built, the transaction has been constructed based on your inputs, but not signed or broadcasted. Now, you must relay the transactions to your end-user for signing and broadcasting.

If you'd like to sign and broadcast in your own system, refer to the [signing and broadcasting transactions](#signing-and-broadcasting-transactions) section for an example.

### Step 3. Wait

Once the transaction is signed and broadcasted, the SOL will be "pending staked" for \~2 days. This delay is a direct consequence of the Solana network's staking mechanics. After this period, the SOL will be staked and begin to earn rewards.

You can tell your SOL is fully staked and earning rewards by checking for when your SOL is added to the unstakeable balance.

## Unstake

Unstaking is the first part of a two-step process to withdraw your staked assets. The second step is [Claim Stake](#claim-stake).

In direct Solana staking, a user would need to select a specific [stake account](https://solana.com/docs/references/staking/stake-accounts) and unstake each stake account individually. With the Coinbase Staking API, the user can simply specify the wallet and the desired unstake amount, and the API will handle the rest. The Coinbase Staking API hides this complexity by automatically creating, merging, and splitting the underlying Solana stake accounts for you. All a user must do is sign and broadcast the transactions and the API will handle the rest.

### Step 1. Create a Stake Operation

<CodeGroup>
  ```typescript Typescript  theme={null}
  import { Coinbase, ExternalAddress } from "@coinbase/coinbase-sdk";

  // Create a new external address on the solana-devnet testnet network.
  let address = new ExternalAddress(Coinbase.networks.SolanaDevnet, "YOUR_WALLET_ADDRESS");

  // To determine the amount of SOL available to unstake, use the `unstakeableBalance` method as shown below:
  let unstakeableBalance = await address.unstakeableBalance(Coinbase.assets.Sol);

  // Build an unstake operation for an amount <= unstakeableBalance, in this case 0.1 SOL.
  let stakingOperation = await address.buildUnstakeOperation(0.1, Coinbase.assets.Sol);
  ```

  Refer to the [ExternalAddress docs](https://coinbase.github.io/coinbase-sdk-nodejs/classes/coinbase_address_external_address.ExternalAddress.html) for a full list of supported methods.

  ```go Go  theme={null}
  // Code assumes you've already created a CDP client as shown in the quickstart guide.

  // Create a new external address on the solana-devnet testnet network.
  address := coinbase.NewExternalAddress(coinbase.SolanaDevnet, "YOUR_WALLET_ADDRESS")

  // To determine the amount of SOL available to unstake, use the `unstakeableBalance` method as shown below:
  unstakeableBalance, err := client.GetUnstakeableBalance(ctx, coinbase.Sol, address)
  if err != nil {
      return err
  }

  // Build an unstake operation for an amount <= unstakeableBalance, in this case 0.1 SOL.
  stakingOperation, err := client.BuildStakeOperation(
      context.Background(),
      big.NewFloat(0.1),
      coinbase.Sol,
      address,
  )
  if err != nil {
      return err
  }
  ```

  Refer to the [ExternalAddress](https://pkg.go.dev/github.com/coinbase/coinbase-sdk-go/pkg/coinbase#NewExternalAddress), [GetStakeableBalance](https://pkg.go.dev/github.com/coinbase/coinbase-sdk-go/pkg/coinbase#Client.GetStakeableBalance) and [BuildStakeOperation](https://pkg.go.dev/github.com/coinbase/coinbase-sdk-go/pkg/coinbase#Client.BuildStakeOperation) functions for more details.
</CodeGroup>

### Step 2. Sign and Broadcast

Once the unstake operation has been built, the transaction has been constructed based on your inputs, but not signed or broadcasted. Now, you must relay the transactions to your end-user for signing and broadcasting.

If you'd like to sign and broadcast in your own system, refer to the [signing and broadcasting transactions](#signing-and-broadcasting-transactions) section for an example.

### Step 3. Wait

After the transaction is signed and broadcasted, the SOL will be "pending unstaked" for \~2 days. This delay is a direct consequence of the Solana network's staking mechanics. After the SOL in unstaked, the SOL will be in a claimable state and can be claimed using the [Claim Stake](#claim-stake) operation.

## Claim Stake

Claim Stake is the second part of a two-step process to withdraw your staked assets. The first step is [Unstake](#unstake).

After SOL is unstaked and the necessary time has passed (\~2 days), the unstaked SOL will be sitting idle on the underlying stake account. This SOL is ready to be claimed. The claim stake operation allows you to claim the unstaked SOL and transfer it back to your wallet.

### Step 1. Create a Stake Operation

<CodeGroup>
  ```typescript Typescript  theme={null}
  import { Coinbase, ExternalAddress } from "@coinbase/coinbase-sdk";

  // Create a new external address on the solana-devnet testnet network.
  let address = new ExternalAddress(Coinbase.networks.SolanaDevnet, "YOUR_WALLET_ADDRESS");

  // Check if there is any balance available to claim.
  let claimableBalance = await address.unstakeableBalance(Coinbase.assets.Sol);

  // Build a claim_stake operation for an amount = claimableBalance.
  // The claim stake operation aims to claim all the withdrawable SOL at that point in time.
  let stakingOperation = await address.buildClaimStakeOperation(claimableBalance, Coinbase.assets.Sol);
  ```

  ```go Go  theme={null}
  // Code assumes you've already created a CDP client as shown in the quickstart guide.

  // Create a new external address on the solana-devnet testnet network.
  address := coinbase.NewExternalAddress(coinbase.SolanaDevnet, "YOUR_WALLET_ADDRESS")

  // Check if there is any balance available to claim.
  claimableBalance, err := client.GetClaimableBalance(ctx, coinbase.Sol, address)
  if err != nil {
      return err
  }

  // Build a claim_stake operation for an amount = claimableBalance.
  // The claim stake operation aims to claim all the withdrawable SOL at that point in time.
  stakingOperation, err := client.BuildClaimStakeOperation(
      context.Background(),
      claimableBalance.Amount(),
      coinbase.Sol,
      address,
  )
  if err != nil {
      return err
  }
  ```
</CodeGroup>

Refer to the [ExternalAddress docs](https://coinbase.github.io/coinbase-sdk-nodejs/classes/coinbase_address_external_address.ExternalAddress.html) for a full list of supported methods.
Refer to the [ExternalAddress](https://pkg.go.dev/github.com/coinbase/coinbase-sdk-go/pkg/coinbase#NewExternalAddress), [GetStakeableBalance](https://pkg.go.dev/github.com/coinbase/coinbase-sdk-go/pkg/coinbase#Client.GetStakeableBalance) and [BuildStakeOperation](https://pkg.go.dev/github.com/coinbase/coinbase-sdk-go/pkg/coinbase#Client.BuildStakeOperation) functions for more details.

### Step 2. Sign and Broadcast

Once the claim  operation has been built, the transaction has been constructed based on your inputs, but not signed or broadcasted. Now, you must relay the transactions to your end-user for signing and broadcasting.

If you'd like to sign and broadcast in your own system, refer to the [signing and broadcasting transactions](#signing-and-broadcasting-transactions) section for an example.

After the transaction is signed and broadcasted, the SOL will be transferred back to your wallet almost immediately. At this stage, the full SOL staking lifecycle is complete.

## View Staking Rewards

After staking your SOL, rewards will begin to accrue on the blockchain that are withdrawable by your wallet. The staking rewards endpoint allows you to view these rewards earned by your wallet over time.

<Warning>
  Viewing historical rewards earned to Solana stake accounts that have dropped below the [rent reserve](https://solana.com/docs/core/fees#rent) are currently not supported. This means that the endpoint might not show all rewards that were earned in the past. This is a known limitation that will be addressed in a future release.
</Warning>

The API provides rewards both in native units (i.e. SOL) and in equivalent USD value. The USD value is calculated using the Coinbase exchange rate in the \~30 seconds after the reward period concluded. As an example, if we provide aggregated rewards on January 20th, 2024 UTC, the underlying SOL value is calculated based on the USD value of SOL within the first 30 seconds of January 21st, 2024.
Look up staking rewards for a specific address.

<CodeGroup>
  ```typescript Typescript  theme={null}
  import { Coinbase, ExternalAddress } from "@coinbase/coinbase-sdk";

  // Create a new external address on the solana-mainnet network for which you want to view staking rewards.
  let address = new ExternalAddress(Coinbase.networks.SolanaMainnet, "YOUR_WALLET_ADDRESS");

  // Get the rewards earned from staking in the last 1 week (default window).
  // Note that it can take several hours for new rewards to show up.
  let rewards = await address.stakingRewards(Coinbase.assets.Sol);

  // Loop through the rewards and print each staking reward.
  rewards.forEach(reward => console.log(reward.toString()));
  ```

  Look up staking rewards for a list of addresses.

  ```typescript theme={null}
  import { Coinbase, StakingReward } from "@coinbase/coinbase-sdk";

  let rewards = await StakingReward.list(
      Coinbase.networks.SolanaMainnet, Coinbase.assets.Sol,
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

  ```go theme={null}
  // Create a new external address on the solana-devnet network for which you want to view staking rewards.
  address := coinbase.NewExternalAddress(coinbase.SolanaDevnet, "YOUR_WALLET_ADDRESS")

  // Get the rewards earned from staking in the last 10 days.
  // Note that it can take several hours for new rewards to show up.
  rewards, err := client.ListStakingRewards(
      context.Background(),
      coinbase.Sol,
      []coinbase.Address{*address},
      time.Now().Add(-10*24*time.Hour),
      time.Now(),
      api.STAKINGREWARDFORMAT_USD,
  )
  if err != nil {
      return err
  }

  // Loop through the rewards and print each staking reward.
  for _, reward := range rewards {
      log.Printf("Staking reward: %s", reward.ToString())
  }
  ```

  Look up staking rewards for a list of addresses.

  ```go theme={null}
  // Get the rewards earned from staking across multiple wallets in the last 10 days.
  // Note that it can take several hours for new rewards to show up.
  rewards, err := client.ListStakingRewards(
      context.Background(),
      coinbase.Sol,
      []coinbase.Address{*address1, *address2},
      time.Now().Add(-10*24*time.Hour),
      time.Now(),
      api.STAKINGREWARDFORMAT_USD,
  )
  if err != nil {
      return err
  }

  // Loop through the rewards and print each staking reward.
  for _, reward := range rewards {
      log.Printf("Staking reward: %s", reward.ToString())
  }
  ```
</CodeGroup>

Refer to the [StakingReward docs](https://coinbase.github.io/coinbase-sdk-nodejs/classes/coinbase_staking_reward.StakingReward.html) for a full list of supported methods and their parameters.
Refer to the [ListStakingRewards](https://pkg.go.dev/github.com/coinbase/coinbase-sdk-go/pkg/coinbase#Client.ListStakingRewards) function for more details.

## View Historical Staking Balances

The staking balances endpoint allows you to view the historical staking balances of your wallet over time, accounting for accruing rewards and auto-compounding stake.
Look up historical staking balances for a specific address.

<CodeGroup>
  ```typescript Typescript  theme={null}
  const balances = await StakingBalance.list(
      NetworkIdentifier.SolanaMainnet,
      Coinbase.assets.Sol,
      wallet,
      startTime,
      new Date().toISOString(),
  );
  ```

  ```go Go  theme={null}
  // Get the balances earned from staking in the last 10 days.
  // Note that it can take several hours for balance snapshots to show up.
  balances, err := client.ListHistoricalStakingBalances(
      ctx,
      coinbase.Sol,
      address,
      time.Now().Add(-10*24*time.Hour),
      time.Now(),
  )
  if err != nil {
      log.Fatalf("error fetching staking balances: %v", err)
  }

  // Loop through the balances and print each staking balance.
  for _, balance := range balances {
      log.Printf("Staking balance: %s", balance.String())
  }
  ```
</CodeGroup>

Refer to the [StakingBalance docs](https://coinbase.github.io/coinbase-sdk-nodejs/interfaces/client_api.StakingBalance.html) for a full list of supported methods and their parameters.
Refer to the [ListHistoricalStakingBalances documentation](https://pkg.go.dev/github.com/coinbase/coinbase-sdk-go/pkg/coinbase#Client.ListHistoricalStakingBalances) function for more details.

## Signing and Broadcasting Transactions

Here's an example of how to sign and broadcast transactions surfaced via the staking operation resource.

<CodeGroup>
  ```typescript Typescript [expandable] theme={null}
  import { Connection, Transaction, Keypair, SendOptions } from "@solana/web3.js";
  import bs58 from "bs58";

  const connection = new Connection("https://api.devnet.solana.com");
  const secretKey = Uint8Array.from(bs58.decode("YOUR_WALLET_PRIVATE_KEY"));
  const key = Keypair.fromSecretKey(secretKey);

  // This code assumes a solana stakingOperation has already been created.

  for (const tx of stakingOperation.getTransactions()) {
      console.log("Tx unsigned payload:", tx.getUnsignedPayload());

      const transaction = Transaction.from(bs58.decode(tx.getUnsignedPayload()));

      transaction.partialSign(key);

      const sendOptions: SendOptions = {
          skipPreflight: false,
          preflightCommitment: "finalized",
      };

      let maxRetries = 20;

      while (maxRetries > 0) {
          try {
              const signature = await connection.sendRawTransaction(transaction.serialize(), sendOptions);
              console.log("Transaction signature:", getTxLink(signature, networkID));
              break;
          } catch (error) {
              await new Promise(resolve => setTimeout(resolve, 3000));
              console.error(`Trying again [%d] Sending transaction...`, 21 - maxRetries);
              maxRetries--;
          }
      }
  }

  function getTxLink(signature: string, networkID: string): string {
      const baseUrl = "https://explorer.solana.com/tx";

      let network = "mainnet";
      if (networkID === Coinbase.networks.SolanaDevnet) {
          network = "devnet";
      }

      return `${baseUrl}/${signature}?cluster=${network}`;
  }
  ```

  ```go Go [expandable] theme={null}
  package main

  import (
      "context"
      "fmt"
      "log"
      "os"
      "time"

      "github.com/btcsuite/btcutil/base58"
      "github.com/coinbase/coinbase-sdk-go/pkg/coinbase"
      bin "github.com/gagliardetto/binary"
      "github.com/gagliardetto/solana-go"
      "github.com/gagliardetto/solana-go/rpc"
  )

  const (
      walletPrivateKey = "YOUR_WALLET_PRIVATE_KEY"
      devnetRPC        = "https://api.devnet.solana.com"
  )

  func main() {
      ctx := context.Background()

      // This code assumes a solana stakingOperation has already been created.

      privateKey, err := decodePrivateKey(walletPrivateKey)

      err = stakingOperation.Sign(privateKey)
      if err != nil {
          log.Fatalf("error signing transaction: %v", err)
      }

      rpcClient := rpc.New(rpcURL)

      maxRetries := uint(5)
      opts := rpc.TransactionOpts{
          SkipPreflight: false,
          MaxRetries:    &maxRetries,
          // NOTE: In production, consider using rpc.CommitmentFinalized instead to ensure the block is included.
          PreflightCommitment: rpc.CommitmentProcessed,
      }

      for _, transaction := range stakingOperation.Transactions() {
          unsignedTx := transaction.UnsignedPayload()
          signedTx := transaction.SignedPayload()

          log.Printf("Unsigned tx payload: %s\n\n", unsignedTx)
          log.Printf("Signed tx payload: %s\n\n", signedTx)

          rawTx := transaction.Raw()
          solanaTx, ok := rawTx.(*solana.Transaction)
          if !ok {
              log.Fatal("failed to cast raw transaction to solana.Transaction")
          }

          sig, err := rpcClient.SendTransactionWithOpts(ctx, solanaTx, opts)
          if err != nil {
              log.Fatalf("failed to send transaction: %v", err)
          }

          log.Printf("Broadcasted tx: %s\n\n", getTxLink(stakingOperation.NetworkID(), sig.String()))
      }
  }

  func decodePrivateKey(privateKeyString string) (*ed25519.PrivateKey, error) {
      // Decode the base58 encoded private key
      privateKeyBytes := base58.Decode(privateKeyString)
      if len(privateKeyBytes) != ed25519.PrivateKeySize {
          log.Fatalf("invalid private key length: expected %d bytes, got %d bytes", ed25519.PrivateKeySize, len(privateKeyBytes))
      }

      // Convert the byte slice to an ed25519 private key
      privateKey := ed25519.PrivateKey(privateKeyBytes)

      return &privateKey, nil
  }

  func getTxLink(networkID, signature string) string {
      if networkID == coinbase.SolanaMainnet {
          return fmt.Sprintf("https://explorer.solana.com/tx/%s", signature)
      } else if networkID == coinbase.SolanaDevnet {
          return fmt.Sprintf("https://explorer.solana.com/tx/%s?cluster=devnet", signature)
      }

      return ""
  }
  ```
</CodeGroup>

