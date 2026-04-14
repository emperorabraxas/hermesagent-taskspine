# CopyAddress
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/CopyAddress



```ts theme={null}
function CopyAddress(props: CopyAddressProps): Element;
```

A component that copies an address to the clipboard.

## Parameters

| Parameter | Type                                                                                             | Description                  |
| --------- | ------------------------------------------------------------------------------------------------ | ---------------------------- |
| `props`   | [`CopyAddressProps`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/CopyAddressProps) | The props for the component. |

## Returns

`Element`

The CopyAddress component.

## Example

```tsx lines theme={null}
// Render the CopyAddress component with a custom label
function CopyAddressExample() {
  const { evmAddress } = useEvmAddress();
  if (!evmAddress) return null;
  return (
    <CopyAddress address={evmAddress} label="My EVM address" />
  );
}
```

