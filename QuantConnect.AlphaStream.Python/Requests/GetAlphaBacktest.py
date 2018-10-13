from datetime import datetime
from time import sleep
from quantconnect.api import Api
from os import linesep

class GetAlphaBacktest(object):
    """ Get the alpha backtest from a given alpha Id.
    In this class, a project and backest is created in QuantConnect.com and it is executed.
    The project algorithm is a QuantConnect Framework one where the Alpha Model use historical insights. """

    def __init__(self, *args, **kwargs):
        ''' Initializes a new instance of the GetAlphaBacktest class
        Args:
            alphaId: Unique hash identifier of a published Alpha.
            clientId: Alpha client Id
            token: Alpha client API token
            userId: QuantConnect user Id
            userToken: QuantConnect user API token'''
        self.__alphaId = str(kwargs.pop('alphaId', args[0]))
        clientId =  str(kwargs.pop('clientId', args[1]))
        token = str(kwargs.pop('token', args[2]))
        self.__content = self.__create_file_content(clientId, token)

        # Create instance of QuantConnect API
        userId = kwargs.pop('userId', args[3])
        userToken = kwargs.pop('userToken', args[4])
        self.__api = Api(userId, userToken)

        if not self.__api.connected():
            raise Exception('Could not connect to QuantConnect. Please verify your credentials.')


    def Run(self):
        ''' Run the backtest for a given alpha
        Returns:
            Json dictionary object with the backtest results for the given alpha '''
        # Creates a project and adds file
        project = self.__get_or_create_project()

        # Compiles and create a backtest
        backtest = self.__compile_and_create_backtest(project)

        # Get backtest results
        result = self.__get_backtest_result(project, backtest)

        # Delete the project
        response = self.__api.delete_project(project['projectId'])
        self.verify_response_success(response)

        return result


    def __get_or_create_project(self):
        '''Gets or creates a project, adds or updates its content and return it
        Returns:
            Project response packet from the QuantConnect.com API'''
        self.log('Get or create project')

        # Look for an alpha backtest project for this alpha id
        project = self.__fetch_project()

        # Create a new project if none has the target name
        if project == None:
            name = f'AlphaBacktest_{self.__alphaId}'
            projectResponse = self.__api.create_project(name, 'C#')
            self.verify_response_success(projectResponse)
            project = projectResponse['projects'][0]

        # Adds or updates main.cs
        projectId = project['projectId']
        response = self.__api.read_project_file(projectId, 'main.cs')
        if not response['success'] and response['errors'][0].startswith('File not found'):
            self.verify_response_success(self.__api.add_project_file(projectId, 'main.cs', self.__content))
        else:
            self.verify_response_success(self.__api.update_project_file_content(projectId, 'main.cs', self.__content))      

        self.log(f'Project: {project["name"]} ({projectId})')
        return project


    def __compile_and_create_backtest(self, project):
        '''Compiles the current code and create a backtest
        Args:
            project: Project object where a backest will be created
        Returns:
            Backtest response packet from the QuantConnect.com API'''
        self.log('Compile and create backtest')

        projectId = project['projectId']
        compile = self.__api.create_compile(projectId)
        self.verify_response_success(compile)

        # Only create a backtest after a successfull build
        compileId = compile['compileId']
        while not compile['state'].startswith('BuildSuccess'):
            sleep(1)
            compile = self.__api.read_compile(projectId, compileId)

        self.log(f'CompileId: {compileId}')

        backtestName = str(datetime.utcnow())
        backtest = self.__api.create_backtest(projectId, compileId, backtestName)
        self.verify_response_success(backtest)

        self.log(f'Backtest: {backtestName} ({backtest["backtestId"]})')
        return backtest


    def __get_backtest_result(self, project, backtest):
        '''Get the backtest result from a given backtest
        Args:
            project: Project object where the backest was created
            backtestId: Backtest object from where we will get the results from
        Returns:
            BacktestResult response packet from the QuantConnect.com API'''
        count = 0
        progress = backtest['progress']
        projectId = project['projectId']
        seconds = 0
        while progress < 1:
            sleep(seconds)
            start = datetime.now()

            # Get the backtest result
            backtest = self.__api.read_backtest(projectId, backtest['backtestId'])
            self.verify_response_success(backtest)

            # Check whether there has been progress
            # If not after 5 tries, delete the project
            if progress == backtest['progress']:
                count = count + 1
                if count >= 5:
                    self.__api.delete_project(projectId)
                    self.log('Too many tries with no progress. Please try.')
                    return None

            progress = backtest['progress']
            self.log(f'Reading backtest result: {100*progress:3.2f}% completed')
            seconds = 10 - min(10, (datetime.now() - start).total_seconds())

        return backtest['result']


    def __fetch_project(self):
        '''Try to fetch the project from a list of projects where its name includes the alpha id
        Returns:
            Project response packet from the QuantConnect.com API'''
        projectId = 0

        result = self.__api.list_projects()
        if not result['success']:
            return None

        projects = [ p for p in result['projects'] if p['name'].endswith(self.__alphaId) ]

        # No projects with the alpha id in its name
        if len(projects) == 0:
            return None

        project = projects[0]
        projectId = project['projectId']

        # If the found project has more than one backtest,
        # it means that something went wrong, so we will delete it
        backtestList = self.__api.list_backtests(projectId)
        if backtestList['success']:
            if len(backtestList['backtests']) > 1:
                self.__api.delete_project(projectId)

        return project


    def __create_file_content(self, clientId, token):
        '''Creates an algorithm code content with the client credentials to fetch the insights for the given alpha
        Args:
            clientId: Alpha client Id
            token: Alpha client API token'''
        content = '''
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
                var client = new RestClient("https://www.quantconnect.com/api/v2/");

                var insights = new List<Insight>();
                var hasData = true;
                var start = 0;

                while (hasData)
                {
                    var timestamp = (int)QuantConnect.Time.TimeStamp();
                    var hash = $"TOKEN:{timestamp}".ToSHA256();
                    var request = new RestRequest($"alpha/ALPHAID/insights?start={start}", Method.GET);

                    request.AddHeader("Timestamp", timestamp.ToString());
                    client.Authenticator = new HttpBasicAuthenticator("CLIENTID", hash);

                    var response = client.Execute(request);

                    var requestInsights = JsonConvert.DeserializeObject<List<Insight>>(response.Content);
                    insights.AddRange(requestInsights);
                    hasData = requestInsights.Count > 0;
                    start += requestInsights.Count;
                }

                if (insights.Count == 0)
                {
                    throw new Exception("No insights from alpha ALPHAID");
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
}'''
        return content.replace('ALPHAID', self.__alphaId).replace('CLIENTID', clientId).replace('TOKEN', token)


    def log(self, message):
        '''Prints the message with the time it was created
        Args:
            message: Message to be printed'''
        print(f'{datetime.utcnow().time()} :: {message}')


    def verify_response_success(self, response):
        ''' Verifies whether rest response is successfull and throws exception of not.
        Args:
            response: Rest reponse of an API call'''
        if not response['success']:
            errors = response.get('errors', response.get('error', dict()))
            raise Exception(linesep.join(errors))