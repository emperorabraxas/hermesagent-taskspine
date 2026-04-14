# store in .env or using the command `export <name>="secret-info"`
CDP_API_KEY_ID=your-api-key-id
CDP_API_KEY_SECRET=your-api-key-secret
CDP_WALLET_SECRET=your-wallet-secret
```

Then, install the required packages:

```bash Node.js theme={null}
npm install @coinbase/cdp-sdk dotenv
```

Finally, instantiate the CDP client as suggested by the [Server Wallet Quickstart](/server-wallets/v2/introduction/quickstart):

```typescript Node.js theme={null}
import { CdpClient } from "@coinbase/cdp-sdk";
import { toAccount } from "viem/accounts";
import dotenv from "dotenv";

dotenv.config();

const cdp = new CdpClient();
const cdpAccount = await cdp.evm.createAccount();
const signer = toAccount(cdpAccount);
```

### Standalone Wallet Libraries

If you prefer to use your own wallet, you can use standalone libraries:

#### EVM (Node.js with viem)

```bash theme={null}
npm install viem
```

```typescript theme={null}
import { privateKeyToAccount } from "viem/accounts";

// Create a signer from private key (use environment variable)
const signer = privateKeyToAccount(
  process.env.EVM_PRIVATE_KEY as `0x${string}`,
);
```

#### EVM (Go)

```go theme={null}
import (
    "crypto/ecdsa"
    "github.com/ethereum/go-ethereum/crypto"
)

// Load private key from environment
privateKey, _ := crypto.HexToECDSA(os.Getenv("EVM_PRIVATE_KEY"))
```

#### EVM (Python)

Install the required package:

```bash theme={null}
pip install eth_account
```

Then instantiate the wallet signer:

```python theme={null}
import os
from eth_account import Account
from x402.mechanisms.evm import EthAccountSigner

account = Account.from_key(os.getenv("EVM_PRIVATE_KEY"))
signer = EthAccountSigner(account)
```

#### Solana (SVM)

Use [SolanaKit](https://www.solanakit.com/) to instantiate a signer:

```typescript theme={null}
import { createKeyPairSignerFromBytes } from "@solana/kit";
import { base58 } from "@scure/base";

// 64-byte base58 secret key (private + public)
const svmSigner = await createKeyPairSignerFromBytes(
  base58.decode(process.env.SOLANA_PRIVATE_KEY!),
);
```

## 3. Make Paid Requests Automatically

You can automatically handle 402 Payment Required responses and complete payment flows using the x402 helper packages.

<Tabs>
  <Tab title="Node.js">
    You can use either `@x402/fetch` or `@x402/axios`:

    <Tabs>
      <Tab title="@x402/fetch">
        **@x402/fetch** extends the native `fetch` API to handle 402 responses and payment headers for you. [Full example here](https://github.com/coinbase/x402/tree/main/examples/typescript/clients/fetch)

        ```typescript theme={null}
        import { x402Client, wrapFetchWithPayment, x402HTTPClient } from "@x402/fetch";
        import { registerExactEvmScheme } from "@x402/evm/exact/client";
        import { privateKeyToAccount } from "viem/accounts";

        // Create signer
        const signer = privateKeyToAccount(process.env.EVM_PRIVATE_KEY as `0x${string}`);

        // Create x402 client and register schemes
        const client = new x402Client();
        registerExactEvmScheme(client, { signer });

        // Wrap fetch with payment handling
        const fetchWithPayment = wrapFetchWithPayment(fetch, client);

        // Make request - payment is handled automatically
        const response = await fetchWithPayment("https://api.example.com/paid-endpoint", {
          method: "GET",
        });

        const body = await response.json();
        console.log("Response:", body);

        // Get payment receipt from response headers
        if (response.ok) {
          const httpClient = new x402HTTPClient(client);
          const paymentResponse = httpClient.getPaymentSettleResponse(
            (name) => response.headers.get(name)
          );
          console.log("Payment settled:", paymentResponse);
        }
        ```

        **Features:**

        * Automatically handles 402 Payment Required responses
        * Verifies payment and generates `PAYMENT-SIGNATURE` headers
        * Retries the request with proof of payment
        * Supports all standard fetch options
      </Tab>

      <Tab title="@x402/axios">
        **@x402/axios** adds a payment interceptor to Axios, so your requests are retried with payment headers automatically. [Full example here](https://github.com/coinbase/x402/tree/main/examples/typescript/clients/axios)

        ```typescript theme={null}
        import { x402Client, withPaymentInterceptor, x402HTTPClient } from "@x402/axios";
        import { registerExactEvmScheme } from "@x402/evm/exact/client";
        import { privateKeyToAccount } from "viem/accounts";
        import axios from "axios";

        // Create signer
        const signer = privateKeyToAccount(process.env.EVM_PRIVATE_KEY as `0x${string}`);

        // Create x402 client and register schemes
        const client = new x402Client();
        registerExactEvmScheme(client, { signer });

        // Create an Axios instance with payment handling
        const api = withPaymentInterceptor(
          axios.create({ baseURL: "https://api.example.com" }),
          client,
        );

        // Make request - payment is handled automatically
        const response = await api.get("/paid-endpoint");
        console.log("Response:", response.data);

        // Get payment receipt
        const httpClient = new x402HTTPClient(client);
        const paymentResponse = httpClient.getPaymentSettleResponse(
          (name) => response.headers[name.toLowerCase()]
        );
        console.log("Payment settled:", paymentResponse);
        ```

        **Features:**

        * Automatically handles 402 Payment Required responses
        * Retries requests with payment headers
        * Exposes payment response in headers
      </Tab>
    </Tabs>
  </Tab>

  <Tab title="Go">
    [Full example here](https://github.com/coinbase/x402/tree/main/examples/go/clients/http)

    ```go theme={null}
    package main

    import (
        "context"
        "encoding/json"
        "fmt"
        "net/http"
        "os"
        "time"

        x402 "github.com/coinbase/x402/go"
        evm "github.com/coinbase/x402/go/mechanisms/evm/exact/client"
    )

    func main() {
        privateKey := os.Getenv("EVM_PRIVATE_KEY")
        url := "http://localhost:4021/weather"

        // Create x402 client and register EVM scheme
        client := x402.NewX402Client()
        evm.RegisterExactEvmScheme(client, &evm.Config{
            PrivateKey: privateKey,
        })

        // Wrap HTTP client with payment handling
        httpClient := x402.WrapHTTPClient(client)

        // Make request - payment is handled automatically
        ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
        defer cancel()

        req, _ := http.NewRequestWithContext(ctx, "GET", url, nil)
        resp, err := httpClient.Do(req)
        if err != nil {
            fmt.Printf("Request failed: %v\n", err)
            return
        }
        defer resp.Body.Close()

        // Read response
        var data map[string]interface{}
        json.NewDecoder(resp.Body).Decode(&data)
        fmt.Printf("Response: %+v\n", data)

        // Check payment response header
        paymentHeader := resp.Header.Get("PAYMENT-RESPONSE")
        if paymentHeader != "" {
            fmt.Println("Payment settled successfully!")
        }
    }
    ```
  </Tab>

  <Tab title="Python (httpx)">
    **httpx** provides async HTTP client support with automatic 402 payment handling.

    [Full HTTPX example](https://github.com/coinbase/x402/tree/main/examples/python/clients/httpx) | [Full Requests example](https://github.com/coinbase/x402/tree/main/examples/python/clients/requests)

    ```python theme={null}
    import asyncio
    import os
    from eth_account import Account

    from x402 import x402Client
    from x402.http import x402HTTPClient
    from x402.http.clients import x402HttpxClient
    from x402.mechanisms.evm import EthAccountSigner
    from x402.mechanisms.evm.exact.register import register_exact_evm_client


    async def main() -> None:
        client = x402Client()
        account = Account.from_key(os.getenv("EVM_PRIVATE_KEY"))
        register_exact_evm_client(client, EthAccountSigner(account))

        http_client = x402HTTPClient(client)

        async with x402HttpxClient(client) as http:
            response = await http.get("https://api.example.com/paid-endpoint")
            await response.aread()

            print(f"Response: {response.text}")

            if response.is_success:
                settle_response = http_client.get_payment_settle_response(
                    lambda name: response.headers.get(name)
                )
                print(f"Payment settled: {settle_response}")


    asyncio.run(main())
    ```
  </Tab>

  <Tab title="Python (requests)">
    **requests** provides sync HTTP client support with automatic 402 payment handling.

    [Full Requests example](https://github.com/coinbase/x402/tree/main/examples/python/clients/requests)

    ```python theme={null}
    import os
    from eth_account import Account

    from x402 import x402ClientSync
    from x402.http import x402HTTPClientSync
    from x402.http.clients import x402_requests
    from x402.mechanisms.evm import EthAccountSigner
    from x402.mechanisms.evm.exact.register import register_exact_evm_client


    def main() -> None:
        client = x402ClientSync()
        account = Account.from_key(os.getenv("EVM_PRIVATE_KEY"))
        register_exact_evm_client(client, EthAccountSigner(account))

        http_client = x402HTTPClientSync(client)

        with x402_requests(client) as session:
            response = session.get("https://api.example.com/paid-endpoint")

            print(f"Response: {response.text}")

            if response.ok:
                settle_response = http_client.get_payment_settle_response(
                    lambda name: response.headers.get(name)
                )
                print(f"Payment settled: {settle_response}")


    main()
    ```
  </Tab>
</Tabs>

### Multi-Network Client Setup

You can register multiple payment schemes to handle different networks:

<Tabs>
  <Tab title="TypeScript">
    ```typescript theme={null}
    import { x402Client, wrapFetchWithPayment } from "@x402/fetch";
    import { registerExactEvmScheme } from "@x402/evm/exact/client";
    import { registerExactSvmScheme } from "@x402/svm/exact/client";
    import { privateKeyToAccount } from "viem/accounts";
    import { createKeyPairSignerFromBytes } from "@solana/kit";
    import { base58 } from "@scure/base";

    // Create signers
    const evmSigner = privateKeyToAccount(
      process.env.EVM_PRIVATE_KEY as `0x${string}`,
    );
    const svmSigner = await createKeyPairSignerFromBytes(
      base58.decode(process.env.SOLANA_PRIVATE_KEY!),
    );

    // Create client with multiple schemes
    const client = new x402Client();
    registerExactEvmScheme(client, { signer: evmSigner });
    registerExactSvmScheme(client, { signer: svmSigner });

    const fetchWithPayment = wrapFetchWithPayment(fetch, client);

    // Now handles both EVM and Solana networks automatically!
    ```
  </Tab>

  <Tab title="Go">
    ```go theme={null}
    import (
        x402 "github.com/coinbase/x402/go"
        x402http "github.com/coinbase/x402/go/http"
        evm "github.com/coinbase/x402/go/mechanisms/evm/exact/client"
        svm "github.com/coinbase/x402/go/mechanisms/svm/exact/client"
        evmsigners "github.com/coinbase/x402/go/signers/evm"
        svmsigners "github.com/coinbase/x402/go/signers/svm"
    )

    // Create signers
    evmSigner, _ := evmsigners.NewClientSignerFromPrivateKey(os.Getenv("EVM_PRIVATE_KEY"))
    svmSigner, _ := svmsigners.NewClientSignerFromPrivateKey(os.Getenv("SVM_PRIVATE_KEY"))

    // Create client with multiple schemes
    x402Client := x402.Newx402Client().
        Register("eip155:*", evm.NewExactEvmScheme(evmSigner)).
        Register("solana:*", svm.NewExactSvmScheme(svmSigner))

    // Wrap HTTP client with payment handling
    httpClient := x402http.WrapHTTPClientWithPayment(
        http.DefaultClient,
        x402http.Newx402HTTPClient(x402Client),
    )

    // Now handles both EVM and Solana networks automatically!
    ```
  </Tab>

  <Tab title="Python">
    ```python theme={null}
    import asyncio
    import os

    from eth_account import Account

    from x402 import x402Client
    from x402.http.clients import x402HttpxClient
    from x402.mechanisms.evm import EthAccountSigner
    from x402.mechanisms.evm.exact.register import register_exact_evm_client
    from x402.mechanisms.svm import KeypairSigner
    from x402.mechanisms.svm.exact.register import register_exact_svm_client


    async def main() -> None:
        client = x402Client()

        # Register EVM scheme
        account = Account.from_key(os.getenv("EVM_PRIVATE_KEY"))
        register_exact_evm_client(client, EthAccountSigner(account))

        # Register SVM scheme
        svm_signer = KeypairSigner.from_base58(os.getenv("SVM_PRIVATE_KEY"))
        register_exact_svm_client(client, svm_signer)

        async with x402HttpxClient(client) as http:
            response = await http.get("https://api.example.com/paid-endpoint")
            print(f"Response: {response.text}")


    asyncio.run(main())
    ```
  </Tab>
</Tabs>

### Supporting the Upto Scheme

If you need to interact with services that use the `upto` payment scheme (usage-based billing), register the `UptoEvmScheme` alongside your existing exact schemes. The upto scheme is transparent to the buyer -- the SDK handles the max-authorization signing automatically, and you are only charged the actual settled amount (which may be less than the authorized maximum).

<Tabs>
  <Tab title="TypeScript">
    ```typescript theme={null}
    import { x402Client } from "@x402/fetch";
    import { ExactEvmScheme } from "@x402/evm/exact/client";
    import { UptoEvmScheme } from "@x402/evm/upto/client";
    import { privateKeyToAccount } from "viem/accounts";

    const signer = privateKeyToAccount(process.env.EVM_PRIVATE_KEY as `0x${string}`);

    const client = new x402Client();
    client.register("eip155:*", new ExactEvmScheme(signer));
    client.register("eip155:*", new UptoEvmScheme(signer));
    ```
  </Tab>

  <Tab title="Go">
    ```go theme={null}
    import (
        x402 "github.com/coinbase/x402/go"
        exactevm "github.com/coinbase/x402/go/mechanisms/evm/exact/client"
        uptoevm "github.com/coinbase/x402/go/mechanisms/evm/upto/client"
        evmsigners "github.com/coinbase/x402/go/signers/evm"
    )

    evmSigner, _ := evmsigners.NewClientSignerFromPrivateKey(os.Getenv("EVM_PRIVATE_KEY"))

    x402Client := x402.Newx402Client().
        Register("eip155:*", exactevm.NewExactEvmScheme(evmSigner)).
        Register("eip155:*", uptoevm.NewUptoEvmScheme(evmSigner))
    ```
  </Tab>
</Tabs>

<Note>
  The `upto` scheme is currently available on EVM networks only (TypeScript and Go SDKs). Python does not yet support upto. When registered, the SDK automatically selects the correct scheme based on what the server advertises in its 402 response.
</Note>

## 4. Discover Available Services (Optional)

Instead of hardcoding endpoints, you can use the x402 Bazaar to dynamically discover available services. This is especially powerful for building autonomous agents that can find and use new capabilities.

<Tabs>
  <Tab title="Node.js">
    ```typescript theme={null}
    import { HTTPFacilitatorClient } from "@x402/core/http";
    import { withBazaar } from "@x402/extensions/bazaar";

    // Create facilitator client with Bazaar extension
    const facilitatorClient = withBazaar(
      new HTTPFacilitatorClient({
        url: "https://api.cdp.coinbase.com/platform/v2/x402"
      })
    );

    // Query available services
    const discovery = await facilitatorClient.extensions.discovery.listResources({
      type: "http",
      limit: 20,
    });

    // Filter services by criteria
    const affordableServices = discovery.items.filter((item) =>
      item.accepts.some((req) => Number(req.amount) < 100000) // Under $0.10
    );

    console.log("Available services:", affordableServices);
    ```
  </Tab>

  <Tab title="Go">
    ```go theme={null}
    import (
        "encoding/json"
        "net/http"
    )

    // Fetch available services
    resp, _ := http.Get("https://api.cdp.coinbase.com/platform/v2/x402/discovery/resources")
    defer resp.Body.Close()

    var services struct {
        Items []map[string]interface{} `json:"items"`
    }
    json.NewDecoder(resp.Body).Decode(&services)

    fmt.Printf("Found %d services\n", len(services.Items))
    ```
  </Tab>

  <Tab title="Python">
    ```python theme={null}
    import asyncio
    import httpx


    async def main() -> None:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://api.cdp.coinbase.com/platform/v2/x402/discovery/resources",
                params={"type": "http", "limit": 20},
            )
            services = response.json()

            # Filter services by criteria
            affordable_services = [
                item for item in services.get("items", [])
                if any(int(req.get("amount", 0)) < 100000 for req in item.get("accepts", []))
            ]

            print(f"Available services: {affordable_services}")


    asyncio.run(main())
    ```
  </Tab>
</Tabs>

<Info>
  Learn more about service discovery in the [x402 Bazaar
  documentation](/x402/bazaar), including how to filter services, understand
  their schemas, and build agents that can autonomously discover new
  capabilities.
</Info>

## 5. Paying with Any ERC-20 Token via Permit2 (EVM)

Some endpoints accept payment in non-USDC ERC-20 tokens via [Permit2](https://github.com/Uniswap/permit2). The official **TypeScript**, **Go**, and **Python** client SDKs handle Permit2 automatically — no extra client code is needed. When a server advertises Permit2 as the transfer method (`extra.assetTransferMethod: "permit2"`), the client SDK creates the correct `PermitWitnessTransferFrom` payload instead of an EIP-3009 authorization.

### Gas Sponsorship (Automatic)

If the server declares a **gas sponsorship extension** (EIP-2612 or ERC-20), the TypeScript, Go, and Python client SDKs handle the Permit2 approval automatically:

* **EIP-2612 gas sponsoring:** The client signs an off-chain `permit()` message. The facilitator submits the approval on-chain — no gas cost to you.
* **ERC-20 gas sponsoring:** The client signs an `approve()` transaction. The facilitator broadcasts it on-chain before settling — no gas cost to you.

No additional client setup is needed for either case. The SDK detects the server's advertised extension and responds accordingly.

### One-Time Manual Approval (Fallback)

If the server uses Permit2 **without** gas sponsorship extensions, you must perform a one-time approval of the payment token to the [Permit2 contract](https://github.com/Uniswap/permit2) (`0x000000000022D473030F116dDEE9F6B43aC78BA3`) before your first payment. This only needs to be done once per token.

<Tabs>
  <Tab title="Node.js">
    ```typescript theme={null}
    import { erc20Abi } from "viem";
    import { walletClient } from "./your-wallet-setup";

    await walletClient.writeContract({
      address: "0xYourTokenAddress",
      abi: erc20Abi,
      functionName: "approve",
      args: [
        "0x000000000022D473030F116dDEE9F6B43aC78BA3", // Permit2 contract
        BigInt("0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"), // max approval
      ],
    });
    ```
  </Tab>

  <Tab title="Python">
    ```python theme={null}
    from web3 import Web3
    from eth_account import Account

    w3 = Web3(Web3.HTTPProvider("https://sepolia.base.org"))
    account = Account.from_key("0xYourPrivateKey")

    PERMIT2_ADDRESS = "0x000000000022D473030F116dDEE9F6B43aC78BA3"
    MAX_UINT256 = 2**256 - 1

    token = w3.eth.contract(
        address=Web3.to_checksum_address("0xYourTokenAddress"),
        abi=[{
            "type": "function",
            "name": "approve",
            "inputs": [
                {"name": "spender", "type": "address"},
                {"name": "amount", "type": "uint256"},
            ],
            "outputs": [{"type": "bool"}],
            "stateMutability": "nonpayable",
        }],
    )

    tx = token.functions.approve(PERMIT2_ADDRESS, MAX_UINT256).build_transaction({
        "from": account.address,
        "nonce": w3.eth.get_transaction_count(account.address),
    })

    signed = account.sign_transaction(tx)
    tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"Approved Permit2: {tx_hash.hex()} (block {receipt['blockNumber']})")
    ```
  </Tab>
</Tabs>

After this one-time approval, all subsequent Permit2 payments for that token work automatically.

<Info>
  For full details on EVM transfer methods and gas sponsorship, see [Network Support](/x402/network-support#evm-support-x402evm).
</Info>

## 6. Error Handling

Clients will throw errors if:

* No scheme is registered for the required network
* The request configuration is missing
* A payment has already been attempted for the request
* There is an error creating the payment header

Common error handling:

```typescript theme={null}
try {
  const response = await fetchWithPayment(url, { method: "GET" });
  // Handle success
} catch (error) {
  if (error.message.includes("No scheme registered")) {
    console.error("Network not supported - register the appropriate scheme");
  } else if (error.message.includes("Payment already attempted")) {
    console.error("Payment failed on retry");
  } else {
    console.error("Request failed:", error);
  }
}
```

## Summary

* Install x402 client packages (`@x402/fetch` or `@x402/axios`) and mechanism packages (`@x402/evm`, `@x402/svm`)
* Create a wallet signer
* Create an `x402Client` and register payment schemes (`exact` for fixed-price, `upto` for usage-based billing)
* Use the provided wrapper/interceptor to make paid API requests
* (Optional) Use the x402 Bazaar to discover services dynamically
* Payment flows are handled automatically for you -- including `upto` where you only pay the actual usage

## References:

* [@x402/fetch on npm](https://www.npmjs.com/package/@x402/fetch)
* [@x402/axios on npm](https://www.npmjs.com/package/@x402/axios)
* [@x402/evm on npm](https://www.npmjs.com/package/@x402/evm)
* [x402 Go module](https://github.com/coinbase/x402/tree/main/go)
* [x402 Python package on PyPI](https://pypi.org/project/x402/)
* [x402 Bazaar documentation](/x402/bazaar) - Discover available services
* [X402 with Embedded Wallets](/embedded-wallets/x402-payments) - User-facing applications with embedded wallets

For questions or support, join our [Discord](https://discord.gg/cdp).

