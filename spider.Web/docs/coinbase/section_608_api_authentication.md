# API Authentication
Source: https://docs.cdp.coinbase.com/api-reference/v2/authentication



## Introduction

<Tip>
  **Looking for Coinbase App authentication?**

  This page covers authentication for Coinbase Developer Platform (CDP) APIs for building onchain apps. If you're looking to access consumer Coinbase App accounts, see the [Coinbase App API Authentication documentation](/coinbase-app/authentication-authorization/api-key-authentication).
</Tip>

Coinbase Developer Platform (CDP) uses three distinct types of authentication keys, each serving a specific purpose:

**Server requests**:

These keys should be stored securely, and used only by trusted back-end services:

* **[Secret API Key](#secret-api-key):** For all server-to-server communication (i.e., REST APIs).
* **[Wallet Secret](#wallet-secret):** Additional requirement for any server-to-server communication that involves sensitive wallet operations (i.e., signing transactions via REST APIs).

**Client requests**:

These keys are designed for client-side communication, and are safe to include in end-user code:

* **[Client API Key](#client-api-key):** For all client-side communication (i.e., JSON-RPC APIs).

## Client API Key

The Client API Key is designed specifically for client-side applications. This key:

* Is present within your [RPC endpoint URL](https://portal.cdp.coinbase.com/products/node) (i.e., `https://api.developer.coinbase.com/rpc/v1/base/<MY-CLIENT-API-KEY>`)
* Authenticates JSON-RPC requests from browser-based applications and mobile apps
* Is safe to include in client-side code
* Has limited functionality by design
* Can be easily rotated if needed

### 1. Create Client API Key

To create a Client API Key:

1. Navigate to your [API Keys dashboard](https://portal.cdp.coinbase.com/projects/api-keys).
2. Select your desired project from the top drop-down.
3. Select the **Client API Key** tab.
4. Copy the generated key.
5. Export as an environment variable:

```bash lines wrap  theme={null}
export CLIENT_API_KEY="your_client_api_key"
```

<Tip>
  Click the **Rotate** button to expire this key and generate a new one.
</Tip>

### 2. Authenticate

To authenticate your client-side code, include it with your JSON-RPC request:

```bash lines wrap theme={null}
curl -L -X "$HTTP_METHOD" https://api.developer.coinbase.com/rpc/v1/base/${CLIENT_API_KEY} \
  -H "Content-Type: application/json" \
  -d '${REQUEST_BODY_JSON}'
```

As an example, you can request the [List Historical Balances](api-reference/json-rpc-api/address-history#cdp-listbalancehistories) JSON-RPC endpoint like so:

```bash lines wrap theme={null}
curl -L -X POST https://api.developer.coinbase.com/rpc/v1/base/${CLIENT_API_KEY} \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "id": 1, "method": "cdp_listBalances", "params": [{"address":"0xF7DCa789B08Ed2F7995D9bC22c500A8CA715D0A8","pageToken":"","pageSize":1}]}'
```

## Secret API Key

The Secret API Key is required for **all server-to-server communication** with CDP APIs. This key:

* Is used to generate a [Bearer Token](#generate-bearer-token) (JWT), which authenticates your CDP project ownership
* Is used in the `Authorization` header of your request
* Is required as the base layer of authentication for all server endpoints
* Must be kept secure and never exposed in client-side code
* Can be configured with IP allowlists and more granular permissions

### 1. Create Secret API Key

To create a Secret API Key:

1. Navigate to your [API Keys dashboard](https://portal.cdp.coinbase.com/projects/api-keys).
2. Select your desired project from the top drop-down.
3. Select the **Secret API Keys** tab.
4. Click **Create API key** and name your key.
5. Optional: Configure additional settings
   * IP allowlist
   * Permission restrictions
   * Signature algorithm (Ed25519 recommended)
6. Click **Create** to generate your API key.

<Frame>
  <img alt="Create API Key" />
</Frame>

A modal will appear with your key details.

<Frame>
  <img alt="API Key Details" />
</Frame>

Make sure you save the API key ID and Secret in a safe place.

<Info>
  **Optional API Key File Download**

  For enhanced security, API key files are no longer automatically downloaded. If you need to reference your API key via file path in your code, click the **Download API key** button in the modal to save the key file. However, it is recommended to copy the key details directly from the modal and use them as environment variables for better security.
</Info>

<Tip>
  To regenerate a Secret API key, click **Configure** to delete and recreate the key.
</Tip>

### 2. Generate Bearer Token

Bearer Tokens (JWTs) are required for **server-to-server communication only**, are included in your `Authorization` header, and are generated using your [Secret API Key](#secret-api-key).

<Tip>
  Use our SDK for easier authentication

  The [CDP SDK](https://github.com/coinbase/cdp-sdk) automatically handles generation of Bearer Tokens for you, streamlining the process of making requests to all of our REST endpoints.
</Tip>

For REST API users, continue reading to:

* Set up your environment for Bearer Token generation by configuring environment variables and installing dependencies
* Export your generated Bearer Token as an environment variable

<Expandable title="More on JWTs">
  A JWT is a compact, self-contained, stateless token format used to securely transmit API keys as a JSON object for authentication with the CDP API. They are typically included in the `Authorization` header of your request.

  Read more in our [JWT documentation](/get-started/authentication/jwt-authentication).
</Expandable>

<Warning>
  Never include Secret API key information in your code.

  Instead, securely store it and retrieve it from an environment variable, a secure database, or other storage mechanism intended for highly-sensitive parameters.
</Warning>

#### Environment setup

To begin, export the following environment variables:

```bash lines wrap theme={null}
export KEY_ID="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
export KEY_SECRET="XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX=="
export REQUEST_METHOD="GET"
export REQUEST_PATH="/platform/v2/evm/token-balances/base-sepolia/0x8fddcc0c5c993a1968b46787919cc34577d6dc5c"
export REQUEST_HOST="api.cdp.coinbase.com"
```

Complete the remaining setup steps for JWT generation below according to your language choice.

#### Generate Bearer Token (JWT) and export

<Tabs>
  <Tab title="JavaScript">
    First, install the CDP SDK:

    ```bash lines wrap theme={null}
    npm install @coinbase/cdp-sdk
    ```

    Create a new file for JWT generation code:

    ```javascript main.js lines wrap [expandable] theme={null}
    const { generateJwt } = require("@coinbase/cdp-sdk/auth");

    const main = async () => {
      // Generate the JWT using the CDP SDK
      const token = await generateJwt({
        apiKeyId: process.env.KEY_ID,
        apiKeySecret: process.env.KEY_SECRET,
        requestMethod: process.env.REQUEST_METHOD,
        requestHost: process.env.REQUEST_HOST,
        requestPath: process.env.REQUEST_PATH,
        expiresIn: 120 // optional (defaults to 120 seconds)
      });
      
      console.log(token);
    };

    main();
    ```

    Finally, run the script to generate the JWT output and export it as an environment variable:

    ```bash lines wrap theme={null}
    export JWT=$(node main.js)
    echo $JWT
    ```
  </Tab>

  <Tab title="TypeScript">
    First, install the CDP SDK:

    ```bash lines wrap theme={null}
    npm install @coinbase/cdp-sdk
    ```

    Create a new file for JWT generation code:

    ```typescript main.ts lines wrap [expandable] theme={null}
    import { generateJwt } from "@coinbase/cdp-sdk/auth";

    const main = async () => {
        // Generate the JWT using the CDP SDK
        const token = await generateJwt({
            apiKeyId: process.env.KEY_ID!,
            apiKeySecret: process.env.KEY_SECRET!,
            requestMethod: process.env.REQUEST_METHOD!,
            requestHost: process.env.REQUEST_HOST!,
            requestPath: process.env.REQUEST_PATH!,
            expiresIn: 120 // optional (defaults to 120 seconds)
        });
        
        console.log(token);
    };

    main();
    ```

    Finally, run the script to generate the JWT output and export it as an environment variable:

    ```bash lines wrap theme={null}
    export JWT=$(npx tsx main.ts)
    echo $JWT
    ```
  </Tab>

  <Tab title="Python">
    First, install the CDP SDK:

    ```bash lines wrap theme={null}
    pip install cdp-sdk
    ```

    Create a new file for JWT generation code:

    ```python main.py lines wrap [expandable] theme={null}
    import os
    from cdp.auth.utils.jwt import generate_jwt, JwtOptions

    # Generate the JWT using the CDP SDK
    jwt_token = generate_jwt(JwtOptions(
        api_key_id=os.getenv('KEY_ID'),
        api_key_secret=os.getenv('KEY_SECRET'),
        request_method=os.getenv('REQUEST_METHOD'),
        request_host=os.getenv('REQUEST_HOST'),
        request_path=os.getenv('REQUEST_PATH'),
        expires_in=120  # optional (defaults to 120 seconds)
    ))

    print(jwt_token)
    ```

    Finally, run the script to generate the JWT output and export it as an environment variable:

    ```bash lines wrap theme={null}
    export JWT=$(python main.py)
    echo $JWT
    ```
  </Tab>

  <Tab title="Go">
    First, install the CDP SDK:

    ```bash lines wrap theme={null}
    go mod init jwt-example
    go get github.com/coinbase/cdp-sdk/go
    ```

    Create a new file for JWT generation code:

    ```go main.go lines wrap [expandable] theme={null}
    package main

    import (
        "fmt"
        "log"
        "os"

        "github.com/coinbase/cdp-sdk/go/auth"
    )

    func main() {
        // Generate the JWT using the CDP SDK
        jwt, err := auth.GenerateJWT(auth.JwtOptions{
            KeyID:         os.Getenv("KEY_ID"),
            KeySecret:     os.Getenv("KEY_SECRET"),
            RequestMethod: os.Getenv("REQUEST_METHOD"),
            RequestHost:   os.Getenv("REQUEST_HOST"),
            RequestPath:   os.Getenv("REQUEST_PATH"),
            ExpiresIn:     120, // optional (defaults to 120 seconds)
        })
        if err != nil {
            log.Fatalf("error building jwt: %v", err)
        }
        
        fmt.Println(jwt)
    }
    ```

    Finally, run the script to generate the JWT output and export it as an environment variable:

    ```bash lines wrap  theme={null}
    export JWT=$(go run main.go)
    echo $JWT
    ```
  </Tab>

  <Tab title="Ruby">
    First, install required dependencies:

    ```bash lines wrap theme={null}
    gem install jwt
    gem install ed25519
    ```

    Create a new file for JWT generation code:

    ```ruby main.rb lines wrap [expandable] theme={null}
    require 'jwt'
    require 'ed25519'
    require 'base64'
    require 'time'
    require 'securerandom'

    # Fetching environment variables
    key_id = ENV['KEY_ID']
    key_secret = ENV['KEY_SECRET']
    request_method = ENV['REQUEST_METHOD']
    request_host = ENV['REQUEST_HOST']
    request_path = ENV['REQUEST_PATH']

    def build_jwt(key_id, key_secret, uri)
      # Decode the Ed25519 private key from base64
      decoded = Base64.decode64(key_secret)
      
      # Ed25519 keys are 64 bytes (32 bytes seed + 32 bytes public key)
      if decoded.length != 64
        raise "Invalid Ed25519 key length"
      end
      
      # Extract the seed (first 32 bytes)
      seed = decoded[0, 32]
      signing_key = Ed25519::SigningKey.new(seed)
      
      # Header for the JWT
      header = {
        alg: 'EdDSA',
        typ: 'JWT',
        kid: key_id,
        nonce: SecureRandom.hex(16)
      }

      # Claims for the JWT
      claims = {
        sub: key_id,
        iss: 'cdp',
        aud: ['cdp_service'],
        nbf: Time.now.to_i,
        exp: Time.now.to_i + 120, # Expiration time: 2 minute from now.
        uri: uri
      }

      # Encode the JWT with EdDSA algorithm
      JWT.encode(claims, signing_key, 'EdDSA', header)
    end

    # Build the JWT with the URI
    token = build_jwt(key_id, key_secret, "#{request_method.upcase} #{request_host}#{request_path}")

    # Print the JWT token
    puts token
    ```

    Finally, run the script to generate the JWT output and export it as an environment variable:

    ```bash lines wrap theme={null}
    export JWT=$(ruby main.rb)
    echo $JWT
    ```
  </Tab>

  <Tab title="PHP">
    First, ensure the Sodium extension is enabled (included by default in PHP 7.2+):

    ```bash lines wrap theme={null}
    # Ensure the sodium extension is enabled
    php -m | grep sodium
    ```

    Create a new file for JWT generation code:

    ```php main.php lines wrap [expandable] theme={null}
    <?php
    function buildJwt() {
        // Fetching values directly from environment variables
        $keyId = getenv('KEY_ID');  
        $keySecret = getenv('KEY_SECRET');
        $requestMethod = getenv('REQUEST_METHOD'); 
        $requestHost = getenv('REQUEST_HOST');
        $requestPath = getenv('REQUEST_PATH');

        // Ensure that the environment variables are set
        if (!$keyId || !$keySecret || !$requestMethod || !$requestHost || !$requestPath) {
            throw new Exception('Required environment variables are missing');
        }

        // Decode the Ed25519 private key from base64
        $decoded = base64_decode($keySecret);
        
        // Ed25519 keys are 64 bytes (32 bytes seed + 32 bytes public key)
        if (strlen($decoded) != 64) {
            throw new Exception('Invalid Ed25519 key length');
        }
        
        // Extract the seed (first 32 bytes) - this is the actual private key for sodium
        $privateKey = substr($decoded, 0, 32);
        
        // Constructing the URI from method, host, and path
        $uri = $requestMethod . ' ' . $requestHost . $requestPath;

        // Setting the current time and creating a unique nonce
        $time = time();
        $nonce = substr(str_replace(['+', '/', '='], '', base64_encode(random_bytes(12))), 0, 16);

        // JWT Header
        $header = [
            'alg' => 'EdDSA',
            'typ' => 'JWT',
            'kid' => $keyId,
            'nonce' => $nonce
        ];

        // JWT Payload
        $payload = [
            'sub' => $keyId,
            'iss' => 'cdp',
            'aud' => ['cdp_service'],
            'nbf' => $time,
            'exp' => $time + 120,  // Token valid for 120 seconds from now
            'uri' => $uri
        ];

        // Encode header and payload
        $encodedHeader = rtrim(strtr(base64_encode(json_encode($header)), '+/', '-_'), '=');
        $encodedPayload = rtrim(strtr(base64_encode(json_encode($payload)), '+/', '-_'), '=');
        
        // Create the message to sign
        $message = $encodedHeader . '.' . $encodedPayload;
        
        // Sign with Ed25519 using sodium
        $signature = sodium_crypto_sign_detached($message, $privateKey);
        
        // Encode signature
        $encodedSignature = rtrim(strtr(base64_encode($signature), '+/', '-_'), '=');
        
        // Create the JWT
        return $message . '.' . $encodedSignature;
    }

    // Example of calling the function to generate the JWT
    try {
        $jwt = buildJwt();
        echo $jwt . "\n";
    } catch (Exception $e) {
        echo "Error generating JWT: " . $e->getMessage() . "\n";
    }
    ```

    Finally, run the script to generate the JWT output and export it as an environment variable:

    ```bash lines wrap theme={null}
    export JWT=$(php main.php)
    echo $JWT
    ```
  </Tab>

  <Tab title="Java">
    First, install required dependencies:

    ```xml lines wrap theme={null}
    <!-- Add this to your pom.xml -->
    <dependency>
        <groupId>com.nimbusds</groupId>
        <artifactId>nimbus-jose-jwt</artifactId>
        <version>9.31</version>
    </dependency>
    ```

    Create a new file for JWT generation code:

    ```java main.java lines wrap [expandable] theme={null}
    import com.nimbusds.jose.*;
    import com.nimbusds.jose.crypto.*;
    import com.nimbusds.jwt.*;
    import java.util.Date;
    import java.util.UUID;
    import java.util.Base64;

    public class Main {
        public static void main(String[] args) throws Exception {
            // Load environment variables
            String keySecret = System.getenv("KEY_SECRET");
            String keyId = System.getenv("KEY_ID");
            String requestMethod = System.getenv("REQUEST_METHOD");
            String requestHost = System.getenv("REQUEST_HOST");
            String requestPath = System.getenv("REQUEST_PATH");

            // Ensure all environment variables are provided
            if (keySecret == null || keyId == null || requestMethod == null || requestHost == null || requestPath == null) {
                throw new IllegalArgumentException("Required environment variables are missing");
            }

            // Decode the Ed25519 private key from base64
            byte[] decoded = Base64.getDecoder().decode(keySecret);
            
            // Ed25519 keys are 64 bytes (32 bytes seed + 32 bytes public key)
            if (decoded.length != 64) {
                throw new Exception("Invalid Ed25519 key length");
            }
            
            // Extract the seed (first 32 bytes) and public key (last 32 bytes)
            byte[] seed = new byte[32];
            byte[] publicKey = new byte[32];
            System.arraycopy(decoded, 0, seed, 0, 32);
            System.arraycopy(decoded, 32, publicKey, 0, 32);
            
            // Create OctetKeyPair for Ed25519
            OctetKeyPair okp = new OctetKeyPair.Builder(Curve.Ed25519, Base64.getUrlEncoder().withoutPadding().encodeToString(publicKey))
                .d(Base64.getUrlEncoder().withoutPadding().encodeToString(seed))
                .keyUse(KeyUse.SIGNATURE)
                .build();

            // Create URI string for current request
            String uri = requestMethod + " " + requestHost + requestPath;

            // Create JWT claims
            JWTClaimsSet claims = new JWTClaimsSet.Builder()
                .issuer("cdp")
                .subject(keyId)
                .notBeforeTime(new Date())
                .expirationTime(new Date(System.currentTimeMillis() + 120000)) // 120 seconds
                .claim("uri", uri)
                .build();

            // Create JWT header with nonce
            JWSHeader header = new JWSHeader.Builder(JWSAlgorithm.EdDSA)
                .keyID(keyId)
                .customParam("nonce", UUID.randomUUID().toString().replace("-", ""))
                .build();

            // Sign the JWT
            SignedJWT signedJWT = new SignedJWT(header, claims);
            JWSSigner signer = new Ed25519Signer(okp);
            signedJWT.sign(signer);

            String jwt = signedJWT.serialize();
            System.out.println(jwt);
        }
    }
    ```

    Finally, compile the script and export the JWT output as an environment variable:

    ```bash lines wrap theme={null}
    javac -cp "nimbus-jose-jwt-9.31.jar:." Main.java
    export JWT=$(java -cp "nimbus-jose-jwt-9.31.jar:." Main)
    echo $JWT
    ```
  </Tab>

  <Tab title="C++">
    First, install required dependencies:

    ```bash lines wrap theme={null}
    # For Ubuntu/Debian
    sudo apt-get install libsodium-dev nlohmann-json3-dev

    # For MacOS
    brew install libsodium nlohmann-json
    ```

    Create a new file for JWT generation code:

    ```cpp main.cpp lines wrap [expandable] theme={null}
    #include <iostream>
    #include <sstream>
    #include <string>
    #include <cstdlib>
    #include <cstring>
    #include <chrono>
    #include <random>
    #include <sodium.h>
    #include <nlohmann/json.hpp>

    // Base64 URL encoding helper
    std::string base64url_encode(const unsigned char* data, size_t len) {
        static const char* base64_chars = 
            "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_";
        
        std::string encoded;
        encoded.reserve(((len + 2) / 3) * 4);
        
        for (size_t i = 0; i < len; i += 3) {
            unsigned int octet1 = data[i];
            unsigned int octet2 = (i + 1 < len) ? data[i + 1] : 0;
            unsigned int octet3 = (i + 2 < len) ? data[i + 2] : 0;
            
            unsigned int combined = (octet1 << 16) | (octet2 << 8) | octet3;
            
            encoded += base64_chars[(combined >> 18) & 0x3F];
            encoded += base64_chars[(combined >> 12) & 0x3F];
            if (i + 1 < len) encoded += base64_chars[(combined >> 6) & 0x3F];
            if (i + 2 < len) encoded += base64_chars[combined & 0x3F];
        }
        
        return encoded;
    }

    // Base64 decode helper
    std::vector<unsigned char> base64_decode(const std::string& encoded) {
        static const unsigned char base64_table[256] = {
            64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64,
            64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64,
            64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 62, 64, 64, 64, 63,
            52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 64, 64, 64, 64, 64, 64,
            64,  0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14,
            15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 64, 64, 64, 64, 64,
            64, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40,
            41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 64, 64, 64, 64, 64,
            64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64,
            64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64,
            64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64,
            64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64,
            64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64,
            64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64
        };
        
        std::vector<unsigned char> decoded;
        decoded.reserve((encoded.length() * 3) / 4);
        
        for (size_t i = 0; i < encoded.length(); ) {
            unsigned char c1 = base64_table[static_cast<unsigned char>(encoded[i++])];
            unsigned char c2 = base64_table[static_cast<unsigned char>(encoded[i++])];
            unsigned char c3 = (i < encoded.length()) ? base64_table[static_cast<unsigned char>(encoded[i++])] : 64;
            unsigned char c4 = (i < encoded.length()) ? base64_table[static_cast<unsigned char>(encoded[i++])] : 64;
            
            if (c1 == 64 || c2 == 64) break;
            
            decoded.push_back((c1 << 2) | (c2 >> 4));
            if (c3 != 64) decoded.push_back((c2 << 4) | (c3 >> 2));
            if (c4 != 64) decoded.push_back((c3 << 6) | c4);
        }
        
        return decoded;
    }

    std::string create_jwt() {
        // Initialize libsodium
        if (sodium_init() < 0) {
            throw std::runtime_error("Failed to initialize libsodium");
        }

        // Fetching environment variables
        const char* key_id_env = std::getenv("KEY_ID");
        const char* key_secret_env = std::getenv("KEY_SECRET");
        const char* request_method_env = std::getenv("REQUEST_METHOD");
        const char* request_host_env = std::getenv("REQUEST_HOST");
        const char* request_path_env = std::getenv("REQUEST_PATH");

        // Ensure all environment variables are present
        if (!key_id_env || !key_secret_env || !request_method_env || !request_host_env || !request_path_env) {
            throw std::runtime_error("Missing required environment variables");
        }

        std::string key_id = key_id_env;
        std::string key_secret = key_secret_env;
        std::string request_method = request_method_env;
        std::string request_host = request_host_env;
        std::string request_path = request_path_env;
        
        // Decode the Ed25519 private key from base64
        std::vector<unsigned char> decoded = base64_decode(key_secret);
        
        // Ed25519 keys are 64 bytes (32 bytes seed + 32 bytes public key)
        if (decoded.size() != 64) {
            throw std::runtime_error("Invalid Ed25519 key length");
        }
        
        // Extract the seed (first 32 bytes)
        unsigned char private_key[32];
        std::memcpy(private_key, decoded.data(), 32);
        
        std::string uri = request_method + " " + request_host + request_path;

        // Generate a random nonce (16 digits)
        std::random_device rd;
        std::mt19937 gen(rd());
        std::uniform_int_distribution<> dis(0, 9);
        std::string nonce;
        for (int i = 0; i < 16; ++i) {
            nonce += std::to_string(dis(gen));
        }

        // Get current timestamp
        auto now = std::chrono::system_clock::now();
        auto now_seconds = std::chrono::duration_cast<std::chrono::seconds>(now.time_since_epoch()).count();

        // Create JWT header
        nlohmann::json header = {
            {"alg", "EdDSA"},
            {"typ", "JWT"},
            {"kid", key_id},
            {"nonce", nonce}
        };

        // Create JWT payload
        nlohmann::json payload = {
            {"sub", key_id},
            {"iss", "cdp"},
            {"aud", nlohmann::json::array({"cdp_service"})},
            {"nbf", now_seconds},
            {"exp", now_seconds + 120},
            {"uri", uri}
        };

        // Encode header and payload
        std::string header_json = header.dump();
        std::string payload_json = payload.dump();
        
        std::string encoded_header = base64url_encode(
            reinterpret_cast<const unsigned char*>(header_json.c_str()), 
            header_json.length()
        );
        std::string encoded_payload = base64url_encode(
            reinterpret_cast<const unsigned char*>(payload_json.c_str()), 
            payload_json.length()
        );
        
        // Create message to sign
        std::string message = encoded_header + "." + encoded_payload;
        
        // Sign with Ed25519
        unsigned char signature[crypto_sign_BYTES];
        crypto_sign_detached(signature, nullptr,
            reinterpret_cast<const unsigned char*>(message.c_str()), message.length(),
            private_key);
        
        // Encode signature
        std::string encoded_signature = base64url_encode(signature, crypto_sign_BYTES);
        
        // Return complete JWT
        return message + "." + encoded_signature;
    }

    int main() {
        try {
            std::string token = create_jwt();
            std::cout << token << std::endl;
        } catch (const std::exception& e) {
            std::cerr << "Error: " << e.what() << std::endl;
            return 1;
        }
        return 0;
    }
    ```

    Finally, compile the script and export the JWT output as an environment variable:

    ```bash lines wrap theme={null}
    g++ main.cpp -o myapp -lsodium -std=c++17
    export JWT=$(./myapp)
    echo $JWT
    ```
  </Tab>

  <Tab title="C#">
    First, install required dependencies:

    ```bash lines wrap theme={null}
    dotnet add package System.IdentityModel.Tokens.Jwt
    dotnet add package BouncyCastle.NetCore
    dotnet add package Microsoft.IdentityModel.Tokens
    dotnet add package Newtonsoft.Json
    ```

    Create a new file for JWT generation code:

    ```csharp GenerateBearerJWT.cs lines wrap [expandable] theme={null}
    using System;
    using System.Collections.Generic;
    using System.Security.Cryptography;
    using System.Text;
    using Org.BouncyCastle.Crypto.Parameters;
    using Org.BouncyCastle.Crypto.Signers;
    using Newtonsoft.Json;

    namespace BearerJWT
    {
        internal class Program
        {
            static void Main(string[] args)
            {
                // Get environment variables
                string keyId = Environment.GetEnvironmentVariable("KEY_ID");
                string keySecret = Environment.GetEnvironmentVariable("KEY_SECRET");
                string requestMethod = Environment.GetEnvironmentVariable("REQUEST_METHOD");
                string requestHost = Environment.GetEnvironmentVariable("REQUEST_HOST");
                string requestPath = Environment.GetEnvironmentVariable("REQUEST_PATH");

                // Validate environment variables
                if (string.IsNullOrEmpty(keyId) || string.IsNullOrEmpty(keySecret) || 
                    string.IsNullOrEmpty(requestMethod) || string.IsNullOrEmpty(requestHost) || 
                    string.IsNullOrEmpty(requestPath))
                {
                    throw new InvalidOperationException("Missing required environment variables");
                }

                string token = GenerateBearerJWT(keyId, keySecret, requestMethod, requestHost, requestPath);
                Console.WriteLine(token);
            }

            static string GenerateBearerJWT(string keyId, string keySecret, string requestMethod, 
                string requestHost, string requestPath)
            {
                // Decode the Ed25519 private key from base64
                byte[] decoded = Convert.FromBase64String(keySecret);
                
                // Ed25519 keys are 64 bytes (32 bytes seed + 32 bytes public key)
                if (decoded.Length != 64)
                {
                    throw new Exception("Invalid Ed25519 key length");
                }
                
                // Extract the seed (first 32 bytes)
                byte[] seed = new byte[32];
                Array.Copy(decoded, 0, seed, 0, 32);
                
                // Create Ed25519 private key parameters
                var privateKey = new Ed25519PrivateKeyParameters(seed, 0);
                
                // Create the URI
                string uri = $"{requestMethod} {requestHost}{requestPath}";

                // Create header
                var header = new Dictionary<string, object>
                {
                    { "alg", "EdDSA" },
                    { "typ", "JWT" },
                    { "kid", keyId },
                    { "nonce", GenerateNonce() }
                };

                // Create payload with timing
                var now = DateTimeOffset.UtcNow.ToUnixTimeSeconds();
                var payload = new Dictionary<string, object>
                {
                    { "sub", keyId },
                    { "iss", "cdp" },
                    { "aud", new[] { "cdp_service" } },
                    { "nbf", now },
                    { "exp", now + 120 }, // 2 minutes expiration
                    { "uri", uri }
                };

                // Encode header and payload
                string headerJson = JsonConvert.SerializeObject(header);
                string payloadJson = JsonConvert.SerializeObject(payload);
                
                string encodedHeader = Base64UrlEncode(Encoding.UTF8.GetBytes(headerJson));
                string encodedPayload = Base64UrlEncode(Encoding.UTF8.GetBytes(payloadJson));
                
                string message = $"{encodedHeader}.{encodedPayload}";
                
                // Sign with Ed25519
                var signer = new Ed25519Signer();
                signer.Init(true, privateKey);
                byte[] messageBytes = Encoding.UTF8.GetBytes(message);
                signer.BlockUpdate(messageBytes, 0, messageBytes.Length);
                byte[] signature = signer.GenerateSignature();
                
                string encodedSignature = Base64UrlEncode(signature);
                
                return $"{message}.{encodedSignature}";
            }

            // Method to generate a dynamic nonce
            static string GenerateNonce()
            {
                var random = new Random();
                var nonce = new char[16];
                for (int i = 0; i < 16; i++)
                {
                    nonce[i] = (char)('0' + random.Next(10));
                }
                return new string(nonce);
            }

            // Base64 URL encoding without padding
            static string Base64UrlEncode(byte[] input)
            {
                return Convert.ToBase64String(input)
                    .Replace("+", "-")
                    .Replace("/", "_")
                    .Replace("=", "");
            }
        }
    }
    ```

    Finally, build and run the project to generate the JWT output and export it as an environment variable:

    ```bash lines wrap theme={null}
    dotnet build
    export JWT=$(dotnet run)
    echo $JWT
    ```
  </Tab>
</Tabs>

<Info>
  Bearer Tokens are valid for **2 minutes** by default. After 2 minutes, you will need to generate a new Bearer Token (JWT) to ensure uninterrupted access to the CDP APIs.
  If you are experiencing issues, please make sure your machine's clock is accurate.
</Info>

### 3. Authenticate

<Tip>
  Use our SDK for easier authentication

  The [CDP SDK](https://github.com/coinbase/cdp-sdk) automatically handles authentication for you, streamlining the process of making requests to all of our REST endpoints.
</Tip>

To authenticate your server-side code, use the JWT token you generated in the previous step as a [Bearer Token](https://swagger.io/docs/specification/v3_0/authentication/bearer-authentication/) within your request:

```bash lines wrap theme={null}
export API_ENDPOINT="https://$REQUEST_HOST$REQUEST_PATH"
