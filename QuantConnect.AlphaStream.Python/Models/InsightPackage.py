from datetime import datetime
from Models.Insight import Insight

class InsightPackage:
    """ Package holding a group of insights emitted from one moment of time. """
    
    def __init__(self, json):
    
        self.AlphaId = json['alpha-id']
        
        self.AlgorithmId = json['algorithm-id']
        
        self.Insights = []
        
        for i in json['insights']:            
            i['source'] = 'live trading'
            self.Insights.append( Insight(i) )  
        