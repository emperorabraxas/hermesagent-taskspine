# useGetAccessToken
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Functions/useGetAccessToken



```ts theme={null}
function useGetAccessToken(): {
  getAccessToken: () => Promise<null | string>;
};
```

Hook to get the access token for the current user.

## Returns

```ts theme={null}
{
  getAccessToken: () => Promise<null | string>;
}
```

Function to get the access token for the current user

| Name               | Type                                 |
| ------------------ | ------------------------------------ |
| `getAccessToken()` | () => `Promise`\<`null` \| `string`> |

## Example

```tsx lines theme={null}
const { getAccessToken } = useGetAccessToken();

const handleGetAccessToken = async () => {
  const accessToken = await getAccessToken();
  console.log("Access Token:", accessToken);
};
```

