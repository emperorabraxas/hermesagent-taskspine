# 2. Sign — signs with the account's private key in the TEE
SIGNED=$(cdp evm accounts sign transaction $address \
  transaction=$TX \
  --jq '.signedTransaction')
