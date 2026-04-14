# recordMfaEnrollmentPrompted
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Functions/recordMfaEnrollmentPrompted



```ts theme={null}
function recordMfaEnrollmentPrompted(options?: {
  idempotencyKey?: string;
}): Promise<RecordMfaEnrollmentPrompted200>;
```

Records that the end user was prompted for MFA enrollment.
This endpoint should be called when the user is shown the MFA enrollment prompt,
regardless of whether they choose to enroll or skip. This helps track when users
were last offered the opportunity to enroll in MFA.

## Parameters

| Parameter                 | Type                              | Description                                |
| ------------------------- | --------------------------------- | ------------------------------------------ |
| `options?`                | \{ `idempotencyKey?`: `string`; } | Optional options for the operation.        |
| `options.idempotencyKey?` | `string`                          | Optional idempotency key for safe retries. |

## Returns

`Promise`\<`RecordMfaEnrollmentPrompted200`>

The result containing the timestamp when enrollment was prompted.

## Example

```typescript lines theme={null}
const result = await recordMfaEnrollmentPrompted();
console.log("MFA enrollment prompt recorded at:", result.enrollmentPromptedAt);
```

