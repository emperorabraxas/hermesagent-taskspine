# Config
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Type-Aliases/Config



```ts theme={null}
type Config = CoreConfig & {
  transports?: Partial<Record<number, Transport>>;
};
```

The config for the CDP hooks.

## Type declaration

| Name          | Type                                         |
| ------------- | -------------------------------------------- |
| `transports?` | `Partial`\<`Record`\<`number`, `Transport`>> |

## Param

The optional transports to use for the public clients. If not provided, the default `http()` transport is used.

## Returns

The config for the CDP hooks.

