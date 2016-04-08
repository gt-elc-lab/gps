import bson
import flask
from flask.views import MethodView
from flask.ext.httpauth import HTTPBasicAuth

import config
from models import User, Post, Conversation


def make_user_response(user):
    return {
        'id': str(user.id),
        'email': user.email,
    }


def AuthenticationError(message):
    return flask.jsonify(message=message), 400


class LoginView(MethodView):

    def get(self):
        pass

    def post(self):
        email = flask.request.json.get('email')
        password = flask.request.json.get('password')
        if email is None or password is None:
            raise AuthenticationError('Missing credentials.')
        user = User.objects(email=email).first()
        if not user:
            return AuthenticationError('User does not exist.')
        # if not user.activated:
        #     return AuthenticationError('Please activate your account.')
        if not user.verify_password(password):
            return AuthenticationError('Incorrect password.')
        flask.g.user = user
        return flask.jsonify(make_user_response(user))


class RegisterView(MethodView):

    def get(self):
        pass

    def post(self):
        email = flask.request.json.get('email')
        password = flask.request.json.get('password')
        if email is None or password is None:
            return AuthenticationError('Missing credentials.')
        if User.objects(email=email).first():
            return AuthenticationError('User already exists.')
        user = User(email=email)
        user.hash_password(password)
        user.create_activation_token()
        user.save()
        # mail = emailer.Emailer()
        # message = config.PROD_ACTIVATION_LINK.format(_id=str(user.id), token=user.activation_token)
        # thr = Thread(target=mail.send_text, args=[[user.email], message])
        # thr.start()
        return flask.jsonify(make_user_response(user))


class RefreshTokenView(MethodView):

    def get(self):
        token = flask.g.user.generate_auth_token()
        return flask.jsonify({ 'token': token.decode('ascii') })

class PostView(MethodView):

    def get(self, r_id):
        posts = Post.objects(resolved=False).order_by('-created')[:10].to_json()
        return flask.Response(posts,  mimetype='application/json')

    def post(self, r_id):
        user = User.objects.get(id=bson.objectid.ObjectId(
            flask.request.args.get('id')))
        post = Post.objects.get(r_id=r_id)
        conversation = Conversation(user, post)

class ConversationView(MethodView):

    def post(self, r_id, user_id):
        user = User.objects.get(id=user_id)
        post = Post.objects.get(r_id=r_id)
        conversation = Conversation(user, post)




