import os, sys
import time
import requests
import pandas as pd
from datetime import datetime
from quantconnect.api import Api

class AlphaBacktest:
    def __init__(self, alpha_id, project_id, qc_user_id, qc_token, alpha_user_id, alpha_token):

        self.api = Api(qc_user_id, qc_token)
        self.project_id = project_id
        code = self.get_code(alpha_id, alpha_user_id, alpha_token)

        self.api.update_project_file_content(self.project_id, 'AlphaStreamsAPIFrameworkAlgorithm.cs', code)
        self.backtest_id = self.create_backtest()

        df = self.get_df('Charts','Strategy Equity','Series','Equity','Values')
        self.curve = ((df / df.iloc[0] - 1) * 100)

    def build_success(self):
        self.compile_id = self.api.create_compile(self.project_id).pop('compileId')
        return self.api.read_compile(self.project_id, self.compile_id)['state'] == 'BuildSuccess'
    
    def create_backtest(self):
        if self.build_success():
            now = str(datetime.utcnow())
            return self.api.create_backtest(self.project_id, self.compile_id, now).get('backtestId')
    
    def read_backest(self):
        if self.build_success() and self.backtest_id is not None:
            return self.api.read_backtest(self.project_id, self.backtest_id)

    def get_df(self, *args):
        result = self.read_backest()
        while not result['completed']:
            time.sleep(10)
            result = self.read_backest()

        df = pd.DataFrame(result['result'][args[0]][args[1]][args[2]][args[3]][args[4]])
        df = df.rename(index=str, columns={"x": "time", "y": args[3]}).set_index('time')
        return df.set_index(pd.to_datetime(df.index, unit='s'))

    def get_code(self, alpha_id, alpha_user_id, alpha_token):
        return '''
using Newtonsoft.Json;
using RestSharp;
using RestSharp.Authenticators;

namespace QuantConnect
{
    public class AlphaStreamsAPIFrameworkAlgorithm : QCAlgorithmFramework
    {
        public override void Initialize()
        {
            var alphaModel = new AlphaStreamsAPIAlphaModel();

            UniverseSettings.Resolution = Resolution.Minute;

            SetStartDate(alphaModel.StartDate);
            SetEndDate(alphaModel.EndDate);
            SetCash(1000000);

            SetAlpha(alphaModel);
            SetUniverseSelection(new ManualUniverseSelectionModel(alphaModel.Symbols));
            SetPortfolioConstruction(new EqualWeightingPortfolioConstructionModel());
            SetExecution(new ImmediateExecutionModel());
            SetRiskManagement(new MaximumDrawdownPercentPerSecurity(0.01m));
        }

        public override void OnOrderEvent(OrderEvent orderEvent)
        {
            if (orderEvent.Status.IsFill())
            {
                Debug($"Purchased Stock: {orderEvent.Symbol}");
            }
        }

        private class AlphaStreamsAPIAlphaModel : AlphaModel
        {
            private readonly Dictionary<DateTime, List<Insight>> _insights;
            public DateTime StartDate { get; private set; }
            public DateTime EndDate { get; private set; }
            public List<Symbol> Symbols { get; private set; }

            public AlphaStreamsAPIAlphaModel()
            {
                Name = "AxAxAxA";

                var userId = "UxUxUxU";
                var token = "TxTxTxT";
                var client = new RestClient("https://www.quantconnect.com/api/v2/");

                var insights = new List<Insight>();
                var hasData = true;
                var start = 0;

                while (hasData)
                {
                    var timestamp = (int)QuantConnect.Time.TimeStamp();
                    var hash = $"{token}:{timestamp}".ToSHA256();
                    var request = new RestRequest($"alpha/{Name}/insights?start={start}", Method.GET);

                    request.AddHeader("Timestamp", timestamp.ToString());
                    client.Authenticator = new HttpBasicAuthenticator(userId, hash);

                    var response = client.Execute(request);

                    var requestInsights = JsonConvert.DeserializeObject<List<Insight>>(response.Content);
                    insights.AddRange(requestInsights);
                    hasData = requestInsights.Count > 0;
                    start += requestInsights.Count;
                }

                if (insights.Count == 0)
                {
                    throw new Exception($"No insights from alpha {Name}");
                }

                _insights = insights
                    .GroupBy(x => x.GeneratedTimeUtc)
                    .ToDictionary(k => k.Key, v => v.ToList());

                StartDate = insights.OrderBy(x => x.GeneratedTimeUtc).First().GeneratedTimeUtc;
                EndDate = insights.OrderBy(x => x.CloseTimeUtc).Last().CloseTimeUtc.AddDays(1);
                Symbols = insights.Select(y => y.Symbol).Distinct().ToList();
            }

            public override IEnumerable<Insight> Update(QCAlgorithmFramework algorithm, Slice data)
            {
                return _insights.ContainsKey(algorithm.UtcTime)
                    ? _insights[algorithm.UtcTime]
                    : Enumerable.Empty<Insight>();
            }
        }
    }
}'''.replace('AxAxAxA', alpha_id).replace('UxUxUxU', alpha_user_id).replace('TxTxTxT', alpha_token)

    def __repr__(self):
        return f'''
        Project Id: {self.project_id}
        Compile Id: {self.compile_id}
        Backtest Id: {self.backtest_id}'''

if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__))
    AlphaBacktest(
        "118d1cbc375709792ea4d823a", 
        1840764, 
        0,
        '',
        'c7bd966e930c4b15b2ec13eb0d6170d9',
        '7030e89cfcc1948f4f93e91edd93d6f687c737844a6969d99d609a78f8d0a5c4091ef11f31c4c0e9cccacefe36ff4c2ad0e15525a85c65b0eafa34064cd11b1c'
        )