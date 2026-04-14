# Get counterparty withdrawal limit
Source: https://docs.cdp.coinbase.com/api-reference/international-exchange-api/rest-api/transfers/get-counterparty-withdrawal-limit

GET /api/v1/transfers/withdraw/{portfolio}/{asset}/counterparty-withdrawal-limit
Get counterparty withdrawal limit within coinbase transfer network

<Tabs>
  <Tab title="TS/JS">
    ```js theme={null}
    const transfersService = new TransfersService(client);

    transfersService.getCounterpartyWithdrawalLimit({
        counterpartyId: 'your-counterparty-id',
        asset: 'ETH',
    }).then(async (response) => {
        console.log('Withdrawal Limit: ', response);
    })
    ```

    For more information, please visit the [INTX TS SDK](https://github.com/coinbase-samples/intx-sdk-ts).
  </Tab>
</Tabs>

