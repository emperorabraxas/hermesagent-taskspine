# IOAuthManager
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Interfaces/IOAuthManager



Interface for OAuth manager implementations.

## Methods

### getOAuthFlowState()

```ts theme={null}
getOAuthFlowState(): Promise<
  | null
| OAuthFlowState>;
```

Gets the OAuth flow state.

#### Returns

`Promise`\<
\| `null`
\| [`OAuthFlowState`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Interfaces/OAuthFlowState)>

***

### setOAuthFlowState()

```ts theme={null}
setOAuthFlowState(oauthFlowState: OAuthFlowState): Promise<void>;
```

Sets the OAuth flow state.

#### Parameters

| Parameter        | Type                                                                                        |
| ---------------- | ------------------------------------------------------------------------------------------- |
| `oauthFlowState` | [`OAuthFlowState`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Interfaces/OAuthFlowState) |

#### Returns

`Promise`\<`void`>

***

### addOAuthStateChangeCallback()

```ts theme={null}
addOAuthStateChangeCallback(callback: OnOAuthStateChangeFn): Promise<void>;
```

Adds a callback to be called when the OAuth state changes.

#### Parameters

| Parameter  | Type                                                                                                      |
| ---------- | --------------------------------------------------------------------------------------------------------- |
| `callback` | [`OnOAuthStateChangeFn`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/OnOAuthStateChangeFn) |

#### Returns

`Promise`\<`void`>

***

### clearOAuthFlowState()

```ts theme={null}
clearOAuthFlowState(): Promise<void>;
```

Clears the OAuth flow state.

#### Returns

`Promise`\<`void`>

***

### handleOAuthCode()

```ts theme={null}
handleOAuthCode(url?: string): Promise<void>;
```

Awaitable method whose promise only resolves when the OAuth manager is ready to be used.

#### Parameters

| Parameter | Type     |
| --------- | -------- |
| `url?`    | `string` |

#### Returns

`Promise`\<`void`>

