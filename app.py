import flask
from api import emoji, va
from api.img import img
import os
app = flask.Flask(__name__)
app.config['upload_folder'] = img.UPLOAD_FOLDER

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,session_id')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS,HEAD')
    # 这里不能使用add方法，否则会出现 The 'Access-Control-Allow-Origin' header contains multiple values 的问题
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@app.route('/')
def root():
    return 'Hellow world! '


@app.route('/emoji2VA')
def emoji2VA():
    character = flask.request.args['emoji']
    return str(emoji.emoji2VA(character))


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


@app.route('/img2mp3', methods=['POST'])
def img2mp3():
    file = flask.request.files['file']
    if file and img.allowed_file(file.filename):
        input_img = os.path.join(app.config['upload_folder'], '1.jpg') 
        file.save(input_img)
        print(input_img)
        v, a = img.img2VA()
        songid = va.va2mp3(int(v), int(a))
        return flask.send_from_directory('music', '%s.mp3' % songid)


@app.route('/humming2mp3', methods=['POST'])
def humming2mp3():
    file = flask.request.files['file']
    file.save('api/humming/1.wav')
    tempdir = os.getcwd()
    os.chdir('api/humming/')
    os.system('python humming.py')
    os.chdir('..')
    os.system('python midi2mp3.py humming/1.mid -o 1.mp3')
    os.chdir(tempdir)
    return flask.send_from_directory('api', '1.mp3')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8008, debug=False)
