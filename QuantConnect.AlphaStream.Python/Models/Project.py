from datetime import datetime
from Models.Author import Author


class Project:
    """Project object where the Alpha source resides. One Project can have multiple generated Alphas."""

    def __init__(self, json):
        self.Id = json['id']

        self.Author = Author(json['author']) if 'author' in json else None

        self.Name = json.get('name', None)

        self.CreatedTime = datetime.utcfromtimestamp(json['created-time']) if 'created-time' in json else None

        self.LastModifiedTime = datetime.utcfromtimestamp(json['last-modified-time']) if 'last-modified-time' in json else None

        self.ParentId = json.get('parent-id')