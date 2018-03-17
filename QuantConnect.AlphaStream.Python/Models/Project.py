from datetime import datetime
from Models.Author import Author

class Project:
    """ Project object for details about the Alpha Project """

    def __init__(self, json):
    
        self.Id = json['id']
        
        self.Author = Author( json['author'] )
        
        self.Created = json['created']
        
        self.LastModified = datetime.utcfromtimestamp( json['last-modified'] )
        
        self.Name = json['name']
        
        self.ParentId = json['parent-id']
        
        