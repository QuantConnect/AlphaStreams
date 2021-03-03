using System;
using QuantConnect.AlphaStream.Models;

namespace QuantConnect.AlphaStream
{
    /// <summary>
    /// Event arguments fired when a new insight is received by the streaming client
    /// </summary>
    public class InsightReceivedEventArgs : EventArgs
    {
        /// <summary>
        /// Gets the alpha id that produced the insight
        /// </summary>
        public string AlphaId { get; }

        /// <summary>
        /// Gets the insight
        /// </summary>
        public AlphaStreamInsight Insight { get; }

        /// <summary>
        /// Initializes a new instance of the <see cref="InsightReceivedEventArgs"/> class
        /// </summary>
        /// <param name="alphaId">The alpha id tht produced the insight</param>
        /// <param name="insight">The insight</param>
        public InsightReceivedEventArgs(string alphaId, AlphaStreamInsight insight)
        {
            AlphaId = alphaId;
            Insight = insight;
        }
    }
}