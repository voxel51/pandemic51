'''
Test Flask app.

Copyright 2020, Voxel51, Inc.
voxel51.com
'''
import datetime

from flask import Flask, render_template


app = Flask(__name__)


@app.route("/")
def home():
    load_time = datetime.datetime.now()
    return render_template("home.html", load_time=load_time)


if __name__ == "__main__":
    # This is used when running locally only
    app.run(host="127.0.0.1", port=5000, debug=True)
