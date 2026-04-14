# Troubleshooting & Help
Source: https://docs.cdp.coinbase.com/api-reference/payment-apis/troubleshooting

Common issues and solutions for CDP Payments API

## Common Issues

<AccordionGroup>
  <Accordion title="401 Unauthorized Errors">
    **Problem**: Getting authentication errors when calling the API

    **Solutions**:

    * Verify you're using the correct API keys for your environment (sandbox vs production)
    * Check that the API key has the required permissions
    * Ensure the `Authorization` header is properly formatted
    * Confirm the API key hasn't expired
  </Accordion>

  <Accordion title="Rate Limiting">
    **Problem**: Hitting rate limits during testing or production use

    **Rate Limit**: 100 requests per minute (RPM)

    **Solutions**:

    * Implement exponential backoff in your code
    * Add delays between rapid consecutive requests
    * Cache responses when appropriate
    * Contact support if you need higher limits for testing
  </Accordion>

  <Accordion title="Transfers Stuck in Pending">
    **Problem**: Transfers not completing

    **Solutions**:

    * Check the transfer amount (some amounts trigger delays)
    * Verify account IDs are valid accounts
    * Ensure you've called the execute endpoint
    * Review transfer status for error messages
  </Accordion>

  <Accordion title="Environment Mismatch">
    **Problem**: Code works in sandbox but fails in production

    **Solutions**:

    * Verify all configuration uses environment variables
    * Check for hardcoded sandbox-specific values
    * Ensure production API keys have correct permissions
    * Review any differences in account setup
  </Accordion>

  <Accordion title="Invalid Request Errors">
    **Problem**: Receiving 400 Bad Request responses

    **Solutions**:

    * Review the [API Conventions](/api-reference/payment-apis/conventions) for correct request formatting
    * Check the [Errors](/api-reference/payment-apis/errors) page for specific error codes
    * Validate your request payload matches the expected schema
    * Ensure all required fields are provided
  </Accordion>
</AccordionGroup>

## Getting Help

If you encounter issues with the CDP Payments API:

<CardGroup>
  <Card title="Discord Community" icon="discord" href="https://discord.gg/cdp">
    Join developer discussions and get community support
  </Card>

  <Card title="API Reference" icon="book" href="/api-reference/payment-apis/overview">
    Complete API documentation for all Payments API endpoints
  </Card>

  <Card title="Service Status" icon="signal" href="/get-started/support/status">
    Check the current status of CDP services
  </Card>

  <Card title="Error Codes" icon="triangle-exclamation" href="/api-reference/payment-apis/errors">
    Reference for all API error codes and their meanings
  </Card>
</CardGroup>

## Additional Resources

<CardGroup>
  <Card title="Authentication Guide" icon="key" href="/get-started/authentication/overview">
    Learn how to authenticate your API requests
  </Card>

  <Card title="Sandbox Environment" icon="flask" href="/api-reference/payment-apis/sandbox">
    Test your integration safely in the sandbox
  </Card>

  <Card title="CDP Portal" icon="browser" href="https://portal.cdp.coinbase.com">
    Manage your API keys and view analytics
  </Card>
</CardGroup>

