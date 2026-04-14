# SOL Staking
Source: https://docs.cdp.coinbase.com/staking/staking-api/protocols/sol/overview



The Coinbase Staking API enables staking any amount of SOL on the Solana network to earn rewards for you and your users. [Get started](/staking/staking-api/protocols/sol/usage)!

The only inputs required are your own wallet and the desired stake (or unstake) amount. There is no need to tediously manage the underlying Solana stake accounts - the API does that heavy lifting for you. The staking rewards automatically accrue on the derived stake accounts, which can be claimed in the two-step process of [unstaking](./usage.mdx#unstake) and [claiming stake](./usage.mdx#claim-stake).

### Who this solution is for

* Wallet providers, onchain apps, and custodians who want to stake native SOL to Coinbase operated validators and have access to detailed staking rewards data.
* Developers looking for a simplified SOL staking solution where they do not need to directly manage stake account creation, splits and merges.

### Validator details

| Network | Address                                                                                                                                  | Location | Commission Fee | Operator  |
| :------ | :--------------------------------------------------------------------------------------------------------------------------------------- | :------- | :------------- | :-------- |
| Mainnet | [`6D2jqw9hyVCpppZexquxa74Fn33rJzzBx38T58VucHx9`](https://solanabeach.io/validator/6D2jqw9hyVCpppZexquxa74Fn33rJzzBx38T58VucHx9)          | Ireland  | 8%             | Coinbase  |
| Devnet  | [`GkqYQysEGmuL6V2AJoNnWZUz2ZBGWhzQXsJiXm2CLKAN`](https://solscan.io/account/GkqYQysEGmuL6V2AJoNnWZUz2ZBGWhzQXsJiXm2CLKAN?cluster=devnet) | N/A      | N/A            | Community |

### Rewards scope

| Data Type                   | Network      | Details                | Historical Depth | Addresses            | Aggregations |
| :-------------------------- | :----------- | :--------------------- | :--------------- | :------------------- | :----------- |
| Historical Rewards          | Mainnet Only | Consensus Rewards Only | Jan 1st, 2024    | All Staked Addresses | Epoch        |
| Historical Staking Balances | Mainnet Only |                        | Aug 15th, 2024   | All Staked Addresses | Epoch        |

<Tip>
  Some staking rewards earned via SOL Staking may be too small to be represented accurately in USD.
  It's recommended to view the staking rewards with the `Native` format option to see the rewards in
  Solana's native denomination, [lamport](https://solana.com/docs/terminology#lamport), which is 9 decimal places.
</Tip>

