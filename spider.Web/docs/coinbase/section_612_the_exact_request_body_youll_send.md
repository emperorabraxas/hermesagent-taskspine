# The exact request body you'll send
export REQUEST_BODY='{"transaction": "0x1234567890123456789012345678901234567890"}'
```

Complete the remaining setup steps for JWT generation below according to your language choice.

#### Generate Wallet Token (JWT) and export

<Tabs>
  <Tab title="JavaScript">
    First, install required dependencies:

    ```bash lines wrap theme={null}
    npm install jose crypto
    ```

    Create a new file to generate your Wallet Token:

    ```javascript generate_wallet_jwt.js lines wrap [expandable] theme={null}
    const jose = require('jose');
    const crypto = require('crypto');

    // Get environment variables
    const walletSecret = process.env.WALLET_SECRET;
    const requestMethod = process.env.REQUEST_METHOD;
    const requestHost = process.env.REQUEST_HOST;
    const requestPath = process.env.REQUEST_PATH;
    const requestBody = process.env.REQUEST_BODY;

    // Create the JWT payload
    const now = Math.floor(Date.now() / 1000);
    const uri = `${requestMethod} ${requestHost}${requestPath}`;

    const payload = {
      iat: now,
      nbf: now,
      jti: crypto.randomBytes(16).toString('hex'),
      uris: [uri]
    };

    function sortKeys(obj) {
      if (!obj || typeof obj !== "object") {
        return obj;
      }

      if (Array.isArray(obj)) {
        return obj.map(sortKeys);
      }

      return Object.keys(obj)
        .sort()
        .reduce(
          (acc, key) => {
            acc[key] = sortKeys(obj[key]);
            return acc;
          },
          {},
        );
    }

    // Add request body if present
    if (requestBody) {
      const sortedBody = sortKeys(JSON.parse(requestBody));
      payload.reqHash = crypto
        .createHash('sha256')
        .update(Buffer.from(JSON.stringify(sortedBody)))
        .digest('hex');
    }

    // Generate the JWT
    (async () => {
      const ecKey = crypto.createPrivateKey({
        key: walletSecret,
        format: "der",
        type: "pkcs8",
        encoding: "base64",
      });

      // Sign JWT
      const jwt = await new jose.SignJWT(payload)
        .setProtectedHeader({ alg: 'ES256', typ: 'JWT' })
        .sign(ecKey);

      console.log(jwt);
    })();
    ```

    Finally, run the script to generate the JWT output and export it as an environment variable:

    ```bash lines wrap theme={null}
    # Generate and export the JWT
    export WALLET_AUTH_JWT=$(node generate_wallet_jwt.js)
    echo $WALLET_AUTH_JWT
    ```
  </Tab>

  <Tab title="TypeScript">
    First, install required dependencies:

    ```bash lines wrap theme={null}
    npm install jose crypto typescript @types/node
    ```

    Configure your TypeScript compiler options

    ```typescript tsconfig.json theme={null}
    {
      "compilerOptions": {
        "target": "ES2020",           // or ES2015 or higher
        "module": "CommonJS",         // or "ESNext" for ESM
        "moduleResolution": "node",
        "lib": ["ES2020"],            // include at least ES2020
        "esModuleInterop": true,
        "forceConsistentCasingInFileNames": true,
        "strict": true,
        "skipLibCheck": true
      }
    }
    ```

    Create a new file to generate your Wallet Token:

    ```typescript generate_wallet_jwt.ts lines wrap [expandable] theme={null}
    import * as jose from 'jose';
    import * as crypto from "crypto";

    // Get environment variables
    const walletSecret = process.env.WALLET_SECRET!;
    const requestMethod = process.env.REQUEST_METHOD!;
    const requestHost = process.env.REQUEST_HOST!;
    const requestPath = process.env.REQUEST_PATH!;
    const requestBody = process.env.REQUEST_BODY;

    // Create the JWT payload
    const now = Math.floor(Date.now() / 1000);
    const uri = `${requestMethod} ${requestHost}${requestPath}`;

    const payload: jose.JWTPayload = {
      iat: now,
      nbf: now,
      jti: crypto.randomBytes(16).toString('hex'),
      uris: [uri]
    };

    function sortKeys(obj: any): any {
      if (!obj || typeof obj !== "object") {
        return obj;
      }

      if (Array.isArray(obj)) {
        return obj.map(sortKeys);
      }

      return Object.keys(obj)
        .sort()
        .reduce(
          (acc, key) => {
            acc[key] = sortKeys(obj[key]);
            return acc;
          },
          {} as Record<string, any>,
        );
    }

    // Add request body if present
    if (requestBody) {
      const sortedBody = sortKeys(JSON.parse(requestBody));
      payload.reqHash = crypto
        .createHash('sha256')
        .update(Buffer.from(JSON.stringify(sortedBody)))
        .digest('hex');
    }

    // Generate the JWT
    (async () => {
      const ecKey = crypto.createPrivateKey({
        key: walletSecret,
        format: "der",
        type: "pkcs8",
        encoding: "base64",
      });

      // Sign JWT
      const jwt = await new jose.SignJWT(payload)
        .setProtectedHeader({ alg: 'ES256', typ: 'JWT' })
        .sign(ecKey);

      console.log(jwt);
    })();
    ```

    Finally, compile and run the script to generate the JWT output and export it as an environment variable:

    ```bash lines wrap theme={null}
    tsc generate_wallet_jwt.ts
    export WALLET_AUTH_JWT=$(npx ts-node generate_wallet_jwt.t)
    echo $WALLET_AUTH_JWT
    ```
  </Tab>

  <Tab title="Python">
    First, install required dependencies:

    ```bash lines wrap theme={null}
    pip install PyJWT==2.8.0
    pip install cryptography==42.0.5
    ```

    Create a new file to generate your Wallet Token:

    ```python generate_wallet_jwt.py lines wrap [expandable] theme={null}
    import jwt
    import time
    import uuid
    import os
    import json
    import hashlib
    import base64
    from cryptography.hazmat.primitives import serialization

    # Get environment variables
    wallet_secret = os.getenv('WALLET_SECRET')
    request_method = os.getenv('REQUEST_METHOD')
    request_host = os.getenv('REQUEST_HOST')
    request_path = os.getenv('REQUEST_PATH')
    request_body = json.loads(os.getenv('REQUEST_BODY'))

    # Create the JWT payload
    now = int(time.time())
    uri = f"{request_method} {request_host}{request_path}"

    payload = {
        'iat': now,
        'nbf': now,
        'jti': str(uuid.uuid4()),
        'uris': [uri]
    }

    def sort_keys(obj: dict) -> dict:
        if not obj or not isinstance(obj, dict | list):
            return obj

        if isinstance(obj, list):
            return [sort_keys(item) for item in obj]

        return {key: sort_keys(obj[key]) for key in sorted(obj.keys())}

    # Add request body if present
    if request_body:
        sorted_body = sort_keys(request_body)
        json_bytes = json.dumps(sorted_body, separators=(",", ":"), sort_keys=True).encode("utf-8")
        payload['reqHash'] = hashlib.sha256(json_bytes).hexdigest()

    der_bytes = serialization.load_der_private_key(
        base64.b64decode(wallet_secret), password=None
    )

    token = jwt.encode(
        payload,
        der_bytes,
        algorithm="ES256",
        headers={"typ": "JWT"},
    )

    print(token)
    ```

    Finally, run the script to generate the JWT output and export it as an environment variable:

    ```bash lines wrap theme={null}
    # Generate and export the JWT
    export WALLET_AUTH_JWT=$(python generate_wallet_jwt.py)
    echo $WALLET_AUTH_JWT
    ```
  </Tab>

  <Tab title="Go">
    First, install required dependencies:

    ```bash lines wrap theme={null}
    go mod init wallet-jwt-example
    go get github.com/golang-jwt/jwt/v5
    go get github.com/sirupsen/logrus
    ```

    Create a new file to generate your Wallet Token:

    ```go generate_wallet_jwt.go lines wrap [expandable] theme={null}
    package main

    import (
        "crypto/rand"
        "crypto/sha256"
        "crypto/x509"
        "encoding/base64"
        "encoding/json"
        "fmt"
        "os"
        "sort"
        "time"

        "github.com/golang-jwt/jwt/v5"
        log "github.com/sirupsen/logrus"
    )

    func sortKeys(v interface{}) interface{} {
        switch val := v.(type) {
        case map[string]interface{}:
            sorted := make(map[string]interface{}, len(val))
            keys := make([]string, 0, len(val))
            for k := range val {
                keys = append(keys, k)
            }
            sort.Strings(keys)
            for _, k := range keys {
                sorted[k] = sortKeys(val[k])
            }
            return sorted
        case []interface{}:
            for i, elem := range val {
                val[i] = sortKeys(elem)
            }
            return val
        default:
            return val
        }
    }

    func generateWalletJWT() (string, error) {
        // Get wallet secret from environment variable
        walletSecret := os.Getenv("WALLET_SECRET")
        if walletSecret == "" {
            return "", fmt.Errorf("WALLET_SECRET environment variable is required")
        }

        derBytes, err := base64.StdEncoding.DecodeString(walletSecret)
        if err != nil {
            return "", fmt.Errorf("failed to base64-decode WALLET_SECRET: %w", err)
        }

        privateKey, err := x509.ParsePKCS8PrivateKey(derBytes)
        if err != nil {
            return "", fmt.Errorf("failed to parse EC private key: %w", err)
        }

        // Get request details from environment variables
        requestMethod := os.Getenv("REQUEST_METHOD")
        requestHost := os.Getenv("REQUEST_HOST")
        requestPath := os.Getenv("REQUEST_PATH")
        requestBody := os.Getenv("REQUEST_BODY")

        uri := fmt.Sprintf("%s %s%s", requestMethod, requestHost, requestPath)

        jti := make([]byte, 16)
        if _, err := rand.Read(jti); err != nil {
            return "", fmt.Errorf("failed to generate JTI: %w", err)
        }

        now := time.Now().Unix()
    	claims := jwt.MapClaims{
            "iat":  now,
            "nbf":  now,
            "jti":  fmt.Sprintf("%x", jti),
            "uris": []string{uri},
        }

        // Add request body if present
        if requestBody != "" {
            var body interface{}
            if err := json.Unmarshal([]byte(requestBody), &body); err != nil {
                return "", fmt.Errorf("failed to parse request body: %w", err)
            }

            sorted := sortKeys(body)

            canonicalJSON, err := json.Marshal(sorted)
            if err != nil {
                return "", fmt.Errorf("failed to marshal sorted request body: %w", err)
            }

            hash := sha256.Sum256(canonicalJSON)
            claims["reqHash"] = fmt.Sprintf("%x", hash[:])
        }

        // Create token with claims
        token := jwt.NewWithClaims(jwt.SigningMethodES256, claims)
        token.Header["typ"] = "JWT"
        token.Header["alg"] = "ES256"

        // Sign and serialize the JWT
        jwtString, err := token.SignedString(privateKey)
        if err != nil {
            return "", fmt.Errorf("failed to sign JWT: %w", err)
        }

        return jwtString, nil
    }

    func main() {
        token, err := generateWalletJWT()
        if err != nil {
            log.Errorf("error generating wallet JWT: %v", err)
            os.Exit(1)
        }
        fmt.Println(token)
    }
    ```

    Run the following to clean up your dependencies:

    ```bash lines wrap theme={null}
    go mod tidy
    ```

    Finally, run the script to generate the JWT output and export it as an environment variable:

    ```bash lines wrap theme={null}
    export WALLET_AUTH_JWT=$(go run generate_wallet_jwt.go)
    echo $WALLET_AUTH_JWT
    ```
  </Tab>

  <Tab title="Ruby">
    First, install required dependencies:

    ```bash lines wrap theme={null}
    gem install jwt
    gem install openssl
    ```

    Create a new file to generate your Wallet Token:

    ```ruby generate_wallet_jwt.rb lines wrap [expandable] theme={null}
    require 'digest'
    require 'jwt'
    require 'json'
    require 'securerandom'

    # Get environment variables
    wallet_secret = ENV['WALLET_SECRET']
    request_method = ENV['REQUEST_METHOD']
    request_host = ENV['REQUEST_HOST']
    request_path = ENV['REQUEST_PATH']
    request_body = ENV['REQUEST_BODY']

    # Create the JWT payload
    now = Time.now.to_i
    uri = "#{request_method} #{request_host}#{request_path}"

    payload = {
      iat: now,
      nbf: now,
      jti: SecureRandom.uuid,
      uris: [uri]
    }

    def sort_keys(obj)
      case obj
      when Hash
        sorted = obj.keys.sort.each_with_object({}) do |key, result|
          result[key] = sort_keys(obj[key])
        end
        sorted
      when Array
        obj.map { |e| sort_keys(e) }
      else
        obj
      end
    end

    # Add request body if present
    if request_body
      parsed_body = JSON.parse(request_body)
      sorted_body = sort_keys(parsed_body)

      canonical_json = JSON.generate(sorted_body)
      req_hash = Digest::SHA256.hexdigest(canonical_json)

      payload[:reqHash] = req_hash
    end

    # Generate the JWT
    token = JWT.encode(payload, wallet_secret, 'ES256', { typ: 'JWT' })

    puts token
    ```

    Finally, run the script to generate the JWT output and export it as an environment variable:

    ```bash theme={null}
    ruby generate_wallet_jwt.rb
    export WALLET_AUTH_JWT=$(ruby generate_wallet_jwt.rb)
    echo $WALLET_AUTH_JWT
    ```
  </Tab>

  <Tab title="PHP">
    First, install required dependencies:

    ```bash lines wrap theme={null}
    composer require firebase/php-jwt
    ```

    Create a new file to generate your Wallet Token:

    ```php generate_wallet_jwt.php lines wrap [expandable] theme={null}
    <?php
    require 'vendor/autoload.php';
    use Firebase\JWT\JWT;

    function sortKeys($data) {
        if (is_array($data)) {
            if (array_keys($data) !== range(0, count($data) - 1)) {
                ksort($data);
            }
            foreach ($data as $key => $value) {
                $data[$key] = sortKeys($value);
            }
        }
        return $data;
    }

    function generateWalletJWT() {
        // Get environment variables
        $walletSecret = getenv('WALLET_SECRET');
        $requestMethod = getenv('REQUEST_METHOD');
        $requestHost = getenv('REQUEST_HOST');
        $requestPath = getenv('REQUEST_PATH');
        $requestBody = getenv('REQUEST_BODY');

        // Ensure required environment variables are set
        if (!$walletSecret || !$requestMethod || !$requestHost || !$requestPath) {
            throw new Exception('Required environment variables are missing');
        }

        // Create the URI
        $uri = $requestMethod . ' ' . $requestHost . $requestPath;

        // Create the JWT payload
        $now = time();
        $payload = [
            'iat' => $now,
            'nbf' => $now,
            'jti' => bin2hex(random_bytes(16)),
            'uris' => [$uri]
        ];

        // Add request body if present
        if ($requestBody) {
            $parsedBody = json_decode($requestBody, true);
            $sortedBody = sortKeys($parsedBody);
            $canonicalJson = json_encode($sortedBody, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
            $reqHash = hash('sha256', $canonicalJson);
            $payload['reqHash'] = $reqHash;
        }

        // Generate the JWT
        return JWT::encode($payload, $walletSecret, 'ES256', null, ['typ' => 'JWT']);
    }

    try {
        $token = generateWalletJWT();
        echo $token;
    } catch (Exception $e) {
        echo "Error generating JWT: " . $e->getMessage();
    }
    ```

    Finally, run the script to generate the JWT output and export it as an environment variable:

    ```bash lines wrap theme={null}
    php generate_wallet_jwt.php
    export WALLET_AUTH_JWT=$(php generate_wallet_jwt.php)
    echo $WALLET_AUTH_JWT
    ```
  </Tab>

  <Tab title="Java">
    First, install required dependencies:

    ```xml lines wrap theme={null}
    <!-- Add these to your pom.xml -->
    <dependencies>
        <dependency>
            <groupId>com.nimbusds</groupId>
            <artifactId>nimbus-jose-jwt</artifactId>
            <version>9.31</version>
        </dependency>
        <dependency>
            <groupId>org.bouncycastle</groupId>
            <artifactId>bcprov-jdk15on</artifactId>
            <version>1.70</version>
        </dependency>
        <dependency>
            <groupId>com.fasterxml.jackson.core</groupId>
            <artifactId>jackson-databind</artifactId>
            <version>2.17.0</version>
        </dependency>
    </dependencies>
    ```

    Create a new file to generate your Wallet Token:

    ```java GenerateWalletJWT.java lines wrap [expandable] theme={null}
    import com.nimbusds.jose.*;
    import com.nimbusds.jose.crypto.*;
    import com.nimbusds.jwt.*;
    import java.security.SecureRandom;
    import java.security.MessageDigest;
    import java.util.*;
    import java.time.Instant;
    import org.bouncycastle.jce.provider.BouncyCastleProvider;
    import java.security.Security;
    import com.fasterxml.jackson.databind.ObjectMapper;
    import com.fasterxml.jackson.databind.SerializationFeature;
    import com.fasterxml.jackson.databind.node.ObjectNode;
    import com.fasterxml.jackson.databind.JsonNode;
    import java.nio.charset.StandardCharsets;

    public class GenerateWalletJWT {
        public static void main(String[] args) throws Exception {
            // Register BouncyCastle as a security provider
            Security.addProvider(new BouncyCastleProvider());

            // Get environment variables
            String walletSecret = System.getenv("WALLET_SECRET");
            String requestMethod = System.getenv("REQUEST_METHOD");
            String requestHost = System.getenv("REQUEST_HOST");
            String requestPath = System.getenv("REQUEST_PATH");
            String requestBody = System.getenv("REQUEST_BODY");

            // Ensure all environment variables are provided
            if (walletSecret == null || requestMethod == null || requestHost == null || requestPath == null) {
                throw new IllegalArgumentException("Required environment variables are missing");
            }

            // Create header
            JWSHeader header = new JWSHeader.Builder(JWSAlgorithm.ES256)
                .type(JOSEObjectType.JWT)
                .build();

            // Create URI
            String uri = requestMethod + " " + requestHost + requestPath;

            // Create claims
            JWTClaimsSet.Builder claimsBuilder = new JWTClaimsSet.Builder()
                .issueTime(Date.from(Instant.now()))
                .notBeforeTime(Date.from(Instant.now()))
                .jwtID(generateJTI());

            // Add URIs
            claimsBuilder.claim("uris", Collections.singletonList(uri));

            ObjectMapper mapper = new ObjectMapper();
            mapper.configure(SerializationFeature.ORDER_MAP_ENTRIES_BY_KEYS, true);

            // Add request body if present
            if (requestBody != null && !requestBody.isEmpty()) {
                JsonNode parsedBody = mapper.readTree(requestBody);
                JsonNode sortedBody = sortJson(parsedBody);

                // Serialize to canonical JSON
                String canonicalJson = mapper.writeValueAsString(sortedBody);

                // Compute SHA-256 hash
                MessageDigest digest = MessageDigest.getInstance("SHA-256");
                byte[] hashBytes = digest.digest(canonicalJson.getBytes(StandardCharsets.UTF_8));
                StringBuilder sb = new StringBuilder();
                for (byte b : hashBytes) {
                    sb.append(String.format("%02x", b));
                }
                String reqHash = sb.toString();

                claimsBuilder.claim("reqHash", reqHash);
            }

            JWTClaimsSet claims = claimsBuilder.build();

            // Create JWT
            SignedJWT signedJWT = new SignedJWT(header, claims);

            // Create signer
            JWSSigner signer = new MACSigner(walletSecret.getBytes());

            // Sign the JWT
            signedJWT.sign(signer);

            // Serialize the JWT
            String jwtString = signedJWT.serialize();
            System.out.println(jwtString);
        }

        private static JsonNode sortJson(JsonNode node) {
            if (node.isObject()) {
                TreeMap<String, JsonNode> sorted = new TreeMap<>();
                node.fields().forEachRemaining(entry ->
                    sorted.put(entry.getKey(), sortJson(entry.getValue()))
                );
                ObjectNode sortedNode = new ObjectMapper().createObjectNode();
                sorted.forEach(sortedNode::set);
                return sortedNode;
            } else if (node.isArray()) {
                for (int i = 0; i < node.size(); i++) {
                    ((ObjectNode) node).set(String.valueOf(i), sortJson(node.get(i)));
                }
            }
            return node;
        }

        private static String generateJTI() {
            SecureRandom random = new SecureRandom();
            byte[] bytes = new byte[16];
            random.nextBytes(bytes);
            return Base64.getUrlEncoder().withoutPadding().encodeToString(bytes);
        }
    }
    ```

    Finally, compile and run the script to generate the JWT output and export it as an environment variable:

    ```bash lines wrap theme={null}
    mvn compile
    export WALLET_AUTH_JWT=$(mvn exec:java -Dexec.mainClass=GenerateWalletJWT)
    echo $WALLET_AUTH_JWT
    ```
  </Tab>

  <Tab title="C++">
    First, install required dependencies:

    ```bash lines wrap theme={null}
    # For Ubuntu/Debian
    sudo apt-get install libssl-dev libjwt-dev libcurl4-openssl-dev

    # For MacOS
    brew install openssl jwt-cpp curl
    ```

    Create a new file to generate your Wallet Token:

    ```cpp generate_wallet_jwt.cpp lines wrap [expandable] theme={null}
    #include <iostream>
    #include <string>
    #include <cstdlib>
    #include <ctime>
    #include <random>
    #include <jwt-cpp/jwt.h>
    #include <nlohmann/json.hpp>
    #include "picosha2.h"

    nlohmann::json sort_json(const nlohmann::json& j) {
        if (j.is_object()) {
            nlohmann::json result(nlohmann::json::value_t::object);
            std::vector<std::string> keys;
            for (auto it = j.begin(); it != j.end(); ++it) {
                keys.push_back(it.key());
            }
            std::sort(keys.begin(), keys.end());
            for (const auto& key : keys) {
                result[key] = sort_json(j.at(key));
            }
            return result;
        } else if (j.is_array()) {
            nlohmann::json result = nlohmann::json::array();
            for (const auto& el : j) {
                result.push_back(sort_json(el));
            }
            return result;
        } else {
            return j;
        }
    }

    std::string generateWalletJWT() {
        // Get environment variables
        const char* walletSecret = std::getenv("WALLET_SECRET");
        const char* requestMethod = std::getenv("REQUEST_METHOD");
        const char* requestHost = std::getenv("REQUEST_HOST");
        const char* requestPath = std::getenv("REQUEST_PATH");
        const char* requestBody = std::getenv("REQUEST_BODY");

        // Ensure all environment variables are present
        if (!walletSecret || !requestMethod || !requestHost || !requestPath) {
            throw std::runtime_error("Missing required environment variables");
        }

        std::string uri = std::string(requestMethod) + " " + std::string(requestHost) + std::string(requestPath);

        // Generate a random JTI
        std::random_device rd;
        std::mt19937 gen(rd());
        std::uniform_int_distribution<> dis(0, 15);
        std::string jti;
        for (int i = 0; i < 32; i++) {
            jti += "0123456789abcdef"[dis(gen)];
        }

        // Get current time
        auto now = std::chrono::system_clock::now();
        auto now_seconds = std::chrono::duration_cast<std::chrono::seconds>(now.time_since_epoch()).count();

        // Create JWT token
        auto token = jwt::create()
            .set_issued_at(now)
            .set_not_before(now)
            .set_payload_claim("jti", jwt::claim(jti))
            .set_payload_claim("uris", jwt::claim(std::vector<std::string>{uri}));

        // Add request body if present
        if (requestBody) {
            nlohmann::json body = nlohmann::json::parse(requestBody);
            nlohmann::json sortedBody = sort_json(body);
            std::string canonicalJson = sortedBody.dump();
            std::string hash = picosha2::hash256_hex_string(canonicalJson);
            token.set_payload_claim("reqHash", jwt::claim(hash));
        }

        // Sign and get the token
        return token.sign(jwt::algorithm::es256(walletSecret));
    }

    int main() {
        try {
            std::string token = generateWalletJWT();
            std::cout << token << std::endl;
        } catch (const std::exception& e) {
            std::cerr << "Error: " << e.what() << std::endl;
            return 1;
        }
        return 0;
    }
    ```

    Finally, compile and run the script to generate the JWT output and export it as an environment variable:

    ```bash lines wrap   theme={null}
    g++ generate_wallet_jwt.cpp -o wallet_jwt -lcurlpp -lcurl -lssl -lcrypto -I/usr/local/include -L/usr/local/lib -ljwt -std=c++17
    export WALLET_AUTH_JWT=$(./wallet_jwt)
    echo $WALLET_AUTH_JWT
    ```
  </Tab>

  <Tab title="C#">
    First, install required dependencies:

    ```bash lines wrap theme={null}
    dotnet add package System.IdentityModel.Tokens.Jwt
    dotnet add package BouncyCastle.NetCore
    dotnet add package Microsoft.IdentityModel.Tokens
    ```

    Create a new file to generate your Wallet Token:

    ```csharp GenerateWalletJWT.cs lines wrap [expandable] theme={null}
    using System;
    using System.Collections.Generic;
    using System.IdentityModel.Tokens.Jwt;
    using System.Linq;
    using System.Security.Cryptography;
    using Microsoft.IdentityModel.Tokens;
    using System.Text;
    using System.Text.Json;
    using System.Text.Json.Nodes;

    namespace WalletJWT
    {
        internal class Program
        {
            static void Main(string[] args)
            {
                // Get environment variables
                string walletSecret = Environment.GetEnvironmentVariable("WALLET_SECRET");
                string requestMethod = Environment.GetEnvironmentVariable("REQUEST_METHOD");
                string requestHost = Environment.GetEnvironmentVariable("REQUEST_HOST");
                string requestPath = Environment.GetEnvironmentVariable("REQUEST_PATH");
                string requestBody = Environment.GetEnvironmentVariable("REQUEST_BODY");

                // Validate environment variables
                if (string.IsNullOrEmpty(walletSecret) || string.IsNullOrEmpty(requestMethod) ||
                    string.IsNullOrEmpty(requestHost) || string.IsNullOrEmpty(requestPath))
                {
                    throw new InvalidOperationException("Missing required environment variables");
                }

                string token = GenerateWalletJWT(walletSecret, requestMethod, requestHost, requestPath, requestBody);
                Console.WriteLine(token);
            }

            static string GenerateWalletJWT(string walletSecret, string requestMethod, string requestHost, 
                string requestPath, string requestBody)
            {
                // Create the URI
                string uri = $"{requestMethod} {requestHost}{requestPath}";

                // Create security key
                var securityKey = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(walletSecret));
                var credentials = new SigningCredentials(securityKey, SecurityAlgorithms.HmacSha256);

                // Create header
                var header = new JwtHeader(credentials);
                header["typ"] = "JWT";

                // Create payload
                var now = DateTimeOffset.UtcNow;
                var payload = new JwtPayload
                {
                    { "iat", now.ToUnixTimeSeconds() },
                    { "nbf", now.ToUnixTimeSeconds() },
                    { "jti", GenerateJTI() },
                    { "uris", new[] { uri } }
                };

                // Add request body if present
                if (!string.IsNullOrEmpty(requestBody))
                {
                    JsonNode parsedBody = JsonNode.Parse(requestBody);

                    var sorted = SortJson(parsedBody);
                    string canonicalJson = sorted.ToJsonString(new JsonSerializerOptions
                    {
                        WriteIndented = false
                    });

                    using var sha256 = SHA256.Create();
                    var hashBytes = sha256.ComputeHash(Encoding.UTF8.GetBytes(canonicalJson));
                    string hashHex = BitConverter.ToString(hashBytes).Replace("-", "").ToLowerInvariant();

                    payload["reqHash"] = hashHex;
                }

                // Create and sign the token
                var token = new JwtSecurityToken(header, payload);
                var tokenHandler = new JwtSecurityTokenHandler();
                return tokenHandler.WriteToken(token);
            }

            static JsonNode SortJson(JsonNode node)
            {
                return node switch
                {
                    JsonObject obj => new JsonObject(
                        obj.OrderBy(kvp => kvp.Key)
                        .ToDictionary(
                            kvp => kvp.Key,
                            kvp => SortJson(kvp.Value)
                        )
                    ),
                    JsonArray arr => new JsonArray(arr.Select(SortJson).ToArray()),
                    _ => node
                };
            }

            // Method to generate a dynamic nonce
            static string GenerateJTI()
            {
                byte[] randomBytes = new byte[16];
                using (var rng = RandomNumberGenerator.Create())
                {
                    rng.GetBytes(randomBytes);
                }
                return Convert.ToBase64String(randomBytes)
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
    export WALLET_AUTH_JWT=$(dotnet run)
    echo $WALLET_AUTH_JWT
    ```
  </Tab>
</Tabs>

<Info>
  Wallet Tokens are valid for **1 minute**. After 1 minute, you will need to generate a new one.
  If you are experiencing issues, please make sure your machine's clock is accurate.
</Info>

<Note>
  The `req` claim in the wallet JWT is still supported for backwards compatibility with the [CDP SDK](https://github.com/coinbase/cdp-sdk), but `reqHash` is now the preferred way to include request body information.
  The `req` claim will eventually be deprecated - we recommend using `reqHash` for all new implementations.
</Note>

### 3. Authenticate

<Tip>
  Use our SDK for easier authentication
  The [CDP SDK](https://github.com/coinbase/cdp-sdk) automatically handles authentication for you, streamlining the process of making requests to all of our REST endpoints.
</Tip>

For endpoints that require wallet authentication (marked with the `X-Wallet-Auth` header requirement), you must include both:

1. The standard Bearer token in the `Authorization` header
2. The Wallet Authentication JWT in the `X-Wallet-Auth`

For example, to sign a transaction:

```bash lines wrap theme={null}