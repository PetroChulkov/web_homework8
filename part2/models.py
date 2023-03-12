from mongoengine import *

connect(host="mongodb+srv://mrpchulkov:pNMopFLl4bnWZ2VN@web-module8.be50r1x.mongodb.net/test2", ssl=True)


class Contacts(Document):
    fullname = StringField(required=True)
    email = StringField(required=True)
    phone = StringField()
    way_to_send = StringField()
    message_sent = BooleanField(default=False)


