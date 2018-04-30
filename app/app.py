from flask import Flask, render_template, url_for, redirect, request, session
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from searchEngine import SearchEngine
import glob
import os
import pickle

SECRET_KEY = 'some secret key'

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config.from_object(__name__)

bootstrap = Bootstrap(app)

class TextForm(FlaskForm):
	query = StringField('', validators=[Required()], render_kw={"placeholder": "What essays are you looking for?"})
	submit = SubmitField('Find')

@app.route('/', methods=['GET', 'POST'])
def index():
	form = TextForm()
	result = []
	search = pickle.load(open('index.pkl', 'rb'))
	if request.method == 'POST':
		if form.validate_on_submit():
			query_text = form.query.data
			result = search.query(query_text)
	return render_template('base.html', form=form, res=result)

if __name__ == '__main__':
	app.run(debug=True)