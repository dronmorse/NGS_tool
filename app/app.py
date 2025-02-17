#!/usr/bin/env python3

from flask import Flask, render_template, request, session, redirect
from flask_session import Session
from helper import sorry, login_required, seqtoDB, delete_files_in_directory
import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash
import os

# starting flask app
app = Flask(__name__)

# auto-reloading
app.config["TEMPLATES_AUTO_RELOAD"] = True

# setting session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.after_request
def after_request(response):

    # Ensure responses aren't cached
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"

    return response

@app.route('/', methods=['GET'])
@login_required
def index():

    if request.method == "GET":

        # set name of the project and available pipelines
        project_title = "Welcome to DNA analysis tool!"
        options = (("/DNAtoPROTEIN", "What does your DNA encode?"),)

        return render_template("index.html", project_title=project_title, options=options)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":

        # check conditions
        if not request.form.get("password") or not request.form.get("confirmation") or request.form.get("password") != request.form.get("confirmation"):

            return sorry("passwords do not match!")

        elif not request.form.get("username"):

            return sorry("please provide a username!")

        try:
            
            # enable sqlite database
            con = sqlite3.connect("data.db")
            db = con.cursor()

            db.execute(
                "INSERT INTO users (username, password) VALUES (?, ?);",
                (request.form.get("username"),
                generate_password_hash(request.form.get("password")))
            )
            con.commit()
            con.close()

            return render_template("login.html")

        except sqlite3.IntegrityError:

            return sorry("Username already exists!")

    else:
        return render_template("register.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return sorry("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return sorry("must provide password", 403)

        # enable sqlite database
        con = sqlite3.connect("data.db")
        db = con.cursor()
        
        # Query database for username and save the outcome in a variable
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", (request.form.get("username"),)
        )
        rowsOut = list(rows)

        # Ensure username exists and password is correct
        if len(list(rowsOut)) != 1 or not check_password_hash(
            list(rowsOut)[0][2], request.form.get("password")):

            con.close()
            
            return sorry("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = list(rowsOut)[0][0]

        con.close()

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET
    else:
        return render_template("login.html")
    
@app.route('/DNAtoPROTEIN', methods=['GET'])
@login_required
def DNAtoPROTEIN():

    # render a welcome page for "What does you DNA encode?" pipeline
    if request.method == "GET":

        return render_template("DNAtoPROTEIN.html")

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():

    if request.method == "GET":

        return render_template("upload.html")
    
    else:

        seq = request.files['upload']

        # check if the file is indeed in .fasta or .fastq format
        if seq.filename[-5:] not in ['fasta', 'fastq']:
            return sorry(text="Please provide a proper FASTA/FASTQ file")

        # save the file to temp
        path = r"temp/{}".format(seq.filename)

        if seq.filename != '':
            
            # delete everything from prevous sessions and create a new file
            delete_files_in_directory(r"temp")
            seq.save(path)

        # save the file to db
        dbCheck = seqtoDB(path)

        # output check
        if dbCheck != None:

            # drop the temp file
            os.remove(path)
            
            return sorry(text=dbCheck)

        return redirect("/inputOverview")

@app.route("/browseseq", methods=["GET", "POST"])
@login_required
def chooseDatabase():
    
    if request.method == "POST":

        # enable sqlite database
        con = sqlite3.connect("data.db")
        db = con.cursor()

        # fetch data from database
        rowTemp = db.execute("SELECT prefix, content FROM seq WHERE id = ?;", (request.form.get("id"),))
        row = list(rowTemp)

        # close the connection
        con.close()

        # delete everything from prevous sessions and create a new file
        delete_files_in_directory(r"temp")

        with open(r"temp/temp.{}".format(request.form.get("filetype")), "a") as f:

            # save data to file and to output string
            f.write(row[0][0])
            f.write(row[0][1])

        return redirect("/inputOverview")
    
    else:

        # enable sqlite database
        con = sqlite3.connect("data.db")
        db = con.cursor()

        # fetch data from database
        rows = db.execute("SELECT id, prefix, content, filetype FROM seq;")
        rowsList = list(rows)

        # close the connection
        con.close()

        return render_template("browseseq.html", rowsList=rowsList)

@app.route("/inputOverview", methods=["GET", "POST"])
@login_required
def inputOverview():

    if request.method == "POST":
        return sorry('')
    
    else:

        return sorry('')