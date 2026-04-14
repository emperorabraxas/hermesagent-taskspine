# MCP Server with x402
Source: https://docs.cdp.coinbase.com/x402/mcp-server



[Model Context Protocol (MCP)](https://www.modelcontextprotocol.io/) is a protocol for passing context between LLMs and other AI agents. This page shows how to use the x402 payment protocol with MCP to make paid API requests through an MCP server, and how to connect it to Claude Desktop.

## What is this integration?

This guide walks you through running an MCP server that can access paid APIs using the x402 protocol. The MCP server acts as a bridge between Claude Desktop (or any MCP-compatible client) and a paid API (such as the sample weather API in the x402 repo). When Claude (or another agent) calls a tool, the MCP server will:

1. Detect if the API requires payment (via HTTP 402 with `PAYMENT-REQUIRED` header)
2. Automatically handle the payment using your wallet via the registered x402 scheme
3. Return the paid data to the client (e.g., Claude)

This lets you (or your agent) access paid APIs programmatically, with no manual payment steps.

## Prerequisites

* Node.js v20+ (install via [nvm](https://github.com/nvm-sh/nvm))
* pnpm v10 (install via [pnpm.io/installation](https://pnpm.io/installation))
* An x402-compatible server to connect to (for this demo, we'll use the [sample express server with weather data](https://github.com/coinbase/x402/tree/main/examples/typescript/servers/express) from the x402 repo, or any external x402 API)
* An Ethereum wallet with USDC (on Base Sepolia, Base Mainnet, or Polygon Mainnet) and/or a Solana wallet with USDC (on Devnet or Mainnet)
* [Claude Desktop with MCP support](https://claude.ai/download)

## Quick Start

### 1. Install and Build

```bash theme={null}