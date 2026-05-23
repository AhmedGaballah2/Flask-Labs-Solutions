from pdb import post_mortem
from forms import PostForm,CommentForm
from flask import Flask,redirect,url_for,render_template,request
from db import db 
from config import POSTGRES_URI
from models import Post , Comment

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = POSTGRES_URI
app.config["SECRET_KEY"]="111"
db.init_app(app)
with app.app_context():
    db.create_all()

@app.route("/")
def home():
    posts=Post.query.all()
    return render_template(
        "home.html",posts=posts)


@app.route("/add-post",methods=["POST","GET"])
def add_post():
    form = PostForm()
    if request.method  == "POST":
        print(request.form)
        title = request.form["title"]
        content = request.form["content"]
        author = request.form["author"]
        new_post = Post(title=title,content=content,author=author)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("add-post.html",form=form)

@app.route("/update-post/<int:id>",methods=["POST","GET","PUT"])
def update_post(id):
    post = Post.query.get_or_404(id)
    form = PostForm(obj=post)
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.author = form.author.data
        db.session.commit() 
        return redirect(url_for("home"))
    return render_template("update-post.html", post=post, form=form)


@app.route("/delete-post/<int:id>",methods=["POST"])
def delete_post(id):
    post = Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/post-details/<int:id>")
def post_details(id):
    post = Post.query.get_or_404(id)
    return render_template("post-details.html",post=post)


@app.route("/add-comment/<int:post_id>",methods=["POST","GET"])
def add_comment(post_id):
    post = Post.query.get_or_404(post_id)
    if request.method == "POST":
        content = request.form["content"]
        author = request.form["author"]
        new_comment = Comment(content=content,author=author,post_id=post_id)
        db.session.add(new_comment)
        db.session.commit()
        return redirect(url_for("home"))
    
@app.route("/about")
def about():
    return "<h1>About Page <h1>"


@app.route("/contact")
def contact():
    return "<h1>Contact Page<h1>"



@app.route("/user/<user_name>")
def user(user_name):
    print(type(user_name))
    return f"<h1>Hello {user_name}<h1>"




@app.route("/user/<user_name>/<int:age>")
def user_age(user_name,age):
    return f"<h1>Hello {user_name}, your age is {age}<h1>"



users_list = [ 
    {"id":1,"name":"ali","age":20}, 
    {"id":2,"name":"ahmed","age":30}, 
] 

@app.route("/users")
def users():
    data = f"""
     <h1>Users Data</h1>
     <ul>
     """
    for user in users_list:
             data += f" <li>id:{user['id']} -- user name:{user['name']} -- age: {user['age']} </li>"
    data += """
     </ul>
 """
    return data 


@app.route("/add-user/<name>/<int:age>")
def add(name,age):
    new_user={"id":len(users_list)+1,"name":name,"age":age}
    users_list.append(new_user)
    return redirect(url_for('users'))

@app.route("/add-user",methods=['GET','POST'])
def add_user():
    if request.method == 'POST':
        name=request.form["name"]
        age=request.form["age"]
        new_user={"id":len(users_list)+1,"name":name,"age":age}
        users_list.append(new_user)
        return redirect(url_for('users'))
    return render_template('add_user.html')

@app.route("/delete-user/<int:id>")
def delete(id):
    for user in users_list:
        if id == user["id"]:
            users_list.remove(user)
    return redirect(url_for('users'))



@app.route("/update-user/<int:id>/edit/<name>")
def edit(id,name):
    for user in users_list:
        if id == user["id"]:
            user["name"]=name

    return redirect(url_for('users')) 


@app.route("/update-user/<int:id>",methods=['GET','POST','PUT'])
def edit_user(id):
    current_user = None
    for u in users_list:
        if u['id'] == id:
            current_user = u
            break
    if request.method == 'POST' or request.method=="PUT":
        current_user['name'] = request.form['name']
        current_user['age'] = request.form['age']
        return redirect(url_for('users'))
    return render_template("update-user.html" , user=current_user)
if __name__ == "__main__":
    app.run(debug=True) 
