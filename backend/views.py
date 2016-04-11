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
        flask.session['user_id'] = str(user.id)
        return flask.jsonify(make_user_response(user))

class UserView(MethodView):


     def get(self, _id):
        user = User.objects.get(id=_id)
        conversations = Conversation.objects(user=user)
        return conversations.to_json()

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
        return flask.jsonify(make_user_response(user))


class RefreshTokenView(MethodView):

    def get(self):
        token = flask.g.user.generate_auth_token()
        return flask.jsonify({ 'token': token.decode('ascii') })

class PostView(MethodView):

    def get(self, r_id):
        if r_id:
            return Post.objects.exclude('content').get(r_id=r_id).to_json()
        posts = Post.objects(accepted=False).order_by('-created')[:10].to_json()
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
        conversation = Conversation()
        conversation.user = user
        conversation.post = post
        post.accepted = True
        post.save()
        conversation.save()
        return 'success'

    def get(self, user_id):
        completed = True if flask.request.args.get('completed') == 'true' else False
        return Conversation.objects(user=user_id, completed=completed).to_json()





