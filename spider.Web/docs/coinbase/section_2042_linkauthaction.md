# LinkAuthAction
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Type-Aliases/LinkAuthAction



```ts theme={null}
type LinkAuthAction = 
  | {
  type: "LINK_AUTH_METHOD";
  payload: {
     method: LinkAuthState["methodToLink"];
  };
}
  | {
  type: "LINK_AUTH_METHOD_ERROR";
  payload: {
     error: LinkAuthState["error"];
  };
}
  | {
  type: "SET_AUTH_METHODS";
  payload: {
     methods: LinkAuthState["authMethods"];
  };
}
  | {
  type: "RESET_STATE";
};
```

The actions that can be performed on the LinkAuth state.

## See

* [LinkAuthState](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/LinkAuthState)
* [LinkAuth](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/LinkAuth)

