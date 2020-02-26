using System;
using System.Collections.Generic;
using Newtonsoft.Json;
using QuantConnect.AlphaStream.Infrastructure;

namespace QuantConnect.AlphaStream.Models
{
    public class Tag
    {
        [JsonProperty("matches")]
        public int Matches { get; set; }

        [JsonProperty("tag")]
        public string TagName { get; set; }
    }
}
