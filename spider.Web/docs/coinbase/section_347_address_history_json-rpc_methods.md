# Address History JSON-RPC Methods
Source: https://docs.cdp.coinbase.com/api-reference/json-rpc-api/address-history

The following JSON-RPC APIs provide convenient access to historical data for your onchain addresses.

## Constructing Requests

**Option 1**: You can use the [JSON RPC playground](https://portal.cdp.coinbase.com/products/onchain-data) to easily create sample JSON RPC requests.

**Option 2**: Alternatively, you can construct your own requests by following the below steps:

1. Log into the [CDP Portal](https://portal.cdp.coinbase.com) and go to the [Data](https://portal.cdp.coinbase.com/products/onchain-data) page.
2. Ensure the correct network in your RPC URL based on the [supported RPC networks](/api-reference/networks#cdp-features).
3. Open a terminal and make your requests based on the supported methods in this API reference page.

<Info>
  **Authentication**

  For information on how to authenticate requests to our JSON-RPC APIs, please visit the **Client API Keys** section of our [Authentication page](/get-started/authentication/cdp-api-keys#client-api-keys).
</Info>

## JSON-RPC Methods for Address History Data

### `cdp_listBalances`

This endpoint retrieves the latest balances for an address.
Note that this JSON RPC endpoint provides a more complete list of assets than the [CDP API](/api-reference/rest-api/addresses/list-address-balances).
However, there is a few seconds of delay in terms of data freshness for indexing a complete list of assets.
If you need more real-time data with whitelisted assets, you should use the [CDP API](/api-reference/rest-api/addresses/list-address-balances).

The [API credit](/data/node/overview#rate-limits) value of this method is 100.

#### Parameters

| Name      | Type   | Req | Description                                                                                                                                               |
| :-------- | :----- | :-: | :-------------------------------------------------------------------------------------------------------------------------------------------------------- |
| address   | string |  Y  | Blockchain address hash. EVM chain address hash should be lowercase.                                                                                      |
| pageSize  | string |  N  | Number of balances to receive in a page. The default value is 25. The maximum value is 100, and values supplied over this will be coerced to the maximum. |
| pageToken | string |  N  | Provided from a previous response's nextPageToken                                                                                                         |

#### Returns

| Field            | Description                                                                                                                                                                                                                                                                |
| :--------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| asset.id         | The identity of the asset for querying for details or history.                                                                                                                                                                                                             |
| asset.type       | The type of Asset the definition describes. For example: "native", "erc20", "erc721", "erc1155", "creditAlphanum4", "fa2".                                                                                                                                                 |
| asset.groupId    | The contract address or group identifier for an Asset. For an NFT or a multi-token Asset this may identify a group of Asset. For a native Asset this will not be set.                                                                                                      |
| asset.subGroupId | The identifier that distinguishes the identity of the Asset within the contract address or group. For an NFT or a multi-token Asset that can have many Assets associated with a contract address, this could be a token ID. For a UTXO, this could be the coin identifier. |
| value            | The amount of the balance in the lowest denomination of the asset. Type is in BigInteger in standard base64 encoding.                                                                                                                                                      |
| valueStr         | The string representation of the balance value to avoid precision loss.                                                                                                                                                                                                    |
| decimals         | The number of decimals the asset utilizes.                                                                                                                                                                                                                                 |
| nextPageToken    | A token which can be provided as `pageToken` to retrieve the next page. If this field is omitted, there are no additional pages.                                                                                                                                           |
|                  |                                                                                                                                                                                                                                                                            |

#### Request/Response

<CodeGroup>
  ```json RequestJSON  theme={null}
  {
      "id": 1,
      "jsonrpc": "2.0",
      "method": "cdp_listBalances",
      "params": [
          {
          "address": "0x0e73fc61bb9d6b7588910c2d14e83bae68222c5d",
          "pageToken": "",
          "pageSize": 2
          }
      ]
  }
  ```

  ```json ResponseJSON theme={null}
  {
      "id": 1,
      "jsonrpc": "2.0",
      "result": {
      "balances": [
      {
          "asset": {
          "id": "08122fa4-510f-5ae4-9675-792c378b0018",
          "type": "erc20",
          "groupId": "0x6BE5830023b84f1C9B5BABB0Ca2B2a9DC5b9eD79",
          "subGroupId": ""
          },
          "value": 52333187000000000000000000,
          "valueStr": "52333187000000000000000000",
          "decimals": 18
      },
      {
          "asset": {
          "id": "1ddd4cf2-18ca-5c11-a7d5-d293330b19c7",
          "type": "erc20",
          "groupId": "0xd9aAEc86B65D86f6A7B5B1b0c42FFA531710b6CA",
          "subGroupId": ""
          },
          "value": 1173345,
          "valueStr": "1173345",
          "decimals": 6
      }
      ],
      "nextPageToken": "Y2ZfUXRhTUpYeTZGZ......M2I3LTY5MmJiMmM1ZTEzNCJ9"
  }
  }
  ```
</CodeGroup>

### `cdp_listBalanceDetails`

This endpoint lists the latest balance details for an asset for an address.
Similar to `cdp_listBalances`, if you need more real-time data, you should use the [CDP API](/api-reference/rest-api/addresses/list-address-balances).

The [API credit](/data/node/overview#rate-limits) value of this method is 100.

#### Parameters

| Name      | Type   | Req | Description                                                                                                                                               |
| :-------- | :----- | :-: | :-------------------------------------------------------------------------------------------------------------------------------------------------------- |
| address   | string |  Y  | Blockchain address hash. EVM chain address hash should be lowercase.                                                                                      |
| assetId   | string |  Y  | Provided from ListBalances or ListAddressTransactions response's asset field                                                                              |
| pageSize  | string |  N  | Number of balances to receive in a page. The default value is 25. The maximum value is 100, and values supplied over this will be coerced to the maximum. |
| pageToken | string |  N  | Provided from a previous response's nextPageToken                                                                                                         |

#### Returns

| Field            | Description                                                                                                                                                                                                                                                                |
| :--------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| asset.id         | The identity of the asset for querying for details or history.                                                                                                                                                                                                             |
| asset.type       | The type of Asset the definition describes. For example: "native", "erc20", "erc721", "erc1155", "creditAlphanum4", "fa2".                                                                                                                                                 |
| asset.groupId    | The contract address or group identifier for an Asset. For an NFT or a multi-token Asset this may identify a group of Asset. For a native Asset this will not be set.                                                                                                      |
| asset.subGroupId | The identifier that distinguishes the identity of the Asset within the contract address or group. For an NFT or a multi-token Asset that can have many Assets associated with a contract address, this could be a token ID. For a UTXO, this could be the coin identifier. |
| value            | The amount of the balance in the lowest denomination of the asset. Type is in BigInteger in standard base64 encoding.                                                                                                                                                      |
| valueStr         | The string representation of the balance value to avoid precision loss.                                                                                                                                                                                                    |
| decimals         | The number of decimals the asset utilizes.                                                                                                                                                                                                                                 |
| nextPageToken    | A token which can be provided as `pageToken` to retrieve the next page. If this field is omitted, there are no additional pages.                                                                                                                                           |

#### Request/Response

<CodeGroup>
  ```json RequestJSON theme={null}
  {
      "id": 1,
      "jsonrpc": "2.0",
      "method": "cdp_listBalanceDetails",
      "params": [
          {
          "address": "0x0e73fc61bb9d6b7588910c2d14e83bae68222c5d",
          "assetId": "08122fa4-510f-5ae4-9675-792c378b0018",
          "pageToken": "",
          "pageSize": 1
          }
      ]
  }
  ```

  ```json ResponseJSON theme={null}
      {
          "id": 1,
          "jsonrpc": "2.0",
          "result": {
          "balances": [
              {
                  "asset": {
                  "id": "08122fa4-510f-5ae4-9675-792c378b0018",
                  "type": "erc20",
                  "groupId": "0x6BE5830023b84f1C9B5BABB0Ca2B2a9DC5b9eD79",
                  "subGroupId": ""
                  },
                  "value": 52333187000000000000000000,
                  "valueStr": "52333187000000000000000000",
                  "decimals": 18
              }
              ],
              "nextPageToken": ""
          }
      }
  ```
</CodeGroup>

### `cdp_listBalanceHistories`

This endpoint lists the balance histories for an asset for an address. `cdp_listBalanceHistory` is also a valid method name for this method.

The [API credit](/data/node/overview#rate-limits) value of this method is 100.

#### Parameters

| Name      | Type   | Req | Description                                                                                                                                               |
| :-------- | :----- | :-: | :-------------------------------------------------------------------------------------------------------------------------------------------------------- |
| address   | string |  Y  | Blockchain address hash. EVM chain address hash should be lowercase.                                                                                      |
| assetId   | string |  Y  | Provided from ListBalances or ListAddressTransactions response's asset field                                                                              |
| pageSize  | string |  N  | Number of balances to receive in a page. The default value is 25. The maximum value is 100, and values supplied over this will be coerced to the maximum. |
| pageToken | string |  N  | Provided from a previous response's nextPageToken                                                                                                         |

#### Returns

| Field         | Description                                                                                                                      |
| :------------ | :------------------------------------------------------------------------------------------------------------------------------- |
| blockHash     | The hash of the block this transaction was included in.                                                                          |
| blockHeight   | The height of the block this transaction was included in.                                                                        |
| value         | The amount of the balance in the lowest denomination of the asset. Type is in BigInteger in standard base64 encoding.            |
| valueStr      | The string representation of the balance value to avoid precision loss.                                                          |
| nextPageToken | A token which can be provided as `pageToken` to retrieve the next page. If this field is omitted, there are no additional pages. |

#### Request/Response

<CodeGroup>
  ```json RequestJSON theme={null}
  {
      "id": 1,
      "jsonrpc": "2.0",
      "method": "cdp_listBalanceHistories",
      "params": [
          {
          "address": "0x0e73fc61bb9d6b7588910c2d14e83bae68222c5d",
          "assetId": "123d82ca-b3f4-527c-ace7-559d5791a564",
          "pageToken": "",
          "pageSize": 2
          }
      ]
  }
  ```

  ```json ResponseJSON theme={null}
  {
      "id": 1,
      "jsonrpc": "2.0",
      "result": {
          "balanceHistories": [
          {
              "blockHeight": 2767233,
              "blockHash": "0x980773f020fea...70ee1a2f349241df338",
              "value": 4999990000000000000000,
              "valueStr": "4999990000000000000000"
          }
          ],
          "nextPageToken": ""
      }
  }
  ```
</CodeGroup>

### `cdp_listAddressTransactions`

This endpoint lists the transactions for an address. `cdp_listTransactions` is also a valid method name for this method.

The [API credit](/data/node/overview#rate-limits) value of this method is 100.

#### Parameters

| Name      | Type   | Req | Description                                                                                                                                               |
| :-------- | :----- | :-: | :-------------------------------------------------------------------------------------------------------------------------------------------------------- |
| address   | string |  Y  | Blockchain address hash. EVM chain address hash should be lowercase.                                                                                      |
| pageSize  | string |  N  | Number of balances to receive in a page. The default value is 25. The maximum value is 100, and values supplied over this will be coerced to the maximum. |
| pageToken | string |  N  | Provided from a previous response's nextPageToken                                                                                                         |

#### Returns

| Field       | Description                                                                                                                                                       |
| :---------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| name        | A unique identifier for the transaction, which cannot be changed once created.In the format of `networks/{network}/indexers/{indexer}/transactions/{transaction}` |
| hash        | The transaction hash                                                                                                                                              |
| blockHash   | The hash of the block this transaction was included in.                                                                                                           |
| blockHeight | The height of the block this transaction was included in.                                                                                                         |
| status      | The status of the transaction                                                                                                                                     |
| content     | The transaction content in either ethereum or rosetta format.                                                                                                     |

#### Request/Response

<CodeGroup>
  ```json RequestJSON theme={null}
  {
      "id": 1,
      "jsonrpc": "2.0",
      "method": "cdp_listAddressTransactions",
      "params": [
          {
          "address": "0x0e73fc61bb9d6b7588910c2d14e83bae68222c5d",
          "pageToken": "",
          "pageSize": 2
          }
      ]
  }
  ```

  ```json ResponseJSON [expandable] theme={null}
      {
      "id": 1,
      "jsonrpc": "2.0",
      "result": {
          "addressTransactions": [
          {
              "name": "networks/polygon-mainnet/indexers/default/transactions/0x8e9a4e099a8453e71b31b6c2c23b25926aadedf096bfb39071f1c84be0a8a06b",
              "hash": "0x8e9a4e099...9071f1c84be0a8a06b",
              "blockHash": "0xa6a7435ad5cc...13405fd38f5d85f",
              "blockHeight": "56393424",
              "status": "CONFIRMED",
              "ethereum": {
              "blockHash": "0xa6a7435ad5cc...13405fd38f5d85f",
              "blockNumber": "56393424",
              "from": "0xa83bd46d2757800bc8314a2cc14714c4afe272b5",
              "gas": "105257",
              "gasPrice": "125953591812",
              "hash": "0x8e9a4e099a8...1f1c84be0a8a06b",
              "input": "0xef6c59...000000000",
              "nonce": "119022",
              "to": "0xf6d1b85af155229acd7b523601148585a1ff67c6",
              "index": "8",
              "value": "0",
              "receipt": {
                  "transactionHash": "0x8e9a4e09...f1c84be0a8a06b",
                  "transactionIndex": "8",
                  "blockHash": "0xa6a7435ad5c...9713405fd38f5d85f",
                  "blockNumber": "56393424",
                  "from": "0xa83bd46d2757800bc8314a2cc14714c4afe272b5",
                  "to": "0xf6d1b85af155229acd7b523601148585a1ff67c6",
                  "cumulativeGasUsed": "893833",
                  "gasUsed": "105257",
                  "contractAddress": "",
                  "logs": [
                  {
                      "removed": false,
                      "logIndex": "27",
                      "transactionHash": "0x8e9a4e09...c84be0a8a06b",
                      "transactionIndex": "8",
                      "blockHash": "0xa6a743...3405fd38f5d85f",
                      "blockNumber": "56393424",
                      "address": "0x5d666f2...7ecd2c8cc44e6",
                      "data": "0x",
                      "topics": [
                      "0xddf252ad1be2c...4a11628f55a4df523b3ef",
                      "0x00000000000000...00000000000000",
                      "0x0000000000...2d14e83bae68222c5d",
                      "0x00000000000...0000000000020c669e"
                      ]
                  }
                  ],
                  "logsBloom": "0x0000000000...00000100000",
                  "root": "",
                  "status": "1",
                  "type": "0",
                  "effectiveGasPrice": "125953591812"
              },
              "tokenTransfers": [
                  {
                  "tokenAddress": "0x5d666f...ecd2c8cc44e6",
                  "fromAddress": "0x000000000...00000000",
                  "toAddress": "0x0e73fc6...bae68222c5d",
                  "value": "",
                  "transactionIndex": "8",
                  "transactionHash": "0x8e9a4e0..e0a8a06b",
                  "logIndex": "27",
                  "blockHash": "0xa6a7435ad5..9713405fd38f5d85f",
                  "blockNumber": "56393424",
                  "erc721": {
                      "fromAddress": "0x000000000..0000",
                      "toAddress": "0x0e73fc61b..e68222c5d",
                      "tokenId": "34367134"
                  }
                  }
              ],
              "type": "0",
              "priorityFeePerGas": "82907832252",
              "flattenedTraces": [
                  {
                  "error": "",
                  "type": "CALL",
                  "from": "0xa83bd46d2...fe272b5",
                  "to": "0xf6d1b85af155229acd7b523601148585a1ff67c6",
                  "value": "0",
                  "gas": "105257",
                  "gasUsed": "105257",
                  "input": "0xef6c599600...000000000000",
                  "output": "",
                  "subtraces": "2",
                  "traceAddress": [],
                  "traceType": "CALL",
                  "callType": "CALL",
                  "traceId": "CALL_0x8e9a4e099a...1c84be0a8a06b",
                  "status": "1",
                  "blockHash": "0xa6a7435ad5...713405fd38f5d85f",
                  "blockNumber": "56393424",
                  "transactionHash": "0x8e9a4e099a...f1c84be0a8a06b",
                  "transactionIndex": "8"
                  }
              ],
              "blockTimestamp": "2024-04-29T18:08:30Z"
              }
          }
          ],
          "nextPageToken": "RlZ6VFBwc2lDSVd...IzEiLCJpZHgiOjB9"
      }
      }
  ```
</CodeGroup>

