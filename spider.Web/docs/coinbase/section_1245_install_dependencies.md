# Install dependencies
npm install viem wagmi @tanstack/react-query
```

<Tip>
  If you've installed previously, delete `node_modules` and `package-lock.json` then run a fresh install to ensure overrides are applied.
</Tip>

## Step 3: Configure Wagmi with Base Account

Create your Wagmi configuration using the `baseAccount` connector:

```typescript title="wagmi.ts" theme={null}
import { cookieStorage, createConfig, createStorage, http } from "wagmi";
import { base, baseSepolia } from "wagmi/chains";
import { baseAccount } from "wagmi/connectors";

export function getConfig() {
  return createConfig({
    chains: [base, baseSepolia],
    multiInjectedProviderDiscovery: false,
    connectors: [
      baseAccount({
        appName: "My Wagmi App",
      }),
    ],
    storage: createStorage({
      storage: cookieStorage,
    }),
    ssr: true,
    transports: {
      [base.id]: http(),
      [baseSepolia.id]: http(),
    },
  });
}

declare module "wagmi" {
  interface Register {
    config: ReturnType<typeof getConfig>;
  }
}
```

## Step 4: Set Up Providers

Wrap your application with the Wagmi and QueryClient providers:

```tsx title="providers.tsx" theme={null}
'use client'

import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { type ReactNode, useState } from 'react'
import { type State, WagmiProvider } from 'wagmi'
import { getConfig } from './wagmi'

export function Providers(props: {
  children: ReactNode
  initialState?: State
}) {
  const [config] = useState(() => getConfig())
  const [queryClient] = useState(() => new QueryClient())

  return (
    <WagmiProvider config={config} initialState={props.initialState}>
      <QueryClientProvider client={queryClient}>
        {props.children}
      </QueryClientProvider>
    </WagmiProvider>
  )
}
```

## Step 5: Send Sponsored Transactions

Use Wagmi's `useWriteContracts` hook with paymaster capabilities to execute gasless transactions.

### Check Paymaster Support

First, check if the connected wallet supports paymaster services:

```tsx title="usePaymasterCapabilities.ts" theme={null}
import { useMemo } from 'react';
import { useAccount } from 'wagmi';
import { useCapabilities } from 'wagmi/experimental';

export function usePaymasterCapabilities() {
  const { address, chainId } = useAccount();
  
  const { data: availableCapabilities } = useCapabilities({
    account: address,
  });

  const capabilities = useMemo(() => {
    if (!availableCapabilities || !chainId) return {};
    
    const chainCapabilities = availableCapabilities[chainId];
    if (chainCapabilities?.paymasterService?.supported) {
      return {
        paymasterService: {
          // Use your proxy URL in production
          url: process.env.NEXT_PUBLIC_PAYMASTER_PROXY_URL,
        },
      };
    }
    return {};
  }, [availableCapabilities, chainId]);

  const isPaymasterSupported = Object.keys(capabilities).length > 0;

  return { capabilities, isPaymasterSupported };
}
```

### Execute Sponsored Transaction

Use the capabilities with `useWriteContracts` to send gasless transactions:

```tsx title="MintPage.tsx" theme={null}
'use client';

import { useAccount, useConnect, useDisconnect } from 'wagmi';
import { useState } from 'react';
import { useWriteContracts } from 'wagmi/experimental';
import { usePaymasterCapabilities } from './usePaymasterCapabilities';

// Your contract details
const NFT_CONTRACT = '0xYourContractAddress';
const NFT_ABI = [
  {
    name: 'mintTo',
    type: 'function',
    stateMutability: 'nonpayable',
    inputs: [{ name: 'to', type: 'address' }],
    outputs: [],
  },
] as const;

export default function MintPage() {
  const { address, isConnected } = useAccount();
  const { connect, connectors } = useConnect();
  const { disconnect } = useDisconnect();
  const [status, setStatus] = useState<'idle' | 'minting' | 'success' | 'error'>('idle');
  
  const { capabilities, isPaymasterSupported } = usePaymasterCapabilities();

  const { writeContracts } = useWriteContracts({
    mutation: {
      onSuccess: () => setStatus('success'),
      onError: () => setStatus('error'),
    },
  });

  const handleMint = async () => {
    if (!address) return;
    
    setStatus('minting');
    try {
      writeContracts({
        contracts: [
          {
            address: NFT_CONTRACT,
            abi: NFT_ABI,
            functionName: 'mintTo',
            args: [address],
          },
        ],
        capabilities, // Includes paymaster if supported
      });
    } catch (error) {
      console.error('Minting failed:', error);
      setStatus('error');
    }
  };

  // Find the Base Account connector
  const baseAccountConnector = connectors.find(c => c.name === 'Base Account');

  if (!isConnected) {
    return (
      <button onClick={() => baseAccountConnector && connect({ connector: baseAccountConnector })}>
        Connect with Base Account
      </button>
    );
  }

  return (
    <div>
      <p>Connected: {address}</p>
      {isPaymasterSupported && <p>✓ Gas sponsorship available</p>}
      
      <button onClick={handleMint} disabled={status === 'minting'}>
        {status === 'minting' ? 'Minting...' : 'Mint NFT (Gasless)'}
      </button>
      
      {status === 'success' && <p>Mint successful!</p>}
      {status === 'error' && <p>Mint failed. Check console for details.</p>}
      
      <button onClick={() => disconnect()}>Disconnect</button>
    </div>
  );
}
```

## Batch Multiple Calls

You can batch multiple contract calls into a single sponsored transaction:

```tsx theme={null}
writeContracts({
  contracts: [
    {
      address: NFT_CONTRACT,
      abi: NFT_ABI,
      functionName: 'mintTo',
      args: [address],
    },
    {
      address: TOKEN_CONTRACT,
      abi: TOKEN_ABI,
      functionName: 'transfer',
      args: [recipientAddress, amount],
    },
  ],
  capabilities,
});
```

All calls execute atomically — if any call fails, the entire transaction reverts.

## Production Considerations

### Use a Paymaster Proxy

Never expose your Paymaster URL in client-side code. Create a backend proxy:

```typescript title="api/paymaster/route.ts" theme={null}
import { NextRequest, NextResponse } from "next/server";

export async function POST(request: NextRequest) {
  const body = await request.json();
  
  const response = await fetch(process.env.CDP_PAYMASTER_URL!, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  
  return NextResponse.json(await response.json());
}
```

Then use your proxy URL in the capabilities:

```tsx theme={null}
paymasterService: {
  url: '/api/paymaster',
}
```

See the [Paymaster Proxy Guide](/paymaster/guides/paymaster-proxy) for more details.

## Resources

* [Base Account Wagmi Template](https://github.com/base/demos/tree/master/base-account/base-account-wagmi-template) — Complete example project
* [Wagmi Experimental Hooks](https://wagmi.sh/react/api/hooks/useCallsStatus) — Documentation for `useWriteContracts` and `useCapabilities`
* [Base Account SDK](https://docs.base.org/base-account) — Full SDK documentation

## Troubleshooting

If you run into errors, check:

* [Paymaster Errors](/paymaster/reference-troubleshooting/errors) — Common error codes and solutions
* [Troubleshooting Guide](/paymaster/reference-troubleshooting/troubleshooting) — Debugging tips for userOperations

