__author__ = 'The Gibs'

from flask.ext.wtf import Form
from wtforms.fields.html5 import DateTimeField
from wtforms_components import TimeField, StringField, SelectField
from wtforms.fields import TextAreaField
from wtforms.validators import DataRequired
from app import parser


class SearchForm(Form):
    url_to_search = StringField('url_to_search', validators=[DataRequired()])
    game_name = StringField('game_name')
    tournament_name = StringField('tournament_name', validators=[DataRequired()])
    blue_score = StringField('blue_score')
    purple_score = StringField('purple_score')
    start_time = DateTimeField('start_time', validators=[DataRequired()], format='%H:%M')
    daylight_savings_time = SelectField('DST',
                                        choices=[("yes", 'Yes'), ("no", 'No'), ("spring", 'Spring'), ("fall", 'Fall')])
    time_zone = SelectField('DST', coerce=str, choices=[("PST", 'PST'), ("EST", 'EST'), ("CST", 'CST'), ("KST", 'KST')])
    lol_vod = StringField('lol_vod')
    youtube_vod = StringField('youtube_vod')
    picks_and_bans_page = StringField('picks_and_bans_page')

class AdminForm(Form):
    item_numbers = TextAreaField('item_numbers')
    special_champ_names = TextAreaField('special_champ_names', default="test")

