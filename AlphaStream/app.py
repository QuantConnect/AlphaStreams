try:
    import AlphaStream
except ImportError:
    import os, sys
    from os.path import dirname 
    sys.path.append(dirname(dirname(__file__)))

from AlphaStream import AlphaStreamClient
from AlphaStream.Requests import GetAlphaByIdRequest

# For your user id and token, please visit your Fund Management Dashboard: https://www.quantconnect.com/alpha/democlient#api-access-tokens
clientId = "c7bd966e930c4b15b2ec13eb0d6170d9"	
token   = "7bc6c200f6084eba41f248468653e2f32066748a384fb1778199b4c12e263f0b68cd44be414fa8d6d73863e659e0a44bb20a77b107a90f40886429c6f360568b"	
alphaId = "392a40ccab3740287a1c30bc6" 

# Create the Alpha Streams SDKs	
api = AlphaStreamRestClient(clientId, token)

print(api.Execute(GetAlphaByIdRequest(alphaId)))
