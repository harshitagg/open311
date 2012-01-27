from mongoengine.document import Document, EmbeddedDocument
from mongoengine.fields import StringField, ListField, EmbeddedDocumentField, BooleanField, DecimalField

class ServiceAttribute(EmbeddedDocument):
    code = StringField(required=True)
    variable = BooleanField(default=False)
    order = DecimalField(required=True)
    description = StringField(required=True)

class Service(Document):
    definition = StringField(required=True)
    code = StringField(required=True)
    name = StringField(required=True)
    metadata = BooleanField(default=False)
    type = StringField(default="realtime")
    keywords = ListField(StringField)
    group = StringField(required=False)
    attributes = ListField(EmbeddedDocumentField(ServiceAttribute))
    