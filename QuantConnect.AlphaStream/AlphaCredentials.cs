using System.IO;
using System.Security.Cryptography;
using System.Text;
using Newtonsoft.Json;

namespace QuantConnect.AlphaStream
{
    public class AlphaCredentials
    {
        [JsonProperty("client-id")]
        public string ClientId { get; }

        [JsonProperty("api-token")]
        public string ApiToken { get; }

        public AlphaCredentials(string clientId, string apiToken)
        {
            ClientId = clientId;
            ApiToken = apiToken;
        }

        public string CreateSecureHash(long stamp)
        {
            return ToSHA256($"{ApiToken}:{stamp}");
        }

        public static AlphaCredentials FromFile(string path)
        {
            return JsonConvert.DeserializeObject<AlphaCredentials>(File.ReadAllText(path));
        }

        private static string ToSHA256(string data)
        {
            var crypt = new SHA256Managed();
            var hash = new StringBuilder();
            var crypto = crypt.ComputeHash(Encoding.UTF8.GetBytes(data), 0, Encoding.UTF8.GetByteCount(data));
            foreach (var theByte in crypto)
            {
                hash.Append(theByte.ToString("x2"));
            }
            return hash.ToString();
        }
    }
}