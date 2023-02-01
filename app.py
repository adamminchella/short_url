from flask import Flask, render_template, redirect, jsonify, url_for, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import qrcode

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


# print(app.root_path, app.instance_path)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        url = request.form['url-input']
        # shorted the url
        shorted_url = id_generator()

        check_url_exists = ShortUrl.query.filter_by(original_url=url).first()

        img = qrcode.make(url)
        img.save(app.root_path + '/static/images/qr.png')

        if check_url_exists:
            return render_template("index.html", short_url=check_url_exists.short_url, original_url=url)

        else:
            # Link for website
            # Creating an instance of qrcode

            new_url = ShortUrl(
                original_url=url, short_url=shorted_url)
            db.session.add(new_url)
            db.session.commit()
            return render_template("index.html", short_url=new_url.short_url, original_url=url)
    else:
        return render_template("index.html"), 200


@app.route("/urls", methods=['GET', 'POST'])
def urls():
    all_urls = ShortUrl.query.all()
    if request.method == 'POST':
        url = request.form['url-input']
        print(url)
        img = qrcode.make(url)
        print(img)
        img.save(app.root_path + '/static/images/qr.png')
        print("askugaslfkabsflkauwhglarugbpaeriguabe")
        return render_template("urls.html", urls=all_urls, img=True), 200
    return render_template("urls.html", urls=all_urls, img=False), 200


@app.route('/<short_url>')
def redirect_url(short_url):
    # get the url from the database
    url = ShortUrl.query.filter_by(short_url=short_url).first()
    print(url)
    if url:
        return redirect(url.original_url)
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
