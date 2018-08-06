from AlphaStreamClient import AlphaStreamClient
from Requests.GetAlphaByIdRequest import GetAlphaByIdRequest

# Initialize credentials
clientId = "c7bd966e930c4b15b2ec13eb0d6170d9"	
token   = "7bc6c200f6084eba41f248468653e2f32066748a384fb1778199b4c12e263f0b68cd44be414fa8d6d73863e659e0a44bb20a77b107a90f40886429c6f360568b"	
alphaId = "392a40ccab3740287a1c30bc6" 

# Create the Alpha Streams SDKs	
api = AlphaStreamClient(clientId, token)

print(api.Execute(GetAlphaByIdRequest(alphaId)))
