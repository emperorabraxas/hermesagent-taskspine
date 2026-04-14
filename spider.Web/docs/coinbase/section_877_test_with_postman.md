# Test with Postman
Source: https://docs.cdp.coinbase.com/coinbase-business/invoicing-api/postman-files



The following Postman collection file is available for download.

* <a href="/coinbase-business/invoicing-api/files/invoicing.postman_collection.json">Coinbase Business Invoicing Collection</a>
* <a href="/coinbase-business/api-architecture/files/coinbase_developer_platform.postman_environment.json">Coinbase Developer Platform Postman Environment</a>

This collection includes example payloads and automatic JWT token generation for authenticated requests.

## Prerequisites

Before using this collection, ensure you have:

* Coinbase Business account
* [CDP API key](/coinbase-business/introduction/get-started#creating-api-keys) using **ECDSA** signature algorithm
* Downloaded the following files (we will use these to setup Postman):
  * **<a href="/coinbase-business/invoicing-api/files/invoicing.postman_collection.json">Invoicing collection</a>**: Pre-configured API requests for listing and retrieving invoices
  * **<a href="/coinbase-business/api-architecture/files/coinbase_developer_platform.postman_environment.json">Environment configuration</a>**: Authentication setup and variables for CDP API access

<Info>
  **Recommended**: Use ECDSA keys for reliable testing with this Postman collection. While the Invoicing API itself supports both ECDSA and Ed25519 keys, ECDSA provides the most consistent experience in Postman.
</Info>

<Info>
  The Invoicing APIs use the same authentication environment as other Coinbase Business APIs. You can reuse the Coinbase Developer Platform environment file.
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

    Select both JSON files you downloaded and import them into your Postman workspace.
  </Step>
</Steps>

## 2. Configure your environment

Set up authentication by adding your CDP API key details to Postman.

<Steps>
  <Step title="Add your API credentials">
    In the left sidebar, click on **Environments**. Select the **Coinbase Developer Platform Postman Environment** option to see your environment variables.

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
    Navigate to the **Collections** tab in Postman and expand the "Coinbase Business Invoicing Collection" we added earlier.

    From the **Environment** dropdown in the upper-right corner, select the **Coinbase Developer Platform Postman Environment** we just configured.
  </Step>

  <Step title="Send your first request">
    Start with the **List Invoices** request and click the **Send** button.

    You should receive a response similar to the following:

    ```console theme={null}
    {
        "invoices": []
    }
    ```
  </Step>

  <Step title="Get a specific invoice">
    1. Select the **Get Invoice** request
    2. Update the `:invoiceUuid` path variable with a valid invoice UUID
    3. Click **Send**
    4. Review the invoice details in the response
  </Step>
</Steps>

## Available endpoints

The Invoicing collection includes the following endpoints:

* **List Invoices** - Retrieves a paginated list of invoices with optional filtering by status, contact email, and sorting options
* **Get Invoice** - Retrieves details of a specific invoice by UUID

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

* [Invoicing API Reference](/coinbase-business/invoicing-api/api-reference) - Detailed API documentation with all request/response schemas
* [Authentication Guide](/coinbase-business/authentication-authorization/api-key-authentication) - Learn more about CDP API key authentication
* [Getting Started Guide](/coinbase-business/introduction/get-started) - Set up your Coinbase Business account and create API keys

