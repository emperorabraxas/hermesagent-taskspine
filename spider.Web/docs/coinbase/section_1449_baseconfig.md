# BaseConfig
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/BaseConfig



```ts theme={null}
type BaseConfig = {
  projectId: string;
  customAuth?: CustomAuth;
  useMock?: boolean;
  debugging?: boolean;
  basePath?: string;
  secureIframeBasePath?: string;
  disableAnalytics?: boolean;
  nativeOAuthCallback?: string;
};
```

Base configuration for the core package.

## Properties

| Property                      | Type                                                                                  | Description                                                                                                                                                                                                                                                                                                                                                           |
| ----------------------------- | ------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| <a /> `projectId`             | `string`                                                                              | The CDP Project ID.                                                                                                                                                                                                                                                                                                                                                   |
| <a /> `customAuth?`           | [`CustomAuth`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/CustomAuth) | Configuration for custom authentication with third-party identity providers. Use this when integrating with Auth0, Firebase, Cognito, or other IDPs. **Example** `lines import { useAuth0 } from '@auth0/auth0-react'; const { getAccessTokenSilently } = useAuth0(); await initialize({ projectId: 'my-project', customAuth: { getJwt: getAccessTokenSilently } });` |
| <a /> `useMock?`              | `boolean`                                                                             | Whether to use the mock implementation.                                                                                                                                                                                                                                                                                                                               |
| <a /> `debugging?`            | `boolean`                                                                             | Whether to enable debugging.                                                                                                                                                                                                                                                                                                                                          |
| <a /> `basePath?`             | `string`                                                                              | The base path for the API.                                                                                                                                                                                                                                                                                                                                            |
| <a /> `secureIframeBasePath?` | `string`                                                                              | The base path for the secure iframe.                                                                                                                                                                                                                                                                                                                                  |
| <a /> `disableAnalytics?`     | `boolean`                                                                             | Whether to disable analytics.                                                                                                                                                                                                                                                                                                                                         |
| <a /> `nativeOAuthCallback?`  | `string`                                                                              | The callback URL for the native OAuth flow.                                                                                                                                                                                                                                                                                                                           |

