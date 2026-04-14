# getCurrentUser
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Functions/getCurrentUser



```ts theme={null}
function getCurrentUser(): Promise<
  | null
| User>;
```

Gets the currently signed-in user, if any.

## Returns

`Promise`\<
\| `null`
\| [`User`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/User)>

The currently signed-in user, or null if no user is signed in.

## Example

```typescript lines theme={null}
const user = await getCurrentUser();
```

