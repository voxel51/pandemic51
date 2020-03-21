"""


"""
import datetime

from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def home():
    load_time = datetime.datetime.now()

    return render_template('home.html', load_time=load_time)


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=5000, debug=True)
