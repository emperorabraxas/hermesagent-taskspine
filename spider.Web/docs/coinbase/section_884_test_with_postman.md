# Test with Postman
Source: https://docs.cdp.coinbase.com/coinbase-business/payment-link-apis/postman-files



The following Postman collection file is available for download.

* <a href="/coinbase-business/payment-link-apis/files/payment_links.postman_collection.json">Coinbase Business Payment Links Collection</a>
* <a href="/coinbase-business/api-architecture/files/coinbase_developer_platform.postman_environment.json">Coinbase Developer Platform Postman Environment</a>

This collection includes example payloads and automatic JWT token generation for authenticated requests.

## Prerequisites

Before using this collection, ensure you have:

* Coinbase Business account
* [CDP API key](/coinbase-business/introduction/get-started#creating-api-keys) using **ECDSA** signature algorithm
* Downloaded the following files (we will use these to setup Postman):
  * **<a href="/coinbase-business/payment-link-apis/files/payment_links.postman_collection.json">Payment Links collection</a>**: Pre-configured API requests for creating, listing, and managing payment links
  * **<a href="/coinbase-business/api-architecture/files/coinbase_developer_platform.postman_environment.json">Environment configuration</a>**: Authentication setup and variables for CDP API access

<Info>
  **Recommended**: Use ECDSA keys for reliable testing with this Postman collection. While the Payment Link API itself supports both ECDSA and Ed25519 keys, ECDSA provides the most consistent experience in Postman.
</Info>

<Info>
  The Payment Link APIs use the same authentication environment as other Coinbase Business APIs. You can reuse the Coinbase Developer Platform environment file.
</Info>

## 1. Setup Postman

<Steps>
  <Step title="Access Postman">
    Use [Postman Web](https://www.postman.com/) to sign in (no installation needed).

    <Tip>Download from [Postman Downloads](https://www.postman.com/downloads/) if you prefer a native app</Tip>.
  </Step>

  <Step title="Import files">
    Once you are logged into Postman, you can import the files into your workspace through the web interface.

    Under "Get Started", click on **Import APIs and collections**.

    <Note>If you already have a Postman workspace, you can select **Import** in the upper-left corner of the screen.</Note>

    <Frame>
      <img alt="Postman import screen showing Import APIs and collections option" />
    </Frame>

    Select both JSON files you downloaded and import them into your Postman workspace.
  </Step>
</Steps>

## 2. Configure your environment

Set up authentication by adding your CDP API key details to Postman.

<Steps>
  <Step title="Add your API credentials">
    In the left sidebar, click on **Environments**. Select the **Coinbase Developer Platform Postman Environment** option to see your environment variables.

    <Frame>
      <img alt="Postman environment screen showing Coinbase Developer Platform Postman Environment in left sidebar" />
    </Frame>

    Add these two variables exactly as shown:

    | Variable     | Value                                | Where to find it                                         |
    | ------------ | ------------------------------------ | -------------------------------------------------------- |
    | `name`       | Your full API key name (with quotes) | From the JSON file downloaded when creating your API key |
    | `privateKey` | Your ECDSA private key (with quotes) | From the JSON file downloaded when creating your API key |

    <Accordion title="Example values">
      **Example environment variable values:**

      ```
      name: "organizations/12345678-1234-5678-1234-567812345678/apiKeys/abcdef12-3456-7890-abcd-ef1234567890"

      privateKey: "-----BEGIN EC PRIVATE KEY-----\nMHcCAQEEIJ8VsC2ifqfxDpq7mnVWdBKnqIRjFFg0zcC9U4RgKHQqoAoGCCqGSM49\nAwEHoUQDQgAEX7M5LCPd6rkeUxIK3/B9+2+3RQFvkEfMU4iN1ABm5VNUqNmRnJv4\nCxcdPIKreo4xuNr2S8Y5SU6IELb8HGc8Ow==\n-----END EC PRIVATE KEY-----\n"
      ```

      **Important:**

      * Include the quotes as part of the value
      * Keep the privateKey on one line with `\n` for line breaks
      * Use an ECDSA key (starts with `-----BEGIN EC PRIVATE KEY-----`)
    </Accordion>
  </Step>
</Steps>

## 3. Authenticate and test endpoints

The Postman collection automatically generates a JWT token before each request using your environment variables.

<Steps>
  <Step title="Prep the collection">
    Navigate to the **Collections** tab in Postman and expand the "Coinbase Business Payment Links Collection" we added earlier.

    From the **Environment** dropdown in the upper-right corner, select the **Coinbase Developer Platform Postman Environment** we just configured.

    <Frame>
      <img alt="Postman request screen showing Coinbase Developer Platform Postman Environment" />
    </Frame>
  </Step>

  <Step title="Send your first request">
    Start with the **List Payment Links** request and click the **Send** button.

    You should receive a response similar to the following:

    ```console theme={null}
    {
        "paymentLinks": []
    }
    ```
  </Step>

  <Step title="Create a payment link">
    1. Select the **Create Payment Link** request
    2. Review the pre-filled request body (you can modify amounts, description, etc.)
    3. Click **Send**
    4. Copy the `url` from the response - this is your payment link!
  </Step>
</Steps>

## Available endpoints

The Payment Links collection includes the following endpoints:

* **Create Payment Link** - Creates a new payment link for accepting cryptocurrency payments
* **List Payment Links** - Retrieves a paginated list of payment links with optional filtering
* **Get Payment Link** - Retrieves details of a specific payment link by ID
* **Deactivate Payment Link** - Deactivates a payment link to prevent further payments

## Troubleshooting

<Warning>
  **Confirm Environment**

  Make sure the correct environment is selected by checking the check mark to the right of the environment name in Postman.
</Warning>

### Common issues and solutions

| Issue                                | Solution                                                       |
| ------------------------------------ | -------------------------------------------------------------- |
| Using Ed25519 key instead of ECDSA   | Use ECDSA key - starts with `-----BEGIN EC PRIVATE KEY-----`   |
| Missing quotes in environment values | Include quotes around `name` and `privateKey` values           |
| Invalid JSON                         | Check the environment dropdown is set to your CDP environment  |
| 401 Unauthorized errors              | Check JWT generation in Postman Console and verify credentials |

### Need additional help?

* **Documentation**: Review the [Authentication Guide](/coinbase-business/authentication-authorization/api-key-authentication)
* **Community**: Join the [CDP Discord](https://discord.com/invite/cdp) for support
* **Support**: Contact Coinbase Business support with your `X-Request-Id` from failed requests

## What to read next

* [Payment Link API Reference](/api-reference/business-api/rest-api/payment-links) - Detailed API documentation with all request/response schemas
* [Authentication Guide](/coinbase-business/authentication-authorization/api-key-authentication) - Learn more about CDP API key authentication
* [Getting Started Guide](/coinbase-business/introduction/get-started) - Set up your Coinbase Business account and create API keys
* [Migrate from Commerce](/coinbase-business/payment-link-apis/migrate/overview) - If you're moving from the Commerce Charge API

