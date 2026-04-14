# Swap Examples
Source: https://docs.cdp.coinbase.com/custom-stablecoins/examples



Code examples for common swap scenarios using the Stableswapper program.

<Note>
  These examples assume you've completed the [Quickstart](/custom-stablecoins/quickstart) setup steps (dependencies, environment variables, and IDL/ABI).
</Note>

<Tabs>
  <Tab title="Solana Virtual Machine">
    ## Setup

    Use these devnet addresses in your examples. For mainnet, replace with your production addresses from [Key Addresses](/custom-stablecoins/key-addresses).

    ```typescript theme={null}
    import * as anchor from "@coral-xyz/anchor";
    import { Program, AnchorProvider } from "@coral-xyz/anchor";
    import { PublicKey } from "@solana/web3.js";
    import {
      TOKEN_PROGRAM_ID,
      ASSOCIATED_TOKEN_PROGRAM_ID,
      getAssociatedTokenAddress,
      getAccount,
      createAssociatedTokenAccountInstruction,
    } from "@solana/spl-token";
    import idl from "./custom_stablecoins.json";

    // Devnet addresses
    const PROGRAM_ID        = new PublicKey("9vDwZVJXw5nxymWmUcgmNpemDH5EBcJwLNhtsznrgJDH");
    const USDC_MINT         = new PublicKey("4zMMC9srt5Ri5X14GAgXhaHii3GnPAEERYPJgZJDncDU");
    const CUSTOM_TOKEN_MINT = new PublicKey("5P6MkoaCd9byPxH4X99kgKtS6SiuCQ67ZPCJzpXGkpCe"); // CBTUSD

    const provider = anchor.AnchorProvider.env();
    anchor.setProvider(provider);
    // @ts-ignore - IDL type compatibility
    const program = new Program(idl, provider);
    ```

    ***

    ## Swap USDC for custom token

    ```typescript theme={null}
    async function swapUsdcForCustomToken() {
      const swapAmount   = new anchor.BN(0.1 * 10 ** 6);   // 0.1 USDC (6 decimals)
      const minAmountOut = new anchor.BN(0.09 * 10 ** 6);  // Allow up to 10% for fees/slippage

      // Derive PDAs
      const [pool] = PublicKey.findProgramAddressSync(
        [Buffer.from("liquidity_pool")],
        PROGRAM_ID
      );

      const [usdcVault] = PublicKey.findProgramAddressSync(
        [Buffer.from("token_vault"), pool.toBuffer(), USDC_MINT.toBuffer()],
        PROGRAM_ID
      );

      const [customTokenVault] = PublicKey.findProgramAddressSync(
        [Buffer.from("token_vault"), pool.toBuffer(), CUSTOM_TOKEN_MINT.toBuffer()],
        PROGRAM_ID
      );

      const [usdcVaultTokenAccount] = PublicKey.findProgramAddressSync(
        [Buffer.from("vault_token_account"), usdcVault.toBuffer()],
        PROGRAM_ID
      );

      const [customTokenVaultTokenAccount] = PublicKey.findProgramAddressSync(
        [Buffer.from("vault_token_account"), customTokenVault.toBuffer()],
        PROGRAM_ID
      );

      const [whitelist] = PublicKey.findProgramAddressSync(
        [Buffer.from("address_whitelist")],
        PROGRAM_ID
      );

      // User token accounts
      const userUsdcAccount = await getAssociatedTokenAddress(
        USDC_MINT,
        provider.wallet.publicKey
      );

      const userCustomTokenAccount = await getAssociatedTokenAddress(
        CUSTOM_TOKEN_MINT,
        provider.wallet.publicKey
      );

      // Fetch pool to get fee recipient
      const poolAccount = await (program.account as any).liquidityPool.fetch(pool);

      const feeRecipientUsdcAccount = await getAssociatedTokenAddress(
        USDC_MINT,
        poolAccount.feeRecipient
      );

      // Create destination ATA if it doesn't exist
      let needsAccountCreation = false;
      try {
        await getAccount(provider.connection, userCustomTokenAccount);
      } catch {
        needsAccountCreation = true;
      }

      // Build swap instruction
      const swapIx = await program.methods
        .swap(swapAmount, minAmountOut)
        .accounts({
          pool,
          inVault: usdcVault,
          outVault: customTokenVault,
          inVaultTokenAccount: usdcVaultTokenAccount,
          outVaultTokenAccount: customTokenVaultTokenAccount,
          userFromTokenAccount: userUsdcAccount,
          toTokenAccount: userCustomTokenAccount,
          feeRecipientTokenAccount: feeRecipientUsdcAccount,
          feeRecipient: poolAccount.feeRecipient,
          fromMint: USDC_MINT,
          toMint: CUSTOM_TOKEN_MINT,
          user: provider.wallet.publicKey,
          whitelist,
          tokenProgram: TOKEN_PROGRAM_ID,
          associatedTokenProgram: ASSOCIATED_TOKEN_PROGRAM_ID,
          systemProgram: anchor.web3.SystemProgram.programId,
        } as any)
        .instruction();

      // Optionally prepend ATA creation
      const transaction = new anchor.web3.Transaction();
      if (needsAccountCreation) {
        transaction.add(
          createAssociatedTokenAccountInstruction(
            provider.wallet.publicKey,
            userCustomTokenAccount,
            provider.wallet.publicKey,
            CUSTOM_TOKEN_MINT
          )
        );
      }
      transaction.add(swapIx);

      const tx = await provider.sendAndConfirm(transaction);
      console.log("Swap successful:", tx);
    }
    ```

    ***

    ## Swap custom token for USDC

    ```typescript theme={null}
    async function swapCustomTokenForUsdc() {
      const swapAmount   = new anchor.BN(0.1 * 10 ** 6);   // 0.1 custom tokens (6 decimals)
      const minAmountOut = new anchor.BN(0.09 * 10 ** 6);  // Allow up to 10% for fees/slippage

      // Derive PDAs
      const [pool] = PublicKey.findProgramAddressSync(
        [Buffer.from("liquidity_pool")],
        PROGRAM_ID
      );

      const [customTokenVault] = PublicKey.findProgramAddressSync(
        [Buffer.from("token_vault"), pool.toBuffer(), CUSTOM_TOKEN_MINT.toBuffer()],
        PROGRAM_ID
      );

      const [usdcVault] = PublicKey.findProgramAddressSync(
        [Buffer.from("token_vault"), pool.toBuffer(), USDC_MINT.toBuffer()],
        PROGRAM_ID
      );

      const [customTokenVaultTokenAccount] = PublicKey.findProgramAddressSync(
        [Buffer.from("vault_token_account"), customTokenVault.toBuffer()],
        PROGRAM_ID
      );

      const [usdcVaultTokenAccount] = PublicKey.findProgramAddressSync(
        [Buffer.from("vault_token_account"), usdcVault.toBuffer()],
        PROGRAM_ID
      );

      const [whitelist] = PublicKey.findProgramAddressSync(
        [Buffer.from("address_whitelist")],
        PROGRAM_ID
      );

      // User token accounts
      const userCustomTokenAccount = await getAssociatedTokenAddress(
        CUSTOM_TOKEN_MINT,
        provider.wallet.publicKey
      );

      const userUsdcAccount = await getAssociatedTokenAddress(
        USDC_MINT,
        provider.wallet.publicKey
      );

      // Fetch pool to get fee recipient
      const poolAccount = await (program.account as any).liquidityPool.fetch(pool);

      const feeRecipientCustomTokenAccount = await getAssociatedTokenAddress(
        CUSTOM_TOKEN_MINT,
        poolAccount.feeRecipient
      );

      // Build and send swap
      const swapIx = await program.methods
        .swap(swapAmount, minAmountOut)
        .accounts({
          pool,
          inVault: customTokenVault,
          outVault: usdcVault,
          inVaultTokenAccount: customTokenVaultTokenAccount,
          outVaultTokenAccount: usdcVaultTokenAccount,
          userFromTokenAccount: userCustomTokenAccount,
          toTokenAccount: userUsdcAccount,
          feeRecipientTokenAccount: feeRecipientCustomTokenAccount,
          feeRecipient: poolAccount.feeRecipient,
          fromMint: CUSTOM_TOKEN_MINT,
          toMint: USDC_MINT,
          user: provider.wallet.publicKey,
          whitelist,
          tokenProgram: TOKEN_PROGRAM_ID,
          associatedTokenProgram: ASSOCIATED_TOKEN_PROGRAM_ID,
          systemProgram: anchor.web3.SystemProgram.programId,
        } as any)
        .instruction();

      const transaction = new anchor.web3.Transaction();
      transaction.add(swapIx);

      const tx = await provider.sendAndConfirm(transaction);
      console.log("Swap successful:", tx);
    }
    ```

    ***

    ## Swap between two custom stablecoins

    <Note>
      The program supports swapping between **any two supported tokens** — not just USDC pairs. To swap between two custom stablecoins, substitute both `CUSTOM_TOKEN_MINT` references with the respective `fromMint` and `toMint` addresses for your tokens.
    </Note>
  </Tab>

  <Tab title="Ethereum Virtual Machine">
    ## Setup

    Use these Base Sepolia addresses in your examples. For mainnet, replace with your production addresses from [Key Addresses](/custom-stablecoins/key-addresses).

    ```typescript theme={null}
    import { ethers } from "ethers";

    // Base Sepolia addresses
    const STABLESWAPPER_ADDRESS = "0x57AB1E2c6289aCe985Bd5c5571EbF6d98CD41Ab7";
    const USDC_ADDRESS          = "0x036CbD53842c5426634e7929541eC2318f3dCF7e";
    const CBTUSD_ADDRESS        = "0x57AB1EFE59b1C7b36b1Dc9315B4782bCcBb83721";

    const ERC20_ABI = [
      "function approve(address spender, uint256 amount) returns (bool)",
      "function allowance(address owner, address spender) view returns (uint256)",
      "function balanceOf(address account) view returns (uint256)",
      "function decimals() view returns (uint8)",
    ];

    const STABLESWAPPER_ABI = [
      "function swap(address tokenIn, address tokenOut, uint256 amountIn, uint256 minAmountOut, address recipient) external",
      "function feeBasisPoints() view returns (uint16)",
      "function feeRecipient() view returns (address)",
      "function isTokenListed(address token) view returns (bool)",
      "function isTokenSwappable(address token) view returns (bool)",
      "function isFeatureEnabled(uint8 feature) view returns (bool)",
      "function isAllowlisted(address addr) view returns (bool)",
      "function getTokenDecimals(address token) view returns (uint8)",
      "function getListedTokens() view returns (address[])",
      "function getReservedAmount(address token) view returns (uint256)",
    ];

    const provider = new ethers.JsonRpcProvider(process.env.RPC_URL);
    const signer = new ethers.Wallet(process.env.PRIVATE_KEY!, provider);

    const stableSwapper = new ethers.Contract(STABLESWAPPER_ADDRESS, STABLESWAPPER_ABI, signer);
    ```

    ***

    ## Swap USDC for custom token

    ```typescript theme={null}
    async function swapUsdcForCustomToken() {
      const usdc = new ethers.Contract(USDC_ADDRESS, ERC20_ABI, signer);

      const amountIn = ethers.parseUnits("0.1", 6);      // 0.1 USDC (6 decimals)
      const minAmountOut = ethers.parseUnits("0.09", 6);  // Allow up to 10% for fees/slippage

      // Approve the Stableswapper to spend USDC
      const currentAllowance = await usdc.allowance(signer.address, STABLESWAPPER_ADDRESS);
      if (currentAllowance < amountIn) {
        const approveTx = await usdc.approve(STABLESWAPPER_ADDRESS, amountIn);
        await approveTx.wait();
      }

      // Execute swap
      const swapTx = await stableSwapper.swap(
        USDC_ADDRESS,      // tokenIn
        CBTUSD_ADDRESS,      // tokenOut
        amountIn,          // amountIn
        minAmountOut,      // minAmountOut
        signer.address     // recipient
      );

      const receipt = await swapTx.wait();
      console.log("Swap successful:", receipt.hash);
    }
    ```

    ***

    ## Swap custom token for USDC

    ```typescript theme={null}
    async function swapCustomTokenForUsdc() {
      const cbtusd = new ethers.Contract(CBTUSD_ADDRESS, ERC20_ABI, signer);

      const amountIn = ethers.parseUnits("0.1", 6);      // 0.1 CBTUSD (6 decimals)
      const minAmountOut = ethers.parseUnits("0.09", 6);  // Allow up to 10% for fees/slippage

      // Approve the Stableswapper to spend CBTUSD
      const currentAllowance = await cbtusd.allowance(signer.address, STABLESWAPPER_ADDRESS);
      if (currentAllowance < amountIn) {
        const approveTx = await cbtusd.approve(STABLESWAPPER_ADDRESS, amountIn);
        await approveTx.wait();
      }

      // Execute swap
      const swapTx = await stableSwapper.swap(
        CBTUSD_ADDRESS,      // tokenIn
        USDC_ADDRESS,      // tokenOut
        amountIn,          // amountIn
        minAmountOut,      // minAmountOut
        signer.address     // recipient
      );

      const receipt = await swapTx.wait();
      console.log("Swap successful:", receipt.hash);
    }
    ```

    ***

    ## Swap to a different recipient

    On Base, you can send swap output directly to another address by specifying a different `recipient`.

    ```typescript theme={null}
    async function swapToRecipient(recipientAddress: string) {
      const usdc = new ethers.Contract(USDC_ADDRESS, ERC20_ABI, signer);

      const amountIn = ethers.parseUnits("1.0", 6);
      const minAmountOut = ethers.parseUnits("0.99", 6);

      const currentAllowance = await usdc.allowance(signer.address, STABLESWAPPER_ADDRESS);
      if (currentAllowance < amountIn) {
        const approveTx = await usdc.approve(STABLESWAPPER_ADDRESS, amountIn);
        await approveTx.wait();
      }

      const swapTx = await stableSwapper.swap(
        USDC_ADDRESS,
        CBTUSD_ADDRESS,
        amountIn,
        minAmountOut,
        recipientAddress    // output tokens go to this address
      );

      const receipt = await swapTx.wait();
      console.log("Swap to recipient successful:", receipt.hash);
    }
    ```

    ***

    ## Query contract state

    Read contract state before executing swaps for validation and fee calculation.

    ```typescript theme={null}
    async function queryContractState() {
      // Check fee configuration
      const feeBps = await stableSwapper.feeBasisPoints();
      console.log("Fee (basis points):", feeBps.toString());

      // Check token status
      const usdcListed = await stableSwapper.isTokenListed(USDC_ADDRESS);
      const usdcSwappable = await stableSwapper.isTokenSwappable(USDC_ADDRESS);
      console.log("USDC listed:", usdcListed, "swappable:", usdcSwappable);

      // Check if swaps are enabled
      const swapsEnabled = await stableSwapper.isFeatureEnabled(0); // 0 = SWAP
      console.log("Swaps enabled:", swapsEnabled);

      // Check allowlist status (only relevant if allowlist feature is enabled)
      const allowlistEnabled = await stableSwapper.isFeatureEnabled(2); // 2 = ALLOWLIST
      if (allowlistEnabled) {
        const isAllowed = await stableSwapper.isAllowlisted(signer.address);
        console.log("Wallet allowlisted:", isAllowed);
      }

      // Get all listed tokens
      const listedTokens = await stableSwapper.getListedTokens();
      console.log("Listed tokens:", listedTokens);
    }
    ```

    ***

    ## Swap between two custom stablecoins

    <Note>
      The contract supports swapping between **any two listed and swappable tokens** — not just USDC pairs. To swap between two custom stablecoins, use their respective addresses as `tokenIn` and `tokenOut`. Both tokens must be listed and have swapping enabled.
    </Note>
  </Tab>
</Tabs>

***

## What to read next

<CardGroup>
  <Card title="Reference" icon="book" href="/custom-stablecoins/reference">
    Complete swap instruction parameters and accounts
  </Card>

  <Card title="Production Readiness" icon="shield-check" href="/custom-stablecoins/production-readiness">
    Helper functions and best practices
  </Card>

  <Card title="Quickstart" icon="rocket" href="/custom-stablecoins/quickstart">
    Get up and running in 10 minutes
  </Card>

  <Card title="Key Addresses" icon="location-dot" href="/custom-stablecoins/key-addresses">
    Program IDs and deployed addresses
  </Card>
</CardGroup>

