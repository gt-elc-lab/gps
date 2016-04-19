import flask
from flask.ext.httpauth import HTTPBasicAuth
from flask.ext.cors import CORS

import views
import models
import labeling

application = flask.Flask(__name__)
application.config['SECRET_KEY'] = 'super secret'

auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(email_or_token, password):
    # first try to authenticate by token
    user = models.User.verify_auth_token(email_or_token)
    if not user:
        # try to authenticate with username/password
        user = models.User.objects(email=email_or_token).first()
        if not user or not user.verify_password(password):
            return False
    flask.g.user = user
    token = user.generate_auth_token(600)
    flask.session['token'] = token.decode('ascii')
    return True


api = flask.Blueprint('api', __name__, template_folder='templates')
CORS(application, resources=r'/api/*', allow_headers='Content-Type', supports_credentials=True)
CORS(labeling.label_server, resources=r'/label/*', allow_headers='Content-Type')

api.add_url_rule('/register',
    view_func=views.RegisterView.as_view('register_view'), methods=['POST'])

api.add_url_rule('/login',
    view_func=views.LoginView.as_view('login_view'), methods=['POST'])

api.add_url_rule('/token',
    view_func=views.RefreshTokenView.as_view('token_refresh_view'), methods=['GET'])

post_view = views.PostView.as_view('post_view')
api.add_url_rule('/post', defaults={'r_id': None},
    view_func=post_view, methods=['GET'])
api.add_url_rule('/post/<string:r_id>', view_func=post_view, methods=['GET'])
api.add_url_rule('/post/<string:r_id>', view_func=post_view,
    methods=['POST'])

conversation_view = views.ConversationView.as_view('conversation_view')
api.add_url_rule('/conversation/<string:_id>', view_func=conversation_view, methods=['GET', 'PUT'])

api.add_url_rule('/conversation/<string:r_id>/<string:user_id>', view_func=conversation_view,
    methods=['POST'])



user_view = views.UserView.as_view('user_view')
api.add_url_rule('/user/<string:_id>', view_func=user_view, methods=['GET'])



@api.route('/label')
def index():
    page = int(flask.request.args.get('page'))
    samples = models.Sample.objects(subreddit='gatech')[page * 20: (page + 1) * 20]
    return samples.to_json()

@api.route('/label/<string:r_id>', methods=['POST'])
def label(r_id):
    sample = models.Sample.objects.get(r_id=r_id)
    sample.label = bool(int(flask.request.args.get('label')))
    sample.save()
    return sample.to_json()

@api.route('/label/count')
def count():
    count = models.Sample.objects(label__exists=True).count()
    return flask.jsonify(count=count)

application.register_blueprint(api, url_prefix='/api')
if __name__ == '__main__':
    application.debug = True
    application.run()