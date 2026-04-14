# Travel Rule for Withdrawals
Source: https://docs.cdp.coinbase.com/exchange/travel-rule/withdrawals



The Travel Rule requires financial institutions, including custodial cryptocurrency exchanges, to share basic information about their customers when sending funds over a certain amount.

VASPs (Virtual Asset Service Providers) like Coinbase that are part of the TRUST (Travel Rule Universal Solution Technology) consortium use the [TRUST solution](https://www.coinbase.com/travelrule) when sharing PII (Personally Identifiable Information) in order to satisfy the Travel Rule data requirements.

The [Withdraw to crypto address](/api-reference/exchange-api/rest-api/transfers/withdraw-to-crypto-address) endpoint supports the Travel Rule as follows:

<Accordion title="Coinbase as a VASP">
  <div>
    Depending on the jurisdiction, you may be required to provide data related to the beneficiary of the withdrawal.

    Users in travel-rule jurisdictions can only withdraw to addresses that have been added to their address-book. In such cases, the `travel_rule_data` is obtained from the address-book.
    Please note that [`post /address-book`](/api-reference/exchange-api/rest-api/transfers/withdraw-to-crypto-address)) has fields to support this.

    Example request:

    ```shell lines wrap theme={null}
    curl -L -X POST 'https://api.exchange.coinbase.com/withdrawals/crypto' \
    -H "Content-Type: application/json" \
    -d "@data.json"
    ```

    `data.json` content:

    ```json lines wrap theme={null}
    {
      "amount": "1.0",
      "currency": "BTC",
      "crypto_address": "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"
    }
    ```
  </div>
</Accordion>

<Accordion title="Coinbase as an intermediary VASP">
  <div>
    Customers can reach out to client-services to use coinbase as an intermediary VASP.

    When Coinbase is used as an intermediary VASP to send crypto on behalf of your customer, you must provide the `is_intermediary` parameter with a value of `true`.
    It is also necessary to provide the `travel_rule_data` parameter with the data necessary to satisfy the Travel Rule data requirements.

    You must attest that you have verified the ownership of the wallet address being withdrawn to, and that you are sending the funds on behalf of your customer by sending: `attest_verified_wallet_ownership = true`

    Example of a request with Travel Rule data when Coinbase is an intermediary VASP:

    ```shell lines wrap theme={null}
    curl -L -X POST 'https://api.exchange.coinbase.com/withdrawals/crypto' \
    -H "Content-Type: application/json" \
    -d "@data.json"
    ```

    `data.json` content:

    ```json lines wrap theme={null}
    {
      "amount": "1.00",
      "currency": "ETH",
      "crypto_address": "0x111111111117dc0aa78b770fa6a738034120c000",
      "travel_rule_data": {
        "originator_name": "customer name",
        "originator_personal_id": "customer personal id",
        "originator_address": {
          "address_1": "customer address 1",
          "city": "San Francisco",
          "state": "CA",
          "country": "US",
          "postal_code": "94102"
        },
        "originator_account": "customer accountID",
        "originator_account_number": "12345",
        "beneficiary_name": "beneficiary name",
        "beneficiary_address": {
          "country": "US"
        },
        "is_self": "true",
        "wallet_type": "WALLET_TYPE_SELF_HOSTED",
        "originating_vasp_for_intermediary": {
          "attest_verified_wallet_ownership": "true"
        }
      }
    }
    ```
  </div>
</Accordion>

<Accordion title="Error responses for missing Travel Rule data">
  <div>
    When the required Travel Rule data has not been provided for a given jurisdiction, an error response will be received, such as the following (HTTP status code 400):

    ```json lines wrap theme={null}
    {
      "message": "missing fields to satisfy travel rule requirements",
      "missing_fields": ["beneficiary_name", "beneficiary_address", "originator_name"]
    }
    ```
  </div>
</Accordion>

