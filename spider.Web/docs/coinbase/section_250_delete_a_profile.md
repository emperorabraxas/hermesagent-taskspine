# Delete a profile
Source: https://docs.cdp.coinbase.com/api-reference/exchange-api/rest-api/profiles/delete-profile

PUT /profiles/{profile_id}/deactivate
Deletes the profile specified by `profile_id` and transfers all funds to the profile specified by `to`. Fails if there are any open orders on the profile to be deleted.


