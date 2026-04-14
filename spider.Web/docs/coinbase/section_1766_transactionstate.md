# TransactionState
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Type-Aliases/TransactionState



```ts theme={null}
type TransactionState = 
  | {
  status: "idle";
}
  | {
  status: "pending";
  hash: Hex;
}
  | {
  status: "success";
  receipt: TransactionReceipt;
}
  | {
  status: "error";
  error: Error;
};
```

Represents the state of an EVM EOA transaction.

* "idle": No transaction in progress.
* "pending": Transaction sent, waiting for confirmation.
* "success": Transaction confirmed, includes receipt.
* "error": Transaction failed, includes error details.

