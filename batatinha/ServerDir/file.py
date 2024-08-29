from config import *
from datetime import datetime

class File(Model):
    id = IntegerField(primary_key=True)
    name = TextField()
    modified = DateTimeField(default=datetime.now)

    class Meta:
        database = db

    def json(self):
        return {
            "name" : self.name,
            "id" : self.id,
            "modified" : self.modified 
        }