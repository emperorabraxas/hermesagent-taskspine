# Hash
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/typescript/auth/Hash



## Functions

### authHash()

```ts theme={null}
function authHash(data: Buffer): Promise<string>;
```

Defined in: [utils/hash.ts:14](https://github.com/coinbase/cdp-sdk/blob/8794662b60e721852bfb60801a1d0bb1bb6e4c59/typescript/src/auth/utils/hash.ts#L14)

Auth-specific hash function using uncrypto for Edge runtime compatibility.
Computes SHA-256 hash of the given data.

#### Parameters

##### data

`Buffer`

The data to hash

#### Returns

`Promise`\<`string`>

Promise that resolves to the hex-encoded hash

