# See https://beta.commerce.coinbase.com/
NEXT_PUBLIC_COINBASE_COMMERCE_API_KEY="GET_FROM_COINBASE_COMMERCE"
```

### Enabling checkout

By default, the checkout functionality is disabled to prevent transactions in non-production environments. To enable the checkout flow for local development, you need to uncomment certain lines of code in the `OnchainStoreCart.tsx` component, along with the imports at the top of the file.

You can also remove the `OnchainStoreModal` component and logic as well as the `MockCheckoutButton` as these were created for demo purposes only.

Next, you'll want to replace `products` in the `OnchainStoreProvider` with your own product items.

After these changes, the actual OnchainKit checkout flow will be functional in your local environment.

### Running locally

```sh lines wrap theme={null}