from mongoengine import *

connect(host="mongodb+srv://mrpchulkov:pNMopFLl4bnWZ2VN@web-module8.be50r1x.mongodb.net/test", ssl=True)


class Authors(Document):
    fullname = StringField(required=True)
    borndate = StringField(max_length=50)
    location = StringField(max_length=50)
    description = StringField()


class Quotes(Document):
    tags = ListField(StringField(max_length=30))
    author = ReferenceField(Authors, dbref=False, reverse_delete_rule=CASCADE)
    quote = StringField()
    meta = {'allow_inheritance': True}




