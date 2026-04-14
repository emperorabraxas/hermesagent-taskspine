# Exchange FIX API Connectivity
Source: https://docs.cdp.coinbase.com/exchange/fix-api/connectivity



[Financial Information eXchange](http://en.wikipedia.org/wiki/Financial_Information_eXchange), or FIX, is a standard protocol which can be used to enter orders, submit cancel requests, and receive fills. FIX API users typically have existing software that runs FIX for order management.

The baseline specification for the Exchange FIX API:

* Order Entry & Market Data: [FIX 5.0 SP2](https://www.onixs.biz/fix-dictionary/5.0/index.html)

<Warning>
  FIX5 Resets Saturdays at 1PM ET

  FIX5 Order Entry and Market Data customers will be logged out every Saturday at 1PM ET (6PM UTC).
</Warning>

<Info>
  Changes are deployed every Monday and Thursday at or near `2PM EST (7PM UTC)`. At that time, a <strong>logout</strong> message is sent from the server to indicate the session is ending. We do not deploy on US federal holidays.
</Info>

## Supported Endpoints

<Info>
  **Production**<br />
  Order Entry (FIX5.0): `tcp+ssl://fix-ord.exchange.coinbase.com:6121`<br />
  Market Data Snapshot Enabled (FIX5.0): `tcp+ssl://fix-md.exchange.coinbase.com:6121`<br />
  Market Data Snapshot Disabled (FIX5.0): `tcp+ssl://fix-md.exchange.coinbase.com:6122`<br />
  Dedicated Drop Copy (FIX5.0): `tcp+ssl://fix-dc.exchange.coinbase.com:6122`<br />

  **Sandbox**<br />
  Order Entry (FIX5.0): `tcp+ssl://fix-ord.sandbox.exchange.coinbase.com:6121`<br />
  Market Data Snapshot Enabled (FIX5.0): `tcp+ssl://fix-md.sandbox.exchange.coinbase.com:6121`<br />
  Market Data Snapshot Disabled (FIX5.0): `tcp+ssl://fix-md.sandbox.exchange.coinbase.com:6122`<br />
  Dedicated Drop Copy (FIX5.0): `tcp+ssl://fix-dc.sandbox.exchange.coinbase.com:6122`<br />
</Info>

<Warning>
  Resend Requests

  Resend requests are not supported. Every connection establishes a new session and a new set of session sequence numbers.
</Warning>

## FIX Gateway

Before logging onto a FIX session, clients must establish a secure connection to the FIX gateway. See the [available endpoints](#supported-endpoints) above.

**TCP SSL**

If your FIX implementation does not support establishing a **native TCP SSL connection**, you must setup a local proxy such as [stunnel](https://www.stunnel.org) to establish a secure connection to the FIX gateway.

**Static IP**

Coinbase Exchange **does not** support static IP addresses. If your firewall rules require a static IP address, you must create a TCP proxy server with a static IP address which is capable of resolving an IP address using DNS.

**AWS IP**

If connecting from servers **outside of AWS** which require firewall rules, use the [AWS provided resources](https://docs.aws.amazon.com/general/latest/gr/aws-ip-ranges.html) to determine how best to whitelist AWS IP ranges.

<Info>
  Changes are deployed every Monday and Thursday at or near `2PM EST (7PM UTC)`. At that time, a <strong>logout</strong> message is sent from the server to indicate the session is ending. We do not deploy on US federal holidays.
</Info>

## Ciphers

Coinbase Exchange supports **TLSv1.2** with the following server ciphers:

| Recommend | Length   | Cipher Suite                  | Elliptic Curve      |
| :-------- | :------- | :---------------------------- | :------------------ |
| Preferred | 128 bits | `ECDHE-RSA-AES128-GCM-SHA256` | Curve P-256 DHE 256 |
| Accepted  | 128 bits | `ECDHE-RSA-AES128-SHA256`     | Curve P-256 DHE 256 |
| Accepted  | 256 bits | `ECDHE-RSA-AES256-GCM-SHA384` | Curve P-256 DHE 256 |
| Accepted  | 256 bits | `ECDHE-RSA-AES256-SHA384`     | Curve P-256 DHE 256 |

## SSL Tunnels

[Exchange FIX API endpoints](/exchange/fix-api/connectivity#supported-endpoints) only accept TCP connections secured by SSL. If your FIX client library cannot establish an SSL connection natively, you must run a local proxy that establishes a secure connection and allows unencrypted local connections.

