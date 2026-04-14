# create a SHA256 hmac with the secret key
hash = OpenSSL::HMAC.digest('sha256', @secret, string)