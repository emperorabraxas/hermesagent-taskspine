# Convert to ISO8601 format strings
end_timestamp = end_time.isoformat()
start_timestamp = start_time.isoformat()

uri = f'https://api.prime.coinbase.com/v1/portfolios/{PORTFOLIO_ID}/candles?product_id=BTC-USD&granularity=ONE_HOUR&start_time={quote(start_timestamp)}&end_time={quote(end_timestamp)}'
url_path = urlparse(uri).path
timestamp = str(int(time.time()))
message = timestamp + 'GET' + url_path
signature_b64 = base64.b64encode(hmac.digest(SECRET_KEY.encode(), message.encode(), hashlib.sha256))

headers = {
   'X-CB-ACCESS-SIGNATURE': signature_b64,
   'X-CB-ACCESS-TIMESTAMP': timestamp,
   'X-CB-ACCESS-KEY': API_KEY,
   'X-CB-ACCESS-PASSPHRASE': PASSPHRASE,
   'Accept': 'application/json'
}

response = requests.get(uri, headers=headers)
parsed_response = json.loads(response.text)

if 'candles' in parsed_response:
    candles = parsed_response['candles']
    
    timestamps = [datetime.fromisoformat(candle['timestamp'].replace('Z', '+00:00')) for candle in candles]
    opens = [float(candle['open']) for candle in candles]
    highs = [float(candle['high']) for candle in candles]
    lows = [float(candle['low']) for candle in candles]
    closes = [float(candle['close']) for candle in candles]
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    for i in range(len(timestamps)):
        color = 'green' if closes[i] >= opens[i] else 'red'
        
        ax.plot([timestamps[i], timestamps[i]], [lows[i], highs[i]], color='black', linewidth=1)
        
        body_height = abs(closes[i] - opens[i])
        body_bottom = min(opens[i], closes[i])
        
        ax.bar(timestamps[i], body_height, bottom=body_bottom, width=0.8/24, 
               color=color, alpha=0.7, edgecolor='black', linewidth=0.5)
    
    ax.set_title('BTC-USD Candlestick Chart', fontsize=16)
    ax.set_xlabel('Time', fontsize=12)
    ax.set_ylabel('Price (USD)', fontsize=12)
    
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M'))
    ax.xaxis.set_major_locator(mdates.HourLocator(interval=6))
    plt.xticks(rotation=45)
    
    plt.tight_layout()
    plt.grid(True, alpha=0.3)
    plt.show()
else:
    print("Error: No candles data in response")
    print(json.dumps(parsed_response, indent=3))
```

