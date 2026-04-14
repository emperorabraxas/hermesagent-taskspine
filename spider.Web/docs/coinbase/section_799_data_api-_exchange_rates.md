# Data API- Exchange Rates
Source: https://docs.cdp.coinbase.com/coinbase-app/track-apis/exchange-rates



## Table of Endpoints

| Name                                      | Method | Endpoint             | Scope |
| :---------------------------------------- | :----- | :------------------- | :---- |
| [Get Exchange Rates](#get-exchange-rates) | GET    | `/v2/exchange-rates` | N/A   |

## Get Exchange Rates

Get current exchange rates. Default base currency is `USD` but it can be defined as any supported currency (see `Currencies` endpoint). Returned rates will define the exchange rate for one unit of the base currency.

**This endpoint doesn't require authentication.**

### HTTP Request

`GET https://api.coinbase.com/v2/exchange-rates`

### Scopes

* *No permission required*

### Arguments

| Parameter | Type   | Required | Description                    |
| :-------- | :----- | :------- | :----------------------------- |
| currency  | string | Optional | Base currency (default: `USD`) |

### Examples

#### Request

<CodeGroup>
  ```shell Shell lines wrap theme={null}
  curl https://api.coinbase.com/v2/exchange-rates?currency=BTC
  ```

  ```ruby Ruby lines wrap theme={null}
  require 'coinbase/wallet'
  client = Coinbase::Wallet::Client.new(api_key: <api key>, api_secret: <api secret>)

  rates = client.exchange_rates({currency: 'BTC'})
  ```

  ```python Python lines wrap theme={null}
  from coinbase.wallet.client import Client
  client = Client(<api_key>, <api_secret>)

  rates = client.get_exchange_rates(currency='BTC')
  ```

  ```javascript JavaScript lines wrap theme={null}
  var Client = require('coinbase').Client;
  var client = new Client({'apiKey': 'API KEY', 
                           'apiSecret': 'API SECRET'});

  client.getExchangeRates({'currency': 'BTC'}, function(err, rates) {
    console.log(rates);
  });
  ```
</CodeGroup>

#### Response

```json lines wrap theme={null}
{
  "data": {
    "currency": "BTC",
    "rates": {
      "AED": "36.73",
      "AFN": "589.50",
      "ALL": "1258.82",
      "AMD": "4769.49",
      "ANG": "17.88",
      "AOA": "1102.76",
      "ARS": "90.37",
      "AUD": "12.93",
      "AWG": "17.93",
      "AZN": "10.48",
      "BAM": "17.38",
      ...
    }
  }
}
```

