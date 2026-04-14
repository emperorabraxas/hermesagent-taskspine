# PersonalSignMessage
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/PersonalSignMessage



```ts theme={null}
type PersonalSignMessage = 
  | string
  | {
  raw: `0x${string}` | Uint8Array;
};
```

Message type for personal\_sign - can be a string or raw format

