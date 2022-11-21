from flask import Flask, redirect, url_for, render_template, request, abort, session
import pymongo
from flask_bcrypt import Bcrypt
from datetime import timedelta




app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = "abcdef"
app.permanent_session_lifetime = timedelta(days=5)



client = pymongo.MongoClient("mongodb+srv://pstud:gVJQTsM2ftVKES5d@inf1039cardapuc.1cskrne.mongodb.net/?retryWrites=true&w=majority&authSource=admin")

db = client.cardapuc

col = db.usuarios


@app.route("/")
def main():
    return render_template("index.html")

@app.route("/login/", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        session["user"] = username

        session.permanent = True
        
        result = col.find_one({"username": username})
        if result is not None:
            pw_unhash = bcrypt.check_password_hash(result["password"], password)
            if pw_unhash == False:
                return render_template("failure.html")
            else:
                return redirect("/user")

        else: 
            return redirect("/cadastro")
        
        return "<p>Success</p>"
    
    return render_template("login.html")

@app.route("/cadastro", methods=["POST", "GET"])
def cadastro():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        result = col.find_one({"username": username})

        if result is None:
            pw_hash = bcrypt.generate_password_hash(password)
            col.insert_one({"username": username, "password": pw_hash})
            return redirect("/login")
        else:
            return redirect("/login")
        
    return render_template("cadastro.html")


@app.route("/user/")
def user():
    if "user" in session:
        user = session["user"]
        return render_template("user.html", user = user)
    else:
        return redirect("/login")

@app.route("/logout/")
def logout():
    session.pop("user", None)
    return redirect("/login")

