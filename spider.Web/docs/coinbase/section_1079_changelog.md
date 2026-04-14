# Changelog
Source: https://docs.cdp.coinbase.com/get-started/changelog

Product updates and announcements for Coinbase Developer Platform (CDP)

<Update label="February 19, 2026">
  ## Onramp

  * **Onramp User Limits API (General Availability)**: Developers can now check a user's remaining purchase capacity (spending and transaction count) for Guest Checkout transactions before initiation. This helps display limits in-app and prevents transaction failures due to limit exceeded errors.

  ## x402

  * **Agentic Wallet monetize-skill upgraded to x402 v2**: The monetize-skill in Agentic Wallet was upgraded from x402 v1 to x402 v2.
</Update>

<Update label="February 11, 2026">
  <Frame>
    <video />
  </Frame>

  ## Agentic Wallets

  * **Agentic Wallets now available**: Introducing wallet infrastructure built specifically for AI agents. Enable autonomous spending, trading, and API payments with built-in security guardrails. [Learn more here](https://docs.cdp.coinbase.com/agentic-wallet/welcome).

  ## Data API

  * **SQL API x402 Support**: Developers can now integrate real-time indexed data with their onchain agents via programmatic payments.

  ## Onramp

  * **Onramp User Limits API (Private Beta)**: Developers can now check a user's remaining purchase capacity (spending and transaction count) for Guest Checkout transactions before initiation. This helps display limits in-app and prevents transaction failures due to limit exceeded errors.

  ## x402

  * **Payments MCP upgraded to support x402 v2**: The Payments MCP now supports the latest x402 v2 protocol.
  * **Bazaar MCP server**: Added Bazaar MCP server to surface HTTP resources as tools and allow them to be invoked.
</Update>

<Update label="February 5, 2026">
  <Frame>
    <video />
  </Frame>

  ## Wallets

  * **Custom OAuth**: Developers can now configure their own OAuth provider credentials for third-party authentication providers (Telegram, Google, X, Apple, etc.).
  * **MFA Components**: Launched ready-to-use React components that make it dead-simple for users to enroll in MFA for sign-ins, transfers, key exports, and more.
</Update>

<Update label="January 28, 2026">
  <Frame>
    <img />
  </Frame>

  ## Embedded Wallets

  * **USDC Send Hooks**: Added `useSendEvmUsdc` and `useSendSolanaUsdc` hooks providing web2-like abstractions for USDC transfers with automatic handling of contracts, decimals, gas sponsorship, and Solana associated token accounts, eliminating common failure modes like the gas gap and decimal errors.

  ## x402 Updates

  * **Fixed Solana settlement bug**: Resolved intermittent settlement failures on SoElana.
  * **Fixed EVM settlement timeout**: Addressed timeout issues caused by gas spikes on EVM chains.
  * **x402 v2 Python package**: Published new x402 v2 Python package to PyPI.
</Update>

<Update label="January 15, 2026">
  <Frame>
    <img />
  </Frame>

  ## Onramp

  * **Email support now enabled for Coinbase onramp**: Users who encounter transaction errors can now contact Coinbase's onramp support email directly, reducing operational overhead for your business. Currently excludes the [Apple Pay onramp API](https://docs.cdp.coinbase.com/onramp/headless-onramp/apple-pay-onramp-api).
  * **Session API purchaseAmount support**: Developers can now pass a parameter when creating an onramp session to specify the exact crypto amount users will receive. [Read more here](https://docs.cdp.coinbase.com/api-reference/v2/rest-api/onramp/create-an-onramp-session).

  ## Wallets

  * **Wallet pre-generation with spend permissions and key import**: Enhanced wallet pre-generation now supports [spend permissions](https://docs.cdp.coinbase.com/embedded-wallets/wallet-pre-generation#spend-permissions) and [key import](https://docs.cdp.coinbase.com/embedded-wallets/wallet-pre-generation#pre-generate-wallet-with-an-existing-private-key) capabilities.
  * **Expanded Mobile SMS auth coverage**: Added 7 new country codes to [Mobile SMS auth](https://docs.cdp.coinbase.com/embedded-wallets/authentication-methods#sms-otp): Antigua and Barbuda, Bahamas, Dominican Republic, Grenada, Guyana, Suriname, Saint Vincent and the Grenadines.

  ## Data API Updates

  * **Optimized Zora queries**: Created specialized tables for Zora events to significantly improve query performance.

  ## x402 Updates

  * **Facilitator error status codes**: The CDP Facilitator had an update to which status codes it returns during errors. Failing to verify or settle will now return a 400 status code, when previously it returned 200.
  * **Facilitator billing enabled**: As of January 1st, billing is now enabled for the CDP Facilitator, with a free tier of 1,000 transactions per month, and \$0.001/transaction afterwards.
</Update>

<Update label="December 18, 2025">
  <Frame>
    <img />
  </Frame>

  ## Onramp

  * **Onramp webhook moved from beta to GA**: Onramp webhooks are now generally available for production use.

  ## Embedded Wallets

  * **Multi-Factor Authentication (MFA)**: You can enable your users to opt-in to added security by authenticating via an authenticator app, for example when logging in or performing sensitive operations like key export.
  * **Custom claims**: When using our Custom Auth feature, you can now pass additional custom claims – arbitrary user metadata you can then use for identity mapping, auth logic, and analytics.

  ## x402 Updates

  * **V2 protocol spec**: x402 V2 expands the protocol beyond single-call, exact payments. It adds wallet-based identity (skip repaying on every call), automatic API discovery, dynamic payment recipients, support for more chains and fiat via CAIP standards, and a fully modular SDK for custom networks and schemes.
</Update>

<Update label="December 10, 2025">
  <a href="https://docs.cdp.coinbase.com/embedded-wallets/wallet-pre-generation">
    <Frame>
      <img />
    </Frame>
  </a>

  ## Onramp

  * **Increased weekly transaction limits (Beta)**: Weekly transaction limits increased from \$500 to \$2,500 for guest checkout. Available to select partners.

  ## x402 Updates

  * **Facilitator pricing announcement**: As announced on 12/1, we will begin charging for our CDP x402 Facilitator on January 1st. [Details](https://x.com/CoinbaseDev/status/1995564027951665551).

  ## Embedded Wallets

  * **[Wallet pre-generation](https://docs.cdp.coinbase.com/embedded-wallets/wallet-pre-generation)**: You can now create wallets for your users before they ever log in to your app! This lets you add tokens (e.g. rewards, loyalty, incentives) and NFTs ahead of time, so your users log in and find something waiting for them.
  * **[Multiple accounts per user](https://docs.cdp.coinbase.com/embedded-wallets/multiple-accounts)**: You can have up to 30 separate accounts for each Embedded Wallet user – 10 each for EVM EOA, EVM smart accounts, and Solana accounts. This enables use cases like holding accounts for payment orchestration.
</Update>

<Update label="December 3, 2025">
  <Frame>
    <img />
  </Frame>

  ## Onramp

  * **[Apple Pay Web App Support](https://docs.cdp.coinbase.com/onramp/headless-onramp/apple-pay-onramp-api#web-app-requirements)**: Allow users to onramp via Apple Pay on any web browser. Schedule a [call](https://calendar.app.google/BLn6fzaz2aCZGvLu7) with our team to start implementing.
  * **[Webhooks (Beta)](https://docs.cdp.coinbase.com/onramp/webhooks)**: Get real-time transaction status updates made by your users.

  ## Wallets

  * **x402 payment hook**: Shipped [x402 payment hook](https://docs.cdp.coinbase.com/embedded-wallets/x402-payments) enabling embedded wallet users to consume any x402-powered API with 3 lines of code.
  * **Flexible wallet creation**: Shipped improvements that offer developers the flexibility to optionally create wallets at login or at a later time.

  ## x402

  * **Minimum transaction amount**: CDP Facilitator now enforces a minimum transaction amount of \$0.001 for all x402 payments.

  ## Data API

  * **Improved error messaging**: Error messages now differentiate between timeouts from long query and timeouts from backend issues (4xx vs. 5xx).
</Update>

<Update label="November 19, 2025">
  <Frame>
    <img />
  </Frame>

  ## Embedded Wallets

  * **Improvements to USDC reward payouts**: Our 3.85% USDC Rewards for Embedded and Server Wallets are now paid out weekly instead of monthly, and we've Expanded eligibility criteria, lowering the minimum required balance.
  * **Authentication method linking components**: Released React components making it seamless to link multiple authentication methods with your Embedded Wallets. Check out the feature at [demo.cdp.coinbase.com](https://demo.cdp.coinbase.com).
  * **Custom authentication**: Custom auth feature is live, enabling applications with existing authentication systems to integrate Embedded Wallets seamlessly.
  * **Secure private key export**: Secure React component is now live for managed private key-export flows within trusted Coinbase domains, ensuring maximum safety and isolation.
  * **x402 Support**: Added the `useX402` hook to automatically consume x402 resources.

  ## Data API

  * **Rate limiting bug fix**: Fixed bug where some users were seeing 429s (rate limiting) when they shouldn't. Users should now see more consistent rate limit behavior once 5 RPS is reached.
  * **Increased SQL API length**: SQL API now accepts queries up to 100k characters.

  ## x402

  * **Payments MCP bug fix**: Fixed a bug where the MCP server would occasionally double-stringify body params. Upgrade by running: `npx @coinbase/payments-mcp@latest install`.
</Update>

<Update label="November 12, 2025">
  <Frame>
    <video />
  </Frame>

  ## Data API

  * **Client-controlled caching**: New feature enables clients to control data freshness or caching preferences. Check out the demo above to see it in action.

  ## x402

  * **Expanded country support**: CDP x402 Facilitator is now available in 100+ countries.
</Update>

<Update label="November 5, 2025">
  <Frame>
    <img />
  </Frame>

  ## Wallets

  * **Sign in with X and authentication linking**: Launched support for Sign in with X on Embedded Wallets, plus authentication method linking that enables users to link multiple logins to the same user and wallet.
  * **Mobile support for Social login**: Google, Apple, and X social login support via React Native is now live.

  ## Data API

  * **Server-side caching**: Users running the same query frequently will now receive responses much faster.

  ## x402

  * **Payments MCP v1.0.5**: App will now automatically check for updates in the background.
</Update>

<Update label="October 29, 2025">
  <Frame>
    <img />
  </Frame>

  ## Wallets

  * **Multiple authentication methods**: Users can now link [multiple login methods](https://docs.cdp.coinbase.com/embedded-wallets/auth-method-linking) to a single embedded wallet account for flexible authentication options.
  * **Expanded SMS support**: Added [10 new countries](https://docs.cdp.coinbase.com/embedded-wallets/authentication-methods#sms-otp) to international SMS authentication coverage.

  ## Data API

  * **Improved query feedback**: Added query analysis upfront so users now receive immediate feedback when queries are too large, request too many rows, etc.
</Update>

<Update label="October 22, 2025">
  <Frame>
    <img />
  </Frame>

  ## x402

  * **Facilitator directory**: Added a new facilitator list on [x402.org](https://www.x402.org/) for easy discovery of available payment routing providers.

  ## Wallets

  * **Expanded authentication options**: Added Sign in with Apple support and enabled linking multiple social login providers to a single wallet for flexible authentication options.

  ## Data API

  * **Increased JOIN limit**: SQL API now supports up to 5 JOINs in queries, up from 3, enabling more complex multi-table queries.
  * **Improved SQL API stability**: Implemented query session controls including result row limits, memory usage protections, AST complexity checks, and timeout enforcement to prevent resource exhaustion and provide faster feedback when queries exceed limits.
  * **Enhanced error visibility**: Added status code metrics tagging to better track and debug project-specific errors, improving operational monitoring.
</Update>

<Update label="October 15, 2025">
  <Frame>
    <img />
  </Frame>

  ## Embedded Wallets

  * **General availability**: Embedded Wallets is now in GA! Integrate Coinbase's trusted crypto infrastructure directly into your app and offer users a self-custody wallet in seconds with just an email, SMS, or Google login. [Check it out](https://docs.cdp.coinbase.com/embedded-wallets/welcome)

  ## SQL API

  * **Enhanced error handling**: DB-side SQL errors now return detailed error messages and proper error codes instead of generic 500 responses, enabling developers to identify and self-correct query issues.
  * **HAVING clause support**: Added support for HAVING clauses in SQL queries, addressing user requests for advanced filtering capabilities.
  * **Log identification support**: Added `log_id` field to views, providing a reliable, onchain-derived unique identifier for event logs to ensure data uniqueness and improve developer experience.
</Update>

<Update label="October 8, 2025">
  <Frame>
    <img />
  </Frame>

  ## Wallets

  * **CDP Solana standard wallet support**: Released CDP Solana standard wallet support, enabling developers to use Embedded Wallet SDK with Solana's standard interface.

  ## x402

  * **x402 Specs**: x402 now supports Solana for all SPL tokens, enabling full interoperability across EVM and Solana networks.
  * **CDP x402 Facilitators**: CDP Facilitators have been upgraded to support Solana as a network option, allowing cross-chain payment routing and settlement between Solana and other supported chains.
</Update>

<Update label="October 1, 2025">
  <Frame>
    <img />
  </Frame>

  ## Wallets

  * **Solana support**: CDP Embedded Wallets now [supports Solana](https://docs.cdp.coinbase.com/embedded-wallets/welcome#supported-networks), including the ability to create and manage wallets on devnet and mainnet, web and mobile support, native Coinbase Onramp integration, sign & send APIs, and secure key export.
  * **Embedded Wallets demo builder**: The demo builder is live at [demo.cdp.coinbase.com](https://demo.cdp.coinbase.com).
</Update>

<Update label="September 24, 2025">
  <Frame>
    <img />
  </Frame>

  ## Wallets

  * **React Native demo app**: The [demo application](https://github.com/coinbase/cdp-wallet-demo-apps/tree/main/apps/react-native-expo) is the
    easiest way to start building with Embedded Wallets.
  * **Usage metrics in CDP Portal**: View your project’s Embedded Wallets usage anytime via the CDP Portal.

  ## Data API

  * **SQL API (Alpha) proxy event logs**: Now supports event logs generated through proxy smart contracts on Base and Base Sepolia, including EIP-1967, EIP-1822, and EIP-897, expanding compatibility with complex contract architectures.

  ## x402

  * **Roadmap on GitHub**: Outlines future development plans and upcoming features for the open payment standard.
</Update>

<Update label="September 17, 2025">
  <Frame>
    <img alt="x402 and Google AP2" />
  </Frame>

  ## Google AP2 + x402 Demo

  * Agents can already talk to each other. And now, with x402 within Google’s new AP2, they can pay each other too. Stablecoins make this possible at the speed of code, unlocking micropayments and new models of automation that legacy rails simply can’t support. [Learn more](https://www.coinbase.com/developer-platform/discover/launches/google_x402).

  ## x402 Bazaar

  * **AI Agent Discover Layer**: x402 Bazaar is the first discovery layer for agentic commerce. It gives agents a single place to find, interact with, and pay for new services - unlocking dynamic, self-improving agents that can evolve as the ecosystem grows. [Learn more](https://www.coinbase.com/developer-platform/discover/launches/x402-bazaar).

  ## Onramp

  * **Txn Hash Performance Improvements**: We now provide transaction hashes to API customers as soon as the send starts, enabling faster transaction tracking and empowering developers to define their own confirmation logic. This improvement reduces transaction hash availability time by \~50% on Base and \~61% on Solana, enhancing flexibility and user experience.

  ## Data API

  * **Base Testnet Support**: SQL API (Alpha) now supports Base Sepolia, enabling developers to query testnet data for integration testing.

  ## Server Wallets

  * **OpenZeppelin Relayer Support**: Server Wallets is a supported signer on OpenZeppelin relayer for EVM and Solana, enabling all OpenZeppelin Relayer users to securely sign transactions via CDP.
</Update>

<Update label="September 10, 2025">
  ## Embedded Wallets

  * **React Native support**: Developers can now easily integrate CDP Embedded Wallets into their mobile apps! Check out the [quickstart](https://docs.cdp.coinbase.com/embedded-wallets/react-native/quickstart).
  * **Onramp integration**: CDP Embedded Wallets now support seamless integration with Coinbase Onramp, making it easy for users to add funds to their wallets. The new Fund component enables developers to quickly add this feature to their apps.

  ## CDP Security Suite Wallet Policies

  * **New Solana policies**: Added support for three new Solana policies. [Learn more](/server-wallets/v2/using-the-wallet-api/policies/solana-idl-policies):
    * `programId` for allowlisting programs
    * `solNetwork` for limiting transaction sends to mainnet or devnet
    * `solMessage` for regex matching when signing solana messages
  * **USD-based limits**: netUSDChange policy criteria support has been added for send and prepare user operation, enabling developers to restrict the total amount of USD spend and exposure per transaction for Server Wallet EVM smart accounts and EOAs

  ## Data API Updates

  Data API now provides improved parameter formatting and enhanced type handling for better developer experience.

  * **Breaking change – Clean parameter formatting**: API `parameters` responses now return plain values instead of type-annotated strings, making data cleaner, easier to read, and simpler to work with.
  * **Smarter type handling**: Large numbers (≥64-bit) are returned as strings to prevent precision loss, while smaller ones stay as JSON numbers.
  * **Simplified map field access**: Map fields like `parameters['from']` now work without explicit type casting. Example: `parameters['from']::String` is no longer needed. The type is inferred from `parameters['from']` alone.
  * **Reliability and consistency improvements**: Fixed bugs to ensure accurate column names in complex queries and improved error messages for smoother debugging.
</Update>

<Update label="August 27, 2025">
  ## Embedded Wallets - New Features

  <Frame>
    <img alt="Embedded Wallets Smart Accounts" />
  </Frame>

  * **Smart Accounts (ERC-4337) Support**: One of our most requested features is here! [Smart Accounts](https://docs.cdp.coinbase.com/embedded-wallets/smart-accounts) enable account abstraction features like batched actions in a single transaction and gas sponsorship via CDP [Paymaster](https://docs.cdp.coinbase.com/paymaster/introduction/welcome#welcome-to-paymaster). [Learn more](https://docs.cdp.coinbase.com/embedded-wallets/smart-accounts).
  * **Native Onramps**: Use the Coinbase Onramp widget seamlessly in your onchain app alongside CDP Embedded Wallets. [Learn more](https://docs.cdp.coinbase.com/onramp/introduction/welcome).

  ## Server Wallets

  * **Solana IDL Policies**: [CDP Security Suite](https://docs.cdp.coinbase.com/api-reference/v2/rest-api/policy-engine/policy-engine) now supports advanced validation of Solana transaction instruction data using Interface Definition Language (IDL) helping you protect your server wallets by locking down the programs it can interact with. [Learn more](https://docs.cdp.coinbase.com/server-wallets/v2/using-the-wallet-api/policies/solana-idl-policies).

  ## Onramp

  * **Webhooks for Onramp**:  Existing Onramp customers can now add in [Webhooks](https://docs.cdp.coinbase.com/webhooks/overview) (now in Beta) to automate user interactions and notifications! Want to get early access? [Contact us](https://support.cdp.coinbase.com/onramp-onboarding).

  ## StableLink - New Payments App

  <Frame>
    <img alt="StableLink Payments App" />
  </Frame>

  * **Seamless onchain payment links**: [StableLink](https://www.stablelink.xyz/?ref=changelog) is an open sourced SaaS template to make a Stripe Link equivalent on crypto rails using CDP's [Embedded Wallets](https://www.coinbase.com/developer-platform/products/embeddedwallets) and [Onramp SDK](https://www.coinbase.com/developer-platform/products/onramp). With StableLink, payments are instant, global, and fee-free. StableLink runs on stablecoins, but users just log in with email & pay by card or Apple Pay. [Check out the demo](https://x.com/Must_be_Ash/status/1958178314331324909).
</Update>

<Update label="August 20, 2025">
  ## Embedded Wallets

  * **Paymaster for Smart Accounts**: [Embedded wallets](/embedded-wallets/welcome) users can now easily sponsor gas to create seamless (and gasless) user experiences using CDP’s Paymaster. [Learn more](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core#smart-account-operations).

    <Frame>
      <img alt="EW Paymaster Code Snippet" />
    </Frame>

  ## Server Wallets

  * **Send Transaction API on Solana**: This feature supports batched transactions and [automatic priority fees](/server-wallets/v2/solana-features/sending-transactions#optimizing-transaction-sends) for faster inclusion in the next block.

    <Frame>
      <img alt="Server Wallets Solana Sends" />
    </Frame>

  ## Data API

  * **SQL Playground now live**: We shipped the SQL Playground in the CDP portal to help devs build and run SQL queries for decoded Base data before integrating with their codebase. [Try it out](https://portal.cdp.coinbase.com/products/data/playground)

    <Frame>
      <img alt="Data API SQL Playground" />
    </Frame>

  ## Community

  * **ETH Global NYC**: We were at ETH Global NYC and gave away \$20K in prizes to some super cool uses of CDP products. [Check out the winners](https://x.com/CoinbaseDev/status/1957488967814971557).

    <Frame>
      <img alt="ETH Global NYC Winners" />
    </Frame>
</Update>

<Update label="August 13, 2025">
  ## Embedded Wallets: Authentication Updates

  * **Mobile SMS Auth** [Launch](/embedded-wallets/authentication-methods#sms-otp): Enable builders to provide simple sign-in experiences using one-time codes via SMS for authentication.
  * **Server-side auth validation** [Launch](/embedded-wallets/implementation-guide#server-side-validation): You can now get and verify access tokens, enabling use of embedded wallet JWT tokens for backend authentication.

  ## Data API: Launches

  * **SQL API Alpha** [Launch](/data/sql-api/welcome): New SQL query endpoint that enables developers to pull real-time and historical decoded logs from the Base blockchain. You can query any arbitrary event signature from any verified Base smart contract with sub-second latency from tip of chain.
  * **Base Token Balances API**: Token balances on Base are getting a performance upgrade. Pull balances from any address with sub-500ms latency (10x improvement) and sub-second freshness end-to-end.

  ## Server Wallets: New Features

  * **[Spend Permissions](/wallet-api/v2/evm-features/spend-permissions#spend-permissions)**: Enable EVM server wallets with smart accounts to delegate spend authorization within pre-set constraints (e.g., a set amount per time period) to other accounts.
  * **[USD-based Wallet Policies](https://x.com/CoinbaseDev/status/1955668537676370129)**: Set max transaction amounts in dollar terms, rather than expressed in native token amounts (e.g. deny transactions above \$XX).
  * **Expanded SOL support**: [Wallet policy support](/wallet-api/v2/using-the-wallet-api/policies/overview) on Solana, with address allowlisting and token values on SOL and SPL token transfers.

  ## Onramp Onboarding: Update

  * **Existing and new customers** are now required to complete lightweight developer onboarding within the [CDP Portal](https://portal.cdp.coinbase.com/) to get full access to [Coinbase Onramp & Offramp](/onramp/introduction/welcome). Developers can complete this on their Developer Portal (Payments > Onramp & Offramp > Apply)

  ## Community Updates

  * **Code:NYC Hackathon**: We had 93 builders come out to hack with us in Brooklyn, NY last weekend. Check out a [recap](https://x.com/CoinbaseDev/status/1954738735909572893).
  * **ETH Global NYC**: We're still in NYC and builders can apply for the [CDP track](https://ethglobal.com/events/newyork2025/prizes/coinbase-developer-platform) of the ETH Global NYC Hackathon.
</Update>

<Update label="August 6, 2025">
  <Frame>
    <img alt="EW Blog Header img" />
  </Frame>

  ## Embedded Wallets: Beta Launch

  CDP's new [Embedded Wallets](https://www.coinbase.com/developer-platform/products/embeddedwallets?utm_source=docs\&utm_campaign=changelog) product is now in beta. It gives builders (and users) simple wallet management without passkeys or seed phrases, and has onramps, trading, and 4.1% USDC rewards built-in using CDP's unified set of APIs. [Try it out](https://portal.cdp.coinbase.com/products/embedded-wallets).

  ## CDP Server Wallets: Network Expansion

  * **Server Wallets now supports [Solana sends](/wallet-api/v2/solana-features/sending-transactions)**: sign & broadcast in one call with sub-200ms latency, 250 TPS throughput, and batching.
  * **[Smart Accounts](/wallet-api/v2/evm-features/smart-accounts)** now support a broader range of EVM networks including Ethereum mainnet, Base, Arbitrum, Optimism, Zora, Polygon, BNB, and Avalanche
  * **[EVM send API](/wallet-api/v2/evm-features/sending-transactions)** supports Arbitrum, Polygon, Optimism, Avalanche in addition to Base and Ethereum Mainnet now.

  ## CDP Security Suite: Policy Engine Demos

  Since launching [Server Wallets](https://www.coinbase.com/developer-platform/products/wallets?utm_source=docs\&utm_campaign=changelog) a few weeks ago, we've gotten a ton of interest and questions about one of its core features: Policy Engine. The team put together some quick demos to show you how to easily [set limits on USDC transfers](https://youtube.com/shorts/s2Pn3r8YqLc), block scams with [approve/deny wallet lists](https://youtube.com/shorts/EJPUZsVQlF0), and even create [multi-rule setups](https://youtube.com/shorts/19KFQOFTOvE) and advanced transaction flows.

  ## Onramp API: Apple Pay Integration Guide

  Apple Pay Onramp [integration guide](/onramp/headless-onramp/overview) is now available in the docs. Apple Pay is one of the most frictionless onboarding experiences for buying crypto and even helped Moonshot [increase conversion by 25%](https://www.coinbase.com/developer-platform/discover/case-studies/moonshot?utm_source=docs\&utm_campaign=changelog).

  ## Onramp/Offramp: Session Token Upgrade

  Effective 7/31/2025, all Coinbase Onramp & Offramp URLs must be securely initialized using the `sessionToken` parameter. This migration is mandatory for continued access to Coinbase Onramp and Offramp APIs.
</Update>

