# MfaListenerOptions
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/MfaListenerOptions



```ts theme={null}
type MfaListenerOptions = {
  scope?: HTMLElement;
};
```

Options for registering an MFA listener.

## Properties

| Property       | Type          | Description                                                                                                                                                                                                                                                    |
| -------------- | ------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| <a /> `scope?` | `HTMLElement` | Optional DOM element that defines the scope for this handler. When provided, this handler will only respond to MFA triggers that originate from within this element (e.g., button clicks inside a container). Handlers without a scope act as global handlers. |

