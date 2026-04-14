# Get transfer
Source: https://docs.cdp.coinbase.com/api-reference/international-exchange-api/rest-api/transfers/get-transfer

GET /api/v1/transfers/{transfer_uuid}

<Tabs>
  <Tab title="Java">
    ```java theme={null}
    TransfersService transfersService = IntxServiceFactory.createTransfersService(client);
    GetTransferRequest request = new GetTransferRequest.Builder()
        .transferUuid("transfer_uuid")
        .build();
    GetTransferResponse response = transfersService.getTransfer(request);
    ```

    For more information, please visit the [INTX Java SDK](https://github.com/coinbase-samples/intx-sdk-java).
  </Tab>

  <Tab title=".NET">
    ```cs theme={null}
    var transfersService = new TransfersService(client);
    var request = new GetTransferRequest(
        TransferUuid: "transfer_uuid"
    );
    var response = transfersService.GetTransfer(request);
    ```

    For more information, please visit the [INTX .NET SDK](https://github.com/coinbase-samples/intx-sdk-dotnet).
  </Tab>

  <Tab title="Go">
    ```go theme={null}
    transfersSvc := transfers.NewTransfersService(client)
    request := &transfers.GetTransferRequest{
        TransferUuid: "transfer_uuid",
    }
    response, err := transfersSvc.GetTransfer(context.Background(), request)
    ```

    For more information, please visit the [INTX Go SDK](https://github.com/coinbase-samples/intx-sdk-go).
  </Tab>

  <Tab title="Python">
    ```python theme={null}
    client = IntxClient()
    request = GetTransferRequest(
        transfer_uuid="transfer_uuid"
    )
    response = client.get_transfer(request)
    ```

    For more information, please visit the [INTX Python SDK](https://github.com/coinbase-samples/intx-sdk-py).
  </Tab>

  <Tab title="TS/JS">
    ```js theme={null}
    const transfersService = new TransfersService(client);

    transfersService.getTransfer({
        transferUuid: 'TRANSFER_UUID_HERE',
    }).then(async (response) => {
        console.log('Transfer: ', response);
    })
    ```

    For more information, please visit the [INTX TS SDK](https://github.com/coinbase-samples/intx-sdk-ts).
  </Tab>

  <Tab title="CLI">
    ```
    intxctl get-transfer --help
    ```

    For more information, please visit the [INTX CLI](https://github.com/coinbase-samples/intx-cli).
  </Tab>
</Tabs>

