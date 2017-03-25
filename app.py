import flask
import numpy as np
import urllib2
import cStringIO
import sys

import exploji

app = flask.Flask(__name__)

emoji_character = None
emoji_color = None

@app.route('/')
def index():
    return flask.render_template("index.html", test=u"\U0001f473\U0001f3fe")

@app.route('/exploji', methods = ['GET', 'POST'])
def exploji(url=None):
    if flask.request.method == 'POST' and flask.request.form is not None and 'url' in flask.request.form:
        url = flask.request.form['url']
    elif flask.request.method == 'GET':
        if 'path' in flask.request.args:
            url = flask.request.args.get('path')
    if url is None:
       return flask.redirect('/')
    else:
        file = cStringIO.StringIO(urllib2.urlopen(url).read())
        output_string = exploji.convert_image_to_emoji(file, emoji_character, emoji_color)
        return flask.render_template("exploji.html", source_image=url, output_string=output_string)
            
@app.route('/about')
def about():
    #   TODO: add about template
    return flask.render_template("about.html")



def main(color_csv, character_csv, debug=True, host='127.0.0.1', port=8080):
    csv_data = np.genfromtxt(color_csv, delimiter=',')
    emoji_color = csv_data[:, 1:]
    csv_data = np.genfromtxt(character_csv, delimiter=',')
    emoji_character = csv_data[:, 1:]
    
    app.run(debug=debug, host=host, port=port)

if __name__ == '__main__':
    main(sys.argv[1])