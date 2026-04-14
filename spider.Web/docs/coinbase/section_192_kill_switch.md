# Kill Switch
Source: https://docs.cdp.coinbase.com/api-reference/derivatives-api/rest-api/risk/kill-switch

/api-reference/derivatives-api/rest-api/cde-spec.json post /rest/kill-switch
Activates a kill switch to cancel orders and lock trading for specified users, firms, or FCMs. Must only include one uuid (fcm, firm, or trading user). When activated, all open orders will be cancelled and new orders will be rejected.


