import bson
from mongoengine import *
from passlib.apps import custom_app_context as pwd_context
import passlib.utils
import datetime
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

import config

connect(host=config.TEST_DB_URI)

class Post(Document):
    r_id = StringField(primary_key=True)
    source = StringField(required=True)
    url = StringField()
    author = StringField()
    title = StringField()
    content = StringField()
    accepted = BooleanField(default=False)
    completed = BooleanField(default=False)
    discarded = BooleanField(default=False)
    created = DateTimeField()


class User(Document):
    email = StringField()
    password = StringField()
    activation_token = StringField()
    activated = BooleanField(default=False)

    def hash_password(self, password):
        self.password = pwd_context.encrypt(password)

    def create_activation_token(self):
        self.activation_token = passlib.utils.generate_password(size=20)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password)

    def verify_activation_token(self, token):
        return pwd_context.verify(token, self.activation_token)

    def generate_auth_token(self, expiration = 3600):
        s = Serializer(config.secret_key, expires_in = expiration)
        return s.dumps({ 'id': self.id })

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(config.secret_key)
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None # valid token, but expired
        except BadSignature:
            return None # invalid token
        user = User.objects(id=bson.objectid.ObjectId(data['id'])).first()
        return user

class Conversation(Document):

    user = ReferenceField('User')
    post = ReferenceField('Post')
    completed = BooleanField(default=False)
    started = DateTimeField(default=datetime.datetime.utcnow)
    ended = DateTimeField()


class Sample(Document):
    r_id = StringField(primary_key=True)
    title = StringField()
    content = StringField()
    label = BooleanField()
    date = DateTimeField()
    subreddit = StringField()