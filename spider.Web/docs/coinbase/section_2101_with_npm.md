# With npm
npm install @coinbase/cdp-react @coinbase/cdp-core @coinbase/cdp-hooks
```

### Gather your CDP Project information

1. Sign in or create an account on the [CDP Portal](https://portal.cdp.coinbase.com)
2. On your dashboard, select a project from the dropdown at the at the top, and copy the Project ID

### Allowlist your local app

1. Navigate to the [Embedded Wallet Configuration](https://portal.cdp.coinbase.com/products/embedded-wallets/cors)
   in CDP Portal, and click Add origin to include your local app
2. Enter the origin of your locally running app - e.g., `http://localhost:3000`
3. Click Add origin again to save your changes

### Setup Provider

Next, you need to wrap your application with the `CDPReactProvider`.

`CDPReactProvider` provides the necessary context for hooks and components to work correctly. It also provides access to config data and theming.

Update your main application file (e.g., `main.tsx` or `App.tsx`) to include the provider:

```tsx lines theme={null}
import React from 'react';
import ReactDOM from 'react-dom/client';
import { App } from './App'; // Your main App component
import { CDPReactProvider, type Config, type Theme } from '@coinbase/cdp-react';

// Config for your dapp
const config: Config = {
  projectId: "your-project-id", // Copy your Project ID here.
  appName: "My app", // the name of your application
  appLogoUrl: "https://picsum.photos/64", // logo will be displayed in select components
}

// You can customize the theme by overriding theme variables
const themeOverrides: Partial<Theme> = {
  "colors-bg-default": "black",
  "colors-bg-alternate": "#121212",
  "colors-fg-default": "white",
  "colors-fg-muted": "#999999",
}

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <CDPReactProvider config={config} theme={themeOverrides}>
      <App />
    </CDPReactProvider>
  </React.StrictMode>,
);
```

#### Analytics Opt-Out

By default the SDK will emit usage analytics to help us improve the SDK. If you would like to opt-out, you can do so by setting the `disableAnalytics` configuration option to `true`.

```tsx lines theme={null}
<CDPReactProvider
  config={{
    projectId: "your-project-id",
    disableAnalytics: true,
  }}
>
  <App />
</CDPReactProvider>
```

### Render a Component

Now you can use the components from the library. Let's add the `AuthButton` component to your application. This component handles both sign-in and sign-out functionality.

```tsx lines theme={null}
// In your App.tsx or any other component
import { AuthButton } from '@coinbase/cdp-react/components/AuthButton';

function App() {
  return (
    <div>
      <h1>Welcome</h1>
      <AuthButton />
    </div>
  );
}

export default App;

```

That's it! You've successfully installed `@coinbase/cdp-react`, set up the provider, and rendered your first component.

