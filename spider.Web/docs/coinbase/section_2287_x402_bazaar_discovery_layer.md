# x402 Bazaar (Discovery Layer)
Source: https://docs.cdp.coinbase.com/x402/bazaar



The x402 Bazaar is the discovery layer for the x402 ecosystem: a machine-readable catalog that helps developers and AI agents find and integrate with x402-compatible API endpoints. Think of it as a search index for payable APIs, enabling autonomous discovery and consumption of services.

<Note>
  The x402 Bazaar is in early development. While our vision is to build the
  "Google for agentic endpoints," we're currently more like "Yahoo search":
  functional but evolving. Features and APIs may change as we gather feedback
  and expand capabilities.
</Note>

## Overview

The Bazaar solves a critical problem in the x402 ecosystem: **discoverability**. Without it, x402-compatible endpoints are like hidden stalls in a vast market. The Bazaar provides:

* **For Buyers (API Consumers)**: Programmatically discover available x402-enabled services, understand their capabilities, pricing, and schemas
* **For Sellers (API Providers)**: Automatic visibility for your x402-enabled services to a global audience of developers and AI agents
* **For AI Agents**: Dynamic service discovery without pre-baked integrations. Query, find, pay, and use

## How It Works

In x402 v2, the Bazaar has been codified as an **official extension** in the reference SDK (`@x402/extensions/bazaar`). This extension enables:

1. **Servers** declare discovery metadata (input/output schemas) in their route configuration
2. **Facilitators** extract and catalog this metadata when processing payments
3. **Clients** query the facilitator's `/discovery/resources` endpoint to find available services

<Info>
  **When does my endpoint appear?** There is no separate registration step. The facilitator catalogs your service the **first time it processes a payment** (verify + settle) for that endpoint. If your service doesn't appear, ensure at least one successful payment has gone through the facilitator whose discovery endpoint you're querying (CDP vs x402.org).
</Info>

### v1 vs v2

| Aspect              | v1 (Deprecated)                             | v2 (Current)                              |
| ------------------- | ------------------------------------------- | ----------------------------------------- |
| Discovery data      | `outputSchema` field in PaymentRequirements | `extensions.bazaar` field in route config |
| Schema validation   | None                                        | JSON Schema validation                    |
| Input specification | Not supported                               | Full input/output schema support          |

## Quickstart for Sellers

To make your endpoints discoverable in the Bazaar, you need to:

1. Register the Bazaar extension on your resource server
2. Declare discovery metadata in your route configuration

<Tip>
  The examples below use the x402.org testnet facilitator for a signup-free quick start. For production, we recommend the [CDP facilitator](/x402/network-support)—its discovery endpoint is at `https://api.cdp.coinbase.com/platform/v2/x402/discovery/resources`.
</Tip>

### Step 1: Install the Extension Package

<Tabs>
  <Tab title="Node.js">
    ```bash theme={null}
    npm install @x402/extensions
    ```
  </Tab>

  <Tab title="Go">
    ```bash theme={null}
    go get github.com/coinbase/x402/go/extensions/bazaar
    ```
  </Tab>

  <Tab title="Python">
    ```bash theme={null}
    pip install "x402[fastapi]"
    ```
  </Tab>
</Tabs>

### Step 2: Register the Extension and Declare Discovery Metadata

<Tabs>
  <Tab title="Node.js (Express)">
    Full example in the [Express server example](https://github.com/coinbase/x402/tree/main/examples/typescript/servers/express).

    ```typescript theme={null}
    import express from "express";
    import { paymentMiddleware } from "@x402/express";
    import { x402ResourceServer, HTTPFacilitatorClient } from "@x402/core/server";
    import { registerExactEvmScheme } from "@x402/evm/exact/server";
    import {
      bazaarResourceServerExtension,
      declareDiscoveryExtension,
    } from "@x402/extensions/bazaar";

    const app = express();

    // Create facilitator client
    const facilitatorClient = new HTTPFacilitatorClient({
      url: "https://x402.org/facilitator",
    });

    // Create resource server and register extensions
    const server = new x402ResourceServer(facilitatorClient);
    registerExactEvmScheme(server);
    server.registerExtension(bazaarResourceServerExtension);

    // Configure payment middleware with discovery metadata
    app.use(
      paymentMiddleware(
        {
          "GET /weather": {
            accepts: {
              scheme: "exact",
              price: "$0.001",
              network: "eip155:84532",
              payTo: "0xYourAddress",
            },
            extensions: {
              // Declare discovery metadata for this endpoint
              ...declareDiscoveryExtension({
                output: {
                  example: {
                    temperature: 72,
                    conditions: "sunny",
                    humidity: 45,
                  },
                  schema: {
                    properties: {
                      temperature: { type: "number" },
                      conditions: { type: "string" },
                      humidity: { type: "number" },
                    },
                    required: ["temperature", "conditions"],
                  },
                },
              }),
            },
          },
        },
        server,
      ),
    );

    app.get("/weather", (req, res) => {
      res.json({
        temperature: 72,
        conditions: "sunny",
        humidity: 45,
      });
    });

    app.listen(4021);
    ```
  </Tab>

  <Tab title="Go (Gin)">
    ```go theme={null}
    package main

    import (
        "net/http"

        x402 "github.com/coinbase/x402/go"
        x402http "github.com/coinbase/x402/go/http"
        ginmw "github.com/coinbase/x402/go/http/gin"
        evm "github.com/coinbase/x402/go/mechanisms/evm/exact/server"
        "github.com/coinbase/x402/go/extensions/bazaar"
        "github.com/coinbase/x402/go/extensions/types"
        "github.com/gin-gonic/gin"
    )

    func main() {
        r := gin.Default()

        // Create discovery extension for the endpoint
        discoveryExt, _ := bazaar.DeclareDiscoveryExtension(
            types.MethodGET,
            nil, // No query params required
            nil, // No input schema
            "",  // Not a body method
            &types.OutputConfig{
                Example: map[string]interface{}{
                    "temperature": 72,
                    "conditions":  "sunny",
                    "humidity":    45,
                },
                Schema: types.JSONSchema{
                    "properties": map[string]interface{}{
                        "temperature": map[string]interface{}{"type": "number"},
                        "conditions":  map[string]interface{}{"type": "string"},
                        "humidity":    map[string]interface{}{"type": "number"},
                    },
                    "required": []string{"temperature", "conditions"},
                },
            },
        )

        r.Use(ginmw.X402Payment(ginmw.Config{
            Routes: x402http.RoutesConfig{
                "GET /weather": {
                    Scheme:  "exact",
                    PayTo:   "0xYourAddress",
                    Price:   "$0.001",
                    Network: x402.Network("eip155:84532"),
                    Extensions: map[string]interface{}{
                        types.BAZAAR: discoveryExt,
                    },
                },
            },
            Facilitator: x402http.NewHTTPFacilitatorClient(&x402http.FacilitatorConfig{
                URL: "https://x402.org/facilitator",
            }),
            Schemes: []ginmw.SchemeConfig{
                {Network: x402.Network("eip155:84532"), Server: evm.NewExactEvmScheme()},
            },
        }))

        r.GET("/weather", func(c *gin.Context) {
            c.JSON(http.StatusOK, gin.H{
                "temperature": 72,
                "conditions":  "sunny",
                "humidity":    45,
            })
        })

        r.Run(":4021")
    }
    ```
  </Tab>

  <Tab title="Python (FastAPI)">
    Full example in the repo [here](https://github.com/coinbase/x402/tree/main/examples/python/servers/fastapi).

    ```python theme={null}
    from typing import Any

    from fastapi import FastAPI

    from x402.http import FacilitatorConfig, HTTPFacilitatorClient, PaymentOption
    from x402.http.middleware.fastapi import PaymentMiddlewareASGI
    from x402.http.types import RouteConfig
    from x402.mechanisms.evm.exact import ExactEvmServerScheme
    from x402.server import x402ResourceServer

    app = FastAPI()

    pay_to = "0xYourAddress"

    facilitator = HTTPFacilitatorClient(
        FacilitatorConfig(url="https://x402.org/facilitator")
    )

    server = x402ResourceServer(facilitator)
    server.register("eip155:84532", ExactEvmServerScheme())

    # Define protected routes with discovery metadata
    routes: dict[str, RouteConfig] = {
        "GET /weather": RouteConfig(
            accepts=[
                PaymentOption(
                    scheme="exact",
                    pay_to=pay_to,
                    price="$0.001",
                    network="eip155:84532",
                ),
            ],
            mime_type="application/json",
            description="Get current weather data for any location",
            extensions={
                "bazaar": {
                    "info": {
                        "output": {
                            "type": "json",
                            "example": {
                                "temperature": 72,
                                "conditions": "sunny",
                                "humidity": 45,
                            },
                        },
                    },
                },
            },
        ),
    }

    app.add_middleware(PaymentMiddlewareASGI, routes=routes, server=server)


    @app.get("/weather")
    async def get_weather() -> dict[str, Any]:
        return {
            "temperature": 72,
            "conditions": "sunny",
            "humidity": 45,
        }


    if __name__ == "__main__":
        import uvicorn
        uvicorn.run(app, host="0.0.0.0", port=4021)
    ```
  </Tab>
</Tabs>

### Discovery Extension Options

The `declareDiscoveryExtension` function accepts configuration for different HTTP methods:

```typescript theme={null}
// For GET endpoints (query params)
declareDiscoveryExtension({
  input: { city: "San Francisco" }, // Example query params
  inputSchema: {
    properties: {
      city: { type: "string", description: "City name" },
    },
    required: ["city"],
  },
  output: {
    example: { temperature: 72 },
    schema: {
      properties: {
        temperature: { type: "number" },
      },
    },
  },
});

// For POST endpoints (request body)
declareDiscoveryExtension({
  input: { prompt: "Hello world" }, // Example body
  inputSchema: {
    properties: {
      prompt: { type: "string", maxLength: 1000 },
    },
    required: ["prompt"],
  },
  bodyType: "json", // Signals this is a body method
  output: {
    example: { response: "Hi there!" },
  },
});
```

## Quickstart for Buyers

To discover available services, use the `withBazaar` wrapper to extend your facilitator client with discovery capabilities.

### Step 1: Install Dependencies

<Tabs>
  <Tab title="Node.js">
    ```bash theme={null}
    npm install @x402/core @x402/extensions @x402/fetch @x402/evm
    ```
  </Tab>

  <Tab title="Go">
    ```bash theme={null}
    go get github.com/coinbase/x402/go
    ```
  </Tab>

  <Tab title="Python">
    ```bash theme={null}
    pip install "x402[httpx]"
    ```
  </Tab>
</Tabs>

### Step 2: Query the Discovery Endpoint

<Tabs>
  <Tab title="Node.js">
    ```typescript theme={null}
    import { HTTPFacilitatorClient } from "@x402/core/http";
    import { withBazaar } from "@x402/extensions/bazaar";
    import { x402Client, wrapFetchWithPayment } from "@x402/fetch";
    import { registerExactEvmScheme } from "@x402/evm/exact/client";
    import { privateKeyToAccount } from "viem/accounts";

    // Create facilitator client with Bazaar extension
    const facilitatorClient = withBazaar(
      new HTTPFacilitatorClient({ url: "https://x402.org/facilitator" })
    );

    // Query available services
    const discovery = await facilitatorClient.extensions.discovery.listResources({
      type: "http",   // Filter by protocol type
      limit: 20,      // Pagination
      offset: 0,
    });

    console.log(`Found ${discovery.items.length} services`);

    // Browse discovered resources
    for (const resource of discovery.items) {
      console.log(`- ${resource.resource}`);
      console.log(`  Type: ${resource.type}`);
      console.log(`  x402 Version: ${resource.x402Version}`);
      console.log(`  Accepts: ${resource.accepts.length} payment method(s)`);
      console.log(`  Last Updated: ${resource.lastUpdated}`);
      if (resource.metadata) {
        console.log(`  Metadata:`, resource.metadata);
      }
    }

    // Select a service and make a paid request
    const selectedService = discovery.items[0];

    // Set up x402 client for payments
    const signer = privateKeyToAccount(process.env.EVM_PRIVATE_KEY as `0x${string}`);
    const client = new x402Client();
    registerExactEvmScheme(client, { signer });

    const fetchWithPayment = wrapFetchWithPayment(fetch, client);

    // Call the discovered service
    const response = await fetchWithPayment(selectedService.resource);
    const data = await response.json();
    console.log("Response:", data);
    ```
  </Tab>

  <Tab title="Go">
    ```go theme={null}
    package main

    import (
        "encoding/json"
        "fmt"
        "net/http"
        "os"

        x402 "github.com/coinbase/x402/go"
        x402http "github.com/coinbase/x402/go/http"
        evm "github.com/coinbase/x402/go/mechanisms/evm/exact/client"
    )

    func main() {
        facilitatorURL := "https://x402.org/facilitator"

        // Query discovery endpoint
        resp, err := http.Get(facilitatorURL + "/discovery/resources?type=http&limit=20")
        if err != nil {
            panic(err)
        }
        defer resp.Body.Close()

        var discovery struct {
            X402Version int `json:"x402Version"`
            Items []struct {
                Resource    string                   `json:"resource"`
                Type        string                   `json:"type"`
                X402Version int                      `json:"x402Version"`
                Accepts     []map[string]interface{} `json:"accepts"`
                LastUpdated string                   `json:"lastUpdated"`
                Metadata    map[string]interface{}   `json:"metadata"`
            } `json:"items"`
            Pagination struct {
                Limit  int `json:"limit"`
                Offset int `json:"offset"`
                Total  int `json:"total"`
            } `json:"pagination"`
        }
        json.NewDecoder(resp.Body).Decode(&discovery)

        fmt.Printf("Found %d services\n", len(discovery.Items))

        // Select a service
        if len(discovery.Items) == 0 {
            fmt.Println("No services found")
            return
        }
        selectedResource := discovery.Items[0].Resource

        // Create x402 client for payments
        client := x402.NewX402Client()
        evm.RegisterExactEvmScheme(client, &evm.Config{
            PrivateKey: os.Getenv("EVM_PRIVATE_KEY"),
        })

        // Make paid request
        httpClient := x402.WrapHTTPClient(client)
        req, _ := http.NewRequest("GET", selectedResource, nil)
        paymentResp, err := httpClient.Do(req)
        if err != nil {
            panic(err)
        }
        defer paymentResp.Body.Close()

        var data map[string]interface{}
        json.NewDecoder(paymentResp.Body).Decode(&data)
        fmt.Printf("Response: %+v\n", data)
    }
    ```
  </Tab>

  <Tab title="Python">
    ```python theme={null}
    import asyncio
    import os

    import httpx
    from eth_account import Account

    from x402 import x402Client
    from x402.http.clients import x402HttpxClient
    from x402.mechanisms.evm import EthAccountSigner
    from x402.mechanisms.evm.exact.register import register_exact_evm_client


    async def main() -> None:
        facilitator_url = "https://x402.org/facilitator"

        # Query discovery endpoint
        async with httpx.AsyncClient() as http:
            response = await http.get(
                f"{facilitator_url}/discovery/resources",
                params={"type": "http", "limit": 20},
            )
            discovery = response.json()

        print(f"Found {len(discovery.get('items', []))} services")

        # Browse discovered resources
        for resource in discovery.get("items", []):
            print(f"- {resource['resource']}")
            print(f"  Type: {resource['type']}")
            print(f"  x402 Version: {resource['x402Version']}")
            print(f"  Accepts: {len(resource['accepts'])} payment method(s)")
            if resource.get("metadata"):
                print(f"  Metadata: {resource['metadata']}")

        # Select a service and make a paid request
        items = discovery.get("items", [])
        if not items:
            print("No services found")
            return

        selected_resource = items[0]["resource"]

        # Set up x402 client for payments
        client = x402Client()
        account = Account.from_key(os.getenv("EVM_PRIVATE_KEY"))
        register_exact_evm_client(client, EthAccountSigner(account))

        # Call the discovered service
        async with x402HttpxClient(client) as http:
            response = await http.get(selected_resource)
            await response.aread()
            print(f"Response: {response.json()}")


    asyncio.run(main())
    ```
  </Tab>
</Tabs>

## API Reference

### Discovery Endpoint

Facilitators that support the Bazaar extension expose a discovery endpoint:

```
GET {facilitator_url}/discovery/resources
```

#### Query Parameters

| Parameter | Type   | Description                                 |
| --------- | ------ | ------------------------------------------- |
| `type`    | string | Filter by protocol type (e.g., `"http"`)    |
| `limit`   | number | Number of resources to return (default: 20) |
| `offset`  | number | Offset for pagination (default: 0)          |

#### Response Schema

```json theme={null}
{
  "x402Version": 2,
  "items": [
    {
      "resource": "https://api.example.com/weather",
      "type": "http",
      "x402Version": 1,
      "accepts": [
        {
          "scheme": "exact",
          "network": "eip155:84532",
          "amount": "1000",
          "asset": "0x036CbD53842c5426634e7929541eC2318f3dCF7e",
          "payTo": "0x209693Bc6afc0C5328bA36FaF03C514EF312287C"
        }
      ],
      "lastUpdated": "2024-01-15T12:30:00.000Z",
      "metadata": {
        "description": "Weather data API",
        "input": { ... },
        "output": { ... }
      }
    }
  ],
  "pagination": {
    "limit": 20,
    "offset": 0,
    "total": 42
  }
}
```

#### Discovered Resource Fields

| Field         | Type     | Required | Description                                                      |
| ------------- | -------- | -------- | ---------------------------------------------------------------- |
| `resource`    | `string` | Yes      | The resource URL being monetized                                 |
| `type`        | `string` | Yes      | Resource type (currently `"http"`)                               |
| `x402Version` | `number` | Yes      | Protocol version supported by the resource                       |
| `accepts`     | `array`  | Yes      | Array of PaymentRequirements specifying accepted payment methods |
| `lastUpdated` | `string` | Yes      | ISO 8601 timestamp of when the resource was last updated         |
| `metadata`    | `object` | No       | Additional metadata (description, schemas, etc.)                 |

### CDP Facilitator Discovery Endpoint

The CDP facilitator's discovery endpoint:

```
GET https://api.cdp.coinbase.com/platform/v2/x402/discovery/resources
```

<Note>
  The default limit is 100 results per request. Use pagination parameters to
  retrieve additional results.
</Note>

### Merchant Discovery Endpoint

To look up all active resources registered to a specific merchant by their `payTo` wallet address, use the merchant discovery endpoint:

```
GET https://api.cdp.coinbase.com/platform/v2/x402/discovery/merchant?payTo=<address>
```

This endpoint is publicly accessible — no API key is required. It is useful for buyers and AI agents that want to discover resources payable to a specific wallet.

#### Query Parameters

| Parameter | Type    | Required | Description                                                    |
| --------- | ------- | -------- | -------------------------------------------------------------- |
| `payTo`   | string  | Yes      | The merchant's wallet address (EVM 0x-prefix or Solana base58) |
| `limit`   | integer | No       | Number of resources to return (default: 25, max: 100)          |
| `offset`  | integer | No       | Number of resources to skip for pagination (default: 0)        |

#### Response Schema

```json theme={null}
{
  "payTo": "0x209693Bc6afc0C5328bA36FaF03C514EF312287C",
  "resources": [
    {
      "resource": "https://api.example.com/premium/data",
      "type": "http",
      "x402Version": 2,
      "accepts": [
        {
          "scheme": "exact",
          "network": "eip155:84532",
          "asset": "0x036CbD53842c5426634e7929541eC2318f3dCF7e",
          "amount": "1000",
          "payTo": "0x209693Bc6afc0C5328bA36FaF03C514EF312287C",
          "maxTimeoutSeconds": 60
        }
      ],
      "lastUpdated": "2025-06-01T12:00:00.000Z",
      "metadata": {
        "description": "Premium data API"
      }
    }
  ],
  "pagination": {
    "limit": 25,
    "offset": 0,
    "total": 1
  }
}
```

The endpoint returns `404` if no active resources are found for the given address, and `400` if the `payTo` parameter is missing or invalid.

See the [full API reference](/api-reference/v2/rest-api/x402-facilitator/get-merchant-resources-by-payto-address) for complete details.

## Extension Architecture

The Bazaar extension follows the x402 v2 extensions pattern:

```typescript theme={null}
// Extension structure
{
  bazaar: {
    info: {
      input: {
        type: "http",
        method: "GET",
        queryParams: { ... }
      },
      output: {
        type: "json",
        example: { ... }
      }
    },
    schema: {
      // JSON Schema validating the info structure
      $schema: "https://json-schema.org/draft/2020-12/schema",
      type: "object",
      properties: { ... }
    }
  }
}
```

### Key Components

| Component                       | Purpose                                                           |
| ------------------------------- | ----------------------------------------------------------------- |
| `bazaarResourceServerExtension` | Server extension that enriches declarations with HTTP method info |
| `declareDiscoveryExtension()`   | Helper to create properly structured extension declarations       |
| `withBazaar()`                  | Client wrapper that adds discovery query methods                  |
| `extractDiscoveryInfo()`        | Facilitator helper to extract discovery data from payments        |

## Best Practices

### For Sellers

1. **Provide clear examples**: Include realistic `output.example` values that demonstrate your API's response format
2. **Document inputs**: Use `inputSchema` with descriptions to help clients understand required parameters
3. **Use appropriate types**: Specify correct JSON Schema types (`string`, `number`, `boolean`, `array`, `object`)

### For Buyers

1. **Cache discovery results**: Don't query discovery on every request
2. **Handle pagination**: Use `offset` and `limit` for large result sets
3. **Validate compatibility**: Check that discovered services support your payment network

## Support

* **GitHub**: [github.com/coinbase/x402](https://github.com/coinbase/x402)
* **Discord**: [Join #x402 channel](https://discord.gg/cdp)
* **Documentation**: [x402 Overview](/x402/welcome)

## FAQ

**Q: How do I get my service listed in the Bazaar?**
A: Register the `bazaarResourceServerExtension` on your resource server and include `declareDiscoveryExtension()` in your route configuration. The facilitator will automatically catalog your service when it processes payments.

**Q: Can I opt out of discovery?**
A: Yes, simply don't include the Bazaar extension in your route configuration. Only routes with the extension will be discoverable.

**Q: What networks are supported?**
A: The Bazaar is network-agnostic. It catalogs services regardless of which payment networks they accept.

**Q: How often is the discovery catalog updated?**
A: Services are cataloged when the facilitator processes payments. The catalog is refreshed as transactions occur.

**Q: When does my service appear in the Bazaar?**
A: After you add the Bazaar extension and discovery metadata to your routes, your service is cataloged the first time the facilitator processes a payment (verify + settle) for that endpoint. There is no separate registration step. If you don't see your service, ensure at least one successful payment has gone through the facilitator whose discovery endpoint you're querying (CDP vs x402.org).

**Q: Is there a test Bazaar for development?**
A: Yes. The [x402.org testnet facilitator](https://x402.org/facilitator) exposes a discovery endpoint at `https://x402.org/facilitator/discovery/resources`. Because that facilitator is testnet-only (Base Sepolia, Solana Devnet), it effectively serves as the test Bazaar—use it for dev and integration testing before querying the CDP facilitator's discovery (which includes mainnet listings).

**Q: Can I list endpoints that require auth or return 200 without payment?**
A: Currently, discovery is populated from endpoints that return 402 and receive payment through the facilitator. Endpoints that require pre-auth, return 200 without payment, or use \$0 "discovery-only" flows may not be cataloged. Support for these patterns is under consideration.

