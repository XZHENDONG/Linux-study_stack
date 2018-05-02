# -*- coding:utf-8 -*-
from flask_wtf import Form
from flask_pagedown.fields import PageDownField
from wtforms.fields import SubmitField

class PageDownFormExample(Form):
    pagedown = PageDownField('Enter your markdown')
    submit = SubmitField('Submit')

@app.route('/', methods = ['GET', 'POST'])
def index():
    form = PageDownFormExample()
    if form.validate_on_submit():
        text = form.pagedown.data
        # do something interesting with the Markdown text
