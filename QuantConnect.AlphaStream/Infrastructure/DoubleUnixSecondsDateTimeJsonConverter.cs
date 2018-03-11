using System;
using Newtonsoft.Json;

namespace QuantConnect.AlphaStream.Infrastructure
{
    /// <summary>
    /// Defines a <see cref="JsonConverter"/> that serializes <see cref="DateTime"/> use the number of whole and fractional seconds since unix epoch
    /// </summary>
    public class DoubleUnixSecondsDateTimeJsonConverter : TypeChangeJsonConverter<DateTime?, double?>
    {
        private static readonly DateTime UnixEpoch = new DateTime(1970, 1, 1, 0, 0, 0, DateTimeKind.Utc);

        /// <summary>
        /// Determines whether this instance can convert the specified object type.
        /// </summary>
        /// <param name="objectType">Type of the object.</param>
        /// <returns>
        /// <c>true</c> if this instance can convert the specified object type; otherwise, <c>false</c>.
        /// </returns>
        public override bool CanConvert(Type objectType)
        {
            return objectType == typeof(DateTime)
                || objectType == typeof(DateTime?);
        }

        /// <summary>
        /// Convert the input value to a value to be serialzied
        /// </summary>
        /// <param name="value">The input value to be converted before serialziation</param>
        /// <returns>A new instance of TResult that is to be serialzied</returns>
        protected override double? Convert(DateTime? value)
        {
            if (value == null)
            {
                return null;
            }

            return (value.Value - UnixEpoch).TotalSeconds;
        }

        /// <summary>
        /// Converts the input value to be deserialized
        /// </summary>
        /// <param name="value">The deserialized value that needs to be converted to T</param>
        /// <returns>The converted value</returns>
        protected override DateTime? Convert(double? value)
        {
            if (value == null)
            {
                return null;
            }

            return UnixEpoch.AddSeconds(value.Value);
        }
    }
}