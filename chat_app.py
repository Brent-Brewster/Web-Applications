from flask import Flask, render_template, request, redirect, abort, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from loginModel import Base, login, chat

app = Flask(__name__)

engine = create_engine("sqlite:///login.db", echo=True)
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()

def fetch_latest_chat_messages():
    latest_messages = session.query(chat.message).order_by(chat.created_at.asc()).all()
    messages = [message[0] for message in latest_messages]
    return messages

def check_login(username, password):
    existing_user = session.query(login).filter_by(username=username).first()
    if existing_user:
        if existing_user.password == password:
            return True
    return False

def checkUser(username):
    if username == "":
        return False
        
    existing_user = session.query(login).filter_by(username=username).first()
    if existing_user:
        return True
    return False

def addUser(username, password, email):
    new_user = login(username=username, password=password, email=email)
    session.add(new_user)
    session.commit()
    return True

def postChat(username, message):
    new_chat = chat(username=username, message= username + ": " + message)
    session.add(new_chat)
    session.commit()
    return True

@app.route("/")
def default():
	return  render_template("loginPage.html")

@app.route("/login", methods=["POST"])
def login_route():
    username = request.form["username"]
    password = request.form["password"]
    if check_login(username, password):
        return render_template("chatPage.html", username=username, password=password)
    else:
        return render_template("loginPage.html", error="Invalid username or password")

@app.route("/Register")
def register():
    return render_template("registerPage.html")

@app.route("/register", methods=["POST"])
def register2():
    username = request.form["username"]
    password = request.form["password"]
    email = request.form["email"]
    repassword = request.form["re-password"]
    if password != repassword:
        return render_template("registerPage.html", error="Passwords do not match")
    else:
        if checkUser(username):
            return render_template("registerPage.html", error="Username already exists")
        else:
            addUser(username, password, email)
    return render_template("chatPage.html", username=username, password=password)

@app.route("/sendChat", methods=["POST"])
def chat_route():
    print("/SendChat")
    username = request.form["username"]
    message = request.form["chat"]
    postChat(username, message)
    return render_template("chatPage.html", username=username)

@app.route("/getMessages", methods=["GET"])
def get_messages():
    messages = fetch_latest_chat_messages()
    return jsonify({'messages': messages})

if __name__ == "__main__":
	app.run()