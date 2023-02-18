""" このファイルは実行メインファイルです．
Flaskのルーティングを設定します．

"""
from flask import Flask, redirect, render_template, request, session

from crud import SQLSession
from helpers import login_required

# Configure application
app = Flask(__name__)

# Configure database
sql = SQLSession()

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"


@app.route('/')
@login_required
def index():  # put application's code here
    return render_template("index.html")


@app.route('/login', methods=['get', 'post'])
def login():
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        pass
        # TODO: ログイン処理
    else:
        return render_template("login.html")


@app.route('/logout', methods=['get', 'post'])
def logout():  # put application's code here
    session.clear()
    # TODO: ログアウト処理
    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # TODO: 登録処理
        user_id = None
        session.clear()
        session["user_id"] = user_id
        return redirect("/")
    else:
        return render_template("register.html")


if __name__ == '__main__':
    app.run()
