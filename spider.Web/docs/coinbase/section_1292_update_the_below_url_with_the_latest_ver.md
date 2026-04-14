# Update the below URL with the latest version of the Server-Signer binary.
SERVER_SIGNER_BINARY_URL="https://prime-onchain-wallet-server-signer-public.s3.us-east-1.amazonaws.com/templates/1.2.1/server-signer.yaml"

TEMP_DIR="/tmp/new-binary"
mkdir -p $TEMP_DIR && cd $TEMP_DIR
curl -o $TEMP_DIR/new-binary.zip $SERVER_SIGNER_BINARY_URL
unzip -o $TEMP_DIR/new-binary.zip
sudo dpkg -i $TEMP_DIR/cdp-signer_*_amd64.deb
sudo systemctl start $SERVICE_NAME
echo "Binary updated and service restarted successfully."
```

The binary is updated now and can be verified by creating a new wallet or signing with an existing one.

