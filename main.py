import jwt
import json
import requests
from time import time
from uuid import uuid4
from base64 import b64encode
from cryptography.hazmat.primitives import serialization

# These are the values you need to set before running this script
TENANT_ID=""
CLIENT_ID=""
THUMBPRINT=""
AUTHORIZATION_CODE=""
REDIRECT_URI="http://localhost/callback"

CERT_X5T=b64encode(bytes.fromhex(THUMBPRINT)).decode("utf-8") 

token_url = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token" # OAuth provider's token endpoint

def private_key():
    with open("mysimplecert.key", "rb") as key_file:
        private_key = serialization.load_pem_private_key( key_file.read(), password=b"1234" )
    return private_key

# make sure x5t corresponds with the cert credentials uploaded for the application in Azure, and that it is BASE64 encoded
# openssl x509 -in mysimplecert.crt -noout -sha1 -fingerprint | cut -d '=' -f2 | tr -d ':' | xxd -r -p | base64
headers = {
    "alg": "RS256",
    "typ": "JWT",
    "x5t": CERT_X5T
    }

claims = {
    "aud": token_url,
    "exp": int(time()) + 10*60,  # Token expiry time (10 minutes)
    "iss": CLIENT_ID,
    "jti": uuid4().hex,
    "sub": CLIENT_ID,
    "iat": int(time()),
}

# Create and sign the JWT
encoded_jwt = jwt.encode(claims, private_key(), algorithm="RS256", headers=headers)

# Body parameters for the token POST request
data = {
    "grant_type": "authorization_code",
    "code": AUTHORIZATION_CODE,
    "redirect_uri": REDIRECT_URI,
    "client_assertion_type": "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
    "client_assertion": encoded_jwt
}

# Make the request and print the response
response = requests.post(token_url, data=data)
if response.status_code == 200:
    print(json.dumps(response.json(), indent=4))
else:
    print(f"Error: {response.status_code}, Description: {response.text}")
