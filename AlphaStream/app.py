try:
    import AlphaStream
except ImportError:
    import os, sys
    from os.path import dirname 
    sys.path.append(dirname(dirname(__file__)))

from AlphaStream import AlphaStreamRestClient
from AlphaStream.Requests import GetAlphaByIdRequest

# For your user id and token, please visit your Fund Management Dashboard: https://www.quantconnect.com/alpha/democlient#api-access-tokens
clientId = "c7bd966e930c4b15b2ec13eb0d6170d9"	
token = "7030e89cfcc1948f4f93e91edd93d6f687c737844a6969d99d609a78f8d0a5c4091ef11f31c4c0e9cccacefe36ff4c2ad0e15525a85c65b0eafa34064cd11b1c"
alphaId = "d0fc88b1e6354fe95eb83225a"

# Create the Alpha Streams SDKs	
api = AlphaStreamRestClient(clientId, token)

print(api.Execute(GetAlphaByIdRequest(alphaId)))
