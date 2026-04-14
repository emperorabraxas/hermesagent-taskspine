# Checkout
Source: https://docs.cdp.coinbase.com/api-reference/payment-acceptance/payments/overview

Redirect or embed the payment checkout experience.

## Redirect flow

Redirect customers to a hosted checkout page.

<Steps>
  <Step title="Create a payment">
    Call `POST /api/v1/payments` with your payment details, including `successRedirectUrl` and `failRedirectUrl` in the request body.
  </Step>

  <Step title="Extract the payment URL">
    From the response, get the `link.url` field.
  </Step>

  <Step title="Redirect customers">
    Redirect customers to the `link.url` to complete the payment.
  </Step>

  <Step title="Handle the redirect">
    After payment completion, customers are automatically redirected to your `successRedirectUrl` or `failRedirectUrl`.
  </Step>
</Steps>

## Embedded checkout

Embed checkout directly in your site using the `<coinbase-payment>` web component. See the [Embedded UI guide](/api-reference/payment-acceptance/payments/embedded-checkout) for setup, events, and theming options.

