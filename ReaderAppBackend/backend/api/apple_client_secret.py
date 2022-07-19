import time
import jwt
def get_client_secret():
    team_id = 'APR949UZ95'
    client_id = 'synesthesia.ReaderApp.client'
    # client_id = 'synesthesia.ReaderApp.client'
    key_id = 'GPD6T964V7'
    with open('apple_key.txt','r') as f:
        key = f.read()
    headers = {
    'alg':'ES256',
    'kid':key_id
    }
    claims = {
        'iss':team_id,
        'iat' : int(time.time()),
        'exp' : int(time.time() + 86400*180),
        'aud' : 'https://appleid.apple.com',
        'sub' : client_id,
    }
    client_secret = jwt.encode(claims, key, algorithm="ES256",headers=headers).decode('utf-8')
    return client_secret
print(get_client_secret())