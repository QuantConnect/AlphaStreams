using System;
using System.IO;
using Newtonsoft.Json.Linq;
using NUnit.Framework;

namespace QuantConnect.AlphaStream.Tests
{
    public static class Credentials
    {
        public static AlphaCredentials Test => LazyTestCredentials.Value;

        private static readonly Lazy<AlphaCredentials> LazyTestCredentials = new Lazy<AlphaCredentials>(() =>
        {
            var directory = TestContext.CurrentContext.TestDirectory;
            var path1 = Path.Combine(directory, "config.json");
            var contents = File.ReadAllText(path1);
            var config = JObject.Parse(contents);
            var credentialsPath = config["alpha-credentials-path"].Value<string>();
            var path = Path.Combine(directory, credentialsPath);
            return AlphaCredentials.FromFile(path);
        });
    }
}