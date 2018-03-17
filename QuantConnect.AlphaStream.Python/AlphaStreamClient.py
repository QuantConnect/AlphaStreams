import json
import requests
import hashlib
import time
import base64
from Requests.GetAlphaByIdRequest import GetAlphaByIdRequest
from Requests.SearchAlphasRequest import SearchAlphasRequest
from Requests.SearchAuthorsRequest import SearchAuthorsRequest
from Requests.GetAlphaInsightsRequest import GetAlphaInsightsRequest
from Models.Alpha import Alpha
from Models.Insight import Insight
from Models.Author import Author


class AlphaStreamClient(object):
    """Alpha Streams Client is the REST executor and client """

    def __init__(self, clientId, token):
        self.__clientId = str(clientId)
        self.__token = str(token)
        self.__url = 'https://beta.quantconnect.com/api/v2/'

    def Execute(self, request, debug=False):
        """ Execute an authenticated request to the Alpha Streams API """
				
        # Create authenticated timestamped token.
        timestamp = str( int(time.time()) )

        # Attach timestamp to token for increasing token randomness
        timeStampedToken = self.__token + ':' + timestamp

        # Hash token for transport
        apiToken = hashlib.sha256( timeStampedToken.encode('utf-8') ).hexdigest()

        # Attach in headers for basic authentication.
        authentication = "{}:{}".format(self.__clientId, apiToken)
        base64string = base64.b64encode(authentication.encode('utf-8'))
        headers = {
            'Authorization' : 'Basic %s' % base64string.decode('ascii'),
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
            messages.append('API returned a result which cannot be parsed into JSON. Please inspect the raw result below:')
            messages.append(result.text)
            json = {'success': False, 'messages': messages}
        
        if type(json) is not list:
            if json['success'] is False:
                raise Exception('There was an exception processing your request: ' + ", ".join(json["messages"]))
    
        return json
        
        
    def GetAlphaById(self, alphaId):
        """ Request details about a specific alpha """
        request = GetAlphaByIdRequest( alphaId )
        result = self.Execute( request )
        return Alpha(result)
        
        
        
    def SearchAlphas(self, *args, **kwargs):
        """ Applying the search criteria supplied; find matching alphas and return an array of alpha objects """
        criteria = SearchAlphasRequest( kwargs=kwargs )
        result = self.Execute( criteria )
        
        alphas = []
        for a in result:
            alphas.append( Alpha(a) )
        
        return alphas
        
    def SearchAuthors(self, *args, **kwargs):
        """ Applying the search criteria supplied; find matching authors and return an array of author objects """
        criteria = SearchAuthorsRequest( kwargs=kwargs )
        result = self.Execute( criteria )
        
        authors = []
        for ath in result:
            authors.append( Author(ath) )
        
        return authors
        
        
    def GetAlphaInsights(self, alphaId, start=0):
        """ Get the insights for a specific alpha """
        request = GetAlphaInsightsRequest(alphaId, start)
        result = self.Execute( request )
        insights = []
        for i in result:
            insights.append( Insight(i) )
        return insights
        
        
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