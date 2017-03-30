import flask
import urllib
import sys
import os
import random


from exploji import convert_image_to_emoji
from setup import emoji_character, emoji_color

app = flask.Flask(__name__)

file_name = 'temp_{}.png'

@app.route('/')
def index():
    return flask.render_template("index.html", message=u'\U0001f601 \U0001f389')

@app.route('/about')
def about():
    return flask.render_template("about.html")

@app.route('/error')
def error():
    return '''<html><head><title>Oops...</title><meta http-equiv="refresh" content="3;url=/" /></head>
                <body><h3><span style="color:red">An error occurred</span><br>Redirecting in 3 seconds...</h3>
            </body></html>'''

@app.route('/exploji', methods = ['GET'])
def exploji_get(url=None, k=5, width=75):
    global file_name
    redirect = False

    if 'url' in flask.request.args and not flask.request.args.get('url').strip() == '':
        url = flask.request.args.get('url')
    if 'k' in flask.request.args and not flask.request.args.get('k').strip() == '':
        k = int(flask.request.args.get('k'))
    if 'width' in flask.request.args and not flask.request.args.get('width').strip() == '':
        width = int(flask.request.args.get('width'))

    if url is None:
        return flask.redirect('/error')
    else:
        file_counter = ''.join(random.choice('0123456789ABCDEF') for i in range(16))
        file = file_name.format(file_counter)
        urllib.urlretrieve(url, file)
        try:
            output_string, dimension = convert_image_to_emoji(file, emoji_color, emoji_character, k=k, width=width)
        except:
            redirect = True
        finally:
            os.remove(file)
            if redirect:
                return flask.redirect('/error')

        out = ''
        for row in output_string:
            for character in row:
                out += character
            out+='<br>'
        return out


@app.route('/exploji', methods = ['POST'])
def exploji_post(url=None, k=5, width=75):
    global file_name
    redirect = False

    if flask.request.form is not None:
        if 'url' in flask.request.form and not flask.request.form['url'].strip() == '':
            url = flask.request.form['url']
        if 'k' in flask.request.form and not flask.request.form['k'].strip() == '':
            k = int(flask.request.form['k'])
        if 'width' in flask.request.form and not flask.request.form['width'].strip() == '':
            width = int(flask.request.form['width'])

    if url is None:
        return flask.redirect('/error')
    else:
        print k, width

        file_counter = ''.join(random.choice('0123456789ABCDEF') for i in range(16))
        file = file_name.format(file_counter)
        urllib.urlretrieve(url, file)
        try:
            output_string, dimension = convert_image_to_emoji(file, emoji_color, emoji_character, k=k, width=width)
        except:
            redirect = True
        finally:
            os.remove(file)
            if redirect:
                return flas

        return flask.render_template("exploji.html", source_image=url, output_string=output_string)


if __name__ == '__main__':
    app.run()
