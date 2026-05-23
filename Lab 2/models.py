from db import db

class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(200),nullable=False)
    content = db.Column(db.Text,nullable=False)
    author = db.Column(db.String(100),nullable=False)
    comments = db.relationship('Comment',backref="posts",lazy=True,cascade="all, delete-orphan")

class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer,primary_key=True)
    content = db.Column(db.Text,nullable=False)
    author = db.Column(db.String(100),nullable=False)
    post_id = db.Column(db.Integer,db.ForeignKey("posts.id"),nullable=False)