import mysql.connector
import bcrypt
from flask import Flask, render_template, request
    
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

app = Flask(__name__)

app.debug = True

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        insert_user(username, password)
        return 'User inserted successfully'

    return render_template('login.html')

if __name__ == '__main__':
    app.run()