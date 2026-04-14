# zIndex
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Variables/zIndex



```ts theme={null}
const zIndex: {
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
  base: {
     value: 0;
     unit: "none";
  };
  raised: {
     value: 1;
     unit: "none";
  };
  popup: {
     value: 200;
     unit: "none";
  };
  scrim: {
     value: 400;
     unit: "none";
  };
  floating: {
     value: 500;
     unit: "none";
  };
};
```

All the z-index tokens.

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
| <a /> `base`          | \{ `value`: `0`; `unit`: `"none"`; }                                                               | -                     |
| `base.value`          | `0`                                                                                                | `0`                   |
| `base.unit`           | `"none"`                                                                                           | `"none"`              |
| <a /> `raised`        | \{ `value`: `1`; `unit`: `"none"`; }                                                               | -                     |
| `raised.value`        | `1`                                                                                                | `1`                   |
| `raised.unit`         | `"none"`                                                                                           | `"none"`              |
| <a /> `popup`         | \{ `value`: `200`; `unit`: `"none"`; }                                                             | -                     |
| `popup.value`         | `200`                                                                                              | `200`                 |
| `popup.unit`          | `"none"`                                                                                           | `"none"`              |
| <a /> `scrim`         | \{ `value`: `400`; `unit`: `"none"`; }                                                             | -                     |
| `scrim.value`         | `400`                                                                                              | `400`                 |
| `scrim.unit`          | `"none"`                                                                                           | `"none"`              |
| <a /> `floating`      | \{ `value`: `500`; `unit`: `"none"`; }                                                             | -                     |
| `floating.value`      | `500`                                                                                              | `500`                 |
| `floating.unit`       | `"none"`                                                                                           | `"none"`              |

