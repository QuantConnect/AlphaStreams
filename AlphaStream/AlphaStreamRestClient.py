from itertools import groupby
import json
import requests
import hashlib
import time
import base64
import os
import pandas as pd
from datetime import datetime, timedelta
from .Models import *
from .Requests import *

class AlphaStreamRestClient(object):
    """Alpha Streams Client is the REST executor and client """

    def __init__(self, *args, **kwargs):
        """Initialize client ID, token, and target url"""
        self.__clientId =  str(kwargs.pop('clientId', args[0]))
        self.__token = str(kwargs.pop('token', args[1]))
        self.__url = 'https://www.quantconnect.com/api/v2/'

    def Execute(self, request, debug=False):
        """ Execute an authenticated request to the Alpha Streams API """

        # Create authenticated timestamped token.
        timestamp = str(int(time.time()))

        # Attach timestamp to token for increasing token randomness
        timeStampedToken = self.__token + ':' + timestamp

        # Hash token for transport
        apiToken = hashlib.sha256(timeStampedToken.encode('utf-8')).hexdigest()

        # Attach in headers for basic authentication.
        authentication = "{}:{}".format(self.__clientId, apiToken)
        base64string = base64.b64encode(authentication.encode('utf-8'))
        headers = {
            'Authorization': 'Basic %s' % base64string.decode('ascii'),
            'Timestamp': timestamp
        }

        # URL endpoint specified in request
        url = self.__url + request.Endpoint

        # Encode the request in parameters of URL. Most of API is GET.
        result = requests.get(url, params=request.GetPayload(), headers=headers)

        if debug:
            print(result.url)
            self.PrettyPrint(result)

        if (result.text == '') or (len(result.text) < 2):
            raise Exception(f'Error processing result. Result text is an empty string or not a string representation of list.\n {result.text}')

        # Convert to object for parsing.
        try:
            json = result.json()
        except Exception as err:
            messages = []
            messages.append(
                'API returned a result which cannot be parsed into JSON. Please inspect the raw result below:')
            messages.append(result.text)
            json = {'success': False, 'messages': messages}

        # Check that json format is correct, handle errors if not
        if type(json) is not list:
            if ('success' in json.keys()) and ('messages' in json.keys()):
                if json['success'] is False:
                    raise Exception(
                        'There was an exception processing your request: {}'.format(", ".join(json["messages"]), json))
            elif ('success' in json.keys()):
                if json['success'] is False:
                    raise Exception(
                        'There was an exception processing your request: {}'.format(json))
            else:
                raise Exception(
                    'There was an exception processing your request: {}'.format(json))

        return json

    def GetAlphaById(self, alphaId):
        """ Request details about a specific alpha """
        request = GetAlphaByIdRequest(alphaId)
        result = self.Execute(request)
        return Alpha(result)

    def GetAuthorById(self, authorId):
        """ Get information about a specific author """
        request = GetAuthorByIdRequest(authorId)
        result = self.Execute(request)
        return Author(result)

    def GetAlphaInsights(self, alphaId, start=0):
        """ Get the insights for a specific alpha """
        request = GetAlphaInsightsRequest(alphaId, start)
        result = self.Execute(request)
        insights = []
        for i in result:
            insights.append(Insight(i))
        return insights

    def GetAlphaErrors(self, alphaId, start=0):
        """ Get the errors for a specific alpha """
        request = GetAlphaErrorsRequest(alphaId, start)
        result = self.Execute(request)
        errors = []
        for i in result:
            errors.append(RuntimeError(i))
        return errors

    def GetAlphaEquityCurve(self, alphaId, date_format = 'date'):
        """ Get the pandas DataFrame with the equity curve for a specific alpha """
        request = GetAlphaEquityCurveRequest(alphaId, date_format)
        result = self.Execute(request)
        for i in result:
            if isinstance(i[0], int):
                i[0] = datetime.utcfromtimestamp(i[0])
            else:
                i[0] = datetime.strptime(i[0], "%d/%m/%Y %H:%M:%S")
        return pd.DataFrame.from_records(result, index=['time'], columns=['time', 'equity', 'sample'])


    def GetAlphaList(self):
         """ Get list of all available alpha Ids """
         request = GetAlphaListRequest()
         return self.Execute(request)

    def GetAlphaOrders(self, alphaId, start = 0):
        """ Get the Orders and OrderEvents for a specific alpha """
        request = GetAlphaOrdersRequest(alphaId, start)
        result = self.Execute(request)
        return [Order(x) for x in result]

    def GetAlphaTags(self):
        """ Get list of number of Alphas with tags matching search criteria"""
        request = GetAlphaTagsRequest()
        result = self.Execute(request)
        return [Tag(res) for res in result]

    def GetHoldings(self, alphaId):
        """Get holdings from a given alpha """

        start_page=0
        start_equity=1000000
        source = 'live trading'

        df = self.GetAlphaEquityCurve(alphaId)
        if not df.empty:
            if source is not 'all':
                df = df.where(df['sample'] == source).dropna()
        if df.empty:
            raise Exception(f'Cannot retrieve equity curve for {alphaId} for {source}')

        equity = start_equity*(df.equity.iloc[-1]/df.equity.iloc[0])

        i = 100*start_page
        orders = list()
        while True:
            result = self.GetAlphaOrders(alphaId, start = i)
            if len(result) == 0: break
            for item in result:
                if item.Source == source:
                    orders.append(item)
            i += 100
            print(f'\rFetching orders. Page: {int(i/100)}...', end='', flush=True)

        algorithmId = orders[-1].AlgorithmId
        orders = [o for o in orders if o.AlgorithmId == algorithmId]

        holdings = list()

        func = lambda x: x.Symbol
        groupedbySymbol = groupby(sorted(orders, key=func), func)
        for symbol, g in groupedbySymbol:
            symbolOrders = list(g)
            quantity = sum([o.Quantity for o in symbolOrders])
            if quantity != 0:
                weight = sum([o.Price*o.Quantity for o in symbolOrders]) / equity
                holdings.append({'symbol': symbol, 'weight': round(weight,4)})

        return holdings

    def DownloadOrders(self, alphaId):
        """Downloads all orders and save to file"""
        with open(f"orders-{alphaId}.csv", mode="w") as fp:
            i = 0
            while True:
                result = self.GetAlphaOrders(alphaId, start = i)
                if len(result) == 0: return
                for order in result:
                    fp.write(f'{order.AlgorithmId},{order.CreatedTime},{order.Symbol},'+
                             f'{order.Price},{order.Quantity},"{order.Type.name}","{order.Status.name}"\n')
                i += 100
                print(f'\rFetching orders. Page: {int(i/100)}...', end='', flush=True)

    def SearchAlphas(self, *args, **kwargs):
        """ Applying the search criteria supplied; find matching alphas and return an array of alpha objects """
        criteria = SearchAlphasRequest(kwargs=kwargs)
        result = self.Execute(criteria)

        alphas = []
        for a in result:
            alphas.append(Alpha(a))

        return alphas

    def SearchAuthors(self, *args, **kwargs):
        """ Applying the search criteria supplied; find matching authors and return an array of author objects """
        criteria = SearchAuthorsRequest(kwargs=kwargs)
        result = self.Execute(criteria)

        authors = []
        for ath in result:
            authors.append(Author(ath))

        return authors

    def CreateConversation(self, alphaId, email, subject, message, cc = ''):
        """ Create a conversation thread. """
        request = CreateConversationRequest(alphaId, email, subject, message, cc)
        result = self.Execute(request)
        if result['success']:
            return 'Conversation thread was successfully created.'
        else:
            return os.linesep.join(result['messages'])

    def ReadConversation(self, alphaId):
        """ Read a conversation thread to confirm receipt and return list of Conversation objects. """
        request = CreateReadRequest(alphaId)
        result = self.Execute(request)
        conversations = [Conversation(i) for i in result]
        return conversations


    def CreateBid(self, *args, **kwargs):
        """ Create a bid price request.
       Args:
            alphaId: Unique id hash of an Alpha published to the marketplace.
            exclusive: Bid for the exclusive price (optional if shared is defined).
            shared: Bid for the shared price (optional if exclusive is defined).
            good_until: Expiration time of the bid."""
        request = CreateBidPriceRequest(*args, **kwargs)
        result = self.Execute(request)
        if result['success']:
            return 'Bid price was successfully created.'
        else:
            return os.linesep.join(result['messages'])

    def PrettyPrint(self, result):
        """ Print out a nice formatted version of the request """
        print ('')
        try:
            parsed = json.loads(result.text)
            print (json.dumps(parsed, indent=4, sort_keys=True))
        except Exception  as err:
            print ('Fall back error (text print)')
            print ('')
            print (result.text)
        print ('')
