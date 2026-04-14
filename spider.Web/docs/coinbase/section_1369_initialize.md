# initialize
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Functions/initialize



```ts theme={null}
function initialize(config: Config): Promise<void>;
```

Initializes the core package. Must be called before using any other functions.

## Parameters

| Parameter | Type                                                                          | Description                             |
| --------- | ----------------------------------------------------------------------------- | --------------------------------------- |
| `config`  | [`Config`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/Config) | The configuration for the core package. |

## Returns

`Promise`\<`void`>

## Example

```typescript lines theme={null}
await initialize({
  projectId: "your-project-id", // Your project ID from the CDP Portal
});
```

