from flask import Flask,request, jsonify
from db import db 
from config import POSTGRES_URI
from models import Post

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = POSTGRES_URI
db.init_app(app)

users_list = [ 
    {"id":1,"name":"ali","age":20}, 
    {"id":2,"name":"ahmed","age":30}, 
] 

@app.route("/api/users")
def users():
    return jsonify({"status": "success", "data": users_list})


@app.route("/api/add-user", methods=['POST'])
def add_user():
    data = request.get_json()
    name = data["name"]
    age = data["age"]
    new_user = {"id": len(users_list) + 1, "name": name, "age": age}
    users_list.append(new_user)
    return jsonify({"status": "success", "user": new_user})


@app.route("/api/delete-user/<int:id>", methods=['DELETE'])
def delete(id):
    for user in users_list:
        if id == user["id"]:
            users_list.remove(user)
            return jsonify({"status": "success", "message": "user deleted"})
    return jsonify({"status": "error", "message": "user not found"})


@app.route("/api/update-user/<int:id>", methods=['PUT'])
def edit_user(id):
    data = request.get_json()
    for u in users_list:
        if u['id'] == id:
            u['name'] = data['name']
            u['age'] = data['age']
            return jsonify({"status": "success", "user": u})
    return jsonify({"status": "error", "message": "user not found"})


@app.route("/api/posts")
def get_posts():
    posts = Post.query.all()
    posts_data = []
    for post in posts:
        posts_data.append({
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "author": post.author
        })
    return jsonify({"status": "success", "data": posts_data})


@app.route("/api/add-post", methods=["POST"])
def add_post():
    data = request.get_json()
    title = data["title"]
    content = data["content"]
    author = data["author"]
    new_post = Post(title=title, content=content, author=author)
    db.session.add(new_post)
    db.session.commit()
    return jsonify({"status": "success", "message": "post created"})


@app.route("/api/update-post/<int:id>", methods=["PUT"])
def update_post(id):
    post = Post.query.get_or_404(id)
    data = request.get_json()
    post.title = data["title"]
    post.content = data["content"]
    post.author = data["author"]
    db.session.commit()
    return jsonify({"status": "success", "message": "post updated"})


@app.route("/api/delete-post/<int:id>", methods=["DELETE"])
def delete_post(id):
    post = Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return jsonify({"status": "success", "message": "post deleted"})


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5001)