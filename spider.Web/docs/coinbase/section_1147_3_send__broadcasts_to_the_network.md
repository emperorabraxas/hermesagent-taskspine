# 3. Send — broadcasts to the network
cdp evm accounts send transaction $address \
  network=base-sepolia \
  transaction=$SIGNED
```

For **ERC-20 transfers**, use `abi-encode` to build the calldata:

```bash theme={null}
DATA=$(cdp util abi-encode "transfer(address,uint256)" 0x4252e0c9A3da5A2700e7d91cb50aEf522D0C6Fe8 1000000)

TX=$(cdp util tx-encode \
  --network base-sepolia \
  --to 0x036CbD53842c5426634e7929541eC2318f3dCF7e \
  --data $DATA \
  --value 0 \
  --from $address)