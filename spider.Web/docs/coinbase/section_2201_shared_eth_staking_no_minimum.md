# Shared ETH Staking (No Minimum)
Source: https://docs.cdp.coinbase.com/staking/staking-api/protocols/shared-eth/overview



Shared ETH Staking allows you to enable ETH rewards for you and your users without requiring the 32 ETH deposit increments typically required by ETH staking.

Our shared ETH staking solution is built using proprietary onchain smart contracts to remove deposit requirements in conjunction with standard Ethereum staking contracts. This approach ensures **end-users are always in custody of their funds**.

### Who this solution is for

* Wallet providers, onchain apps, and custodians with users who will be staking amounts of ETH below the 32 ETH deposit minimums.
* Developers looking for instant onchain payouts of revenue share (if applicable).

### Integration Contract Details

<Info>
  Contract addresses:

  **Mainnet**: `0x2e3956e1ee8b44ab826556770f69e3b9ca04a2a7`\
  **Testnet (Hoodi)**: `0x1213548c871eb4d51e89fde31c35c1685e3057f4`
  **Commission fee**: 15%

  Developers with a private integrating contract will have been sent their contract address details separately.
</Info>

### Rewards scope

| Data Type          | Network      | Details          | Historical Depth          | Addresses            | Aggregations |
| ------------------ | ------------ | ---------------- | ------------------------- | -------------------- | ------------ |
| Historical Rewards | Mainnet Only | All Reward Types | Oct 1st, 2023 (Inception) | All Staked Addresses | Daily        |

<Tip>
  Some staking rewards earned via Shared ETH Staking may be too small to be represented accurately in USD.
  It's recommended to view the staking rewards with the `Native` format option in that scenario to
  see the rewards in Ethereum's native denomination, [Wei](https://ethereum.org/en/developers/docs/intro-to-ether/#denominations), which is 18 decimal places.
</Tip>

### Billing

Shared ETH staking uses proprietary smart contracts which automatically settle commissions and rewards onchain. There is no offchain invoicing when using Shared ETH staking. You can view rewards and download reports in the CDP Portal.

