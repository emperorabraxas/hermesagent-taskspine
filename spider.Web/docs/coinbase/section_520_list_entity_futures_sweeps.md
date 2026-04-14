# List Entity Futures Sweeps
Source: https://docs.cdp.coinbase.com/api-reference/prime-api/rest-api/futures/list-entity-futures-sweeps

GET /v1/entities/{entity_id}/futures/sweeps
Retrieve fcm sweeps in open status, including pending and processing sweeps.

### Pending vs. Processing Sweeps

* A pending sweep is a sweep that has not started processing and can be cancelled
* A processing sweep is a sweep that is currently being processed and cannot be cancelled

Once a sweep is complete, it no longer appears in the list of sweeps.

