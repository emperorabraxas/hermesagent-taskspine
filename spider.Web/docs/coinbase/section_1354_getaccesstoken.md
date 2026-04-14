# getAccessToken
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Functions/getAccessToken



```ts theme={null}
function getAccessToken(options: {
  forceRefresh: boolean;
}): Promise<null | string>;
```

Gets the access token for the current user.

## Parameters

| Parameter              | Type                            | Description                              |
| ---------------------- | ------------------------------- | ---------------------------------------- |
| `options`              | \{ `forceRefresh`: `boolean`; } | The options for getting the token.       |
| `options.forceRefresh` | `boolean`                       | Whether to force a refresh of the token. |

## Returns

`Promise`\<`null` | `string`>

The access token for the current user, or null if no user is signed in.

## Example

```typescript lines theme={null}
const accessToken = await getAccessToken();
```

