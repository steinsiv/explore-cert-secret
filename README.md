# explore-cert-secret 

Simple explore code using certificates over `client_secret` in the leg2 of OAuth2 authorization code exchange. Assertion is here a signed JWT.

## Create certificate

#### 1. Create private key, here encrypted with AES256
```sh
❯ openssl genrsa -aes256 -out mysimplecert.key 2048
```

#### 2. Create self signed certificate X.509 (creating and processing CSR). SHA256 digest will be signed.
```sh
❯ openssl req -x509 -key mysimplecert.key -sha256 -days 365 -out mysimplecert.crt -subj "/CN=MySimpleAppCert"
```

#### 3. Checking cert and SHA1 thumbprint
```sh
❯ openssl x509 -in mysimplecert.crt -text -noout
❯ openssl x509 -in mysimplecert.crt -noout -sha1 -fingerprint
```

## Upload certificate to Azure 

`App-Registrations -> Certificates & Secrets`

Upload `mysimplecert.crt`, verify thumbprint, and remember to check redirect URL for the application.

The code in leg 2, `main.py` assumes you have an authorization code already

## LEG 1: Get authorization code

Visit URL in browser:
```ts
https://login.microsoftonline.com/<TENANT_ID>/oauth2/v2.0/authorize
?client_id=<CLIENT_ID>
&response_type=code
&redirect_uri=<REDIRECT_URL>
&response_mode=query
&scope=<SCOPE>
&state=123456789
```

Make note of the authorization code in redirect. To be used in leg 2.

## LEG 2: Get tokens

See `main.py` for retrieving tokens using certificate instead of `client_secret`

```sh
❯ pip install -r requirements.txt
❯ python main.py

 access_token = 'eyJ0...'
{
    "token_type": "Bearer",
    "scope": "openid profile email",
    "expires_in": 3860,
    "ext_expires_in": 3860,
    "access_token": "eyJ0...",
    "id_token": "eyJ0..."
}
```

# Refs
https://security.stackexchange.com/questions/262630/oauth2-what-is-the-advantage-of-using-certificate-over-client-secret-credentia  
https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-client-creds-grant-flow#second-case-access-token-request-with-a-certificate  
https://learn.microsoft.com/en-us/entra/identity-platform/certificate-credentials
