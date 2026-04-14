# TokenValue
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Type-Aliases/TokenValue



```ts theme={null}
type TokenValue = {
  value: string | number;
  unit?: "px" | "none";
  modify?:   | {
     type: "color-alpha";
     value: number | string;
   }
     | {
     type: "color-hsl";
     value: [number, number, number];
   }
     | {
     type: "color-mix";
     value: ReadonlyArray<string | readonly [string, string]>;
   }
     | {
     type: "multiply";
     value: number | string;
   };
};
```

Represents a single theme value, which can be a direct value or a reference with modifications.

## Properties

| Property        | Type                                                                                                                                                                                                                                                                                                        | Description                                                                                              |
| --------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| <a /> `value`   | `string` \| `number`                                                                                                                                                                                                                                                                                        | The value of the token.                                                                                  |
| <a /> `unit?`   | `"px"` \| `"none"`                                                                                                                                                                                                                                                                                          | Unit for numeric values. Defaults to "px" if not specified. Use "none" for unitless values like z-index. |
| <a /> `modify?` | \| \{ `type`: `"color-alpha"`; `value`: `number` \| `string`; } \| \{ `type`: `"color-hsl"`; `value`: \[`number`, `number`, `number`]; } \| \{ `type`: `"color-mix"`; `value`: `ReadonlyArray`\<`string` \| readonly \[`string`, `string`]>; } \| \{ `type`: `"multiply"`; `value`: `number` \| `string`; } | Modifications to the value.                                                                              |

