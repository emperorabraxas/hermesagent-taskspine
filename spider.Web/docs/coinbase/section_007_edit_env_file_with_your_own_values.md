# edit .env file with your own values
pnpm install
pnpm start
```

## Vercel AI SDK

[Vercel AI SDK](https://sdk.vercel.ai/docs/introduction) is a library for building AI-powered applications with React and JavaScript/TypeScript. Our implementation demonstrates creating a terminal-style chatbot with access to CDP AgentKit actions.

### Prerequisites

#### Checking Node Version

Before using the example, ensure that you have Node.js 18 or higher installed. You can check your Node version by running:

```bash lines wrap theme={null}
node --version
```

If you don't have the correct version, you can install it using [nvm](https://github.com/nvm-sh/nvm):

```bash lines wrap theme={null}
nvm install node
```

#### API Keys

You'll need the following API keys:

* [CDP API Key](https://portal.cdp.coinbase.com/access/api)
* [OpenAI API Key](https://platform.openai.com/docs/quickstart#create-and-export-an-api-key)

Once you have them, rename the `.env-local` file to `.env` and set the API keys to their corresponding environment variables:

* `CDP_API_KEY_NAME`
* `CDP_API_KEY_PRIVATE_KEY`
* `OPENAI_API_KEY`

### Setting Up the Example

Clone the repository and navigate to the example directory:

```bash lines wrap theme={null}