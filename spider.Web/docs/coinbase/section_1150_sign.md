# Sign
SIGNED=$(cdp solana accounts sign transaction $address \
  transaction=$TX \
  --jq '.signedTransaction')
