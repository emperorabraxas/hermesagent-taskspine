# EnrollMfaProps
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/EnrollMfaProps



Props for the EnrollMfa component.

## Extends

* `Omit`\<`HTMLAttributes`\<`HTMLDivElement`>, `"children"`>

## Properties

| Property                 | Type                                                                                                                                     | Description                                                                                                                                                                                                                                                                                                                                     |
| ------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| <a /> `children?`        | \| `ReactNode` \| (`state`: [`EnrollMfaState`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/EnrollMfaState)) => `ReactNode` | The children of the component. Leave empty to use the default enrollment UI. If a function is provided, it will be called with the current state of the enrollment flow. The function should return a `ReactNode`. **Example** `<EnrollMfa> {(state) => ( <> <EnrollMfaTitle /> <EnrollMfaDescription /> <EnrollMfaFlow /> </> )} </EnrollMfa>` |
| <a /> `onEnrollSuccess?` | () => `void`                                                                                                                             | A function to call when the enrollment is successful.                                                                                                                                                                                                                                                                                           |
| <a /> `resetOnSuccess?`  | `boolean`                                                                                                                                | Whether to reset the enrollment state when the enrollment is successful. Defaults to `true`.                                                                                                                                                                                                                                                    |

