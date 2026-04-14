# Idempotency
Source: https://docs.cdp.coinbase.com/api-reference/v2/idempotency



Idempotency ensures that an API request produces the same result regardless of how many times it is sent. This is particularly important for operations that modify state, like creating accounts or signing transactions, where duplicate requests could cause unintended side effects.

## How it works

The CDP APIs support idempotency through the `X-Idempotency-Key` header. When you include an idempotency key with a request, the API responds as follows:

* Processes the request as normal if it's the first use of the key within the last 24 hours
* Returns the exact same response as the first request if the same request is retried with the same key
* Returns an error if the same key is used with different request parameters

This mechanism ensures that temporary issues like network failures don't result in duplicate operations.

<Important>
  The idempotency key **must** be a valid UUID v4 string. Any other format will be rejected by the API.
</Important>

## Using idempotency keys

### Header format

The `X-Idempotency-Key` header must be a valid UUID v4 string. For example:

```
X-Idempotency-Key: 8e03978e-40d5-43e8-bc93-6894a57f9324
```

### Generating keys

Each unique request must use a new UUID v4. The API strictly enforces the UUID v4 format requirement and will reject any other format. Here's how to generate a valid UUID v4 in different languages:

<CodeGroup>
  ```typescript TypeScript lines wrap theme={null}
  import { v4 as uuidv4 } from 'uuid';

  // Generate a new idempotency key
  const idempotencyKey = uuidv4();
  ```

  ```javascript JavaScript lines wrap theme={null}
  import { v4 as uuidv4 } from 'uuid';

  // Generate a new idempotency key
  const idempotencyKey = uuidv4();
  ```

  ```python Python lines wrap theme={null}
  import uuid

  // Generate a new idempotency key
  idempotency_key = str(uuid.uuid4())
  ```

  ```go Go lines wrap theme={null}
  import "github.com/google/uuid"

  // Generate a new idempotency key
  idempotencyKey := uuid.New().String()
  ```

  ```ruby Ruby lines wrap theme={null}
  require 'securerandom'

  // Generate a new idempotency key
  idempotency_key = SecureRandom.uuid
  ```

  ```php PHP lines wrap theme={null}
  // Using PHP's built-in UUID generator (PHP 7.4+)
  $idempotencyKey = uuid_create(UUID_TYPE_RANDOM);

  // Alternative using ramsey/uuid package
  use Ramsey\Uuid\Uuid;
  $idempotencyKey = Uuid::uuid4()->toString();
  ```

  ```java Java lines wrap theme={null}
  import java.util.UUID;

  // Generate a new idempotency key
  String idempotencyKey = UUID.randomUUID().toString();
  ```

  ```cpp C++ lines wrap [expandable] theme={null}
  #include <uuid/uuid.h>
  #include <string>

  std::string generateIdempotencyKey() {
      uuid_t uuid;
      char uuid_str[37];
      
      uuid_generate_random(uuid);
      uuid_unparse_lower(uuid, uuid_str);
      
      return std::string(uuid_str);
  }
  ```

  ```csharp C# lines wrap [expandable] theme={null}
  using System;

  // Generate a new idempotency key
  string idempotencyKey = Guid.NewGuid().ToString();
  ```
</CodeGroup>

## Best practices

1. **Generate new keys**: Always generate a new UUID v4 for each unique request.

2. **Store keys**: Keep track of idempotency keys and their responses for retry scenarios.

3. **Key lifetime**: Keys should be unique within a rolling 24-hour timeframe.

4. **Retry logic**: Implement exponential backoff when retrying failed requests:

<CodeGroup>
  ```typescript TypeScript lines wrap [expandable] theme={null}
  import { v4 as uuidv4 } from 'uuid';

  async function makeIdempotentRequest<T>(url: string, data: unknown): Promise<T> {
    const idempotencyKey = uuidv4();
    let retries = 0;
    const maxRetries = 3;

    while (retries < maxRetries) {
      try {
        const response = await fetch(url, {
          method: "POST",
          headers: {
            "X-Idempotency-Key": idempotencyKey
          },
          body: JSON.stringify(data)
        });

        if (response.ok) {
          return response.json();
        }

        if (response.status === 422) {
          const error = await response.json();
          if (error.errorType === "idempotency_error") {
            throw new Error("Idempotency key conflict");
          }
        }

      } catch (error) {
        retries++;
        if (retries === maxRetries) throw error;
        
        // Exponential backoff
        await new Promise(resolve => 
          setTimeout(resolve, Math.pow(2, retries) * 1000)
        );
      }
    }
    throw new Error("Max retries exceeded");
  }
  ```

  ```javascript JavaScript lines wrap [expandable] theme={null}
  import { v4 as uuidv4 } from 'uuid';

  async function makeIdempotentRequest(url, data) {
    const idempotencyKey = uuidv4();
    let retries = 0;
    const maxRetries = 3;

    while (retries < maxRetries) {
      try {
        const response = await fetch(url, {
          method: "POST",
          headers: {
            "X-Idempotency-Key": idempotencyKey
          },
          body: JSON.stringify(data)
        });

        if (response.ok) {
          return response.json();
        }

        if (response.status === 422) {
          const error = await response.json();
          if (error.errorType === "idempotency_error") {
            throw new Error("Idempotency key conflict");
          }
        }

      } catch (error) {
        retries++;
        if (retries === maxRetries) throw error;
        
        // Exponential backoff
        await new Promise(resolve => 
          setTimeout(resolve, Math.pow(2, retries) * 1000)
        );
      }
    }
  }
  ```

  ```python Python lines wrap [expandable] theme={null}
  import time
  import uuid
  from typing import Any, Dict

  def make_idempotent_request(url: str, data: Dict[str, Any]) -> Dict[str, Any]:
      idempotency_key = str(uuid.uuid4())
      retries = 0
      max_retries = 3
      
      while retries < max_retries:
          try:
              response = requests.post(
                  url,
                  headers={"X-Idempotency-Key": idempotency_key},
                  json=data
              )
              
              if response.ok:
                  return response.json()
                  
              if response.status_code == 422:
                  error = response.json()
                  if error.get("errorType") == "idempotency_error":
                      raise ValueError("Idempotency key conflict")
                      
          except Exception as e:
              retries += 1
              if retries == max_retries:
                  raise e
                  
              # Exponential backoff
              time.sleep(2 ** retries)
  ```

  ```go Go lines wrap [expandable] theme={null}
  import (
      "encoding/json"
      "fmt"
      "github.com/google/uuid"
      "time"
  )

  func makeIdempotentRequest(url string, data interface{}) (*http.Response, error) {
      idempotencyKey := uuid.New().String()
      maxRetries := 3
      
      for retries := 0; retries < maxRetries; retries++ {
          requestBody, _ := json.Marshal(data)
          req, _ := http.NewRequest("POST", url, bytes.NewBuffer(requestBody))
          req.Header.Set("X-Idempotency-Key", idempotencyKey)
          
          client := &http.Client{}
          resp, err := client.Do(req)
          
          if err == nil && resp.StatusCode == http.StatusOK {
              return resp, nil
          }
          
          if resp != nil && resp.StatusCode == 422 {
              var errorResp struct {
                  ErrorType string `json:"errorType"`
              }
              json.NewDecoder(resp.Body).Decode(&errorResp)
              if errorResp.ErrorType == "idempotency_error" {
                  return nil, fmt.Errorf("idempotency key conflict")
              }
          }
          
          // Exponential backoff
          time.Sleep(time.Second * time.Duration(1<<retries))
      }
      
      return nil, fmt.Errorf("max retries exceeded")
  }
  ```

  ```ruby Ruby lines wrap [expandable] theme={null}
  require 'securerandom'

  def make_idempotent_request(url, data)
    idempotency_key = SecureRandom.uuid
    retries = 0
    max_retries = 3

    while retries < max_retries
      begin
        response = HTTP.headers(
          'X-Idempotency-Key' => idempotency_key
        ).post(url, json: data)

        return response.parse if response.status.success?

        if response.code == 422
          error = JSON.parse(response.body.to_s)
          raise 'Idempotency key conflict' if error['errorType'] == 'idempotency_error'
        end

      rescue StandardError => e
        retries += 1
        raise e if retries == max_retries

        # Exponential backoff
        sleep(2 ** retries)
        retry
      end
    end
  end
  ```

  ```php PHP lines wrap [expandable] theme={null}
  function makeIdempotentRequest($url, $data) {
      $idempotencyKey = uuid_create(UUID_TYPE_RANDOM);
      $maxRetries = 3;
      $retries = 0;

      while ($retries < $maxRetries) {
          try {
              $client = new GuzzleHttp\Client();
              $response = $client->post($url, [
                  'headers' => ['X-Idempotency-Key' => $idempotencyKey],
                  'json' => $data
              ]);

              if ($response->getStatusCode() === 200) {
                  return json_decode($response->getBody(), true);
              }

          } catch (GuzzleHttp\Exception\ClientException $e) {
              if ($e->getResponse()->getStatusCode() === 422) {
                  $error = json_decode($e->getResponse()->getBody(), true);
                  if ($error['errorType'] === 'idempotency_error') {
                      throw new Exception('Idempotency key conflict');
                  }
              }

              $retries++;
              if ($retries === $maxRetries) {
                  throw $e;
              }

              // Exponential backoff
              sleep(pow(2, $retries));
          }
      }

      throw new Exception('Max retries exceeded');
  }
  ```

  ```java Java lines wrap [expandable] theme={null}
  import java.util.UUID;

  public class IdempotentRequest {
      public static <T> T makeIdempotentRequest(String url, Object data, Class<T> responseType) 
              throws Exception {
          String idempotencyKey = UUID.randomUUID().toString();
          int maxRetries = 3;
          int retries = 0;

          while (retries < maxRetries) {
              try {
                  HttpClient client = HttpClient.newHttpClient();
                  HttpRequest request = HttpRequest.newBuilder()
                      .uri(URI.create(url))
                      .header("X-Idempotency-Key", idempotencyKey)
                      .POST(HttpRequest.BodyPublishers.ofString(
                          new ObjectMapper().writeValueAsString(data)))
                      .build();

                  HttpResponse<String> response = client.send(
                      request, HttpResponse.BodyHandlers.ofString());

                  if (response.statusCode() == 200) {
                      return new ObjectMapper()
                              .readValue(response.body(), responseType);
                  }

                  if (response.statusCode() == 422) {
                      JsonNode error = new ObjectMapper()
                              .readTree(response.body());
                      if ("idempotency_error".equals(
                              error.get("errorType").asText())) {
                          throw new Exception("Idempotency key conflict");
                      }
                  }

              } catch (Exception e) {
                  retries++;
                  if (retries == maxRetries) throw e;

                  // Exponential backoff
                  Thread.sleep((long) Math.pow(2, retries) * 1000);
              }
          }

          throw new Exception("Max retries exceeded");
      }
  }
  ```

  ```cpp C++ lines wrap [expandable] theme={null}
  #include <cpprest/http_client.h>
  #include <uuid/uuid.h>

  using namespace web::http;
  using namespace web::http::client;

  class IdempotentRequest {
  public:
      static pplx::task<json::value> makeIdempotentRequest(
          const string& url, 
          const json::value& data
      ) {
          string idempotencyKey = generateUuid();
          int maxRetries = 3;
          int retries = 0;

          while (retries < maxRetries) {
              try {
                  http_client client(url);
                  http_request request(methods::POST);
                  request.headers().add("X-Idempotency-Key", idempotencyKey);
                  request.set_body(data);

                  return client.request(request)
                  .then([](http_response response) {
                      if (response.status_code() == 200) {
                          return response.extract_json();
                      }
                      
                      if (response.status_code() == 422) {
                          auto error = response.extract_json().get();
                          if (error["errorType"].as_string() == "idempotency_error") {
                              throw std::runtime_error("Idempotency key conflict");
                          }
                      }
                      throw std::runtime_error("Request failed");
                  });

              } catch (const std::exception& e) {
                  retries++;
                  if (retries == maxRetries) throw e;

                  // Exponential backoff
                  std::this_thread::sleep_for(
                      std::chrono::seconds(static_cast<int>(pow(2, retries)))
                  );
              }
          }
          throw std::runtime_error("Max retries exceeded");
      }

  private:
      static string generateUuid() {
          uuid_t uuid;
          char uuid_str[37];
          uuid_generate_random(uuid);
          uuid_unparse_lower(uuid, uuid_str);
          return string(uuid_str);
      }
  };
  ```

  ```csharp C# lines wrap [expandable] theme={null}
  using System;
  using System.Net.Http;
  using System.Threading.Tasks;

  public class IdempotentRequest
  {
      public static async Task<T> MakeIdempotentRequest<T>(
          string url, 
          object data,
          int maxRetries = 3)
      {
          var idempotencyKey = Guid.NewGuid().ToString();
          var retries = 0;

          using var client = new HttpClient();

          while (retries < maxRetries)
          {
              try
              {
                  var request = new HttpRequestMessage(HttpMethod.Post, url);
                  request.Headers.Add("X-Idempotency-Key", idempotencyKey);
                  request.Content = new StringContent(
                      JsonSerializer.Serialize(data),
                      Encoding.UTF8,
                      "application/json"
                  );

                  var response = await client.SendAsync(request);

                  if (response.IsSuccessStatusCode)
                  {
                      var content = await response.Content.ReadAsStringAsync();
                      return JsonSerializer.Deserialize<T>(content);
                  }

                  if (response.StatusCode == HttpStatusCode.UnprocessableEntity)
                  {
                      var error = await JsonSerializer.DeserializeAsync<ErrorResponse>(
                          await response.Content.ReadAsStreamAsync()
                      );
                      if (error?.ErrorType == "idempotency_error")
                      {
                          throw new Exception("Idempotency key conflict");
                      }
                  }

              }
              catch (Exception e)
              {
                  retries++;
                  if (retries == maxRetries) throw;

                  // Exponential backoff
                  await Task.Delay(TimeSpan.FromSeconds(Math.Pow(2, retries)));
              }
          }

          throw new Exception("Max retries exceeded");
      }
  }
  ```
</CodeGroup>

## Supported endpoints

You can identify endpoints that support idempotency by looking for the `X-Idempotency-Key` parameter in the documentation for the related endpoint. When present, this optional header parameter indicates that the endpoint supports idempotent requests.

For example, in the [Create an EVM account](/api-reference/v2/rest-api/evm-accounts/create-an-evm-account) endpoint documentation, you'll see a field that allows you to pass the `X-Idempotency-Key` header.

<Tip>
  Generally, all `POST` endpoints that modify state (like creating accounts or signing transactions) support idempotency.
</Tip>

## Error handling

### Invalid idempotency key format

If you provide an idempotency key that is not a valid UUID v4, the API will reject the request:

```json lines wrap theme={null}
{
  "errorType": "invalid_request",
  "errorMessage": "parameter \"X-Idempotency-Key\" in header has an error: must be a valid UUID v4 format (e.g., 8e03978e-40d5-43e8-bc93-6894a57f9324)"
}
```

### Idempotency key conflict

This occurs when you use the same idempotency key with different request parameters:

```json lines wrap theme={null}
{
  "errorType": "idempotency_error",
  "errorMessage": "Idempotency key '8e03978e-40d5-43e8-bc93-6894a57f9324' was already used with a different request payload. Please try again with a new idempotency key."
}
```

### Already processing

This error occurs in certain highly-concurrent scenarios whereby you send multiple requests within a short period with the same idempotency key. Note that under normal circumstances, sending the same request with the same idempotency
key within a 24-hour period will return the same response as the first request.

```json lines wrap theme={null}
{
  "errorType": "already_exists",
  "errorMessage": "Another request with the same idempotency key is currently processing."
}
```

## Usage constraints

Idempotency keys are subject to the following limitations:

* Keys must be valid UUID v4 strings
* Keys should be unique within a 24-hour window
* Duplicate requests with the same key count towards your API rate limits

## Security considerations

While idempotency keys aren't sensitive like API keys, we recommend following these security practices:

* Use cryptographically secure UUID v4 generators
* Don't use sequential or predictable keys (only UUID v4 format is accepted)
* Don't reuse keys across different operations
* Store keys securely if you need to reference them later

