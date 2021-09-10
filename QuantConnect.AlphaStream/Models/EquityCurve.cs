using System;

namespace QuantConnect.AlphaStream.Models
{
    public class EquityCurve
    {
        /// <summary>
        /// Timestamp of equity curve point
        /// </summary>
        public DateTime Time { get; }

        /// <summary>
        /// Alpha Id. Unified equity curve has data of more than one version of an Alpha.
        /// </summary>
        public string Id { get; }

        /// <summary>
        /// Dollar value of the equity
        /// </summary>
        public double Equity { get; }

        /// <summary>
        /// Sample of equity point (in-sample or live-trading)
        /// </summary>
        public string Sample { get; }

        /// <summary>
        /// Creates a new instance of EquityCurve
        /// </summary>
        /// <param name="time">Timestamp of equity curve point</param>
        /// <param name="equity">Dollar value of the equity</param>
        /// <param name="sample">Sample of equity point (in-sample or live-trading)</param>
        /// <param name="id">Alpha Id. Unified equity curve has data of more than one version of an Alpha.</param>
        public EquityCurve(DateTime time, double equity, string sample, string id)
        {
            Time = time;
            Equity = equity;
            Sample = sample;
            Id = id;
        }

        /// <summary>
        /// Returns a string that represents the EquityCurve object
        /// </summary>
        /// <returns>A string that represents the EquityCurve object</returns>
        public override string ToString() => $"{Time},{Equity},{Sample},{Id}";
    }
}