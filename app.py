from flask import Flask, session, request, render_template, redirect, url_for
import os
from db_script import get_user, add_user, get_forums, add_forums, read_forum, add_post, get_posts
import base64

authorizated = False
user_id = None
error_value = "ㅤ"

def index(): 
    if authorizated:
        if  request.method == "GET":
            return redirect(url_for("main-page"))
        else:
            return redirect(url_for("main-page"))
    else:
        return redirect(url_for("authorization"))

def mainpage():
    global error_value
    if authorizated == True:
        if request.method == "POST":
            if not request.form['create-forum-input'] is None:
                error_value = add_forums({
                    "id_user": user_id,
                    "name": request.form['create-forum-input']
                })
                print(error_value)
                if error_value == None:
                    error_value = "Такой форум уже существует."
                return redirect(url_for("main-page"))
        # request.method = "GET"
        row = get_forums()
        print(error_value)
        if error_value != "ㅤ" and error_value != "Такой форум уже существует.":
            error_value = "ㅤ"
        return render_template("main-page.html", forums = row, error = error_value)
    else:
        return redirect(url_for("authorization"))



def authorization():
    if request.method == "POST":
        login = get_user(request.form["login"], request.form["password"]) 
        try:
            if login[1] == request.form["login"]:
                global authorizated
                global user_id
                user_id = login[0]
                authorizated = True
                return redirect(url_for("index"))
        except:
            return redirect(url_for("authorization-failed"))
    return render_template("authorization.html")

def authorization_failed():
    if request.method == "POST":
        login = get_user(request.form["login"], request.form["password"]) 
        try:
            if login[1] == request.form["login"]:
                global authorizated
                global user_id
                user_id = login[0]
                authorizated = True
                return redirect(url_for("index"))
        except:
            return render_template("authorization-failed.html")
    return render_template("authorization-failed.html")


def registration():
    if request.method == "POST":
        user = {
            "login": request.form.get("login"),
            # "name": request.form.get("name"),
            "password": request.form.get("password"),
            "image": request.files.get("image")
        }
        add_user(user)
        return redirect(url_for("authorization"))
    return render_template("registration.html")

folder = os.getcwd()

app = Flask(__name__, template_folder="template", static_folder="static")
# @app.errorhandler(400)
# def handle_400(e):
#     return f"Ошибка 400: {e}", 400

def open_forum():
    if authorizated == True:
        forum_id = request.form.get('forum_id') or request.args.get('forum_id')
        if not forum_id:
            return "Forum ID missing", 400
        forum_name = read_forum(forum_id)
        
        
        message = request.form.get('send-message-input')
        if request.method == "POST":    
            if not request.form.get('send-message-input') is None:
                print(message)
                if not message is None:
                    send_message(forum_name, message)
                    return redirect(url_for("open_forum", forum_id=forum_id))
        rows = get_posts(forum_name[0])
        return render_template(f"forums/forum-page-{forum_name[0]}-{forum_id}.html", name = forum_name[0], id = forum_id, posts = rows)
    else:
        return redirect(url_for("authorization"))

def send_message(forum_name, message):
    global user_id
    add_post(forum_name,message,user_id)
    return redirect(url_for("open_forum"))
    
    
    

    
app.add_url_rule("/", "index", index, methods = ["post", "get"])
app.add_url_rule("/main-page", "main-page", mainpage, methods = ["post", "get"])
app.add_url_rule("/authorization", "authorization", authorization, methods = ["post", "get"])
app.add_url_rule("/authorization-failed", "authorization-failed", authorization_failed, methods = ["post", "get"])
app.add_url_rule("/registration", "registration", registration, methods = ["post", "get"])
app.add_url_rule("/open_forum", "open_forum", open_forum, methods = ["post", "get"])

app.config["SECRET_KEY"] = "DASISTPLAKEPLAKEQUIZ"

if __name__ == "__main__":
    app.run(debug=True)
