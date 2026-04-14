# useProjectConfig
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Functions/useProjectConfig



```ts theme={null}
function useProjectConfig(): 
  | {
  projectConfig: undefined;
}
  | {
  projectConfig: null | ProjectConfig;
};
```

A hook for reading the pre-fetched project configuration.
The config is fetched during SDK initialization and cached in core state.
Returns null if the project is not configured (404 during init).

## Returns

\| \{
`projectConfig`: `undefined`;
}
\| \{
`projectConfig`: `null` | `ProjectConfig`;
}

The project configuration, null if not configured, or undefined if not initialized.

