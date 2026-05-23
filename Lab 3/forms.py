from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField
from wtforms.validators import DataRequired,Length,Email

class PostForm(FlaskForm):
    title = StringField("Title",validators=[DataRequired(),Length(min=5,max=200)],render_kw={
        "placeholder":"enter title",
        "class":"form-control"
    })
    content = TextAreaField("Content",validators=[DataRequired(),Length(min=10,max=500)],render_kw={
        "class":"form-control"
    })
    author = StringField("Author",validators=[DataRequired()],render_kw={
        "class":"form-control"
    })
    submit = SubmitField("Submit",render_kw={
        "class":"btn btn-primary"
    })



class CommentForm(FlaskForm):
    content = TextAreaField("Content",validators=[DataRequired(),Length(min=10,max=500)],render_kw={
        "class":"form-control"
    })
    author = StringField("Author",validators=[DataRequired()],render_kw={
        "class":"form-control"
    })
    submit = SubmitField("Add Comment",render_kw={
        "class":"btn btn-primary"
    })