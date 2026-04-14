# Embedded UI
Source: https://docs.cdp.coinbase.com/api-reference/payment-acceptance/payments/embedded-checkout



The payment UI can be embedded natively into your website using Coinbase's `<coinbase-payment>` web component. This allows customers to complete payments without leaving your checkout page.

## Setup

```html theme={null}
<script 
  type="module"
  src="https://payments.coinbase.com/payments/components/v1/payment-link.mjs"
></script>

<coinbase-payment id="payment-link"></coinbase-payment>
```

## Rendering

Call `render()` with the payment object from `POST /api/v1/payments`:

```javascript theme={null}
const paymentComponent = document.querySelector('#payment-link');
paymentComponent.render({ payment });
```

To re-render with updated payment data, call `render()` again. To navigate back to the wallet selection view, call `back()`:

```javascript theme={null}
paymentComponent.back();
```

## Attributes

| Attribute | Description                                                                                                                                               |
| --------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `layout`  | Set to `"single-column"` to force the small desktop view regardless of screen size. Set to `"default"` for the standard 2-column layout when appropriate. |

```html theme={null}
<coinbase-payment layout="single-column"></coinbase-payment>
```

## Events

The component emits Custom Events for handling payment outcomes:

| Event           | Description                                                               |
| --------------- | ------------------------------------------------------------------------- |
| `rendered`      | Fired when the component is ready. Includes `installedWallets` in detail. |
| `completed`     | Payment completed. Detail includes `status: 'success' \| 'failure'`.      |
| `cancelled`     | User cancelled the payment.                                               |
| `walletAction`  | Wallet interaction events (selected, connected, rejected).                |
| `pageNavigated` | Navigation between views. Detail includes `page` name.                    |
| `paymentError`  | Error occurred. Detail includes `error` message.                          |
| `deeplink`      | Deeplink URL for mobile wallet redirects. Detail includes `url`.          |

```javascript theme={null}
paymentComponent.addEventListener('completed', (event) => {
  if (event.detail.status === 'success') {
    // Handle successful payment
  }
});

paymentComponent.addEventListener('paymentError', (event) => {
  console.error('Payment error:', event.detail.error);
});
```

## Deeplink handling (iframes)

When the component is rendered inside an iframe, it cannot redirect the browser directly. You must handle the `deeplink` event to perform the redirect from the parent page:

```javascript theme={null}
paymentComponent.addEventListener('deeplink', (event) => {
  window.location.href = event.detail.url;
});
```

## iFrame permissions

If embedding the component inside an iframe, configure the following permissions to enable passkey and clipboard access:

```html theme={null}
<iframe 
  src="your-checkout-page.html"
  allow="publickey-credentials-get; publickey-credentials-create; clipboard-write"
></iframe>
```

## Theming

Customize the component appearance using CSS custom properties:

```css theme={null}
coinbase-payment {
  --cb-color-background-primary: #ffffff;
  --cb-color-text-primary: #000000;
  --cb-color-button-primary: #005bd3;
  --cb-color-button-primary-hover: #004bb3;
  --cb-typography-header-font-family: 'Your Font', sans-serif;
  --cb-typography-body-font-family: 'Your Font', sans-serif;
  --cb-border-radius-button-primary: 8px;
}
```

<Accordion title="All CSS custom properties">
  | Property                             | Default        |
  | ------------------------------------ | -------------- |
  | `--cb-color-background-primary`      | white          |
  | `--cb-color-background-secondary`    | white          |
  | `--cb-color-qr-background`           | white          |
  | `--cb-color-text-primary`            | black          |
  | `--cb-color-link-hover`              | -              |
  | `--cb-color-button-primary`          | #005bd3 (blue) |
  | `--cb-color-button-primary-hover`    | #005bd3 (blue) |
  | `--cb-color-button-primary-text`     | -              |
  | `--cb-color-button-border-primary`   | -              |
  | `--cb-color-accent-primary`          | -              |
  | `--cb-border-radius-button-primary`  | -              |
  | `--cb-color-navigation-hover`        | -              |
  | `--cb-color-border-primary`          | -              |
  | `--cb-color-icon`                    | grey           |
  | `--cb-color-icon-background-hover`   | light gray     |
  | `--cb-typography-header-font-family` | System         |
  | `--cb-typography-body-font-family`   | System         |
</Accordion>

