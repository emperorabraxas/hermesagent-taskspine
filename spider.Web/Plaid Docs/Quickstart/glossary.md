Glossary 
=========

#### A glossary of Plaid terminology 

#### Tokens, identifiers, and keys 

Plaid tokens are in the format `[type]-[environment]-[uuid]`, where the type may be `public`, `access`, `link`, or `asset-report`, and the environment may be `sandbox`, `development`, or `production`; a token will only ever be valid within the environment it was created. The UUID is a 32 character hexadecimal string in the pattern of 8-4-4-4-12 characters and conforms to the [RFC 4122 standard](https://tools.ietf.org/html/rfc4122) .

##### Access token 

An `access_token` is a token that can be used to make API requests related to a specific Item. You will typically obtain an `access_token` by calling [/item/public\_token/exchange](https://plaid.com/docs/api/items/index.html.md#itempublic_tokenexchange) . For more details, see the [Token exchange flow](https://plaid.com/docs/api/items/index.html.md#token-exchange-flow) . An `access_token` does not expire, although it may require updating, such as when a user changes their password, or if the end user is required to renew their consent on the Item. For more information, see [When to use update mode](https://plaid.com/docs/link/update-mode/index.html.md#when-to-use-update-mode) .

Access tokens should always be stored securely, and associated with the user whose data they represent. For more details on safely storing access tokens, see the [Open Finance Data Security Standard](https://ofdss.org/#documents) . An `access_token` can only be used to make a request if a Plaid API [client id](https://plaid.com/docs/quickstart/glossary/index.html.md#client-id) and [secret](https://plaid.com/docs/quickstart/glossary/index.html.md#secret) are also provided, and cannot be used on its own. If compromised, an `access_token` can be rotated via [/item/access\_token/invalidate](https://plaid.com/docs/api/items/index.html.md#itemaccess_tokeninvalidate) . If no longer needed, it can be revoked via [/item/remove](https://plaid.com/docs/api/items/index.html.md#itemremove) .

##### Asset report token 

An `asset_report_token` is a token used to make API requests related to a specific Asset Report. You will obtain an `asset_report_token` by calling [/asset\_report/create](https://plaid.com/docs/api/products/assets/index.html.md#asset_reportcreate) . An `asset_report_token` does not expire, and should always be stored securely, and should be associated in your database with the user whose data it represents. If compromised or no longer needed, an `asset_report_token` can be revoked via [/asset\_report/remove](https://plaid.com/docs/api/products/assets/index.html.md#asset_reportremove) .

##### Client ID 

Your `client_id` is an identifier required by the Plaid API. It must be provided for almost all API calls. Your client ID can be found on the [Dashboard](https://dashboard.plaid.com/developers/keys) . Your client ID uniquely identifies your team and will be the same for all API calls made on behalf of your organization, regardless of the API environment or the specific individual using the API.

##### Item ID 

An `item_id` uniquely identifies a Plaid [Item](https://plaid.com/docs/quickstart/glossary/index.html.md#item) . The `item_id` is part of the response for API endpoints that operate on a specific Item, including most product endpoints, as well as [/item/get](https://plaid.com/docs/api/items/index.html.md#itemget) and [/item/public\_token/exchange](https://plaid.com/docs/api/items/index.html.md#itempublic_tokenexchange) .

##### Link token 

A `link_token` is a token used to initialize Link, and must be provided any time you are presenting your user with the Link interface. You can obtain a Link token by calling [/link/token/create](https://plaid.com/docs/api/link/index.html.md#linktokencreate) . For more details, see the [Token exchange flow](https://plaid.com/docs/api/items/index.html.md#token-exchange-flow) . A `link_token` expires after 4 hours (or after 30 minutes, when being used with update mode), except when using [Hosted Link](https://plaid.com/docs/link/hosted-link/index.html.md) , which allows customizing the `link_token` lifetime, or when used with Identity Verification, in which case it does not expire.

##### Link session ID 

The `link_session_id` is a unique ID included in all Link callbacks. For faster issue resolution, the `link_session_id` should be included when contacting Support regarding a specific Link session.

##### Processor token 

A `processor_token` is a token used by a Plaid partner to make API calls on your behalf. You can obtain a `processor_token` by calling [/processor/token/create](https://plaid.com/docs/api/processors/index.html.md#processortokencreate) or [/processor/stripe/bank\_account\_token/create](https://plaid.com/docs/api/processors/index.html.md#processorstripebank_account_tokencreate) and providing an `access_token`. The `processor_token` does not expire. Once successfully passed to the processor, it can be either deleted from your database, or retained to manage the processor's permissions and access via [/processor/token/permissions/set](https://plaid.com/docs/api/processors/index.html.md#processortokenpermissionsset) . You should always retain the `access_token`, since it will be needed to activate [update mode](https://plaid.com/docs/link/update-mode/index.html.md) for the underlying Item.

##### Public token 

A `public_token` is a token obtained after Link, typically from the `onSuccess` callback. This token can be exchanged for an `access_token` by calling [/item/public\_token/exchange](https://plaid.com/docs/api/items/index.html.md#itempublic_tokenexchange) . For more details, see the [Token exchange flow](https://plaid.com/docs/api/items/index.html.md#token-exchange-flow) . A `public_token` expires after 30 minutes. If using the [Hosted Link](https://plaid.com/docs/link/hosted-link/index.html.md) flow or [Multi-Item Link](https://plaid.com/docs/link/multi-item-link/index.html.md) flow, the public token is instead obtained from the [/link/token/get](https://plaid.com/docs/api/link/index.html.md#linktokenget) endpoint, the `SESSION_FINISHED` webhook, or the `ITEM_ADD_RESULT` webhook.

##### Request ID 

A `request_id` is a unique ID returned as part of the response body for every Plaid API response (except for API endpoints that return binary data, in which case the `request_id` will be found in the header). The `request_id` can be used to look up the request on the [Activity Log](https://dashboard.plaid.com/activity/logs) and should be included when contacting Support regarding a specific API call.

##### Secret 

Your secret is used to authenticate calls to the Plaid API. Secrets can be found on the [dashboard](https://dashboard.plaid.com/developers/keys) . Your secret should be kept secret and rotated if it is ever compromised. For more information, see [rotating keys](https://plaid.com/docs/account/security/index.html.md#rotating-keys) .

##### User id 

A Plaid `user_id`, or User, is a representation of a single end user of your application within Plaid’s systems that can be shared across multiple products, such as Plaid Check and Protect. Each User is represented by a unique `user_id`, which you can use to make API calls for that User. When you initialize a Link Token with a `user_id`, each Item successfully linked in the Link session will be associated with the corresponding User.

The `user_id` replaces the legacy `user_token` and is the preferred representation of a user in all Plaid contexts except for the Plaid Inc. (non-CRA) Income Verification product.

##### User token 

Note: While the Plaid `user_token` is still supported and there are no plans to discontinue support for it, the `user_id` must be used instead of the `user_token` by all new Plaid integrations, except those using the Plaid Inc. (non-CRA) Income Verification product.

A `user_token` is used when working with Plaid's Income or Employment APIs, with Plaid Check, or with the Multi-Item Link flow. It is used to associate data from multiple sources with a single user and must be provided when initializing [/link/token/create](https://plaid.com/docs/api/link/index.html.md#linktokencreate) for these flows. A `user_token` is created by calling [/user/create](https://plaid.com/docs/api/users/index.html.md#usercreate) and does not expire. Ensure that you store the `user_token` along with your user's identifier in your database, as it is not possible to retrieve a previously created `user_token`.

#### Environments 

To use Link with bank data in Production or Limited Production in the US or Canada, all customers who created accounts after October 31, 2024 must [select a use case description](https://dashboard.plaid.com/link/data-transparency-v5) from the Link Customization section of the Dashboard.

##### Production 

Production ([https://production.plaid.com](https://production.plaid.com) ) is one of two Plaid environments on which you can run your code, along with Sandbox. Unlike Sandbox, Production uses real data.

##### Limited Production 

Limited Production is a restricted mode of the Production ([https://production.plaid.com](https://production.plaid.com) ) environment. In Limited Production, you can make free API calls using real-world data for testing purposes, but the number of API calls you can make and the number of Items you can create is capped, and you cannot connect to certain large institutions that use OAuth, like Bank of America, Chase, or Wells Fargo. To remove these limitations, apply for full Production access and complete the OAuth registration form. You will still be able to use your remaining free API calls in full Production before being billed. For more details on Limited Production, see [Testing with live data using Limited Production](https://plaid.com/docs/sandbox/index.html.md#testing-with-live-data-using-limited-production) .

The following products are supported in Limited Production: Assets, Auth, Balance, Identity (including Identity Match), Income, Investments, Liabilities, Payment Initiation, Transactions (including Transactions Refresh and Recurring Transactions), and Enrich.

##### Sandbox 

The Sandbox ([https://sandbox.plaid.com](https://sandbox.plaid.com) ) is one of two Plaid environments on which you can run your code, along with Production. Sandbox is a free test environment in which no real data can be used. The Sandbox environment also offers a number of special Sandbox-only capabilities to make testing easier. For more information, see [Sandbox](https://plaid.com/docs/sandbox/index.html.md) .

##### Development 

Development ([https://development.plaid.com](https://development.plaid.com) ) was a Plaid environment on which you could run your code, along with Sandbox and Production. To simplify the development process, Plaid replaced the Development environment with the ability to test with real data for free directly in Production. On June 20, 2024, the Plaid Development environment was decommissioned, and all Development Items were removed.

#### Other Plaid terminology 

##### Account 

An account is a single account held by a user at a financial institution; for example, a specific checking account or savings account. A user may have more than one account at a given institution; the overall object that contains all of these accounts is the Item. Each account is uniquely identified by an `account_id`, which will not change, unless Plaid is unable to reconcile the account with the data returned by the financial institution; for more information, see [INVALID\_ACCOUNT\_ID](https://plaid.com/docs/errors/invalid-input/index.html.md#invalid_account_id) .

Plaid will automatically detect when an account is closed, and will no longer return the `account_id` for a closed account. If an `access_token` is deleted, and the same credentials that were used to generate that `access_token` are used to generate a new `access_token` on a later date, the new `account_id` will be different from the `account_id` associated with the original `access_token`.

##### Dashboard 

The Plaid Dashboard is used to manage your Plaid developer account, configure your account for OAuth, and to obtain keys and secrets. The Dashboard also contains a number of useful features, including troubleshooting tools, activity and usage logs, billing data, details and status for supported institutions, and the ability to request additional products or environments or to submit a support ticket. It can be found at [dashboard.plaid.com](https://dashboard.plaid.com) . For more information, see [Your Plaid developer account](https://plaid.com/docs/account/index.html.md) .

##### Item 

An Item represents a login at a financial institution. A single end-user of your application might have accounts at different financial institutions, which means they would have multiple different Items. An Item is not the same as a financial institution account, although every account will be associated with an Item. For example, if a user has one login at their bank that allows them to access both their checking account and their savings account, a single Item would be associated with both of those accounts. Each Item linked within your application will have a corresponding `access_token`, which is a token that you can use to make API requests related to that specific Item.

Two Items created for the same set of credentials at the same institution will be considered different and not share the same `item_id`.

##### Link 

Link is Plaid's client-side, user-facing UI that allows end users to connect their financial institution account to your application. For more information, see [Link](https://plaid.com/docs/link/index.html.md) .

##### Plaid Consumer Reporting Agency 

Plaid Consumer Reporting Agency, also known as Plaid CRA or Plaid Check, is focused on building solutions for customers who want ready-made credit risk insights from consumer-permissioned cash flow data. Plaid Check is a Consumer Reporting Agency as defined by the Fair Credit Reporting Act (FCRA), allowing it to provide enhanced insights not available from Plaid Inc. products. For more information, see [Plaid Check](https://plaid.com/docs/check/index.html.md) . Plaid's other products described in the docs, including Assets, Statements, and Income, are provided by Plaid Inc., which is not a consumer reporting agency.