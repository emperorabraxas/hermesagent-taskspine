# CopySolanaKeyButton
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/CopySolanaKeyButton



```ts theme={null}
function CopySolanaKeyButton(props: CopySolanaKeyButtonProps): null | Element;
```

The CopySolanaKeyButton component is used to copy the private key of a Solana account.

## Parameters

| Parameter | Type                                                                                                             | Description                                      |
| --------- | ---------------------------------------------------------------------------------------------------------------- | ------------------------------------------------ |
| `props`   | [`CopySolanaKeyButtonProps`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/CopySolanaKeyButtonProps) | The props for the CopySolanaKeyButton component. |

## Returns

`null` | `Element`

The CopySolanaKeyButton component.

## Examples

```tsx lines theme={null}
// Render the CopySolanaKeyButton component
function CopySolanaKeyButtonExample() {
  const { solanaAddress } = useSolanaAddress();
  if (!solanaAddress) return null;
  return (
    <CopySolanaKeyButton address={solanaAddress} />
  );
}
```

```tsx lines theme={null}
// Render the CopySolanaKeyButton component with custom labels
function CopySolanaKeyButtonExample() {
  const { solanaAddress } = useSolanaAddress();
  if (!solanaAddress) return null;
  return (
    <CopySolanaKeyButton address={solanaAddress} label="Copy private key" copiedLabel="Private key copied" />
  );
}
```

```tsx lines theme={null}
// Render the CopySolanaKeyButton component with a different variant
function CopySolanaKeyButtonExample() {
  const { solanaAddress } = useSolanaAddress();
  if (!solanaAddress) return null;
  return (
    <CopySolanaKeyButton address={solanaAddress} variant="secondary" />
  );
}
```

```tsx lines theme={null}
// Render the CopySolanaKeyButton component with theme overrides
function CopySolanaKeyButtonExample() {
  const { solanaAddress } = useSolanaAddress();
  if (!solanaAddress) return null;
  return (
    <CopySolanaKeyButton address={solanaAddress} theme={{ fontUrl: "https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,100..900;1,100..900&display=swap", fontFamily: '"Roboto", sans-serif' }} />
  );
}
```

