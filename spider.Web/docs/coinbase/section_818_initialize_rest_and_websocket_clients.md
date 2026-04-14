# initialize REST and WebSocket clients
rest_client = RESTClient(api_key=api_key, api_secret=api_secret, verbose=True)
ws_client = WSClient(api_key=api_key, api_secret=api_secret, on_message=on_message, verbose=True)
