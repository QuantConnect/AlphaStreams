using System;

namespace QuantConnect.AlphaStream.Infrastructure
{
    public static class Time
    {
        public static readonly DateTime UnixEpoch = new DateTime(1970, 1, 1, 0, 0, 0, DateTimeKind.Utc);

        public static long ToUnixTime(this DateTime utcNow)
        {
            var epoch = utcNow - UnixEpoch;
            return (long)epoch.TotalSeconds;
        }

        public static DateTime ToDateTime(this long stamp)
        {
            return UnixEpoch.AddSeconds(stamp);
        }
    }
}
