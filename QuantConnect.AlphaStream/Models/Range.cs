using System;

namespace QuantConnect.AlphaStream.Models
{
    /// <summary>
    /// Provides factory methods for creating number and date ranges
    /// </summary>
    public static class Range
    {
        public static NumberRange<int> Create(int minimum, int maximum)
        {
            return new NumberRange<int>(minimum, maximum);
        }

        public static NumberRange<int> Create(int? minimum, int? maximum)
        {
            return new NumberRange<int>(minimum, maximum);
        }

        public static NumberRange<long> Create(long minimum, long maximum)
        {
            return new NumberRange<long>(minimum, maximum);
        }

        public static NumberRange<long> Create(long? minimum, long? maximum)
        {
            return new NumberRange<long>(minimum, maximum);
        }

        public static NumberRange<decimal> Create(decimal minimum, decimal maximum)
        {
            return new NumberRange<decimal>(minimum, maximum);
        }

        public static NumberRange<decimal> Create(decimal? minimum, decimal? maximum)
        {
            return new NumberRange<decimal>(minimum, maximum);
        }

        public static NumberRange<double> Create(double minimum, double maximum)
        {
            return new NumberRange<double>(minimum, maximum);
        }

        public static NumberRange<double> Create(double? minimum, double? maximum)
        {
            return new NumberRange<double>(minimum, maximum);
        }

        public static DateRange<DateTime> Create(DateTime minimum, DateTime maximum)
        {
            return new DateRange<DateTime>(minimum, maximum);
        }

        public static DateRange<DateTime> Create(DateTime? minimum, DateTime? maximum)
        {
            return new DateRange<DateTime>(minimum, maximum);
        }
    }
}