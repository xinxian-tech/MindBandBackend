import flask
from api import emoji, va
app = flask.Flask(__name__)


@app.route('/')
def root():
    return 'Hellow world! '


@app.route('/emoji2VA')
def emoji2VA():
    character = flask.request.args['emoji']
    return emoji.emoji2VA(character)


@app.route('/VA2mp3')
def VA2mp3():
    v = flask.request.args['v']
    a = flask.request.args['a']
    songid = va.va2mp3(int(v), int(a))
    return flask.send_from_directory('music', '%s.mp3' % songid)


@app.route('/emoji2mp3')
def emoji2mp3():
    character = flask.request.args['emoji']
    v, a = emoji.emoji2VA(character)
    songid = va.va2mp3(int(v), int(a))
    return flask.send_from_directory('music', '%s.mp3' % songid)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8008, debug=False)
