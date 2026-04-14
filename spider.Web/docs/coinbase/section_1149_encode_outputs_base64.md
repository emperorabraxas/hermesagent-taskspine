# Encode (outputs base64)
TX=$(cdp util tx-encode \
  --network solana-devnet \
  --to <recipient> \
  --value 1000000 \
  --from $address)
