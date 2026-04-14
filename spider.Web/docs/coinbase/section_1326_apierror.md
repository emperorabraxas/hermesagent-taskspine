# APIError
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Classes/APIError



Extended API error that encompasses both OpenAPI errors and other API-related errors

## Extends

* `Error`

## Constructors

### Constructor

```ts theme={null}
new APIError(
   statusCode: number, 
   errorType: APIErrorType, 
   errorMessage: string, 
   correlationId?: string, 
   errorLink?: string, 
   cause?: Error): APIError;
```

Constructor for the APIError class

#### Parameters

| Parameter        | Type                                                                                      | Description                           |
| ---------------- | ----------------------------------------------------------------------------------------- | ------------------------------------- |
| `statusCode`     | `number`                                                                                  | The HTTP status code                  |
| `errorType`      | [`APIErrorType`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/APIErrorType) | The type of error                     |
| `errorMessage`   | `string`                                                                                  | The error message                     |
| `correlationId?` | `string`                                                                                  | The correlation ID                    |
| `errorLink?`     | `string`                                                                                  | URL to documentation about this error |
| `cause?`         | `Error`                                                                                   | The cause of the error                |

#### Returns

`APIError`

#### Overrides

```ts theme={null}
Error.constructor
```

## Methods

### toJSON()

```ts theme={null}
toJSON(): {
  errorLink?: string;
  correlationId?: string;
  name: string;
  statusCode: number;
  errorType: APIErrorType;
  errorMessage: string;
};
```

Convert the error to a JSON object, excluding undefined properties

#### Returns

```ts theme={null}
{
  errorLink?: string;
  correlationId?: string;
  name: string;
  statusCode: number;
  errorType: APIErrorType;
  errorMessage: string;
}
```

The error as a JSON object

| Name             | Type                                                                                      |
| ---------------- | ----------------------------------------------------------------------------------------- |
| `errorLink?`     | `string`                                                                                  |
| `correlationId?` | `string`                                                                                  |
| `name`           | `string`                                                                                  |
| `statusCode`     | `number`                                                                                  |
| `errorType`      | [`APIErrorType`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/APIErrorType) |
| `errorMessage`   | `string`                                                                                  |

## Properties

| Property               | Type                                                                                      |
| ---------------------- | ----------------------------------------------------------------------------------------- |
| <a /> `statusCode`     | `number`                                                                                  |
| <a /> `errorType`      | [`APIErrorType`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/APIErrorType) |
| <a /> `errorMessage`   | `string`                                                                                  |
| <a /> `correlationId?` | `string`                                                                                  |
| <a /> `errorLink?`     | `string`                                                                                  |

