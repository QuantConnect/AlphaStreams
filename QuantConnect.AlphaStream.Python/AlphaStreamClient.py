import json
import requests
import hashlib
import time
import base64
import os

from Requests.GetAlphaListRequest import GetAlphaListRequest
from Requests.GetAlphaByIdRequest import GetAlphaByIdRequest
from Requests.GetAlphaErrorsRequest import GetAlphaErrorsRequest
from Requests.SearchAlphasRequest import SearchAlphasRequest
from Requests.SearchAuthorsRequest import SearchAuthorsRequest
from Requests.GetAlphaInsightsRequest import GetAlphaInsightsRequest
from Requests.GetAuthorByIdRequest import GetAuthorByIdRequest
from Requests.SubscribeRequest import SubscribeRequest
from Requests.UnsubscribeRequest import UnsubscribeRequest
from Requests.GetAlphaPricesRequest import GetAlphaPricesRequest
from Requests.GetAlphaBacktest import GetAlphaBacktest
from Requests.CreateConversationRequest import CreateConversationRequest

from Models.Alpha import Alpha
from Models.Author import Author
from Models.RuntimeError import RuntimeError
from Models.Insight import Insight
from Models.Price import Price
from Models.AlphaBacktestResult import AlphaBacktestResult

class AlphaStreamClient(object):
    """Alpha Streams Client is the REST executor and client """

    def __init__(self, *args, **kwargs):
        self.__clientId =  str(kwargs.pop('clientId', args[0]))
        self.__token = str(kwargs.pop('token', args[1]))
        self.__url = 'https://www.quantconnect.com/api/v2/'

        length = len(args)  
        self.__userId = str(kwargs.pop('userId', args[2] if length > 3 else None))
        self.__userToken = str(kwargs.pop('userToken', args[3] if length > 3 else None))

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

        # Convert to object for parsing.
        try:
            json = result.json()
        except Exception as err:
            messages = []
            messages.append(
                'API returned a result which cannot be parsed into JSON. Please inspect the raw result below:')
            messages.append(result.text)
            json = {'success': False, 'messages': messages}

        if type(json) is not list:
            if json['success'] is False:
                raise Exception(
                    'There was an exception processing your request: {}'.format(", ".join(json["messages"]), json))

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

    def GetAlphaPrices(self, alphaId, start=0):
        """ Get the prices for a specific alpha """
        request = GetAlphaPricesRequest(alphaId, start)
        result = self.Execute(request)
        prices = []
        for i in result:
            prices.append(Price(i))
        return prices

    def GetAlphaErrors(self, alphaId, start=0):
        """ Get the errors for a specific alpha """
        request = GetAlphaErrorsRequest(alphaId, start)
        result = self.Execute(request)
        errors = []
        for i in result:
            errors.append(RuntimeError(i))
        return errors

    def GetAlphaList(self):
         """ Get list of all available alpha Ids """
         request = GetAlphaListRequest()
         return self.Execute(request)

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

    def Subscribe(self, alphaId):
        """ Subscribe to an alpha """
        request = SubscribeRequest(alphaId)
        result = self.Execute(request)
        return result['success']

    def Unsubscribe(self, alphaId):
        """ Unsubscribe from an alpha """
        request = UnsubscribeRequest(alphaId)
        result = self.Execute(request)
        return result['success']

    def CreateConversation(self, alphaId, email, subject, message, cc = ''):
        """ Create a conversation thread. """
        request = CreateConversationRequest(alphaId, email, subject, message, cc)
        result = self.Execute(request)
        if result['success']:
            return 'Conversation thread was successfully created.'
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
        print ('')

    def GetAlphaBacktest(self, alphaId):
        ''' Run the backtest for a given alpha '''
        request = GetAlphaBacktest(alphaId, self.__clientId, self.__token, self.__userId, self.__userToken)
        result = request.Run()
        return AlphaBacktestResult(result)