using Newtonsoft.Json;
using QuantConnect.AlphaStream.Infrastructure;
using System;
using System.Collections.Generic;

namespace QuantConnect.AlphaStream.Models
{
    public class EquityCurve
    {
        public Dictionary<DateTime, double, string> Equity { get; set; }

        //public List<double> Equity { get; set; }

        //public List<string> Sample { get; set; }
    }
}