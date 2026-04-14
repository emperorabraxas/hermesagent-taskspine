# Welcome to Coinbase INTX API
Source: https://docs.cdp.coinbase.com/api-reference/international-exchange-api/rest-api/introduction



<Tip>
  REST API Reference
  You can access the REST API docs from the sidebar or download the <a href="/api-reference/international-exchange-api/rest-api/intx-spec.yaml">OpenAPI</a> spec directly.
</Tip>

## Basics

All requests and responses are `application/json` content type and follow typical HTTP response status codes for success and failure.

Request URLs must be lowercase as URLs are [case-sensitive](https://www.w3.org/TR/WD-html40-970708/htmlweb.html).

## Status Codes

### Success

A successful response is indicated by HTTP status code 200 and may contain an optional body. If the response has a body it is documented under each resource.

<Frame>
  <img alt="In the API Reference, click the green 200 to view the response body of a successful response." />
</Frame>

### Errors

```json lines wrap theme={null}
{
    "message": "Invalid Price"
}
```

Unless otherwise stated, errors to bad requests respond with HTTP 4xx or status codes. The body also contains a `message` parameter indicating the cause. Your language HTTP library should be configured to provide message bodies for non-2xx requests so that you can read the message field from the body.

### Common Error Codes

| Status Code | Reason                                                        |
| :---------- | :------------------------------------------------------------ |
| 400         | Bad Request -- Invalid request format                         |
| 401         | Unauthorized -- Invalid API Key                               |
| 403         | Forbidden -- You do not have access to the requested resource |
| 404         | Not Found                                                     |
| 500         | Internal Server Error                                         |

