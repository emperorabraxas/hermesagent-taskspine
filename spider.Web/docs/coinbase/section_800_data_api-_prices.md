# Data API- Prices
Source: https://docs.cdp.coinbase.com/coinbase-app/track-apis/prices



## Table of Endpoints

| Name                              | Method | Endpoint                         | Scope |
| :-------------------------------- | :----- | :------------------------------- | :---- |
| [Get Buy Price](#get-buy-price)   | GET    | `/v2/prices/:currency_pair/buy`  | N/A   |
| [Get Sell Price](#get-sell-price) | GET    | `/v2/prices/:currency_pair/sell` | N/A   |
| [Get Spot Price](#get-spot-price) | GET    | `/v2/prices/:currency_pair/spot` | N/A   |

## Get Buy Price

Get the total price to buy one bitcoin or ether.

Note that exchange rates fluctuates so the price is only correct for seconds at the time. This buy price includes standard Coinbase fee (1%) but excludes any other fees including bank fees. If you need more accurate price estimate for a specific payment method or amount, see buy bitcoin endpoint and `quote: true` option.

**This endpoint doesn't require authentication.**

### HTTP Request

`GET https://api.coinbase.com/v2/prices/:currency_pair/buy`

### Scopes

* *No permission required*

### Examples

#### Request

<CodeGroup>
  ```shell Shell lines wrap theme={null}
  curl https://api.coinbase.com/v2/prices/BTC-USD/buy \
    -H 'Authorization: Bearer abd90df5f27a7b170cd775abf89d632b350b7c1c9d53e08b340cd9832ce52c2c'
  ```

  ```ruby Ruby lines wrap theme={null}
  require 'coinbase/wallet'
  client = Coinbase::Wallet::Client.new(api_key: <api key>, api_secret: <api secret>)

  price = client.buy_price({currency_pair: 'BTC-USD'})
  ```

  ```python Python lines wrap theme={null}
  from coinbase.wallet.client import Client
  client = Client(<api_key>, <api_secret>)

  price = client.get_buy_price(currency_pair = 'BTC-USD')
  ```

  ```javascript JavaScript lines wrap theme={null}
  var Client = require('coinbase').Client;
  var client = new Client({'apiKey': 'API KEY',
                           'apiSecret': 'API SECRET'});

  client.getBuyPrice({'currencyPair': 'BTC-USD'}, function(err, price) {
    console.log(price);
  });
  ```
</CodeGroup>

#### Response

```json lines wrap theme={null}
{
  "data": {
    "amount": "1020.25",
    "currency": "USD"
  }
}
```

## Get Sell Price

Get the total price to sell one bitcoin or ether.

Note that exchange rates fluctuates so the price is only correct for seconds at the time. This sell price includes standard Coinbase fee (1%) but excludes any other fees including bank fees. If you need more accurate price estimate for a specific payment method or amount, see sell bitcoin endpoint and `quote: true` option.

**This endpoint doesn't require authentication.**

### HTTP Request

`GET https://api.coinbase.com/v2/prices/:currency_pair/sell`

### Scopes

* *No permission required*

### Examples

#### Request

<CodeGroup>
  ```shell Shell lines wrap theme={null}
  curl https://api.coinbase.com/v2/prices/BTC-USD/sell /
    -H 'Authorization: Bearer abd90df5f27a7b170cd775abf89d632b350b7c1c9d53e08b340cd9832ce52c2c'
  ```

  ```ruby Ruby lines wrap theme={null}
  require 'coinbase/wallet'
  client = Coinbase::Wallet::Client.new(api_key: <api key>, api_secret: <api secret>)

  price = client.sell_price({currency_pair: 'BTC-USD'})
  ```

  ```python Python lines wrap theme={null}
  from coinbase.wallet.client import Client
  client = Client(<api_key>, <api_secret>)

  price = client.get_sell_price(currency_pair = 'BTC-USD')
  ```

  ```javascript JavaScript lines wrap theme={null}
  var Client = require('coinbase').Client;
  var client = new Client({'apiKey': 'API KEY',
                           'apiSecret': 'API SECRET'});

  client.getSellPrice({'currencyPair': 'BTC-USD'}, function(err, price) {
    console.log(price);
  });
  ```
</CodeGroup>

#### Response

```json lines wrap theme={null}
{
  "data": {
    "amount": "1010.25",
    "currency": "USD"
  }
}
```

## Get Spot Price

Get the current market price for bitcoin. This is usually somewhere in between the buy and sell price.

Note that exchange rates fluctuates so the price is only correct for seconds at the time.

You can also get historic prices with `date` parameter.

**This endpoint doesn't require authentication.**

### HTTP Request

`GET https://api.coinbase.com/v2/prices/:currency_pair/spot`

### Scopes

* *No permission required*

### Arguments

| Parameter | Type   | Required | Description                                            |
| :-------- | :----- | :------- | :----------------------------------------------------- |
| date      | string | Optional | For historic spot price, use format `YYYY-MM-DD` (UTC) |

### Examples

#### Request

<CodeGroup>
  ```shell Shell lines wrap theme={null}
  curl https://api.coinbase.com/v2/prices/BTC-USD/spot \
    -H 'Authorization: Bearer abd90df5f27a7b170cd775abf89d632b350b7c1c9d53e08b340cd9832ce52c2c'
  ```

  ```ruby Ruby lines wrap theme={null}
  require 'coinbase/wallet'
  client = Coinbase::Wallet::Client.new(api_key: <api key>, api_secret: <api secret>)

  price = client.spot_price({currency_pair: 'BTC-USD'})
  ```

  ```python Python lines wrap theme={null}
  from coinbase.wallet.client import Client
  client = Client(<api_key>, <api_secret>)

  price = client.get_spot_price(currency_pair = 'BTC-USD')
  ```

  ```javascript JavaScript lines wrap theme={null}
  var Client = require('coinbase').Client;
  var client = new Client({'apiKey': 'API KEY',
                           'apiSecret': 'API SECRET'});

  client.getSpotPrice({'currencyPair': 'BTC-USD'}, function(err, price) {
    console.log(price);
  });
  ```
</CodeGroup>

#### Response

```json lines wrap theme={null}
{
  "data": {
    "amount": "1015.00",
    "currency": "USD"
  }
}
```

