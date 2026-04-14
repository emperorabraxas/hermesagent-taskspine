# 1. Setup and Fund Avalanche Wallet
Source: https://docs.cdp.coinbase.com/staking/staking-delegation-guides/avalanche/avalanche-wallet/setup-and-fund-avalanche-wallet



## 1. Create an Avalanche wallet

1. Navigate to [Avalanche Wallet](https://wallet.avax.network/).

2. Select **Create New Wallet**.

3. Select **Generate Key Phrase**.

4. Copy your Key Phrase (mnemonic seed phrase) and store it somewhere safe.

<Warning>
  Ensure that you store your Key Phrase somewhere safe where it cannot be lost or compromised. Your Key Phrase is the master key to your wallet; loss or compromise of your Key Phrase may result in permanent loss of your AVAX.
</Warning>

5. Confirm you have secured your Key Phrase and select **Access Wallet**.

6. Verify your Key Phrase (Mnemonic phrase) by filling in the blanks with the correct words, and select **Verify**.

7. Select **Access Wallet**.

## 2. Locate Platform Wallet Address

1. Navigate to the [Avalanche Wallet](https://wallet.avax.network/) dashboard.

   <img />

2. Verify which platform wallet address to use by navigating to the exchange or wallet where your AVAX is stored, then view your Avalanche wallet address, by selecting a "Receive Avalanche" option.

3. Determine the Avalanche chain for this wallet based on the address' prefix:

   * X-Chain wallet addresses begin with "X-avax..."
   * C-Chain wallet addresses begin with "0x..."
   * P-Chain wallet addresses begin with "P-avax..."

<Warning>
  You can toggle between 3 options for your wallet address in the upper right corner of the Avalanche Wallet: X, P, or C, which indicate your unique wallet addresses for the Avalanche X-Chain, C-Chain, and P-Chain.

  * **X-Chain** is the Exchange Chain. Its sole purpose is for sending and receiving funds.
  * **C-Chain** is the Contract Chain. This is the chain used for smart contracts and defi, and it has an Ethereum-style address. If your AVAX is stored with Coinbase, your balance is on the C-Chain.
  * **P-Chain** is the Platform Chain. This is the chain for staking AVAX or running a validator. The P-Chain can receive transfers from the X and C chains using the Cross Chain transaction in the Avalanche Wallet.

  Proceed with caution during these steps to ensure you are depositing AVAX to the correct wallet. You can lose your AVAX funds if you send them to the wrong chain's wallet.
</Warning>

4. Return to the [Avalanche Wallet](https://wallet.avax.network/) dashboard.

5. Under **Derived Wallet Address**, toggle the wallet options so that the same chain is selected (X, C, or P) as your wallet address on the exchange or wallet where your AVAX is stored (the address that appears on the Avalanche Wallet dashboard should have the same prefix as your wallet address on the exchange).

6. Copy the Derived Platform Wallet Address.

## 3. Fund Avalanche Wallet

1. Navigate to the exchange or wallet where your AVAX is stored and send your AVAX to the appropriate Avalanche Wallet chain address you just copied.

2. Your AVAX balance should now appear on your Avalanche Wallet dashboard.

<Info>
  If you receive an error message from the exchange or wallet where your AVAX is stored stating that this is not a valid AVAX address, go back to the Avalanche dashboard and instead copy the address of the Avalanche chain that matches the chain on which your AVAX is currently stored.

  For example, if your AVAX is stored with Coinbase on the Avalanche C-Chain, and you receive an error message when trying to send your AVAX out to Avalanche Wallet, go back to Avalanche Wallet and ensure you have copied the C-Chain address to send your AVAX from Coinbase to.
</Info>

