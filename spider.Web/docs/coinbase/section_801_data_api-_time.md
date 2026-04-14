# Data API- Time
Source: https://docs.cdp.coinbase.com/coinbase-app/track-apis/time



## Table of Endpoints

| Name                                  | Method | Endpoint   | Scope |
| :------------------------------------ | :----- | :--------- | :---- |
| [Get Current Time](#get-current-time) | GET    | `/v2/time` | N/A   |

## Get Current Time

Get the API server time.

**This endpoint doesn't require authentication.**

### HTTP Request

`GET https://api.coinbase.com/v2/time`

### Scopes

* *No permission required*

### Examples

#### Request

<CodeGroup>
  ```shell Shell lines wrap theme={null}
  curl https://api.coinbase.com/v2/time
  ```

  ```ruby Ruby lines wrap theme={null}
  require 'coinbase/wallet'
  client = Coinbase::Wallet::Client.new(api_key: <api key>, api_secret: <api secret>)

  time = client.time
  ```

  ```python Python lines wrap theme={null}
  from coinbase.wallet.client import Client
  client = Client(<api_key>, <api_secret>)

  time = client.get_time()
  ```

  ```javascript JavaScript lines wrap theme={null}
  var Client = require('coinbase').Client;
  var client = new Client({'apiKey': 'API KEY', 
                           'apiSecret': 'API SECRET'});

  client.getTime(function(err, time) {
    console.log(time);
  });
  ```
</CodeGroup>

#### Response

```json lines wrap theme={null}
{
  "data": {
    "iso": "2015-06-23T18:02:51Z",
    "epoch": 1435082571
  }
}
```

