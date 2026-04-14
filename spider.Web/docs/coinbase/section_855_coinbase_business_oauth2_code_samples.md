# Coinbase Business OAuth2 Code Samples
Source: https://docs.cdp.coinbase.com/coinbase-business/authentication-authorization/oauth2/oauth2-code-samples



This guide will show samples in different languages for our Coinbase Business OAuth2 flow. It assumes that you have already [created an OAuth client](/coinbase-business/authentication-authorization/oauth2/integrations) on the [Coinbase Developer Platform](https://portal.cdp.coinbase.com).

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
    	"encoding/json"
    	"fmt"
    	"log"
    	"net/http"
    	"net/url"
    )

    // Replace these with your Coinbase Business credentials and desired configuration.
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
    	// For demo purposes, we store the state in a cookie.
    	http.SetCookie(w, &http.Cookie{
    		Name:  "oauthstate",
    		Value: state,
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

    	// Exchange the code for an access token.
    	token, err := exchangeCodeForToken(code)
    	if err != nil {
    		http.Error(w, fmt.Sprintf("Error exchanging token: %v", err), http.StatusInternalServerError)
    		return
    	}

    	// For demo purposes, we simply output the access token.
    	fmt.Fprintf(w, "Access token: %s\n", token.AccessToken)
    	fmt.Fprintf(w, "Refresh token: %s\n", token.RefreshToken)
    }

    // exchangeCodeForToken makes a POST request to Coinbase's token endpoint to exchange the authorization code for an access token.
    func exchangeCodeForToken(code string) (*TokenResponse, error) {
    	data := url.Values{}
    	data.Set("grant_type", "authorization_code")
    	data.Set("code", code)
    	data.Set("redirect_uri", redirectURI)
    	data.Set("client_id", clientID)
    	data.Set("client_secret", clientSecret)

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

    // Coinbase Business credentials and configuration
    $clientID     = 'YOUR_CLIENT_ID';
    $clientSecret = 'YOUR_CLIENT_SECRET';
    $redirectURI  = 'http://localhost:8000/index.php'; // Make sure this URI is registered in your Coinbase Business app
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

        // Build the query parameters for the authorization URL
        $params = http_build_query([
            'response_type' => 'code',
            'client_id'     => $clientID,
            'redirect_uri'  => $redirectURI,
            'scope'         => $scope,
            'state'         => $state,
        ]);

        // Redirect the user to Coinbase's OAuth authorization endpoint
        header("Location: $authURL?$params");
        exit;
    }
    ?>
    ```
  </Tab>
</Tabs>

