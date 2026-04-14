# 2. Sign it
SIGNED=$(cdp evm accounts sign transaction $address \
  transaction=$TX \
  --jq '.signedTransaction')
