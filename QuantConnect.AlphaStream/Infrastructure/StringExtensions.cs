using System.Collections.Generic;
using System.IO;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;

namespace QuantConnect.AlphaStream.Infrastructure
{
    public static class StringExtensions
    {
        public static IEnumerable<string> AsLines(this string str)
        {
            using (var reader = new StringReader(str))
            {
                string line;
                while ((line = reader.ReadLine()) != null)
                {
                    yield return line;
                }
            }
        }

        public static string FormatAsJsonIfPossible(this string str)
        {
            try
            {
                var jToken = JToken.Parse(str);
                return jToken.ToString(Formatting.Indented);
            }
            catch
            {
                return str;
            }
        }
    }
}
