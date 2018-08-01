using Newtonsoft.Json;
using Newtonsoft.Json.Converters;
using System.Runtime.Serialization;

namespace QuantConnect.AlphaStream.Models
{
    /// <summary>
    /// Alpha Status
    /// </summary>
    [JsonConverter(typeof(StringEnumConverter), true)]
    public enum AlphaStatus
    {
        /// <summary>
        /// Unknown status
        /// </summary>
        [EnumMember(Value = "")] Unknown,

        /// <summary>
        /// Running alpha model
        /// </summary>
        [EnumMember(Value = "running")] Running,

        /// <summary>
        /// Stopped alpha model
        /// </summary>
        [EnumMember(Value = "stopped")] Stopped
    }
}