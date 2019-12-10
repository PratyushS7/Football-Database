from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from FM.models import Club


class RegistrationForm(FlaskForm):
    club = StringField('Club Name',
                           validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_club(self, club):
        club=Club.query.filter_by(clubn=club.data).first()
        if club:
            raise ValidationError('This club already exists')



class LoginForm(FlaskForm):
    club = StringField('Club Name',
                           validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember')
    submit = SubmitField('Login')



class UpdateAccountForm(FlaskForm):
    club = StringField('Club name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    picture=FileField('Update Club Picture', validators=[FileAllowed(['jpg','png','jpeg'])])
    submit = SubmitField('Update')

    def validate_club(self, club):
        if club.data!=current_user.clubn:
            club=Club.query.filter_by(clubn=club.data).first()
            if club:
                raise ValidationError('That name is taken. Please choose a different one')

class AddManagerForm(FlaskForm):
    name=StringField('Manager Name', validators=[DataRequired()])
    desc=TextAreaField('Description', validators=[DataRequired()])
    picture=FileField('Update Player Picture', validators=[FileAllowed(['jpg','png','jpeg'])])
    submit=SubmitField('Add Manager')


class AddPlayerForm(FlaskForm):
    name=StringField('Player Name', validators=[DataRequired()])
    age=StringField('Player age', validators=[DataRequired()])
    country=StringField('Player country', validators=[DataRequired()])
    position=StringField('Player position', validators=[DataRequired()])
    picture=FileField('Update Player Picture', validators=[FileAllowed(['jpg','png','jpeg'])])
    submit=SubmitField('Add Player')

class AddStadiumForm(FlaskForm):
    name=StringField('Stadium Name', validators=[DataRequired()])
    city=StringField('City', validators=[DataRequired()])
    submit=SubmitField('Add Stadium')

class UpdatePlayerForm(FlaskForm):
    name = StringField('Player name',validators=[DataRequired()])
    age=StringField('Player age', validators=[DataRequired()])
    country=StringField('Player country', validators=[DataRequired()])
    position=StringField('Player position', validators=[DataRequired()])
    picture=FileField('Update Player Picture', validators=[FileAllowed(['jpg','png','jpeg'])])
    submit = SubmitField('Update')


class UpdateManagerForm(FlaskForm):
    name = StringField('Manager name',validators=[DataRequired()])
    desc=TextAreaField('Description', validators=[DataRequired()])
    picture=FileField('Update Manager Picture', validators=[FileAllowed(['jpg','png','jpeg'])])
    submit = SubmitField('Update')
