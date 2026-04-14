# Staking API Usage
Source: https://docs.cdp.coinbase.com/staking/staking-api/reference/api-usage



<Tip>
  Staking API can be accessed via the CDP SDK, a simple client library for interacting with the Staking API, or through the CDP API, a restful API for direct http requests.
  For details on getting started with our SDK, see our [quickstart](/staking/staking-api/introduction/quickstart).
</Tip>

## Authentication

Our REST APIs use JWT tokens for authentication. Find more information on generating a JWT token in the language of your choice [here](/get-started/authentication/jwt-authentication#code-samples).

## Making an API request

1. Click through any API in the reference [here](/api-reference/rest-api/staking/build-a-new-staking-operation) to learn more about its parameters and usage.

2. Fill in the parameters. For APIs like [BuildStakingOperation](/api-reference/rest-api/staking/build-a-new-staking-operation) and [GetStakingContext](/api-reference/rest-api/staking/get-staking-context) that require custom options, refer to the [staking options](#staking-options) section below for available options.
   <div>
     <Frame>
       <img alt="API Input" />
     </Frame>
   </div>

3. Select your preferred language on the right to generate a sample request code. Use this as a reference to make a staking API request.

   For example, for the `BuildStakingOperation` API, the generated code for a Partial ETH stake of `0.1 ETH` will look like this in some of the common languages:

   <CodeGroup>
     ```bash Bash  theme={null}
     curl -s -L 'https://api.cdp.coinbase.com/platform/v1/stake/build' \
     -H 'Content-Type: application/json' \
     -H 'Accept: application/json' \
     -d '{
         "network_id": "ethereum-hoodi",
         "asset_id": "ETH",
         "address_id": "0xabcd",
         "action": "stake",
         "options": {
             "mode": "partial",
             "amount": "100000000000000000"
         }
     }'
     ```

     ```node NodeJs [expandable] theme={null}
     const axios = require('axios');

     let data = JSON.stringify({
         "network_id": "ethereum-hoodi",
         "asset_id": "ETH",
         "address_id": "0xabcd",
         "action": "stake",
         "options": {
             "mode": "partial",
             "amount": "100000000000000000"
         }
     });

     let config = {
         method: 'post',
         maxBodyLength: Infinity,
         url: 'https://api.cdp.coinbase.com/platform/v1/stake/build',
         headers: {
             'Content-Type': 'application/json',
             'Accept': 'application/json'
         },
         data : data
     };

     axios.request(config)
     .then((response) => {
         console.log(JSON.stringify(response.data));
     })
     .catch((error) => {
         console.log(error);
     });
     ```

     ```go Go [expandable] theme={null}
     package main

     import (
     "fmt"
     "net/http"
     "io/ioutil"
     "strings"
     )

     func main() {
     url := "https://api.cdp.coinbase.com/platform/v1/stake/build"
     method := "POST"
     payload := strings.NewReader(`{"network_id":"ethereum-hoodi","asset_id":"ETH","address_id":"0xabcd","action":"stake","options":{"mode":"partial","amount":"100000000000000000"}}`)

     client := &http.Client {}
     req, err := http.NewRequest(method, url, payload)

     if err != nil {
         fmt.Println(err)
         return
     }

     req.Header.Add("Content-Type", "application/json")
     req.Header.Add("Accept", "application/json")

     res, err := client.Do(req)
     if err != nil {
         fmt.Println(err)
         return
     }
     defer res.Body.Close()

     body, err := ioutil.ReadAll(res.Body)
     if err != nil {
         fmt.Println(err)
         return
     }
     fmt.Println(string(body))
     }
     ```
   </CodeGroup>

4. Finally, add the JWT token, obtained from the authentication section [above](#authentication), as a Bearer header in your request.
   The code will look like this:

   <CodeGroup>
     ```bash cURL theme={null}
     export JWT="generated-jwt-token" # Replace with your JWT token

     curl -s -L 'https://api.cdp.coinbase.com/platform/v1/stake/build' \
     -H 'Content-Type: application/json' \
     -H 'Accept: application/json' \
     -H "Authorization: Bearer ${JWT}" \
     -d '{
         "network_id": "ethereum-hoodi",
         "asset_id": "ETH",
         "address_id": "0xabcd",
         "action": "stake",
         "options": {
             "mode": "partial",
             "amount": "100000000000000000"
         }
     }'
     ```

     ```node NodeJs [expandable] theme={null}
     const axios = require('axios');

     let data = JSON.stringify({
         "network_id": "ethereum-hoodi",
         "asset_id": "ETH",
         "address_id": "0xabcd",
         "action": "stake",
         "options": {
             "mode": "partial",
             "amount": "100000000000000000"
         }
     });

     let JWT = 'generated-jwt-token'; // Replace with your JWT token

     let config = {
         method: 'post',
         maxBodyLength: Infinity,
         url: 'https://api.cdp.coinbase.com/platform/v1/stake/build',
         headers: {
             'Content-Type': 'application/json',
             'Accept': 'application/json',
             'Authorization': `Bearer ${JWT}`
         },
         data : data
     };

     axios.request(config)
     .then((response) => {
         console.log(JSON.stringify(response.data));
     })
     .catch((error) => {
         console.log(error);
     });
     ```

     ```go Go [expandable] theme={null}
     package main

     import (
     "fmt"
     "net/http"
     "io/ioutil"
     "strings"
     )

     func main() {
     url := "https://api.cdp.coinbase.com/platform/v1/stake/build"
     method := "POST"
     payload := strings.NewReader(`{"network_id":"ethereum-hoodi","asset_id":"ETH","address_id":"0xabcd","action":"stake","options":{"mode":"partial","amount":"100000000000000000"}}`)
     jwt := "generated-jwt-token" // Replace with your JWT token

     client := &http.Client {}
     req, err := http.NewRequest(method, url, payload)

     if err != nil {
         fmt.Println(err)
         return
     }

     req.Header.Add("Content-Type", "application/json")
     req.Header.Add("Accept", "application/json")
     req.Header.Add("Authorization", fmt.Sprintf("Bearer %s", jwt))

     res, err := client.Do(req)
     if err != nil {
         fmt.Println(err)
         return
     }
     defer res.Body.Close()

     body, err := ioutil.ReadAll(res.Body)
     if err != nil {
         fmt.Println(err)
         return
     }
     fmt.Println(string(body))
     }
     ```
   </CodeGroup>

***

## Staking Options

Some staking APIs such as [BuildStakingOperation](/api-reference/rest-api/staking/build-a-new-staking-operation) and [GetStakingContext](/api-reference/rest-api/staking/get-staking-context) require additional options to be passed in the request body specific to the staking network.
See below to find the options available for each staking network.

Once you have identified which options you need, you can add them to the request body under the `options` field like so:

```json lines wrap theme={null}
{
  ...
  "options": {
    "mode": "partial",
    "amount": "100000000000000000",
    "integrator_contract_address": "custom-integrator-address"
  }
}
```

### Shared ETH Staking

Shared ETH staking supports the following `BuildStakingOperation` actions: `stake`, `unstake` and `claim_stake`.
See the tabs below for details on the options that can be used with each one.

<Tabs>
  <Tab title="Stake">
    | Field Name                                     | Description                                                                                                                                                                                                                                      |
    | ---------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
    | mode <br />*required*                          | The mode of staking.<br />For Shared ETH Staking this should be `partial`.                                                                                                                                                                       |
    | amount <br />*required*                        | The amount to stake in `wei`.                                                                                                                                                                                                                    |
    | integrator\_contract\_address <br />*optional* | The contract address for the staking operation.<br />Defaults to the integrator contract address associated with the CDP account or a [shared integrator contract address](/staking/staking-api/protocols/shared-eth/overview) for that network. |
  </Tab>

  <Tab title="Unstake">
    | Field Name                                     | Description                                                                                                                                                                                                                                      |
    | ---------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
    | mode <br />*required*                          | The mode of staking.<br />For Shared ETH Staking this should be `partial`.                                                                                                                                                                       |
    | amount <br />*required*                        | The amount to unstake in `wei`.                                                                                                                                                                                                                  |
    | integrator\_contract\_address <br />*optional* | The contract address for the staking operation.<br />Defaults to the integrator contract address associated with the CDP account or a [shared integrator contract address](/staking/staking-api/protocols/shared-eth/overview) for that network. |
  </Tab>

  <Tab title="Claim Stake">
    | Field Name                                     | Description                                                                                                                                                                                                                                      |
    | ---------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
    | mode <br />*required*                          | The mode of staking.<br />For Shared ETH Staking this should be `partial`.                                                                                                                                                                       |
    | integrator\_contract\_address <br />*optional* | The contract address for the staking operation.<br />Defaults to the integrator contract address associated with the CDP account or a [shared integrator contract address](/staking/staking-api/protocols/shared-eth/overview) for that network. |
  </Tab>

  <Tab title="Get Staking Context">
    | Field Name                                     | Description                                                                                                                                                                                                                                      |
    | ---------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
    | mode <br />*required*                          | The mode of staking.<br />For Shared ETH Staking this should be `partial`.                                                                                                                                                                       |
    | integrator\_contract\_address <br />*optional* | The contract address for the staking operation.<br />Defaults to the integrator contract address associated with the CDP account or a [shared integrator contract address](/staking/staking-api/protocols/shared-eth/overview) for that network. |
  </Tab>
</Tabs>

### Dedicated ETH Staking

Dedicated ETH staking supports the following `BuildStakingOperation` actions: `stake` and `unstake`.
See the tabs below for details on the options that can be used with each one.

<Tabs>
  <Tab title="Stake">
    | Field Name                                    | Description                                                                                                                                                                                                                       |
    | --------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
    | mode <br />*required*                         | The mode of staking.<br />For Dedicated ETH Staking this should be `native`.                                                                                                                                                      |
    | amount <br />*required*                       | The amount to stake in `wei` and in `multiples of 32 ETH`.                                                                                                                                                                        |
    | funding\_address <br />*optional*             | Funding address for the stake operation.<br />Defaults to the address initiating the stake operation.                                                                                                                             |
    | withdrawal\_address <br />*optional*          | Rewards and withdrawal address.<br />Defaults to the address initiating the stake operation.                                                                                                                                      |
    | fee\_recipient\_address <br />*optional*      | Tx fee recipient address.<br />Defaults to the address initiating the stake operation.                                                                                                                                            |
    | withdrawal\_credential\_type <br />*optional* | Prefix indicating the type of withdrawal credentials for the validator.<br />Set to `0x02` for provisioning post Pectra validators.<br /> Possible values: `0x01`, `0x02`<br />Defaults to pre Pectra validator prefix of `0x01`. |
    | top\_up\_validator\_pubkey <br />*optional*   | The validator public key to top up.<br /> If provided, instead of creating a new validator, the existing validator will be topped up with the specified amount.                                                                   |
  </Tab>

  <Tab title="Unstake">
    | Field Name                            | Description                                                                                                                                |
    | ------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
    | mode <br />*required*                 | The mode of staking.<br />For Dedicated ETH Staking this should be `native`.                                                               |
    | amount <br />*required*               | The amount to unstake in `wei` and in `multiples of 32 ETH`.                                                                               |
    | unstake\_type <br />*optional*        | The type of unstaking operation to perform.<br /> Possible values: `consensus`, `execution`<br />Defaults to `consensus`.                  |
    | immediate <br />*optional*            | Set to `true` for immediate unstake using `Coinbase managed unstake` process.<br />Defaults to `false` for `User managed unstake` process. |
    | validator\_pub\_keys <br />*optional* | Comma-separated list of validator public keys to unstake.<br />Defaults to validators selected based on the unstake amount.                |
  </Tab>

  <Tab title="Consolidate">
    | Field Name                                 | Description                                                                                                                           |
    | ------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------- |
    | source\_validator\_pubkey <br />*required* | The source validator public key to consolidate. This can be either a 0x01 or 0x02 validator.                                          |
    | target\_validator\_pubkey <br />*required* | The target validator public key to which the source validator will be consolidated into. This can be either a 0x01 or 0x02 validator. |
  </Tab>

  <Tab title="Get Staking Context">
    | Field Name                                    | Description                                                                                                                                                                                                                |
    | --------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
    | mode <br />*required*                         | The mode of staking.<br />For Dedicated ETH Staking this should be `native`.                                                                                                                                               |
    | validator\_pub\_keys <br />*optional*         | List of comma separated validator public keys to retrieve unstakeable balance for.<br />Defaults to all validators.                                                                                                        |
    | withdrawal\_credential\_type <br />*optional* | Prefix indicating the type of validator for which we want to get the context.<br />Set to `0x02` for post Pectra validators.<br /> Possible values: `0x01`, `0x02`<br />Defaults to pre Pectra validator prefix of `0x01`. |
  </Tab>
</Tabs>

### SOL Staking

SOL staking supports the following `BuildStakingOperation` actions: `stake`, `unstake` and `claim_stake`.
See the tabs below for details on the options that can be used with each one.

<Tabs>
  <Tab title="Stake">
    | Field Name                          | Description                                                                                                                                                                                        |
    | ----------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
    | amount <br />*required*             | The amount to stake in `lamports`.                                                                                                                                                                 |
    | validator\_address <br />*optional* | The validator address to which you want to stake.<br />Defaults to the Coinbase Solana validator. See [here](/staking/staking-api/protocols/sol/overview#validator-details) for validator details. |
  </Tab>

  <Tab title="Unstake">
    | Field Name              | Description                          |
    | ----------------------- | ------------------------------------ |
    | amount <br />*required* | The amount to unstake in `lamports`. |
  </Tab>
</Tabs>

