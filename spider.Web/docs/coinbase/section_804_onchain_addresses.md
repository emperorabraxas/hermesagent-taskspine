# Onchain Addresses
Source: https://docs.cdp.coinbase.com/coinbase-app/transfer-apis/onchain-addresses



## Table of Endpoints

| Name                                    | Method | Endpoint                                                      | Legacy Scope               | CDP API Key Scope |
| :-------------------------------------- | :----- | :------------------------------------------------------------ | :------------------------- | :---------------- |
| [Create Address](#create-address)       | POST   | `/v2/accounts/:account_id/addresses`                          | `wallet:addresses:create`  | `transfer`        |
| [List Addresses](#list-addresses)       | GET    | `/v2/accounts/:account_id/addresses`                          | `wallet:addresses:read`    | `view`            |
| [Show Address](#show-address)           | GET    | `/v2/accounts/:account_id/addresses/:address_id`              | `wallet:addresses:read`    | `view`            |
| [List Transactions](#list-transactions) | GET    | `/v2/accounts/:account_id/addresses/:address_id/transactions` | `wallet:transactions:read` | `view`            |

## Overview

The **Address resource** represents an address for any [Coinbase supported asset](https://help.coinbase.com/en/coinbase/supported-crypto). An account can have more than one address, but an address can only be associated with one account.

To be notified when an address receives a new transactions, you can set up an API notification

| Parameter                                 | Description                                                                                        |
| :---------------------------------------- | :------------------------------------------------------------------------------------------------- |
| `id` *string*                             | Resource ID                                                                                        |
| `address` *string*                        | Address for any [Coinbase supported asset](https://help.coinbase.com/en/coinbase/supported-crypto) |
| `name` *string, optional*                 | User defined label for the address                                                                 |
| `network` *string*                        | Name of blockchain                                                                                 |
| `created_at` *timestamp*                  |                                                                                                    |
| `updated_at` *timestamp*                  |                                                                                                    |
| `resource` *string, constant **address*** |                                                                                                    |
| `resource_path` *string*                  |                                                                                                    |

#### Example Address Resource

```json lines wrap theme={null}
{
  "id": "dd3183eb-af1d-5f5d-a90d-cbff946435ff",
  "address": "mswUGcPHp1YnkLCgF1TtoryqSc5E9Q8xFa",
  "name": "One off payment",
  "created_at": "2015-01-31T20:49:02Z",
  "updated_at": "2015-03-31T17:25:29-07:00",
  "network": "bitcoin",
  "resource": "address",
  "resource_path": "/v2/accounts/2bbf394c-193b-5b2a-9155-3b4732659ede/addresses/dd3183eb-af1d-5f5d-a90d-cbff946435ff"
}
```

## Create Address

Creates a new address for an account. Addresses can be created for wallet account types.

<Tip>
  You can create an address with an empty `POST` request as all arguments are optional. This is handy if you need to create new receive addresses for an account on-demand.
</Tip>

### HTTP Request

`POST https://api.coinbase.com/v2/accounts/:account_id/addresses`

### Scopes

* `wallet:addresses:create`

### Arguments

| Parameter | Type   | Required | Description                                                                                                                                                                   |
| :-------- | :----- | :------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| name      | string | Optional | Address label                                                                                                                                                                 |
| network   | string | Optional | The blockchain network for the address (e.g., `ethereum`, `solana`, `bitcoin`, `base`, `polygon`). If not provided, the default network for the account's asset will be used. |

### Examples

#### Request

<CodeGroup>
  ```shell Shell [expandable] lines wrap theme={null}
  curl https://api.coinbase.com/v2/accounts/82de7fcd-db72-5085-8ceb-bee19303080b/addresses \
    -X POST \
    -H 'Content-Type: application/json' \
    -H 'Authorization: Bearer abd90df5f27a7b170cd775abf89d632b350b7c1c9d53e08b340cd9832ce52c2c' \
    -d '{"name": "New receive address", "network": "ethereum"}'
  }
  ```

  ````ruby Ruby  lines wrap theme={null}
  ```ruby lines wrap
  require 'coinbase/wallet'
  client = Coinbase::Wallet::Client.new(api_key: <api key>, api_secret: <api secret>)

  address = client.create_address('2bbf394c-193b-5b2a-9155-3b4732659ede')
  ````

  ```python Python  lines wrap theme={null}
  import requests

  # For instructions generating JWT, check the "API Key Authentication" section
  JWT_TOKEN = "<your_jwt_token>"

  ENDPOINT_URL = f"https://api.coinbase.com/v2/accounts/:account_id/addresses"

  def create_address():
      # Generate headers with JWT for authentication
      headers = {
          "Authorization": f"Bearer {JWT_TOKEN}"
      }

      data = {
          "name": "Test new address",
          "network": "ethereum"
      }

      # Make the API request
      response = requests.post(ENDPOINT_URL, data=data, headers=headers)

      return response.json()  # Return the JSON response

  address = create_address()
  print(address)
  ```

  ```javascript JavaScript  lines wrap theme={null}
  var Client = require('coinbase').Client;

  var client = new Client({'apiKey': 'API KEY',
                           'apiSecret': 'API SECRET'});

  client.getAccount('82de7fcd-db72-5085-8ceb-bee19303080b', function(err, account) {
    account.createAddress(null, function(err, address) {
      console.log(address);
    });
  });
  ```
</CodeGroup>

#### Response (201)

```json lines wrap theme={null}
{
  "data": {
    "id": "dd3183eb-af1d-5f5d-a90d-cbff946435ff",
    "address": "0xc0ffee254729296a45a3885639AC7E10F9d54979",
    "name": "New receive address",
    "created_at": "2015-01-31T20:49:02Z",
    "updated_at": "2015-03-31T17:25:29-07:00",
    "network": "ethereum",
    "resource": "address",
    "resource_path": "/v2/accounts/2bbf394c-193b-5b2a-9155-3b4732659ede/addresses/dd3183eb-af1d-5f5d-a90d-cbff946435ff"
  }
}
```

## List Addresses

Lists addresses for an account.

<Warning>
  An address can only be associated with one account. See [Create Address](#create-address) to create new addresses.
</Warning>

### HTTP Request

`GET https://api.coinbase.com/v2/accounts/:account_id/addresses`

### Scopes

* `wallet:addresses:read`

### Examples

#### Request

<CodeGroup>
  ```shell Shell  lines wrap theme={null}
  curl https://api.coinbase.com/v2/accounts/2bbf394c-193b-5b2a-9155-3b4732659ede/addresses \
    -H 'Authorization: Bearer abd90df5f27a7b170cd775abf89d632b350b7c1c9d53e08b340cd9832ce52c2c'
  ```

  ```ruby Ruby  lines wrap theme={null}
  require 'coinbase/wallet'
  client = Coinbase::Wallet::Client.new(api_key: <api key>, api_secret: <api secret>)

  addresses = client.addresses('2bbf394c-193b-5b2a-9155-3b4732659ede')
  ```

  ```python Python  lines wrap theme={null}
  import requests

  # For instructions generating JWT, check the "API Key Authentication" section
  JWT_TOKEN = "<your_jwt_token>"

  ENDPOINT_URL = f"https://api.coinbase.com/v2/accounts/:account_id/addresses"

  def get_addresses():
      # Generate headers with JWT for authentication
      headers = {
          "Authorization": f"Bearer {JWT_TOKEN}"
      }

      # Make the API request
      response = requests.get(ENDPOINT_URL, headers=headers)

      return response.json()  # Return the JSON response

  addresses = get_addresses()
  print(addresses)
  ```

  ```javascript JavaScript  lines wrap theme={null}
  var Client = require('coinbase').Client;

  var client = new Client({'apiKey': 'API KEY',
                           'apiSecret': 'API SECRET'});

  client.getAccount('82de7fcd-db72-5085-8ceb-bee19303080b', function(err, account) {
    account.getAddresses(function(err, addresses) {
      console.log(addresses);
    });
  });
  ```
</CodeGroup>

#### Response

```json lines wrap theme={null}
{
  "pagination": {
    "ending_before": null,
    "starting_after": null,
    "limit": 25,
    "order": "desc",
    "previous_uri": null,
    "next_uri": null
  },
  "data": [
    {
      "id": "dd3183eb-af1d-5f5d-a90d-cbff946435ff",
      "address": "mswUGcPHp1YnkLCgF1TtoryqSc5E9Q8xFa",
      "name": null,
      "created_at": "2015-01-31T20:49:02Z",
      "updated_at": "2015-03-31T17:25:29-07:00",
      "network": "bitcoin",
      "resource": "address",
      "resource_path": "/v2/accounts/2bbf394c-193b-5b2a-9155-3b4732659ede/addresses/dd3183eb-af1d-5f5d-a90d-cbff946435ff"
    },
    {
      "id": "ac5c5f15-0b1d-54f5-8912-fecbf66c2a64",
      "address": "mgSvu1z1amUFAPkB4cUg8ujaDxKAfZBt5Q",
      "name": null,
      "created_at": "2015-03-31T17:23:52-07:00",
      "updated_at": "2015-01-31T20:49:02Z",
      "network": "bitcoin",
      "resource": "address",
      "resource_path": "/v2/accounts/2bbf394c-193b-5b2a-9155-3b4732659ede/addresses/ac5c5f15-0b1d-54f5-8912-fecbf66c2a64"
    }
  ]
}
```

## Show Address

Get an single address for an account.

<Warning>
  An address can only be associated with one account. See [Create Address](#create-address) to create new addresses.
</Warning>

### HTTP Request

`GET https://api.coinbase.com/v2/accounts/:account_id/addresses/:address_id`

### Scopes

* `wallet:addresses:read`

### Examples

#### Request

<CodeGroup>
  ```shell Shell  lines wrap theme={null}
  curl https://api.coinbase.com/v2/accounts/2bbf394c-193b-5b2a-9155-3b4732659ede/addresses/dd3183eb-af1d-5f5d-a90d-cbff946435ff \
    -H 'Authorization: Bearer abd90df5f27a7b170cd775abf89d632b350b7c1c9d53e08b340cd9832ce52c2c'
  ```

  ```ruby Ruby  lines wrap theme={null}
  require 'coinbase/wallet'
  client = Coinbase::Wallet::Client.new(api_key: <api key>, api_secret: <api secret>)

  address = client.address('2bbf394c-193b-5b2a-9155-3b4732659ede', 'dd3183eb-af1d-5f5d-a90d-cbff946435ff')
  ```

  ```python Python  lines wrap theme={null}
  import requests

  # For instructions generating JWT, check the "API Key Authentication" section
  JWT_TOKEN = "<your_jwt_token>"

  ENDPOINT_URL = "https://api.coinbase.com/v2/accounts/:account_id/addresses/:address_id"

  def show_address():
      # Generate headers with JWT for authentication
      headers = {
          "Authorization": f"Bearer {JWT_TOKEN}"
      }

      # Make the API request
      response = requests.get(ENDPOINT_URL, headers=headers)

      return response.json()  # Return the JSON response

  address = show_address()
  print(address)
  ```

  ```javascript JavaScript  lines wrap theme={null}
  var Client = require('coinbase').Client;

  var client = new Client({'apiKey': 'API KEY',
                           'apiSecret': 'API SECRET'});

  client.getAccount('82de7fcd-db72-5085-8ceb-bee19303080b', function(err, account) {
    account.getAddress('dd3183eb-af1d-5f5d-a90d-cbff946435ff', function(err, address) {
      console.log(address);
    });
  });
  ```
</CodeGroup>

#### Response

```json lines wrap theme={null}
{
  "data": {
    "id": "dd3183eb-af1d-5f5d-a90d-cbff946435ff",
    "address": "mswUGcPHp1YnkLCgF1TtoryqSc5E9Q8xFa",
    "name": null,
    "callback_url": null,
    "created_at": "2015-01-31T20:49:02Z",
    "updated_at": "2015-03-31T17:25:29-07:00",
    "network": "bitcoin",
    "resource": "address",
    "resource_path": "/v2/accounts/2bbf394c-193b-5b2a-9155-3b4732659ede/addresses/dd3183eb-af1d-5f5d-a90d-cbff946435ff/"
  }
}
```

## List Transactions

List transactions that have been sent to a specific address.

### HTTP Request

`GET https://api.coinbase.com/v2/accounts/:account_id/addresses/:address_id/transactions`

### Scopes

* `wallet:transactions:read`

### Examples

#### Request

<CodeGroup>
  ```shell Shell  lines wrap theme={null}
  curl https://api.coinbase.com/v2/accounts/2bbf394c-193b-5b2a-9155-3b4732659ede/addresses/dd3183eb-af1d-5f5d-a90d-cbff946435ff/transactions \
    -H 'Authorization: Bearer abd90df5f27a7b170cd775abf89d632b350b7c1c9d53e08b340cd9832ce52c2c'
  ```

  ```ruby Ruby  lines wrap theme={null}
  require 'coinbase/wallet'
  client = Coinbase::Wallet::Client.new(api_key: <api key>, api_secret: <api secret>)

  txs = client.address_transactions('2bbf394c-193b-5b2a-9155-3b4732659ede', 'dd3183eb-af1d-5f5d-a90d-cbff946435ff')
  ```

  ```python Python  lines wrap theme={null}
  import requests

  # For instructions generating JWT, check the "API Key Authentication" section
  JWT_TOKEN = "<your_jwt_token>"

  ENDPOINT_URL = "https://api.coinbase.com/v2/accounts/:account_id/addresses/:address_id/transactions"

  def list_transactions():
      # Generate headers with JWT for authentication
      headers = {
          "Authorization": f"Bearer {JWT_TOKEN}"
      }

      # Make the API request
      response = requests.get(ENDPOINT_URL, headers=headers)

      return response.json()  # Return the JSON response

  transactions = list_transactions()
  print(transactions)
  ```

  ```javascript JavaScript  lines wrap theme={null}
  var Client = require('coinbase').Client;

  var client = new Client({'apiKey': 'API KEY',
                           'apiSecret': 'API SECRET'});

  client.getAccount('82de7fcd-db72-5085-8ceb-bee19303080b', function(err, account) {
    account.getAddress('dd3183eb-af1d-5f5d-a90d-cbff946435ff', function(err, address) {
      console.log(address);
      address.getTransactions({}, function(err, txs) {
        console.log(txs);
      });
    });
  });
  ```
</CodeGroup>

#### Response

```json lines wrap theme={null}
{
  "pagination": {
    "ending_before": null,
    "starting_after": null,
    "limit": 25,
    "order": "desc",
    "previous_uri": null,
    "next_uri": null
  },
  "data": [
    {
      "id": "57ffb4ae-0c59-5430-bcd3-3f98f797a66c",
      "type": "send",
      "status": "completed",
      "amount": {
        "amount": "0.00100000",
        "currency": "BTC"
      },
      "native_amount": {
        "amount": "0.01",
        "currency": "USD"
      },
      "description": null,
      "created_at": "2015-03-11T13:13:35-07:00",
      "updated_at": "2015-03-26T15:55:43-07:00",
      "resource": "transaction",
      "resource_path": "/v2/accounts/2bbf394c-193b-5b2a-9155-3b4732659ede/transactions/57ffb4ae-0c59-5430-bcd3-3f98f797a66c",
      "network": {
        "status": "off_blockchain",
        "name": "bitcoin"
      },
      "from": {
        "id": "a6b4c2df-a62c-5d68-822a-dd4e2102e703",
        "resource": "user"
      }
    }
  ]
}
```

