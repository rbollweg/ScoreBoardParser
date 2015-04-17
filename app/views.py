__author__ = 'The Gibs'

from flask import render_template, flash, redirect
from app import app, parser
from .forms import SearchForm, AdminForm
import datetime
import urllib.request

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = SearchForm()
    readme_request = urllib.request.urlopen('http://pastebin.com/raw.php?i=y8vvW8Tq')
    readme = readme_request.read().decode("utf-8")
    if form.validate_on_submit():
        flash("Parse requested for %s" % form.url_to_search)
        url_search = form.url_to_search._value()
        game_name = form.game_name._value()
        tournament_name = form.tournament_name._value()
        blue_score = form.blue_score._value()
        purple_score = form.purple_score._value()
        daylight_savings = form.daylight_savings_time.data
        start_time = form.start_time._value()
        time_zone = form.time_zone.data
        lol_vod = form.lol_vod._value()
        youtube_vod = form.youtube_vod._value()
        picks_and_bans_page = form.picks_and_bans_page._value()
        template = parser.spider(url_search, game_name, tournament_name, blue_score, purple_score, daylight_savings,
                                 start_time, time_zone, lol_vod, youtube_vod, picks_and_bans_page)
        return render_template("results.html",
                               title='Results',
                               template=template,
                               form=form,
                               readme=readme)
    return render_template("index.html",
                           title='Home',
                           form=form,
                           readme=readme)




@app.route('/admin', methods=['GET', 'POST'])
def admin():
    form = AdminForm()
    item_dict = parser.item_dict
    special_champ_names = parser.champ_name_dict
    form.item_numbers.data = item_dict
    form.special_champ_names.data = special_champ_names
    if form.validate_on_submit():
        test = form.special_champ_names.raw_data
        return render_template('admin.html',
                           title='Admin',
                           form = form)
    return render_template('admin.html',
                           title='Admin',
                           form = form)

@app.route('/search', methods=['GET', 'POST'])
def search():
    return render_template('results.html',
                           title='Searching',
                           form=form)


