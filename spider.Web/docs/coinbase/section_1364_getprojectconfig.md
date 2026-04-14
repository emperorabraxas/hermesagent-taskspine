# getProjectConfig
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Functions/getProjectConfig



```ts theme={null}
function getProjectConfig(): Promise<ProjectConfig>;
```

Gets the project configuration for the current project.

## Returns

`Promise`\<`ProjectConfig`>

The project configuration.

## Example

```typescript lines theme={null}
const result = await getProjectConfig();
console.log("Project name:", result.name);
```

