import flask

app = flask.Flask(__name__)

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
        return flask.render_template("exploji.html", source_image=url, output_string=u"Python is \U0001f600")
            
@app.route('/about')
def about():
    #   TODO: add about template
    return flask.render_template("about.html")



def main(debug=True, host='127.0.0.1', port=8080):
    app.run(debug=debug, host=host, port=port)

if __name__ == '__main__':
    main()