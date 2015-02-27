__author__ = 'The Gibs'

from flask.ext.wtf import Form
from wtforms_components import TimeField, StringField, SelectField
from wtforms.validators import DataRequired


class SearchForm(Form):
    url_to_search = StringField('url_to_search', validators=[DataRequired()])
    game_name = StringField('game_name')
    tournament_name = StringField('tournament_name', validators=[DataRequired()])
    blue_score = StringField('blue_score')
    purple_score = StringField('purple_score')
    start_time = TimeField('start_time', validators=[DataRequired()])
    daylight_savings_time = SelectField('DST',
                                        choices=[("no", 'No'), ("yes", 'Yes'), ("spring", 'Spring'), ("fall", 'Fall')])
    time_zone = SelectField('DST', coerce=str, choices=[("PST", 'PST'), ("EST", 'EST'), ("CST", 'CST'), ("KST", 'KST')])
    lol_vod = StringField('lol_vod')
    youtube_vod = StringField('youtube_vod')
    picks_and_bans_page = StringField('picks_and_bans_page')

