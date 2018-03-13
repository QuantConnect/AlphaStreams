using System;
using System.IO;
using System.Security.Cryptography;
using System.Text;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;

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

        public static AlphaCredentials FromConfiguration()
        {
            if (!File.Exists("config.json"))
            {
                throw new FileNotFoundException("Please specify 'alpha-credentials-path' in 'config.json'");
            }

            var config = JObject.Parse(File.ReadAllText("config.json"));
            var credentialsPath = config["alpha-credentials-path"];
            if (credentialsPath == null)
            {
                throw new Exception("Please specify 'alpha-credentials-path' in 'config.json'");
            }

            return FromFile(credentialsPath.Value<string>());
        }

        public static AlphaCredentials FromFile(string path)
        {
            if (!File.Exists(path))
            {
                throw new FileNotFoundException($"AlphaCredentials file not found: {new FileInfo(path).FullName}");
            }

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