import flask
import numpy as np
import urllib
import sys
import csv


from exploji import convert_image_to_emoji

application = flask.Flask(__name__)

emoji_character = None
emoji_color = None
file_name = 'temp_file_{}.png'
file_counter = 0

@application.route('/')
def index():
    return flask.render_template("index.html", test=u'\U0001f601 \U0001f389')

@application.route('/exploji', methods = ['GET', 'POST'])
def exploji(url=None, k=5, width=75):
    global file_counter
    global emoji_character
    global emoji_color
    global file_name
    if flask.request.method == 'POST' and flask.request.form is not None and 'url' in flask.request.form:
        url = flask.request.form['url']
        k = int(flask.request.form['k'])
        width = int(flask.request.form['width'])
        file_counter += 1
        urllib.urlretrieve(url, file_name.format(file_counter))
        output_string, dimension= convert_image_to_emoji(file_name.format(file_counter), emoji_color, emoji_character, k=k, width=width)
        return flask.render_template("exploji.html", source_image=url, output_string=output_string)
    elif flask.request.method == 'GET':
        if 'path' in flask.request.args:
            url = flask.request.args.get('path')
        if 'k' in flask.request.args:
            k = int(flask.request.args.get('k'))
        if 'width' in flask.request.args:
            width = int(flask.request.args.get('width'))
    if url is None:
       return flask.redirect('/')
    else:
        file_counter += 1
        urllib.urlretrieve(url, file_name.format(file_counter))
        output_string, dimension= convert_image_to_emoji(file_name.format(file_counter), emoji_color, emoji_character, k=k, width=width)
        out = ''
        for row in output_string:
            for character in row:
                out += character
            out+='<br>'
        return out

@application.route('/about')
def about():
    #   TODO: add about template
    return flask.render_template("about.html")



def main(color_csv, character_csv, debug=True, host='127.0.0.1', port=80):
    global emoji_character
    global emoji_color

    csv_data = np.genfromtxt(color_csv, delimiter=',')
    emoji_color = csv_data[:, 1:]

    with open(character_csv, 'rb') as f:
        reader = csv.reader(f)
        emoji_character = list(reader)
    emoji_character = [a[1].decode('utf8') for a in emoji_character]
    # print emoji_character
    application.run(debug=debug, host=host, port=port)

if __name__ == '__main__':
    main('col.csv', 'char.csv')
