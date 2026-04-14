# isSignedIn
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Functions/isSignedIn



```ts theme={null}
function isSignedIn(): Promise<boolean>;
```

Returns whether the user is currently signed in.

## Returns

`Promise`\<`boolean`>

Whether the user is currently signed in.

## Example

```typescript lines theme={null}
const signedIn = await isSignedIn();
if (signedIn) {
  console.log("User is signed in");
}
```

