from forms import PostForm, CommentForm
from flask import Flask, redirect, url_for, render_template, request
from flask.views import MethodView
from db import db 
from config import POSTGRES_URI
from models import Post, Comment

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = POSTGRES_URI
app.config["SECRET_KEY"]="111"
db.init_app(app)
with app.app_context():
    db.create_all()


class HomeView(MethodView):
    def get(self):
        posts = Post.query.all()
        return render_template("home.html", posts=posts)


class AddPostView(MethodView):
    def get(self):
        form = PostForm()
        return render_template("add-post.html", form=form)

    def post(self):
        title = request.form["title"]
        content = request.form["content"]
        author = request.form["author"]
        new_post = Post(title=title, content=content, author=author)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("home"))


class UpdatePostView(MethodView):
    def get(self, id):
        post = Post.query.get_or_404(id)
        form = PostForm(obj=post)
        return render_template("update-post.html", post=post, form=form)

    def post(self, id):
        post = Post.query.get_or_404(id)
        form = PostForm(obj=post)
        if form.validate_on_submit():
            post.title = form.title.data
            post.content = form.content.data
            post.author = form.author.data
            db.session.commit() 
            return redirect(url_for("home"))
        return render_template("update-post.html", post=post, form=form)


class DeletePostView(MethodView):
    def post(self, id):
        post = Post.query.get_or_404(id)
        db.session.delete(post)
        db.session.commit()
        return redirect(url_for("home"))


class PostDetailsView(MethodView):
    def get(self, id):
        post = Post.query.get_or_404(id)
        return render_template("post-details.html", post=post)


class AddCommentView(MethodView):
    def post(self, post_id):
        post = Post.query.get_or_404(post_id)
        content = request.form["content"]
        author = request.form["author"]
        new_comment = Comment(content=content, author=author, post_id=post_id)
        db.session.add(new_comment)
        db.session.commit()
        return redirect(url_for("home"))
    

class AboutView(MethodView):
    def get(self):
        return "<h1>About Page <h1>"


class ContactView(MethodView):
    def get(self):
        return "<h1>Contact Page<h1>"


app.add_url_rule("/", view_func=HomeView.as_view("home"))
app.add_url_rule("/add-post", view_func=AddPostView.as_view("add_post"))
app.add_url_rule("/update-post/<int:id>", view_func=UpdatePostView.as_view("update_post"))
app.add_url_rule("/delete-post/<int:id>", view_func=DeletePostView.as_view("delete_post"))
app.add_url_rule("/post-details/<int:id>", view_func=PostDetailsView.as_view("post_details"))
app.add_url_rule("/add-comment/<int:post_id>", view_func=AddCommentView.as_view("add_comment"))
app.add_url_rule("/about", view_func=AboutView.as_view("about"))
app.add_url_rule("/contact", view_func=ContactView.as_view("contact"))


if __name__ == "__main__":
    app.run(debug=True)