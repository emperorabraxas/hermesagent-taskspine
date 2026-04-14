# 1. Encode an unsigned transaction
TX=$(cdp util tx-encode \
  --network base-sepolia \
  --to 0x0000000000000000000000000000000000000000 \
  --value 0.00001ether \
  --from $address)
