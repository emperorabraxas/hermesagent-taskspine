# The address to filter by
target_address = "0x0e73fc61bb9d6b7588910c2d14e83bae68222c5d"
```

3. Run the script

```shell lines wrap theme={null}
python app.py
```

4. The script will generate a CSV file named `transactions_{address}_{timestamp}.csv`

#### Output Format

<Frame>
  <img />
</Frame>

The CSV includes the following columns:

| Column            | Description                                         |
| :---------------- | :-------------------------------------------------- |
| type              | Transaction type (native/erc20/erc721/erc1155)      |
| direction         | send/receive                                        |
| contract\_address | Token contract address (empty for native transfers) |
| from\_address     | Sender address                                      |
| to\_address       | Recipient address                                   |
| value             | Transfer amount                                     |
| token\_id         | NFT token ID (for ERC721/ERC1155)                   |
| log\_index        | Event log index                                     |
| transaction\_hash | Transaction hash                                    |
| block\_number     | Block number                                        |

