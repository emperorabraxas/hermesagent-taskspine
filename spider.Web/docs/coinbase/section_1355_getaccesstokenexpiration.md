# getAccessTokenExpiration
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Functions/getAccessTokenExpiration



```ts theme={null}
function getAccessTokenExpiration(): Promise<null | number>;
```

Gets the expiration time of the access token for the current user.

## Returns

`Promise`\<`null` | `number`>

The expiration time of the access token for the current user, or null if no user is signed in.

## Example

```typescript lines theme={null}
const accessTokenExpiration = await getAccessTokenExpiration();
```

