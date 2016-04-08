import flask

import models

label_server = flask.Blueprint('label', __name__, template_folder='templates')
LIMIT = 20

@label_server.route('/', defaults={'page': 0})
@label_server.route('/<int:page>')
def index(page):
    samples = models.Sample.objects(subreddit='gatech')[page: page +LIMIT]
    return samples.to_json()

@label_server.route('/sample/<string:r_id>', methods=['GET'])
def label(r_id):
    sample = models.Sample.objects.get(r_id=r_id)
    sample.label = bool(flask.request.args.get('label'))
    sample.save()
    return 'ok'