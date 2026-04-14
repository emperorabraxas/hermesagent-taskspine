# List payment methods
Source: https://docs.cdp.coinbase.com/api-reference/payment-apis/rest-api/payment-methods-under-development/list-payment-methods

get /v2/payment-methods
List payment methods linked to your entity. Payment methods represent external financial instruments that can be used as a target for transfers. The list will not include disabled or deleted payment methods.

**Currently Supported Types:**
- `fedwire`: Domestic USD wire transfers
- `swift`: International wire transfers
- `sepa`: SEPA EUR transfers

**Note:** Payment methods are created and verified through your linked CDP entity. Currently, fetching payment methods is only supported for Prime investment vehicles linked to CDP.


