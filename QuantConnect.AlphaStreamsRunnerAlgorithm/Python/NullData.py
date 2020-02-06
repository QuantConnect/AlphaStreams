from clr import AddReference
AddReference("System")
AddReference("QuantConnect.Algorithm")
AddReference("QuantConnect.Common")

from System import *
from QuantConnect import *
from QuantConnect.Algorithm import *
from QuantConnect.Python import PythonData
from QuantConnect.Data import SubscriptionDataSource

from datetime import datetime, timedelta

class NullData(PythonData):
    ''' Null data source provides no actual data, but is used to force the Alpha Model
        Update() method to fire every second. This won't cause any data issues such as
        missing data subscriptions with a brokerage.
    '''
    counter = 0  # Used to increment the data timestamp

    def GetSource(self, config, date, isLive):
        if isLive:
            return SubscriptionDataSource('http://localhost/', SubscriptionTransportMedium.Rest)
        else:
            return SubscriptionDataSource('http://www.google.com', SubscriptionTransportMedium.RemoteFile)

    def Reader(self, config, line, date, isLive):

        data = NullData()
        data.Symbol = config.Symbol
        data.Value = 1
        data.Close = 1
        data.Open = 1
        data.Low = 1
        data.High = 1
        data.Volume = 1

        if isLive:
            data.Time = Extensions.ConvertFromUtc(datetime.utcnow(), config.DataTimeZone)
        else:
            data.Time = date + timedelta(seconds=self.counter)
            self.counter += 1

        return data