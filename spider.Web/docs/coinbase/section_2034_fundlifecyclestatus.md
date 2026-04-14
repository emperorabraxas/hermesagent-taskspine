# FundLifecycleStatus
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Type-Aliases/FundLifecycleStatus



```ts theme={null}
type FundLifecycleStatus = 
  | {
  statusName: "init";
  statusData: null;
}
  | {
  statusName: "exit";
  statusData: null;
}
  | {
  statusName: "error";
  statusData: OnrampError;
}
  | {
  statusName: "transactionSubmitted";
  statusData: null;
}
  | {
  statusName: "transactionSuccess";
  statusData:   | OnrampSuccessEventData
     | null;
}
  | {
  statusName: "transactionPending";
  statusData: null;
};
```

The lifecycle statuses of the Fund component.

