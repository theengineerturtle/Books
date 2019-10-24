from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, TextAreaField
from wtforms.validators import Required, Length

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[Required(), Length(1,16)])
    password = PasswordField('Password', validators=[Required()])
    remember_me = BooleanField('Remember me!')
    submit = SubmitField('Submit')

class SearchForm(FlaskForm):
    searchtext = StringField('isbn, title, author or year of any books', validators=[Required()])
    submit = SubmitField('Search')

class ReviewForm(FlaskForm):
    rating = SelectField(u'Rating', choices=[('1','1'), ('2','2'), ('3','3'), ('4','4'), ('5','5')])
    comment = TextAreaField( 'Leave a commet', validators=[Length(0,64)])
    submit = SubmitField('Submit')
