# Cancel Entity Futures Sweep
Source: https://docs.cdp.coinbase.com/api-reference/prime-api/rest-api/futures/create-entity-futures-sweep

DELETE /v1/entities/{entity_id}/futures/sweeps
Cancel the pending sweep for a given entity. A user will only be able to have one pending sweep at a time. If the sweep is not found, a 404 will be returned.


