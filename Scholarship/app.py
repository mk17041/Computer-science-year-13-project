from pickle import TRUE
#import MySQLdb
from flask import Flask, render_template, request, redirect, jsonify, session, flash, logging
app = Flask(__name__)
import mysql.connector
import bcrypt
app.secret_key = 'thisisoursecretkey'
    
# Function to hash the password
def hash_password(password):
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return hashed_password.decode("utf-8")

# Function to insert a user with hashed password
def insert_user(username, password):
# Connect to MySQL
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="root1234",
        database="userdata"
    )

# Create a cursor object to interact with the database
    mycursor = db.cursor()

 # Hash the password
    hashed_password = hash_password(password)

# Insert the user into the database
    query = "INSERT INTO users (username, password_hash) VALUES (%s, %s)"
    values = (username, hashed_password)
    mycursor.execute(query, values)


 # Commit the changes to database
    db.commit()

# Close the cursor and database connection
    mycursor.close()
    db.close()



app.debug = True

#database setup
db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="root1234",
        database="userdata"
    )


@app.route("/login1", methods = ["POST","GET"])
def login():
    #if user submits form 
    if request.method == "POST":
        #creating varibles from form data from html
        username = request.form["username"]
        password = request.form["password"]
        #cur = open data base
        mycursor = db.cursor(buffered=True, dictionary=True)
        #searches in logintable where username/password is = to what user inputted
        mycursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        login = mycursor.fetchone()
        #if true transfers to menu
        if login: 
                session["loggedin"] = TRUE
                session["username"] = login["username"]
                return redirect("/")
        #else outputs 'wrong username or password'
        else:
            error = 'wrong username or password'
            return render_template("login.html", error = error)
    else: 
        return render_template("login.html")
    
if __name__ == '__main__':
    app.run(debug=True, port=8000)