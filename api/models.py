from mongoengine.document import Document
from mongoengine.fields import StringField

class Service(Document):
    definition = StringField(required=True)
    code = StringField(required=True)