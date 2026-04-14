# 1. Encode — builds an unsigned EIP-1559 transaction
TX=$(cdp util tx-encode \
  --network base-sepolia \
  --to 0x4252e0c9A3da5A2700e7d91cb50aEf522D0C6Fe8 \
  --value 0.00001ether \
  --from $address)
