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


    def service_list_info(self):
        _keywords = ",".join(self.keywords)
        return {'service_code': self.code,
                'service_name': self.name,
                'description': self.definition,
                'metadata': self.metadata,
                'type': self.type,
                'keywords': _keywords,
                'group': self.group}