# FundModal
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/FundModal



```ts theme={null}
function FundModal(props: FundModalProps): Element;
```

A fund modal component that wraps the [Fund](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/Fund) component.

## Parameters

| Parameter | Type                                                                                         | Description                            |
| --------- | -------------------------------------------------------------------------------------------- | -------------------------------------- |
| `props`   | [`FundModalProps`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/FundModalProps) | The props for the FundModal component. |

## Returns

`Element`

The FundModal component.

## See

* [FundModalTrigger](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/FundModalTrigger) for the trigger button.
* [FundModalContent](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/FundModalContent) for the modal content.

## Examples

```tsx lines theme={null}
// Render the FundModal component
function App() {
  const fetchBuyQuote: FundProps["fetchBuyQuote"] = async (params) => {
    // call the buy quote API
  }
  const fetchBuyOptions: FundProps["fetchBuyOptions"] = async params => {
    // call the buy options API
  }
  return (
    <CDPReactProvider config={config} theme={themeOverrides}>
      <FundModal
        country="US"
        subdivision="NY"
        cryptoCurrency="eth"
        fiatCurrency="usd"
        fetchBuyQuote={fetchBuyQuote}
        fetchBuyOptions={fetchBuyOptions}
        network="base"
        presetAmountInputs={[10, 25, 50]}
      />
    </CDPReactProvider>
  );
}
```

```tsx lines theme={null}
// Render the FundModal component with a custom trigger button
function App() {
  const fetchBuyQuote: FundProps["fetchBuyQuote"] = async (params) => {
    // call the buy quote API
  }
  const fetchBuyOptions: FundProps["fetchBuyOptions"] = async params => {
    // call the buy options API
  }
  return (
    <CDPReactProvider config={config} theme={themeOverrides}>
      <FundModal
        country="US"
        subdivision="NY"
        cryptoCurrency="eth"
        fiatCurrency="usd"
        fetchBuyQuote={fetchBuyQuote}
        fetchBuyOptions={fetchBuyOptions}
        network="base"
        presetAmountInputs={[10, 25, 50]}
      >
        <button className="fund-button">
          Get ETH
        </button>
      </FundModal>
    </CDPReactProvider>
  );
}
```

