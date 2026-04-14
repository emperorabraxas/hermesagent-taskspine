# npm
npm install @coinbase/cdp-react @coinbase/cdp-hooks @coinbase/cdp-core viem
```

<Steps>
  <Step title="Set up .env file">
    Set the environment variables in your .env.local file:

    ```bash theme={null}
    NEXT_PUBLIC_PROJECT_ID=your_coinbase_cdp_project_id
    NEXT_PUBLIC_GELATO_API_KEY=your_gelato_api_key
    ```
  </Step>

  <Step title="Import Dependencies">
    ```tsx src/App.tsx theme={null}
    import { CDPReactProvider } from "@coinbase/cdp-react";
    import { AuthButton } from "@coinbase/cdp-react/components/AuthButton";
    import { useCurrentUser, useEvmAddress } from "@coinbase/cdp-hooks";
    import { toViemAccount } from "@coinbase/cdp-core";
    import { baseSepolia } from "viem/chains";
    import { createPublicClient, http } from "viem";
    import {
      createBundlerClient,
      toCoinbaseSmartAccount,
    } from "viem/account-abstraction";
    ```
  </Step>

  <Step title="Configure React provider">
    Set up the CDP React Provider in your app:

    ```tsx src/App.tsx theme={null}
    "use client";

    import { CDPReactProvider } from "@coinbase/cdp-react";

    function Providers({ children }: { children: React.ReactNode }) {
      return (
        <CDPReactProvider
          config={{
            projectId: process.env.NEXT_PUBLIC_PROJECT_ID as string,
            ethereum: {
              createOnLogin: "eoa",
            },
            appName: "Your App Name",
          }}
        >
          {children}
        </CDPReactProvider>
      );
    }
    ```
  </Step>

  <Step title="Create Bundler Client">
    Set up your component to use Coinbase CDP hooks and create a bundler client with Gelato integration:

    ```tsx src/App.tsx theme={null}
    "use client";

    import { AuthButton } from "@coinbase/cdp-react/components/AuthButton";
    import { useCurrentUser, useEvmAddress } from "@coinbase/cdp-hooks";
    import { toViemAccount } from "@coinbase/cdp-core";
    import { baseSepolia } from "viem/chains";
    import { createPublicClient, http } from "viem";
    import {
      createBundlerClient,
      toCoinbaseSmartAccount,
    } from "viem/account-abstraction";

    export default function Home() {
      const { evmAddress } = useEvmAddress();
      const { currentUser } = useCurrentUser();

      const createAccount = async () => {
        if (!currentUser?.evmAccounts) return;

        const viemAccount = await toViemAccount(currentUser?.evmAccounts[0]);

        const client = createPublicClient({
          chain: baseSepolia,
          transport: http(),
        });

        const account = await toCoinbaseSmartAccount({
          client,
          owners: [viemAccount],
          version: "1.1",
        });

        const bundlerClient = createBundlerClient({
          client: client,
          transport: http(
            `https://api.gelato.digital/bundlers/${baseSepolia.id}/rpc?apiKey=${process.env.NEXT_PUBLIC_GELATO_API_KEY}&sponsored=true`
          ),
        });

        console.log("Bundler client created:", bundlerClient);
        console.log("Smart account address:", account.address);
      };

      return (
        <div>
          <AuthButton />
          <div>{evmAddress}</div>
          <button onClick={createAccount}>Create Account</button>
        </div>
      );
    }
    ```
  </Step>

  <Step title="Send User Operations">
    Send sponsored user operations using the bundler client:

    ```tsx src/App.tsx theme={null}
    const sendUserOperation = async () => {
      const response = await bundlerClient.sendUserOperation({
        account,
        calls: [
          {
            to: account.address,
            value: BigInt(0),
            data: "0x",
          },
        ],
        maxFeePerGas: BigInt(0),
        maxPriorityFeePerGas: BigInt(0),
      });

      console.log("User operation response:", response);
    };
    ```
  </Step>
</Steps>

