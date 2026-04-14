# useRecordMfaEnrollmentPrompted
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Functions/useRecordMfaEnrollmentPrompted



```ts theme={null}
function useRecordMfaEnrollmentPrompted(): {
  recordMfaEnrollmentPrompted: (options?: {
     idempotencyKey?: string;
  }) => Promise<RecordMfaEnrollmentPrompted200>;
};
```

A hook for recording when the end user was prompted for MFA enrollment.
This should be called when the user is shown the MFA enrollment prompt,
regardless of whether they choose to enroll or skip.

## Returns

An object containing the recordMfaEnrollmentPrompted function.

| Name                            | Type                                                                                            |
| ------------------------------- | ----------------------------------------------------------------------------------------------- |
| `recordMfaEnrollmentPrompted()` | (`options?`: \{ `idempotencyKey?`: `string`; }) => `Promise`\<`RecordMfaEnrollmentPrompted200`> |

