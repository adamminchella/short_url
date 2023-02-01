from flask import Flask, render_template, redirect, jsonify, url_for, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from config import Config

import string
import random

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

CORS(app)

from models import ShortUrl


def id_generator(size=6, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        url = request.form['url-input']
        # shorted the url
        shorted_url = id_generator()

        check_url_exists = ShortUrl.query.filter_by(original_url=url).first()

        if check_url_exists:
            return redirect(url_for('urls'))

        else:
            short_url = ShortUrl(original_url=url, short_url=shorted_url)
            db.session.add(short_url)
            db.session.commit()
            return redirect(url_for('urls'))
    else:
        return render_template("index.html"), 200


@app.route("/urls")
def urls():
    all_urls = ShortUrl.query.all()
    return render_template("urls.html", urls=all_urls), 200


@app.route('/<short_url>')
def redirect_url(short_url):
    # get the url from the database
    url = ShortUrl.query.filter_by(short_url=short_url).first()
    if url:
        return redirect(url.original_url)
    return render_template('404.html'), 404


if __name__ == "__main__":
    app.run(debug=True)
