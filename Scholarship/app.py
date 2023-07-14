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

    # Commit the changes to the database
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
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        mycursor = db.cursor(buffered=True, dictionary=True)
        mycursor.execute(
            "SELECT * FROM users WHERE username = %s", (username,))
        user = mycursor.fetchone()

        if user and bcrypt.checkpw(password.encode("utf-8"), user["password_hash"].encode("utf-8")):
            session["loggedin"] = True
            session["username"] = user["username"]
            return redirect("/landing")
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

        mycursor = db.cursor()
        query = "INSERT INTO users (username, password_hash) VALUES (%s, %s)"
        values = (username, hash_password(password))
        mycursor.execute(query, values)
        db.commit()

        return redirect("/login")
    else:
        return render_template("signup.html")


@app.route("/landing")
def home():
    if "loggedin" in session:
        username = session["username"]

        # Retrieve the user's recipes from the database
        mycursor = db.cursor()
        mycursor.execute(
            "SELECT * FROM users WHERE username = %s", (username,))
        recipes = mycursor.fetchall()
        mycursor.close()

        return render_template("landing.html", username=username, recipes=recipes)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("loggedin", None)
    session.pop("username", None)
    return redirect("/login")


@app.route("/recipes")
def recipes():
    if "loggedin" in session:
        username = session["username"]

        # Retrieve the user's recipes from the database
        mycursor = db.cursor()
        mycursor.execute("""
            SELECT recipes.id, recipes.user_id, recipes.recipe_name, recipes.instructions, recipes.date
            FROM users
            JOIN recipes ON users.personID = recipes.user_id
            WHERE users.username = %s
        """, (username,))
        recipes = mycursor.fetchall()
        mycursor.close()
        print(recipes)

        return render_template("recipes.html", recipes=recipes)
    else:
        return redirect("/login")


@app.route("/edit")
def edit():
    return render_template("edit.html")


@app.route("/Rcreate", methods=["POST", "GET"])
def create():
    if "loggedin" in session:
        username = session["username"]

        # Retrieve the list of ingredients from the database
        mycursor = db.cursor()
        mycursor.execute("SELECT Short_Food_Name FROM mytable")
        ingredients = mycursor.fetchall()
        mycursor.close()

        # Pass the ingredients to the template
        return render_template("create.html", ingredients=ingredients)
    else:
        return redirect("/login")


@app.route("/saverecipe", methods=["POST", "GET"])
def save_recipe():
    if request.method == "POST":
        recipe_name = request.form["recipe-name"]
        date = request.form["date"]
        instructions = request.form["instructions"]
        selected_food = request.form.getlist("selected_food")

        # Retrieve the user's personID from the database
        username = session["username"]
        mycursor = db.cursor(buffered=True, dictionary=True)
        mycursor.execute(
            "SELECT personID FROM users WHERE username = %s", (username,))
        user = mycursor.fetchone()
        user_id = user["personID"]
        mycursor.close()

        # Insert the recipe into the recipes table
        mycursor = db.cursor()
        query = "INSERT INTO recipes (user_id, recipe_name, date, instructions) VALUES (%s, %s, %s, %s)"
        values = (user_id, recipe_name, date, instructions)
        mycursor.execute(query, values)
        recipe_id = mycursor.lastrowid

        # Insert the ingredients into the ingredients table
        for ingredient in selected_food:
            query = "INSERT INTO ingredients (recipe_id, ingredient_name) VALUES (%s, %s)"
            values = (recipe_id, ingredient)
            mycursor.execute(query, values)

        # Commit the changes to the database
        db.commit()

        # Close the cursor
        mycursor.close()

    return redirect("/landing")

@app.route("/recipespage", methods=["POST", "GET"])
def recipes_page():
    if "loggedin" in session:
        username = session["username"]

        # Retrieve the recipe details from the database
        mycursor = db.cursor()
        mycursor.execute("""
            SELECT recipes.recipe_name, recipes.date, recipes.instructions, ingredients.ingredient_name
            FROM users
            JOIN recipes ON users.personID = recipes.user_id
            JOIN ingredients ON recipes.id = ingredients.recipe_id
            WHERE users.username = %s
        """, (username,))
        recipe_details = mycursor.fetchall()
        mycursor.close()
        print("hi")

        return render_template("recipespage.html", recipe_details=recipe_details)
    else:
        return redirect("/login")

@app.route("/recipespage/<int:id>")
def recipe_page(id):
    if "loggedin" in session:
        username = session["username"]

        # Retrieve the recipe details from the database
        mycursor = db.cursor()
        mycursor.execute("""
            SELECT recipes.recipe_name, recipes.date, recipes.instructions, ingredients.ingredient_name
            FROM users
            JOIN recipes ON users.personID = recipes.user_id
            JOIN ingredients ON recipes.id = ingredients.recipe_id
            WHERE users.username = %s AND recipes.id = %s
        """, (username, id))
        recipe_details = mycursor.fetchall()
        mycursor.close()


        return render_template("recipespage.html", recipe_details=recipe_details)
    else:
        return redirect("/login")




if __name__ == '__main__':
    app.run(debug=True, port=8000)
