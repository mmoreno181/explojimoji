import flask
import urllib
import sys
import os
import random


from exploji import convert_image_to_emoji
from resources import emoji_character, emoji_color

app = flask.Flask(__name__)

file_name = 'temp_{}.png'


@app.route('/')
def index():
    message = u'\U0001f601 \U0001f389'
    return flask.render_template("index.html", message=message)

@app.route('/about')
def about():
    return flask.render_template("about.html")

@app.route('/error', methods = ['GET'])
def error():
    valid_sources = ['/api']
    if 'source' in flask.request.args and flask.request.args.get('source') in valid_sources:
        return '''<html><head><title>Oops...</title><meta http-equiv="refresh" content=3;url="/api"></head>
                    <body><h3><span style="color:red">An error occurred</span><br>Redirecting in 3 seconds...</h3>
                </body></html>'''
    return '''<html><head><title>Oops...</title><meta http-equiv="refresh" content=3;url="/"></head>
                <body><h3><span style="color:red">An error occurred</span><br>Redirecting in 3 seconds...</h3>
            </body></html>'''

@app.route('/api', methods = ['GET'])
def api(url=None, k=5, width=75, json=False):
    global file_name
    redirect = False

    if 'url' in flask.request.args and not flask.request.args.get('url').strip() == '':
        url = flask.request.args.get('url')
    if 'k' in flask.request.args and not flask.request.args.get('k').strip() == '':
        k = int(flask.request.args.get('k'))
    if 'width' in flask.request.args and not flask.request.args.get('width').strip() == '':
        width = int(flask.request.args.get('width'))
    if 'json' in flask.request.args:
        json = True

    if url is None:
        return '<a href="/">Home</a>'\
            '<h3>HTTP GET => /api<br><br>Required params:<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;url=&lt;source image url&gt;'\
            '<br><br>Optional params:<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;k=&lt;number of clusters; default=5&gt;'\
            '<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;width=&lt;number of emoji characters per row; default=75&gt;'\
            '<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;json (returns json response; default is unformatted emoji characters)</h3>'

    file_counter = ''.join(random.choice('0123456789ABCDEF') for i in range(16))
    file = file_name.format(file_counter)
        
    try:
        urllib.urlretrieve(url, file)
        output_string, dimension = convert_image_to_emoji(file, emoji_color, emoji_character, k=k, width=width)
        
        if json:
            out = []
            for row in output_string:
                row_dict = {'row':[]}
                for character, url in row:
                    row_dict['row'].append({'character':character, 'image_url':url})
                out.append(row_dict)
            return flask.jsonify(out)
        else:
            out = ""
            for row in output_string:
                for character, url in row:
                    out += character
                out += "<br>"
            return out

    except:
        redirect = True

    finally:
        try:
            os.remove(file)
        except:
            pass
        if redirect:
            return flask.redirect('/error?source=/api')


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
        

    file_counter = ''.join(random.choice('0123456789ABCDEF') for i in range(16))
    file = file_name.format(file_counter)
    
    try:
        urllib.urlretrieve(url, file)
        output_string, dimension = convert_image_to_emoji(file, emoji_color, emoji_character, k=k, width=width)
        return flask.render_template("exploji.html", source_image=url, output_string=output_string)
    
    except:
        redirect = True

    finally:
        try:
            os.remove(file)
        except:
            pass
        if redirect:
            return flask.redirect('/error')


if __name__ == '__main__':
    app.run(debug=True)
