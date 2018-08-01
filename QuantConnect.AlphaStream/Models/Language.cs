using Newtonsoft.Json;
using Newtonsoft.Json.Converters;
using System.Runtime.Serialization;

namespace QuantConnect.AlphaStream.Models
{
    /// <summary>
    /// Author preferred programming language.
    /// </summary>
    [JsonConverter(typeof(StringEnumConverter), true)]
    public enum Language
    {
        /// <summary>
        /// Unknown language
        /// </summary>
        [EnumMember(Value = "")] Unknown,

        /// <summary>
        /// C# programming language
        /// </summary>
        [EnumMember(Value = "C#")] CSharp,

        /// <summary>
        /// Python programming language
        /// </summary>
        [EnumMember(Value = "Py")] Python
    }
}