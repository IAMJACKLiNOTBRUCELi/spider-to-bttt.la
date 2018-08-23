import flask
from pymongoer import Mongodber
import json

app = flask.Flask(__name__)
mongo_db = Mongodber()


@app.route('/hello')
def hha():
    return "hhahahah"


@app.route('/proxy/ip_port')
def get_proxy_ip():
    args = flask.request.args
    return json.dumps(mongo_db.get_proxy_ip(args['count']), ensure_ascii=False)


def app_run():
    app.run(port='5000')


if __name__ == '__main__':
    app_run()
