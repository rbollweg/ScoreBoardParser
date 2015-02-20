__author__ = 'The Gibs'


from flask import render_template, flash, redirect
from app import app, parser
from .forms import SearchForm
import datetime


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = SearchForm()
    if form.validate_on_submit():
        flash("Parse requested for %s" % form.url_to_search)
        url_search = form.url_to_search._value()
        game_name = form.game_name._value()
        blue_score = form.blue_score._value()
        purple_score = form.purple_score._value()
        template = parser.spider(url_search, game_name, blue_score, purple_score)
        return render_template("results.html",
                           title='Results',
                           template = template,
                           form = form)
    return render_template("index.html",
                        title='Home',
                        form = form)



@app.route('/search', methods=['GET', 'POST'])
def search():

    return render_template('results.html',
                           title='Searching',
                           form=form)


