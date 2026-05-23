

from flask import Flask,redirect,url_for,render_template,request



app = Flask(__name__)



@app.route("/")
def home():
    return render_template("home.html")

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
