# ModuleResolutionError
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Classes/ModuleResolutionError



Error thrown when required native modules are not available in the React Native environment.

## Extends

* `Error`

## Constructors

### Constructor

```ts theme={null}
new ModuleResolutionError(
   moduleName: string, 
   requiredFor: string, 
   message?: string): ModuleResolutionError;
```

Creates a new ModuleResolutionError.

#### Parameters

| Parameter     | Type     | Description                                  |
| ------------- | -------- | -------------------------------------------- |
| `moduleName`  | `string` | The name of the missing module.              |
| `requiredFor` | `string` | The API or feature that requires the module. |
| `message?`    | `string` | Optional custom error message.               |

#### Returns

`ModuleResolutionError`

#### Overrides

```ts theme={null}
Error.constructor
```

## Properties

| Property            | Modifier | Type     | Description                                          |
| ------------------- | -------- | -------- | ---------------------------------------------------- |
| <a /> `moduleName`  | `public` | `string` | The name of the missing module.                      |
| <a /> `requiredFor` | `public` | `string` | The API or feature that requires the missing module. |

