from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, EmailField, IntegerField, RadioField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, Email

#input form 만드는 곳

class UserCreateForm(FlaskForm):
    username = StringField('사용자이름', validators=[DataRequired(), Length(min=3, max=25)])
    password1 = PasswordField('비밀번호', validators=[
        DataRequired(), EqualTo('password2', '비밀번호가 일치하지 않습니다')])
    password2 = PasswordField('비밀번호확인', validators=[DataRequired()])
    email = EmailField('이메일', validators=[DataRequired(), Email()])
    age=IntegerField('나이', validators=[DataRequired()])
    gender= StringField('성별', validators=[DataRequired()])
    height=IntegerField('키', validators=[DataRequired()])
    weight=IntegerField('몸무게', validators=[DataRequired()])
    bodyshape=StringField('체형', validators=[DataRequired()])
    purpose=StringField('운동목적', validators=[DataRequired()])

class UserLoginForm(FlaskForm):
    email = EmailField('이메일', validators=[DataRequired(), Email()])
    password = PasswordField('비밀번호', validators=[DataRequired()])

# class PredataForm(FlaskForm):
    #ex_part= StringField('운동부위', validators=[DataRequired()])
    # count_per_set=IntegerField('세트별 횟수', validators=[DataRequired()])
    # set_count=IntegerField('세트 수', validators=[DataRequired()])
    #power=StringField('운동강도', validators=[DataRequired()])


class UserModifyForm(FlaskForm):
    #username = StringField('사용자이름', validators=[DataRequired(), Length(min=3, max=25)])
    email = EmailField('이메일', validators=[DataRequired(), Email()])
    age=IntegerField('나이', validators=[DataRequired()])
    height=IntegerField('키', validators=[DataRequired()])
    weight=IntegerField('몸무게', validators=[DataRequired()])
    bodyshape=StringField('체형', validators=[DataRequired()])
    purpose=StringField('운동목적', validators=[DataRequired()])
