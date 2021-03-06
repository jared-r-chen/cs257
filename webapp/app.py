'''
    app.py
    Aaron Schondorf and Jared Chen, 11 November 2021

'''
import flask
import argparse
import api

app = flask.Flask(__name__, static_folder='static', template_folder='templates')
app.register_blueprint(api.api, url_prefix='/api')

@app.route('/')
def home():
    return flask.render_template('index.html')

@app.route('/songs-like')
def songs_like():
    return flask.render_template('songs_like.html')

@app.route('/help-page')
def help():
    return flask.render_template('help_page.html')



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('host', help='the host to run on')
    parser.add_argument('port', type=int, help='the port to listen on')
    arguments = parser.parse_args()
    app.run(host=arguments.host, port=arguments.port, debug=True)
