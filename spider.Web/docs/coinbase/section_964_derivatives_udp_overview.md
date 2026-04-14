# Derivatives UDP Overview
Source: https://docs.cdp.coinbase.com/derivatives/udp/overview



The Multicast UDP Market Data API includes multiple groups of data channels/streams for unique sets of related products and instruments. Each group is comprised of 3 pairs of channels:

* <b><small>INCREMENTAL UPDATES</small></b> - A/B UDP multicast groups with <b>real-time updates</b> for orders, trades, market state changes, and instrument definitions.

* <b><small>SNAPSHOTS</small></b> - A/B UDP multicast groups with <b>periodic snapshots</b> of orders and instrument definitions/statuses at a regular interval.

* <b><small>RETRANSMIT SERVICE</small></b> - UDP unicast with updates by <b>InstrSeqNum range</b> using request/response model.

<Info>
  `A/B` refers to two multicast groups (A and B) used to transmit redundant data in the case of failover.
</Info>

