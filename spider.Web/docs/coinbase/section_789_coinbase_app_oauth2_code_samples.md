# Coinbase App OAuth2 Code Samples
Source: https://docs.cdp.coinbase.com/coinbase-app/oauth2-integration/oauth2-code-samples



This guide will show samples in different languages for our Coinbase App OAuth2 flow. It assumes that you have already [created an OAuth client](/coinbase-app/oauth2-integration/integrations) on the [Coinbase Developer Platform](https://portal.cdp.coinbase.com).

<Info>
  Remember to include your **RedirectURI** within your OAuth2 client in order for a redirect to take place after the user has completed their OAuth2 step.
</Info>

<Tabs>
  <Tab title="Go">
    1. Create a new directory and generate a Go file called `main.go`.
    2. Paste the Go snippet below into `main.go`.
    3. Run `go run main.go`
    4. Visit `http://localhost:8000/login` (for this example)
    5. Go through OAuth2 process and confirm you're being redirected to `http://localhost:8000/callback` (for this example)

    ```go lines wrap [expandable] theme={null}
    package main

    import (
    	"crypto/rand"
    	"crypto/sha256"
    	"encoding/base64"
    	"encoding/json"
    	"fmt"
    	"log"
    	"net/http"
    	"net/url"
    )

    // Replace these with your Coinbase App credentials and desired configuration.
    var (
    	clientID     = "YOUR_CLIENT_ID"
    	clientSecret = "YOUR_CLIENT_SECRET"
    	// Make sure your redirect URI is registered with your OAuth2 client.
    	redirectURI = "http://localhost:8000/callback"
    	// Coinbase OAuth2 endpoints
    	authURL  = "https://login.coinbase.com/oauth2/auth"
    	tokenURL = "https://login.coinbase.com/oauth2/token"
    )

    // TokenResponse models the response received after exchanging the code.
    type TokenResponse struct {
    	AccessToken  string `json:"access_token"`
    	TokenType    string `json:"token_type"`
    	ExpiresIn    int    `json:"expires_in"`
    	RefreshToken string `json:"refresh_token"`
    	Scope        string `json:"scope"`
    }

    func main() {
    	http.HandleFunc("/login", loginHandler)
    	http.HandleFunc("/callback", callbackHandler)

    	log.Println("Starting server on :8000")
    	log.Fatal(http.ListenAndServe(":8000", nil))
    }

    // loginHandler initiates the OAuth2 flow.
    func loginHandler(w http.ResponseWriter, r *http.Request) {
    	state, err := generateState()
    	if err != nil {
    		http.Error(w, "Error generating state", http.StatusInternalServerError)
    		return
    	}

    	// Generate PKCE parameters for additional security
    	codeVerifier, err := generateCodeVerifier()
    	if err != nil {
    		http.Error(w, "Error generating code verifier", http.StatusInternalServerError)
    		return
    	}
    	codeChallenge := generateCodeChallenge(codeVerifier)

    	// For demo purposes, we store the state and code verifier in cookies.
    	http.SetCookie(w, &http.Cookie{
    		Name:  "oauthstate",
    		Value: state,
    		Path:  "/",
    	})
    	http.SetCookie(w, &http.Cookie{
    		Name:  "code_verifier",
    		Value: codeVerifier,
    		Path:  "/",
    	})

    	// Build the authorization URL.
    	params := url.Values{}
    	params.Add("response_type", "code")
    	params.Add("client_id", clientID)
    	params.Add("redirect_uri", redirectURI)
    	// Adjust the scope as needed per Coinbase’s documentation.
    	params.Add("scope", "wallet:user:read")
    	params.Add("state", state)
    	params.Add("code_challenge", codeChallenge)
    	params.Add("code_challenge_method", "S256")

    	http.Redirect(w, r, authURL+"?"+params.Encode(), http.StatusFound)
    }

    // callbackHandler handles the OAuth2 callback and exchanges the code for an access token.
    func callbackHandler(w http.ResponseWriter, r *http.Request) {
    	// Retrieve state and code from the query parameters.
    	query := r.URL.Query()
    	state := query.Get("state")
    	code := query.Get("code")

    	// Validate the state using the stored cookie.
    	cookie, err := r.Cookie("oauthstate")
    	if err != nil || cookie.Value != state {
    		http.Error(w, "Invalid state", http.StatusBadRequest)
    		return
    	}

    	// Retrieve the code verifier from the cookie.
    	verifierCookie, err := r.Cookie("code_verifier")
    	if err != nil {
    		http.Error(w, "Missing code verifier", http.StatusBadRequest)
    		return
    	}

    	// Exchange the code for an access token.
    	token, err := exchangeCodeForToken(code, verifierCookie.Value)
    	if err != nil {
    		http.Error(w, fmt.Sprintf("Error exchanging token: %v", err), http.StatusInternalServerError)
    		return
    	}

    	// For demo purposes, we simply output the access token.
    	fmt.Fprintf(w, "Access token: %s\n", token.AccessToken)
    	fmt.Fprintf(w, "Refresh token: %s\n", token.RefreshToken)
    }

    // exchangeCodeForToken makes a POST request to Coinbase's token endpoint to exchange the authorization code for an access token.
    func exchangeCodeForToken(code, codeVerifier string) (*TokenResponse, error) {
    	data := url.Values{}
    	data.Set("grant_type", "authorization_code")
    	data.Set("code", code)
    	data.Set("redirect_uri", redirectURI)
    	data.Set("client_id", clientID)
    	data.Set("client_secret", clientSecret)
    	data.Set("code_verifier", codeVerifier)

    	resp, err := http.PostForm(tokenURL, data)
    	if err != nil {
    		return nil, err
    	}
    	defer resp.Body.Close()

    	var tokenRes TokenResponse
    	if err := json.NewDecoder(resp.Body).Decode(&tokenRes); err != nil {
    		return nil, err
    	}
    	return &tokenRes, nil
    }

    // generateState creates a random string to be used as the OAuth state parameter.
    func generateState() (string, error) {
    	b := make([]byte, 16)
    	_, err := rand.Read(b)
    	if err != nil {
    		return "", err
    	}
    	return fmt.Sprintf("%x", b), nil
    }

    // generateCodeVerifier creates a cryptographically random string for PKCE.
    func generateCodeVerifier() (string, error) {
    	b := make([]byte, 96) // 128 characters when base64url encoded
    	_, err := rand.Read(b)
    	if err != nil {
    		return "", err
    	}
    	return base64.RawURLEncoding.EncodeToString(b), nil
    }

    // generateCodeChallenge creates a code challenge from the code verifier using S256 method.
    func generateCodeChallenge(codeVerifier string) string {
    	hash := sha256.Sum256([]byte(codeVerifier))
    	return base64.RawURLEncoding.EncodeToString(hash[:])
    }
    ```
  </Tab>

  <Tab title="PHP">
    1. Create a new directory and generate a PHP file called `index.php`.
    2. Paste the PHP snippet below into `index.php`.
    3. Run `php -S localhost:8000`
    4. Visit `http://localhost:8000/index.php` (for this example)
    5. Go through OAuth2 process and confirm you're being redirected to `http://localhost:8000/index.php` (for this example)

    ```php lines wrap [expandable] theme={null}
    <?php
    session_set_cookie_params([
        'lifetime' => 0,
        'path' => '/',
        'domain' => 'localhost',
        'secure' => false,    // false since we're not using HTTPS on localhost
        'httponly' => true,   // helps prevent client-side access
    ]);

    session_start();

    // Coinbase App credentials and configuration
    $clientID     = 'YOUR_CLIENT_ID';
    $clientSecret = 'YOUR_CLIENT_SECRET';
    $redirectURI  = 'http://localhost:8000/index.php'; // Make sure this URI is registered in your Coinbase app
    $authURL      = 'https://login.coinbase.com/oauth2/auth';
    $tokenURL     = 'https://login.coinbase.com/oauth2/token';
    $scope        = 'wallet:user:read'; // Adjust the scope as needed

    // Check if this is the callback request
    if (isset($_GET['code'])) {
        // Validate the 'state' parameter to mitigate CSRF attacks
        if (!isset($_GET['state']) || !isset($_SESSION['oauth_state']) || $_GET['state'] !== $_SESSION['oauth_state']) {
            die("Invalid state parameter.");
        }

        $code = $_GET['code'];

        // Prepare data for token exchange
        $data = [
            'grant_type'    => 'authorization_code',
            'code'          => $code,
            'redirect_uri'  => $redirectURI,
            'client_id'     => $clientID,
            'client_secret' => $clientSecret,
    		'code_verifier' => $_SESSION['code_verifier'],
        ];

        // Initialize cURL to make a POST request
        $ch = curl_init($tokenURL);
        curl_setopt($ch, CURLOPT_POST, true);
        curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query($data));
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_HTTPHEADER, [
            'Content-Type: application/x-www-form-urlencoded'
        ]);

        $response = curl_exec($ch);
        if (curl_errno($ch)) {
            die('Error: ' . curl_error($ch));
        }
        curl_close($ch);

        // Decode the JSON response
        $tokenResponse = json_decode($response, true);
        if (isset($tokenResponse['error'])) {
            die("Error in token exchange: " . $tokenResponse['error_description']);
        }

        // Display the tokens (for demonstration purposes only)
        echo "Access Token: " . htmlspecialchars($tokenResponse['access_token']) . "<br>";
        if (isset($tokenResponse['refresh_token'])) {
            echo "Refresh Token: " . htmlspecialchars($tokenResponse['refresh_token']) . "<br>";
        }
        exit;
    } else {
        // No code parameter detected, so start the OAuth login flow

        // Generate a random state value for CSRF protection and store it in the session
        $state = bin2hex(random_bytes(16));
        $_SESSION['oauth_state'] = $state;
    	
    	// Generate PKCE parameters for additional security
        $codeVerifier = generateCodeVerifier();
        $codeChallenge = generateCodeChallenge($codeVerifier);
        $_SESSION['code_verifier'] = $codeVerifier;

        // Build the query parameters for the authorization URL
        $params = http_build_query([
            'response_type'         => 'code',
            'client_id'             => $clientID,
            'redirect_uri'          => $redirectURI,
            'scope'                 => $scope,
            'state'                 => $state,
            'code_challenge'        => $codeChallenge,
            'code_challenge_method' => 'S256',
        ]);

        // Redirect the user to Coinbase's OAuth authorization endpoint
        header("Location: $authURL?$params");
        exit;
    }

    // Generate a cryptographically random string for PKCE code verifier
    function generateCodeVerifier() {
        return rtrim(strtr(base64_encode(random_bytes(96)), '+/', '-_'), '=');
    }

    // Generate code challenge from code verifier using S256 method
    function generateCodeChallenge($codeVerifier) {
        return rtrim(strtr(base64_encode(hash('sha256', $codeVerifier, true)), '+/', '-_'), '=');
    }
    ?>
    ```
  </Tab>
</Tabs>

