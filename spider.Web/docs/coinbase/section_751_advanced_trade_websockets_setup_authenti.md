# Advanced Trade WebSockets. Setup, Authentication, and Subscriptions
Source: https://docs.cdp.coinbase.com/coinbase-app/advanced-trade-apis/guides/websocket



## 1. Introduction

This guide provides a comprehensive overview of setting up Coinbase Advanced Trade WebSockets, including essential steps for authentication and managing subscriptions. Coinbase’s Advanced Trade WebSocket API enables real-time access to market data and user-specific order information, empowering developers to build robust trading applications and monitoring tools. In this first part, you’ll learn how to establish WebSocket connections, authenticate using JWT tokens, and efficiently subscribe to key channels, such as market data and user-specific channels. With this foundational knowledge, you’ll be prepared to integrate the WebSocket API seamlessly into your application.

<Tip>
  You can quickly scroll to any section of this article by using the links on the outline of this guide on the right-hand side of the page.
</Tip>

### Overview of WebSocket Functionality

The Coinbase Developer Platform's Advanced Trade product provides two WebSocket endpoints:

* **Market Data Endpoint**: `wss://advanced-trade-ws.coinbase.com`
  This public WebSocket feed delivers real-time updates on market orders and trades for various cryptocurrency products.

* **User Order Data Endpoint**: `wss://advanced-trade-ws-user.coinbase.com`
  This authenticated WebSocket feed provides real-time updates on the user’s orders, including order status and updates on active trades.

Both endpoints provide live data streams using WebSocket connections, enabling developers to receive real-time updates on trading activity, order books, and market movements. This guide will cover how to correctly establish these WebSocket connections, manage subscriptions, and handle potential errors during integration.

## 2. Setting Up WebSocket Connections

To integrate with the Coinbase Advanced Trade WebSockets, developers need to establish a WebSocket connection with either the Market Data or User Order Data endpoints. This section will guide you through the process of setting up these WebSocket connections and ensuring they remain active.

### WebSocket Endpoints

**Market Data Endpoint**: `wss://advanced-trade-ws.coinbase.com`
This endpoint provides real-time market data, including updates on orders, trades, and price changes for various cryptocurrency pairs. Authentication is not required for most channels on this endpoint.

**User Order Data Endpoint**: `wss://advanced-trade-ws-user.coinbase.com`
This endpoint provides updates related to a user's orders, including order status, fills, and real-time changes. It requires authentication using a JWT (JSON Web Token).

### Basic Connection Setup

After establishing a WebSocket connection, the server expects a subscription message to be sent within 5 seconds; otherwise, the connection will be terminated. This subscription message tells the WebSocket server which channels and products the client wants to receive data for. Developers can subscribe to multiple channels, but each subscription must be sent in a unique message.

### Example: Connecting Without Authentication (Market Data Endpoint)

For public data, you can set up a basic WebSocket connection without authentication. Here is an example in Python that connects to the market data WebSocket and subscribes to the `ticker` channel for the BTC-USD product.
First, let’s install the necessary dependency::

`pip install websocket`

```python [expandable] lines wrap theme={null}
import websocket
import json
