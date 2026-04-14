# borderRadius
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Variables/borderRadius



```ts theme={null}
const borderRadius: {
  badge: {
     value: "{borderRadius.full}";
  };
  banner: {
     value: "{borderRadius.lg}";
  };
  cta: {
     value: "{borderRadius.full}";
  };
  input: {
     value: "{borderRadius.sm}";
  };
  link: {
     value: "{borderRadius.full}";
  };
  modal: {
     value: "{borderRadius.sm}";
  };
  select: {
     trigger: {
        value: "{borderRadius.sm}";
     };
     list: {
        value: "{borderRadius.sm}";
     };
  };
  none: {
     value: 0;
  };
  xs: {
     value: "{font.size.base}";
     modify: {
        type: "multiply";
        value: 0.25;
     };
  };
  sm: {
     value: "{font.size.base}";
     modify: {
        type: "multiply";
        value: 0.5;
     };
  };
  md: {
     value: "{font.size.base}";
     modify: {
        type: "multiply";
        value: 0.75;
     };
  };
  lg: {
     value: "{font.size.base}";
     modify: {
        type: "multiply";
        value: 1;
     };
  };
  xl: {
     value: "{font.size.base}";
     modify: {
        type: "multiply";
        value: 1.5;
     };
  };
  full: {
     value: 99999;
  };
};
```

All the border radius tokens.

## Type declaration

| Name                   | Type                                                                                                | Default value           |
| ---------------------- | --------------------------------------------------------------------------------------------------- | ----------------------- |
| <a /> `badge`          | \{ `value`: `"{borderRadius.full}"`; }                                                              | -                       |
| `badge.value`          | `"{borderRadius.full}"`                                                                             | `"{borderRadius.full}"` |
| <a /> `banner`         | \{ `value`: `"{borderRadius.lg}"`; }                                                                | -                       |
| `banner.value`         | `"{borderRadius.lg}"`                                                                               | `"{borderRadius.lg}"`   |
| <a /> `cta`            | \{ `value`: `"{borderRadius.full}"`; }                                                              | -                       |
| `cta.value`            | `"{borderRadius.full}"`                                                                             | `"{borderRadius.full}"` |
| <a /> `input`          | \{ `value`: `"{borderRadius.sm}"`; }                                                                | -                       |
| `input.value`          | `"{borderRadius.sm}"`                                                                               | `"{borderRadius.sm}"`   |
| <a /> `link`           | \{ `value`: `"{borderRadius.full}"`; }                                                              | -                       |
| `link.value`           | `"{borderRadius.full}"`                                                                             | `"{borderRadius.full}"` |
| <a /> `modal`          | \{ `value`: `"{borderRadius.sm}"`; }                                                                | -                       |
| `modal.value`          | `"{borderRadius.sm}"`                                                                               | `"{borderRadius.sm}"`   |
| <a /> `select`         | \{ `trigger`: \{ `value`: `"{borderRadius.sm}"`; }; `list`: \{ `value`: `"{borderRadius.sm}"`; }; } | -                       |
| `select.trigger`       | \{ `value`: `"{borderRadius.sm}"`; }                                                                | -                       |
| `select.trigger.value` | `"{borderRadius.sm}"`                                                                               | `"{borderRadius.sm}"`   |
| `select.list`          | \{ `value`: `"{borderRadius.sm}"`; }                                                                | -                       |
| `select.list.value`    | `"{borderRadius.sm}"`                                                                               | `"{borderRadius.sm}"`   |
| <a /> `none`           | \{ `value`: `0`; }                                                                                  | -                       |
| `none.value`           | `0`                                                                                                 | `0`                     |
| <a /> `xs`             | \{ `value`: `"{font.size.base}"`; `modify`: \{ `type`: `"multiply"`; `value`: `0.25`; }; }          | -                       |
| `xs.value`             | `"{font.size.base}"`                                                                                | `"{font.size.base}"`    |
| `xs.modify`            | \{ `type`: `"multiply"`; `value`: `0.25`; }                                                         | -                       |
| `xs.modify.type`       | `"multiply"`                                                                                        | `"multiply"`            |
| `xs.modify.value`      | `0.25`                                                                                              | `0.25`                  |
| <a /> `sm`             | \{ `value`: `"{font.size.base}"`; `modify`: \{ `type`: `"multiply"`; `value`: `0.5`; }; }           | -                       |
| `sm.value`             | `"{font.size.base}"`                                                                                | `"{font.size.base}"`    |
| `sm.modify`            | \{ `type`: `"multiply"`; `value`: `0.5`; }                                                          | -                       |
| `sm.modify.type`       | `"multiply"`                                                                                        | `"multiply"`            |
| `sm.modify.value`      | `0.5`                                                                                               | `0.5`                   |
| <a /> `md`             | \{ `value`: `"{font.size.base}"`; `modify`: \{ `type`: `"multiply"`; `value`: `0.75`; }; }          | -                       |
| `md.value`             | `"{font.size.base}"`                                                                                | `"{font.size.base}"`    |
| `md.modify`            | \{ `type`: `"multiply"`; `value`: `0.75`; }                                                         | -                       |
| `md.modify.type`       | `"multiply"`                                                                                        | `"multiply"`            |
| `md.modify.value`      | `0.75`                                                                                              | `0.75`                  |
| <a /> `lg`             | \{ `value`: `"{font.size.base}"`; `modify`: \{ `type`: `"multiply"`; `value`: `1`; }; }             | -                       |
| `lg.value`             | `"{font.size.base}"`                                                                                | `"{font.size.base}"`    |
| `lg.modify`            | \{ `type`: `"multiply"`; `value`: `1`; }                                                            | -                       |
| `lg.modify.type`       | `"multiply"`                                                                                        | `"multiply"`            |
| `lg.modify.value`      | `1`                                                                                                 | `1`                     |
| <a /> `xl`             | \{ `value`: `"{font.size.base}"`; `modify`: \{ `type`: `"multiply"`; `value`: `1.5`; }; }           | -                       |
| `xl.value`             | `"{font.size.base}"`                                                                                | `"{font.size.base}"`    |
| `xl.modify`            | \{ `type`: `"multiply"`; `value`: `1.5`; }                                                          | -                       |
| `xl.modify.type`       | `"multiply"`                                                                                        | `"multiply"`            |
| `xl.modify.value`      | `1.5`                                                                                               | `1.5`                   |
| <a /> `full`           | \{ `value`: `99999`; }                                                                              | -                       |
| `full.value`           | `99999`                                                                                             | `99999`                 |

