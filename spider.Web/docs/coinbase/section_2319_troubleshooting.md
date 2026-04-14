# Troubleshooting
Source: https://docs.cdp.coinbase.com/x402/support/troubleshooting



This page covers common errors when integrating with x402. For general questions, see the [FAQ](/x402/support/faq).

<Info>
  Need help? Join the [x402 Discord](https://discord.gg/cdp) for support from the community.
</Info>

## Common Errors

### `Unable to estimate gas`

<Note>
  This is a client-side EVM error, not an x402 error. It occurs when your wallet or provider can't simulate the transaction.
</Note>

This error happens when creating the payment payload, before the facilitator is called.

<AccordionGroup>
  <Accordion title="Common causes">
    * **Insufficient token balance**: Your wallet doesn't have enough USDC to cover the payment amount.
    * **Invalid recipient address**: The `payTo` address in payment requirements is invalid or a contract that can't receive tokens.
    * **Network RPC issues**: The RPC endpoint is unavailable or rate-limited.
    * **Wrong network**: Your wallet is connected to a different network than specified in the payment requirements.
  </Accordion>

  <Accordion title="How to fix">
    Verify your wallet has sufficient balance and is connected to the correct network:

    ```typescript theme={null}
    // 1. Check your wallet balance
    const balance = await provider.getBalance(walletAddress);
    console.log("ETH Balance:", balance);

    // 2. Check USDC balance
    const usdcContract = new ethers.Contract(USDC_ADDRESS, ERC20_ABI, provider);
    const usdcBalance = await usdcContract.balanceOf(walletAddress);
    console.log("USDC Balance:", usdcBalance);

    // 3. Verify payment requirements
    const response = await fetch(url);
    if (response.status === 402) {
      const paymentRequired = response.headers.get("PAYMENT-REQUIRED");
      console.log("Payment requirements:", JSON.parse(atob(paymentRequired)));
    }
    ```
  </Accordion>
</AccordionGroup>

### `invalid_payload` or `invalid_request: doesn't match schema (oneOf)`

These errors mean the payment payload is malformed or doesn't match what the facilitator expects. Common variants:

<AccordionGroup>
  <Accordion title="Schema / version mismatch">
    The payload structure doesn't match the `x402Version`. v1 and v2 have different payload schemas.

    **How to fix:** Ensure your payload structure matches the version you're using. If using v2, set `x402Version: 2` and use the v2 payload shape. See the [Migration Guide](/x402/migration-guide) for schema differences.
  </Accordion>

  <Accordion title="Mixed v1/v2 imports">
    Your code mixes imports from v1 and v2 packages, causing inconsistent payload formats.

    **How to fix:** Use only v2 packages (`@x402/*`) or only v1 packages. Avoid mixing `x402-express` with `@x402/express` in the same process.
  </Accordion>

  <Accordion title="Wrong or missing fields">
    Required fields are missing, malformed, or don't match the payment requirements (e.g., wrong `payTo`, `network`, or amount).

    **How to fix:** Compare your payload to the `PAYMENT-REQUIRED` header. Ensure `scheme`, `network`, `payTo`, and amount match. For price format, use a dollar-prefixed string (e.g. `"$0.10"`).
  </Accordion>

  <Accordion title="Invalid or malformed signature">
    The signature doesn't verify against the authorization data.

    **How to fix:** Ensure you're signing with the correct private key and that the payload hasn't been modified. Check network ID (CAIP-2 format) and expiry (`validBefore`).
  </Accordion>
</AccordionGroup>

### `402 Payment Required` (after attaching payment header)

The server is still returning 402 even though you included the `PAYMENT-SIGNATURE` header.

<AccordionGroup>
  <Accordion title="Common causes">
    * **Wrong header name**: Using legacy `X-PAYMENT` instead of `PAYMENT-SIGNATURE`.
    * **Invalid signature**: Wrong chain ID or payload fields.
    * **Insufficient amount**: Payment amount is less than required.
    * **KYT flagged**: Payer address was flagged by Know Your Transaction checks.
  </Accordion>

  <Accordion title="How to fix">
    Check the `error` field in the server's JSON response for details. Common fixes:

    * Use `PAYMENT-SIGNATURE` header (not `X-PAYMENT`)
    * Verify your USDC balance meets the required amount
    * Check that your network ID matches (e.g., `eip155:8453` for Base mainnet)
  </Accordion>
</AccordionGroup>

### Works on testnet, fails on mainnet

Your integration works on Base Sepolia but fails on Base mainnet.

<AccordionGroup>
  <Accordion title="Common causes">
    * **Wrong network ID**: Using testnet ID (`eip155:84532`) instead of mainnet (`eip155:8453`).
    * **Wrong facilitator**: The x402.org testnet facilitator (`https://x402.org/facilitator`) does NOT support mainnet.
    * **No mainnet USDC**: Your wallet has testnet USDC but not mainnet USDC.
    * **Insufficient gas**: Mainnet requires real ETH for gas fees.
  </Accordion>

  <Accordion title="How to fix">
    * Update network to `eip155:8453` (Base mainnet)
    * Use CDP facilitator for mainnet: `https://api.cdp.coinbase.com/platform/v2/x402`
    * Fund your wallet with mainnet USDC and ETH
    * See [Network Support](/x402/network-support) for facilitator details
  </Accordion>
</AccordionGroup>

### `No scheme registered`

The x402 client or server doesn't have a payment scheme registered for the requested network.

<AccordionGroup>
  <Accordion title="Common causes">
    * **Missing scheme registration**: You didn't call `.register()` for the network.
    * **Wrong network ID format**: Using legacy format (`base-sepolia`) instead of CAIP-2 (`eip155:84532`).
  </Accordion>

  <Accordion title="How to fix">
    Register the appropriate scheme for your network:

    ```typescript theme={null}
    // Client-side
    import { registerExactEvmScheme } from "@x402/evm/exact/client";
    const client = new x402Client();
    registerExactEvmScheme(client, { signer });

    // Server-side
    import { ExactEvmScheme } from "@x402/evm/exact/server";
    const server = new x402ResourceServer(facilitatorClient)
      .register("eip155:8453", new ExactEvmScheme());
    ```

    See [Migration Guide](/x402/migration-guide) for CAIP-2 network ID format.
  </Accordion>
</AccordionGroup>

## Facilitator API Error Codes

When the facilitator returns an error, check the `invalidReason` (for verify) or `errorReason` (for settle) field.

<AccordionGroup>
  <Accordion title="Verification errors (invalidReason)">
    | Error Code                                                 | Meaning                                    |
    | ---------------------------------------------------------- | ------------------------------------------ |
    | `insufficient_funds`                                       | Payer doesn't have enough tokens           |
    | `invalid_scheme`                                           | Unsupported payment scheme                 |
    | `invalid_network`                                          | Unsupported network                        |
    | `invalid_x402_version`                                     | Wrong protocol version (v1 vs v2 mismatch) |
    | `invalid_payload`                                          | Malformed payment payload                  |
    | `invalid_exact_evm_payload_signature`                      | EVM signature verification failed          |
    | `invalid_exact_evm_payload_authorization_value_too_low`    | Payment amount less than required          |
    | `invalid_exact_evm_payload_authorization_valid_before`     | Payment authorization expired              |
    | `invalid_exact_evm_payload_authorization_from_address_kyt` | Payer address flagged by KYT               |
    | `invalid_exact_svm_payload_transaction_simulation_failed`  | Solana transaction simulation failed       |
  </Accordion>

  <Accordion title="Settlement errors (errorReason)">
    | Error Code                                            | Meaning                                   |
    | ----------------------------------------------------- | ----------------------------------------- |
    | `settle_exact_failed_onchain`                         | Transaction failed onchain                |
    | `settle_exact_node_failure`                           | Blockchain node connection failed         |
    | `settle_exact_evm_transaction_confirmation_timed_out` | EVM transaction confirmation timed out    |
    | `settle_exact_svm_transaction_confirmation_timed_out` | Solana transaction confirmation timed out |
  </Accordion>
</AccordionGroup>

For the complete list, see the [x402 Facilitator API Reference](/api-reference/v2/rest-api/x402-facilitator/verify-a-payment).

## Still Need Help?

* [x402 Discord](https://discord.gg/cdp) - Community support
* [GitHub Issues](https://github.com/coinbase/x402/issues) - Bug reports and feature requests

