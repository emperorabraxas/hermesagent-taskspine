# Postman Files
Source: https://docs.cdp.coinbase.com/get-started/tools/postman-files



The following Postman collection and environment files are available for download.

* <a href="/get-started/downloads/coinbase_developer_platform.postman_environment.json">Coinbase Developer Platform Postman Environment</a> (Required for all Collections)
* <a href="/get-started/downloads/coinbase_advanced_trading.postman_collection.json">Coinbase Advanced Trade Postman Collection</a>
* <a href="/get-started/downloads/coinbase_app.postman_collection.json">Coinbase App Postman Collection</a>
* <a href="/get-started/downloads/cdp_sdk_collection.postman_collection.json">CDP SDK Collection</a>

## Coinbase Developer Platform Collection

### Step 1: Download Postman

If don't have Postman installed, download and install [Postman](https://www.postman.com/downloads/) from their website.

### Step 2: Download and Import Files

1. **Download Collection:**
   * Download the relevant collection from above

2. **Import Collection into Postman:**
   * Open Postman.
   * Click on **Import** in the upper left corner.
   <Frame>
     <img />
   </Frame>
   * Select the downloaded JSON file and import it.

### Step 3: Configure Environment Variables

Once the files are imported, you need to configure your environment variables.

1. **Download Postman Environment:**
   * <a href="/get-started/downloads/coinbase_developer_platform.postman_environment.json">Coinbase Developer Platform Postman Environment</a>

2. **Import Environment into Postman:**
   * Open Postman.
   * Click on the same **Import** button in the upper left corner.
   * Select the downloaded JSON file and import it.

3. **Select the Environment:**

   * In Postman, click on the environment dropdown near the top right of the screen and select "Coinbase Developer Platform Postman Environment".

   <Frame>
     <img />
   </Frame>

   * Or by using the **Environments** tab on the left bar - Make sure the correct environment is selected by checking the check mark to the
     right of the environment name in Postman.

   <Frame>
     <img />
   </Frame>

4. **Set Up Variables:**

   * Click the Environments tab under My Workspace on the left of the screen
   * Select the "Coinbase Developer Platform Postman Environment".
   * Configure the following variables: <br /><br />

   | Variable     | Current value                                                                             |
   | :----------- | :---------------------------------------------------------------------------------------- |
   | `name`       | `"organizations/{ORG_ID}/apiKeys/{KEY_ID}"` (Include quotes)                              |
   | `privateKey` | `"-----BEGIN EC PRIVATE KEY-----\{KEY}\n-----END EC PRIVATE KEY-----\n"` (Include quotes) |

   <Info>
     Ensure that the values are entered exactly as shown, including the quotes.
   </Info>

### Step 4: Authenticate and Test Endpoints

1. **Send Requests:**
   * Navigate to the "Collections" tab in Postman.
   * Expand the "Coinbase Developer Platform Postman Collection".
   * Select any request and click **Send** to test the endpoint.

2. **Check Responses:**
   * Ensure that the responses are as expected.
   * If you encounter any issues, refer to the detailed response messages to understand the problem.

### Important Notes

<Warning> Confirm Environment
Make sure the correct environment is selected by checking the check mark to the right of the environment name in Postman. </Warning>

<Info>If you run into any issues, please reach out to us in the [CDP Discord](https://discord.com/invite/cdp) channel for assistance. </Info>

