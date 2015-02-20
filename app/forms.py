__author__ = 'The Gibs'


from flask.ext.wtf import Form
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired

class SearchForm(Form):
    url_to_search = StringField('url_to_search', validators=[DataRequired()])