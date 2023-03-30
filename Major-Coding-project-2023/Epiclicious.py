from pickle import TRUE
from flask import Flask, render_template, request, redirect, jsonify, session, flash, logging
app = Flask(__name__)

@app.route("/", methods = ["POST","GET"])
def create_page():
    #if user submits form 
    if request.method == "POST":
        #creating varibles from form data
        username = request.form["username"]
        password = request.form["psw"]
        #cur = open data base
        cur = db_connect.cursor(dictionary=True)
        #inserts the username/password the user has inputted into logintable inside the database so the login is saved
        cur.execute("INSERT into logintable(username, password) VALUES(%s, %s)",(username, password))
        db_connect.commit()
        return redirect("/login")
    else:
        return render_template("create.html")