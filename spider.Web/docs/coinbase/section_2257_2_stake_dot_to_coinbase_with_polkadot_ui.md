# 2. Stake DOT to Coinbase with Polkadot UI
Source: https://docs.cdp.coinbase.com/staking/staking-delegation-guides/polkadot/polkadot-ui-live/stake-with-polkadot-ui



## 1. Join the Coinbase Nomination Pool

1. On the Polkadot Staking Dashboard, click **Connect** in the top right corner.

2. Select your Stash account to connect the Polkadot.js wallet. Your Controller account is fetched automatically.

3. Ensure your controller has the nominal funds (≥ 5 DOTs) it needs for the "existential deposit" and to pay for transaction fees.

4. On the left menu, select **Pools** and then **All Pools** from the top menu.

5. Enter the address of the Coinbase Nomination Pool in the Search field. See [**Validator Information**](#validator-information) below.

<Info>
  The Coinbase nomination pool manages the selection of nominees and selects the Coinbase validators.
</Info>

<Warning>
  Joining a nomination pool bonds your DOT. You must wait the unbonding period of 28 days before it can be removed.
</Warning>

6. Verify that the Nomination Pool ID matches that in [**Validator Information**](#validator-information).

7. Click **Join** on the Nomination Pool.

8. If everything looks correct, click **Sign and Submit**.

9. Enter your stash password in the pop-up and click **Sign the transaction**, or confirm the Nominate transaction on your Ledger.

10. Once you've confirmed the details, approve the transaction.

11. Wait for the Transaction Success banner to pop up. This process can take a while if the network is behind.

Once complete, the Pools Overview screen should show that you are now a member of the Coinbase nomination pool, and the nominees should display.

**Validator Information**

<Info>
  **COINBASE VALIDATOR INFORMATION**

  **Nomination Pool name:** Coinbase

  **Nomination Pool address:** `13UVJyLnbVq86c4FQeiGGKD7WwtbFCPFeNovcHTqGakKuAMY`

  **Nomination Pool ID:** 58

  **Validator name:** Coinbase

  **Validator addresses:**

  **01:** `1VrK0TKunzstYPuxPpjArGnZestrrGxqpNnYvGBuqYikd6#`\
  **02:** `16OqxsIqicpKume1DksyGDrs3mdiznTb5YVmZywQvkteavY`\
  **03:** `12Ye9HPrF6qAdqsNSSqyFS5HTFsYf6fVnKUxThNCiraqz8z`\
  **04:** `12citkDgfF3GYdITRSqLxUn5XrvnqKq3BGZYbsJnaMfhQpTn`\
  **05:** `12nf26ZaKmyHFTRLLG5MrJspthbrT2hqiNBAGmL363Y6BPuN`\
  **06:** `12qTBKYMsTZ6UACilrnziicXqaXZEQFAUPvBQITSrcQMSLYo`\
  **07:** `1A2ATy1FFu5yQ9ZzqhPLsRckPqVkLmsM5AQyCTvGnGxGho`\
  **08:** `1DY65jjuwNk2Lxe84TyrGBvLxjfEZBAMktFBZCJCiX7RFCvS`\
  **09:** `134YFAX3ckRdEj5ox3aU6k3EkYAznoqNGWrMrKCGjsdTJZM`\
  **10:** `12EC0Ri5MjyiMQL23NTMGzJhuf0fp54sLNvJHpCEfBoQGrMZ`\
  **11:** `12HFJanq2nLfkKPHsEMp742MpNNqnvS6qdrqjsxAnGLNRrj`\
  **12:** `12waN6HnkfrGyZZyMKPAaSqHFSG52vXTEktMAzitr1b2TM4`\
  **13:** `138HkNksoqyexeNGm3MMbUS6kehD19SZdyqt3DMPSZKkQsP`\
  **14:** `14xcfeqDx1SVQGrTkVZ6b23sWsGZrevo7QQjGtaNssAGa5D0`\
  **15:** `146HhKhPvf7PnofrdfMsLDnrdpMkXCigM6jVGQ72zMow1oM`\
  **16:** `14wFAALTs5hUUdabN37QMbZvRqYyUrJp6meeDR94TZ2qhrL`

  The Coinbase Pool nominates these validator addresses. If staking directly, enter each of the Coinbase validator addresses from the list above.

  The Coinbase pool selects all validators from this list, and joining indicates your willingness to support any of them. The protocol automatically allocates pool stake to a subset of the validators from this nominated list that have been selected to participate and earn rewards each era. As such, selecting all validators increases your opportunities to earn rewards. See the [Polkadot FAQ](/staking/staking-delegation-guides/polkadot/polkadot-faq) to learn more.
</Info>

<Tip>
  **Congratulations! You are now staking with Coinbase.**
</Tip>

