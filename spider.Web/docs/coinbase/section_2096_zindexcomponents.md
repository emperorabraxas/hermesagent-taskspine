# zIndexComponents
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Variables/zIndexComponents



```ts theme={null}
const zIndexComponents: {
  select: {
     list: {
        value: "{zIndex.popup}";
     };
  };
  modal: {
     overlay: {
        value: "{zIndex.scrim}";
     };
     dialog: {
        value: "{zIndex.floating}";
     };
  };
};
```

Component z-index tokens.

## Type declaration

| Name                  | Type                                                                                               | Default value         |
| --------------------- | -------------------------------------------------------------------------------------------------- | --------------------- |
| <a /> `select`        | \{ `list`: \{ `value`: `"{zIndex.popup}"`; }; }                                                    | -                     |
| `select.list`         | \{ `value`: `"{zIndex.popup}"`; }                                                                  | -                     |
| `select.list.value`   | `"{zIndex.popup}"`                                                                                 | `"{zIndex.popup}"`    |
| <a /> `modal`         | \{ `overlay`: \{ `value`: `"{zIndex.scrim}"`; }; `dialog`: \{ `value`: `"{zIndex.floating}"`; }; } | -                     |
| `modal.overlay`       | \{ `value`: `"{zIndex.scrim}"`; }                                                                  | -                     |
| `modal.overlay.value` | `"{zIndex.scrim}"`                                                                                 | `"{zIndex.scrim}"`    |
| `modal.dialog`        | \{ `value`: `"{zIndex.floating}"`; }                                                               | -                     |
| `modal.dialog.value`  | `"{zIndex.floating}"`                                                                              | `"{zIndex.floating}"` |

