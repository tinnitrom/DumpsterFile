from flask import Flask, session, request, render_template, redirect, url_for
import os
from db_script import get_user, add_user

authorizated = False

def index(): 
    if authorizated:
        if  request.method == "GET":
            print(6)
            return redirect(url_for("check"))
        else:
            print(7)
            return redirect(url_for("check"))
    else:
        return redirect(url_for("authorization"))

def check():
    return render_template("check.html")


def authorization():
    print(1)
    if request.method == "POST":
        login = get_user(request.form["login"], request.form["password"]) 
        print(login)
        try:
            if login[1] == request.form["login"]:
                global authorizated
                print(111)
                authorizated = True
                return redirect(url_for("index"))
        except:
            return redirect(url_for("authorization-failed"))
    return render_template("authorization.html")

def authorization_failed():
    print(1)
    if request.method == "POST":
        login = get_user(request.form["login"], request.form["password"]) 
        print(login)
        try:
            if login[1] == request.form["login"]:
                global authorizated
                authorizated = True
                return redirect(url_for("index"))
        except:
            return render_template("authorization-failed.html")
    return render_template("authorization-failed.html")

def registration():
    if request.method == "POST":
        user = {
            "login": request.form.get("login"),
            "name": request.form.get("name"),
            "password": request.form.get("password"),
            "about": request.form.get("about", ""),
            "image": request.files.get("image")
        }
        add_user(user)
        return redirect(url_for("authorization"))
    return render_template("registration.html")

folder = os.getcwd()

app = Flask(__name__, template_folder="template", static_folder="static")
@app.errorhandler(400)
def handle_400(e):
    return f"Ошибка 400: {e}", 400

app.add_url_rule("/", "index", index, methods = ["post", "get"])
app.add_url_rule("/check", "check", check, methods = ["post", "get"])
app.add_url_rule("/authorization", "authorization", authorization, methods = ["post", "get"])
app.add_url_rule("/authorization-failed", "authorization-failed", authorization_failed, methods = ["post", "get"])
app.add_url_rule("/registration", "registration", registration, methods = ["post", "get"])

app.config["SECRET_KEY"] = "DASISTPLAKEPLAKEQUIZ"

if __name__ == "__main__":
    app.run(debug=True)

