# KeyPair
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/KeyPair



```ts theme={null}
type KeyPair = {
  privateKey: CryptoKey | KeyObject | JWK | Uint8Array;
  publicKeyBase64: string;
};
```

A secp256r1 key pair.

## Properties

| Property                | Type                                                | Description                                                                                |
| ----------------------- | --------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| <a /> `privateKey`      | `CryptoKey` \| `KeyObject` \| `JWK` \| `Uint8Array` | The unextractable private key, in a format that can be used to sign and verify JWT tokens. |
| <a /> `publicKeyBase64` | `string`                                            | The base64-encoded public key.                                                             |

