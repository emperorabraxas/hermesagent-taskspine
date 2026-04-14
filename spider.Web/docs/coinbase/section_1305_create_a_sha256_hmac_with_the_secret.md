# create a sha256 hmac with the secret
secret = Base64.decode64(@secret)
hash = OpenSSL::HMAC.digest('sha256', secret, what)
Base64.strict_encode64(hash)
```

##### JavaScript

```js lines wrap theme={null}
// Function to generate a signature using Google's crypto-js package
function sign(str, secret) {
  const hash = CryptoJS.HmacSHA256(str, secret);
  return hash.toString(CryptoJS.enc.Base64);
}
// Function to build the payload required to sign
function buildPayload(ts, method, requestPath, body) {
  return `${ts}${method}${requestPath}${body}`;
}
// Build the string we want to sign using information defined above
const strToSign = buildPayload(
  Math.floor(Date.now() / 1000),
  "GET",
  "/v1/portfolios/<YOUR_PORTFOLIO_ID_HERE>/orders",
  "",
);
// Sign it!
const sig = sign(strToSign, SIGNING_KEY);
```

