import flask
import numpy as np
import urllib
import sys
import csv

from exploji import convert_image_to_emoji

app = flask.Flask(__name__)

emoji_character = None
emoji_color = None
file_name = 'temp_file_{}.png'
file_counter = 0

@app.route('/')
def index():
    return flask.render_template("index.html")

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
        global file_counter
        global emoji_character
        global emoji_color
        global file_name
        
        file_counter += 1
        # URL = 'http://ecx.images-amazon.com/images/I/41qJGxrMW0L._SL500_AA300_.jpg'
        # urllib.urlretrieve(URL, "000001.jpg")
        # urllib.urlretrieve(URL, file_name.format(file_counter))
        output_string = convert_image_to_emoji(file_name.format(1), emoji_color, emoji_character)
        print type(output_string)
        print output_string.encode('utf8')[0]
        return flask.render_template("exploji.html", source_image=url, output_string=output_string)
            
@app.route('/about')
def about():
    #   TODO: add about template
    return flask.render_template("about.html")



def main(color_csv, character_csv, debug=True, host='127.0.0.1', port=8080):
    global emoji_character
    global emoji_color
    
    csv_data = np.genfromtxt(color_csv, delimiter=',')
    emoji_color = csv_data[:, 1:]
    
    with open(character_csv, 'rb') as f:
        reader = csv.reader(f)
        emoji_character = list(reader)
    emoji_character = [a[1].encode('utf8') for a in emoji_character]
    print emoji_character[0]
    app.run(debug=debug, host=host, port=port)

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])