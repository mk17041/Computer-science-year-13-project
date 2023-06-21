from pickle import TRUE
from flask import Flask, render_template, request, redirect, session
import mysql.connector
import bcrypt
import re
from flask_bcrypt import Bcrypt

app = Flask(__name__)
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

    # Database setup
db = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="root1234",
            database="userdata"
        )

@app.route("/login", methods=["POST", "GET"])
def login():
    # If user submits form 
    if request.method == "POST":

        # Creating varibles from form data from html
        username = request.form["username"]
        password = request.form["password"]

        # mycursor = open data base
        mycursor = db.cursor(buffered=True, dictionary=True)

        # Searches in users where username/password is = to what user inputted
        mycursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = mycursor.fetchone()

        # If true transfers to menu
        if user and bcrypt.checkpw(password.encode("utf-8"), user["password_hash"].encode("utf-8")):
            session["loggedin"] = TRUE
            session["username"] = user["username"]
            return redirect("/home")
        
        # Else outputs 'wrong username or password'
        else:
            error = 'Wrong username or password'
            return render_template("login.html", error=error)
    else:
        return render_template("login.html")
    

@app.route("/signup", methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        confirm_password = request.form["confirm-password"]

        if password != confirm_password:
            error = "Passwords do not match"
            return render_template("signup.html", error=error)

        # Check if the input is a valid email address
        is_valid_email = re.match(r"[^@]+@[^@]+\.[^@]+", username)

        if is_valid_email:
            # It's a valid email address
            # Perform further processing or validation here
            # ...
            pass
        else:
            # It's not a valid email address
            # Handle the error condition accordingly
            error = "Invalid email address"
            return render_template("signup.html", error=error)

        # Insert the user into the database with hashed password
        mycursor = db.cursor()
        query = "INSERT INTO users (username, password_hash) VALUES (%s, %s)"
        values = (username, hash_password(password))
        mycursor.execute(query, values)
        db.commit()

        return redirect("/login")
    else:
        return render_template("signup.html")
    
    

@app.route("/home")
def home():
    return render_template("home.html")

if __name__ == '__main__':
    app.run(debug=True, port=8000)
