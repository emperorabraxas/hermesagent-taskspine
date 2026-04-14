# Example payloads
Source: https://docs.cdp.coinbase.com/api-reference/payment-apis/webhooks/example-payloads



Use this page to quickly compare incoming webhook request body examples for transfer events.

## Example payloads

<Tabs>
  <Tab title="Quoted">
    Transfer fee quote is ready:

    ```json lines wrap theme={null}
    {
      "eventId": "<uuid>",
      "eventType": "payments.transfers.quoted",
      "timestamp": "2026-01-01T00:00:00Z",
      "data": {
        "createdAt": "2026-01-01T00:00:00Z",
        "expiresAt": "2026-01-01T00:15:00Z",
        "fees": [
          {
            "amount": "0.19",
            "asset": "usdc",
            "type": "network"
          }
        ],
        "source": {
          "accountId": "account_<uuid>",
          "asset": "usdc"
        },
        "sourceAmount": "100.19",
        "sourceAsset": "usdc",
        "status": "quoted",
        "target": {
          "address": "0x<address>",
          "asset": "usdc",
          "network": "ethereum"
        },
        "targetAmount": "100.00",
        "targetAsset": "usdc",
        "transferId": "transfer_<uuid>",
        "updatedAt": "2026-01-01T00:00:10Z"
      }
    }
    ```
  </Tab>

  <Tab title="Processing">
    Transfer is being executed:

    ```json lines wrap theme={null}
    {
      "eventId": "<uuid>",
      "eventType": "payments.transfers.processing",
      "timestamp": "2026-01-01T00:02:30Z",
      "data": {
        "createdAt": "2026-01-01T00:00:00Z",
        "expiresAt": "2026-01-01T00:15:00Z",
        "fees": [
          {
            "amount": "0.19",
            "asset": "usdc",
            "type": "network"
          }
        ],
        "source": {
          "accountId": "account_<uuid>",
          "asset": "usdc"
        },
        "sourceAmount": "100.19",
        "sourceAsset": "usdc",
        "status": "processing",
        "target": {
          "address": "0x<address>",
          "asset": "usdc",
          "network": "ethereum"
        },
        "targetAmount": "100.00",
        "targetAsset": "usdc",
        "transferId": "transfer_<uuid>",
        "updatedAt": "2026-01-01T00:02:30Z"
      }
    }
    ```
  </Tab>

  <Tab title="Failed">
    Transfer failed:

    ```json lines wrap theme={null}
    {
      "eventId": "<uuid>",
      "eventType": "payments.transfers.failed",
      "timestamp": "2026-01-01T00:05:00Z",
      "data": {
        "createdAt": "2026-01-01T00:00:00Z",
        "expiresAt": "2026-01-01T00:15:00Z",
        "failureReason": "Insufficient Balance",
        "fees": [
          {
            "amount": "0.19",
            "asset": "usdc",
            "type": "network"
          }
        ],
        "source": {
          "accountId": "account_<uuid>",
          "asset": "usdc"
        },
        "sourceAmount": "100.19",
        "sourceAsset": "usdc",
        "status": "failed",
        "target": {
          "address": "0x<address>",
          "asset": "usdc",
          "network": "ethereum"
        },
        "targetAmount": "100.00",
        "targetAsset": "usdc",
        "transferId": "transfer_<uuid>",
        "updatedAt": "2026-01-01T00:05:00Z"
      }
    }
    ```
  </Tab>

  <Tab title="Completed">
    Transfer finished successfully:

    ```json lines wrap theme={null}
    {
      "eventId": "<uuid>",
      "eventType": "payments.transfers.completed",
      "timestamp": "2026-01-01T00:05:00Z",
      "data": {
        "createdAt": "2026-01-01T00:00:00Z",
        "expiresAt": "2026-01-01T00:15:00Z",
        "fees": [
          {
            "amount": "0.19",
            "asset": "usdc",
            "type": "network"
          }
        ],
        "source": {
          "accountId": "account_<uuid>",
          "asset": "usdc"
        },
        "sourceAmount": "100.19",
        "sourceAsset": "usdc",
        "status": "completed",
        "target": {
          "address": "0x<address>",
          "asset": "usdc",
          "network": "ethereum"
        },
        "targetAmount": "100.00",
        "targetAsset": "usdc",
        "transferId": "transfer_<uuid>",
        "updatedAt": "2026-01-01T00:05:00Z"
      }
    }
    ```
  </Tab>

  <Tab title="Completed (with deposit data)">
    Completed transfer with deposit destination details:

    ```json lines wrap theme={null}
    {
      "eventId": "<uuid>",
      "eventType": "payments.transfers.completed",
      "timestamp": "2026-01-01T00:05:00Z",
      "data": {
        "createdAt": "2026-01-01T00:00:00Z",
        "completedAt": "2026-01-01T00:05:00Z",
        "source": {
          "address": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
          "network": "base",
          "asset": "usdc"
        },
        "sourceAmount": "100.00",
        "sourceAsset": "usdc",
        "status": "completed",
        "target": {
          "accountId": "account_<uuid>",
          "asset": "usdc"
        },
        "targetAmount": "100.00",
        "targetAsset": "usdc",
        "transferId": "transfer_<uuid>",
        "details": {
          "depositDestination": {
            "id": "depositDestination_<uuid>"
          },
          "onchainTransactions": [
            {
              "transactionHash": "0x363cd3b3d4f49497cf5076150cd709307b90e9fc897fdd623546ea7b9313cecb",
              "network": "base"
            }
          ]
        },
        "updatedAt": "2026-01-01T00:05:00Z"
      }
    }
    ```
  </Tab>
</Tabs>

<Note>
  This page shows full incoming webhook request bodies (`eventId`, `eventType`, `timestamp`, `data`).

  See [Transfers example payloads](/api-reference/payment-apis/rest-api/transfers/example-payloads) for `source` and `target` payload object examples.
</Note>

