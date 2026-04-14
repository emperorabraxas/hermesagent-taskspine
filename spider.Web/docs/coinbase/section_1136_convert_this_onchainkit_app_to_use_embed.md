# "Convert this OnchainKit app to use embedded wallets instead of external wallet connections, keeping all DeFi components but changing the authentication layer"
```

## Re-configuring your app

Once you have scaffolded your project, it should have come equipped with a hidden `.env` file.

This file is used to store environment-specific variables for your development setup. It allows you to configure settings like API keys, project IDs, and network configurations without hardcoding them into your application code. This file is crucial for maintaining security and flexibility, as it keeps sensitive information out of your codebase and allows for easy changes to configuration settings.

<Warning>
  **Never commit your `.env` file to version control!,** It contains sensitive API keys that could compromise your CDP account if exposed publicly.
</Warning>

## What to read next

Your environment is now configured for AI-first development. Continue with:

* **[AI Development Workflows](/get-started/develop-with-ai/development/develop-with-ai-workflows)**: Learn day-to-day development practices, advanced configuration, debugging strategies, and best practices

* **[AI-Assisted Deployment Guide](/get-started/develop-with-ai/development/ai-deployment)**: Detailed deployment setup and environment variable configuration for production releases

