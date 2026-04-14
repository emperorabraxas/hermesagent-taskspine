# Message structure
Source: https://docs.cdp.coinbase.com/derivatives/udp/message-structure



CDE multicast UDP market data messages are encoded with Simple Binary Encoding (SBE) format with [little-endian](https://www.geeksforgeeks.org/dsa/little-and-big-endian-mystery/) byte ordering. A UDP packet can contain zero or more messages, up to a maximum length of 1400 bytes.

## Packet Header

All packets across all channels start with a packet header followed by zero or messages, up to a maximum length of 1400 bytes. The packet header has the following structure:

| Packet Header        | Type   | Length | Offset | Description                                                                                                                                                                                                                                                                    |
| :------------------- | :----- | :----- | :----- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| SendingTime          | int64  | 8      | 0      | Nanoseconds since epoch                                                                                                                                                                                                                                                        |
| SeqNum               | int64  | 8      | 8      | Sequence number. Differs based on context: <ul><li>Incremental: Sequence generated from trading system, never reset </li><li>Snapshot: Sequence associated with last incremental update</li><li>Retransmit reject: Sequence sent by client, acts as a correlation ID</li></ul> |
| ChannelId            | uint16 | 2      | 16     | Channel ID for a ProductCode/Instrument set.                                                                                                                                                                                                                                   |
| PktFlags             | uint8  | 1      | 18     | Bitset: <br />`0x01`: incremental update <br />`0x02`: snapshot <br />`0x04`: retransmit                                                                                                                                                                                       |
| PktMessageCount      | uint8  | 1      | 19     | Count of messages within packet                                                                                                                                                                                                                                                |
| SnapshotInstrumentId | int32  | 4      | 20     | Instrument ID of messages in snapshot packet (not used for incrementals)                                                                                                                                                                                                       |

## Message Header

Each message in a packet starts with a message header. Existing fields are never removed or modified, but new fields and messages may be added.

<Info>
  Message versioning follows standard SBE versioning practices. New versions are backwards compatible with older clients.
</Info>

| Message Header | Type   | Length | Offset | Description                                                                                                                                                             |
| :------------- | :----- | :----- | :----- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| FrameLength    | uint16 | 2      | 0      | Total message size in bytes including this header. Also includes repeating groups and var length data. Indicates empty space at end of message data for byte alignment. |
| BlockLength    | uint16 | 2      | 2      | Total length of message body in bytes excluding this header and any repeating groups or variable length field.                                                          |
| TemplateId     | uint16 | 2      | 4      | Message template identifier, specified for each message type in spec within parenthesis (##).                                                                           |
| SchemaId       | uint16 | 2      | 6      | ID of message schema containing the template. Constant: `SchemaId=1201`                                                                                                 |
| Version        | uint16 | 2      | 8      | Version of message schema                                                                                                                                               |

