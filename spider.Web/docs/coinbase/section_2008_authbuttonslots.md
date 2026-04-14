# AuthButtonSlots
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Type-Aliases/AuthButtonSlots



```ts theme={null}
type AuthButtonSlots = {
  placeholder?: (props: Pick<HTMLAttributes<HTMLDivElement>, "className">) => ReactNode;
  signOutButton?: (props: Pick<SignOutButtonProps, "onSuccess">) => ReactNode;
  signInModal?: (props: Pick<SignInModalProps, "open" | "setIsOpen" | "onSuccess">) => ReactNode;
};
```

Component slots for the AuthButton.

## Extended by

* [`AuthButtonProps`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/AuthButtonProps)

## Properties

| Property               | Type                                                                                                                                                                            | Description                                                  |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------ |
| <a /> `placeholder?`   | (`props`: `Pick`\<`HTMLAttributes`\<`HTMLDivElement`>, `"className"`>) => `ReactNode`                                                                                           | The placeholder to render while the CDP SDK is initializing. |
| <a /> `signOutButton?` | (`props`: `Pick`\<[`SignOutButtonProps`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/SignOutButtonProps), `"onSuccess"`>) => `ReactNode`                          | The sign out button, rendered when the user is signed in.    |
| <a /> `signInModal?`   | (`props`: `Pick`\<[`SignInModalProps`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/SignInModalProps), `"open"` \| `"setIsOpen"` \| `"onSuccess"`>) => `ReactNode` | The sign in modal, rendered when the user is signed out.     |

