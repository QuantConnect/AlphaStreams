import AlphaStreams.AlphaStreamsClient
import AlphaStreams.Models.Alpha

# Initialize credentials
clientId    = "c7bd966e930c4b15b2ec13eb0d6170d9"
token       = "7bc6c200f6084eba41f248468653e2f32066748a384fb1778199b4c12e263f0b68cd44be414fa8d6d73863e659e0a44bb20a77b107a90f40886429c6f360568b"

# Create the Alpha Streams SDKs
api = AlphaStreamsClient(clientId, token)

print ( api.Execute(GetAlphaByIdRequest(id)) )

