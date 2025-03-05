#!/usr/bin/env python3

import Bio.Blast
from Bio.Blast import NCBIWWW
import Bio.SeqIO
from flask import Flask, render_template, request, session, redirect
from flask_session import Session
import sqlite3
from helper import sorry, login_required, seqtoDB, delete_files_in_directory, buildInputFile
from werkzeug.security import check_password_hash, generate_password_hash
import os

# command to run the server: flask --debug run --exclude-patterns temp/*

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
        options = (("/DNAtoPROTEIN", "What does your DNA encode?"), ("/FASTQAnalysis", "Peform quick analysis of a FASTQ file"))

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

@app.route("/managedb", methods=['GET', 'POST'])
@login_required
def managedb():

    if request.method == "POST":

        # fetch id
        id = request.form.get("id")
        
        # connect to database
        con = sqlite3.connect("data.db")
        db = con.cursor()

        # remove given entry
        db.execute("DELETE FROM seq WHERE id = ?;", (id,))
        con.commit()

        # close conection
        con.close()

        return redirect("/managedb")

    else:

        # connect to a database
        con = sqlite3.connect("data.db")
        db = con.cursor()
        
        # fetch and save the data
        rows = db.execute("SELECT id, name, content, filetype FROM seq WHERE user_id = ?", (session["user_id"],))
        rowsList = list(rows)

        # close the connection
        con.close()

        return render_template("managedb.html", rowsList=rowsList)

@app.route('/DNAtoPROTEIN', methods=['GET'])
@login_required
def DNAtoPROTEIN():

    # render a welcome page for "What does you DNA encode?" pipeline
    if request.method == "GET":

        return render_template("DNAtoPROTEIN.html")
    
@app.route('/FASTQAnalysis', methods=['GET'])
@login_required
def FASTQAnalysis():

    # render a welcome page for "What does you DNA encode?" pipeline
    if request.method == "GET":

        return render_template("FASTQAnalysis.html")


# for both FASTA and FASTQ!
@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():

    if request.method == "POST":

        seq = request.files['upload']

        # check if the file is indeed in .fasta or .fastq format
        if seq.filename[-5:] != request.form.get("filetype"):

            return sorry(text="Please provide a proper file!")

        # save the file to temp
        path = r"temp/{}".format(seq.filename)

        if seq.filename != '':
            
            # delete everything from prevous sessions and create a new file
            delete_files_in_directory(r"temp")
            seq.save(path)

        # save the file to db - if file is in db, save step is skipped
        seqtoDB(path, seq.filename, session["user_id"])

        return redirect("/inputOverview")
            
    else:

        return render_template(f"upload{request.args.get("filetype").upper()}.html", filetype=request.args.get("filetype")) 

# for both FASTA and FASTQ!
@app.route("/browseseq", methods=["GET", "POST"])
@login_required
def chooseDatabase():
    
    if request.method == "POST":

        # enable sqlite database
        con = sqlite3.connect("data.db")
        db = con.cursor()

        # fetch data from database
        rowTemp = db.execute("SELECT content FROM seq WHERE user_id = ? AND filetype LIKE ?;", (session["user_id"],request.form.get("filetype")))
        row = list(rowTemp)

        # close the connection
        con.close()

        # delete everything from previous sessions and create a new file
        delete_files_in_directory(r"temp")

        with open(r"temp/temp.{}".format(request.form.get("filetype")), "a") as f:

            # save data to file
            f.write(row[0][0])

        return redirect("/inputOverview")
    
    else:

        # enable sqlite database
        con = sqlite3.connect("data.db")
        db = con.cursor()

        # fetch data from database
        rows = db.execute("SELECT id, name, content, filetype FROM seq WHERE filetype LIKE ? AND user_id = ?;", (request.args.get('filetype'), session["user_id"]))
        
        rowsList = list(rows)

        # close the connection
        con.close()

        return render_template("browseseq.html", rowsList=rowsList, filetype=request.args.get("filetype"))

# for both FASTA and FASTQ!
@app.route("/inputOverview", methods=["GET", "POST"])
@login_required
def inputOverview():

    if request.method == "POST":

        if request.form.get("pageChoice") == "fastq":
        
            # rename the file to uniform name
            os.system("mv temp/*.fastq temp/inputFile.fastq")

            # run fastqp for QC analysis
            filePath = rf"temp/inputFile.{request.form.get("pageChoice")}"
            command = f"fastqc {filePath}"

            os.system(command)

            return render_template("FASTQCPreview.html")
        
        else:

            # clear the temp directory
            delete_files_in_directory(r"temp")

            buildInputFile(r"temp", prefix=request.form.get("header"), data=request.form.get("content"), filetype=request.form.get("pageChoice"),  name="inputFile")

            # getting the sequence (necessary, as SeqIO.parse returns an iterator)
            sequence = Bio.SeqIO.read(r"temp/inputFile.fasta", "fasta")       

            # setting e-mail 
            Bio.Blast.email = request.form.get("email")

            # perform blastn BLAST against a core nucleotide database
            print('Doing the BLAST and retrieving the results...')
            
            # result_stream = Bio.Blast.qblast("blastn", "core_nt", format(sequence, "fasta"), format_type="XML")
            result_stream = NCBIWWW.qblast("blastn", "nt", sequence.format("fasta"), format_type="HTML", hitlist_size=50)
            print("done")

            # saving the output to HTML file 
            with open(r"temp/BLAST.html", "w") as out:
                out.write(result_stream.read())
            
            # open the output to read the file
            lines = []
            with open(r"temp/BLAST.html", "r") as out:
                lines = out.readlines()
            
            remove = True
            # remove each line after the comment line and after the alignment table
            with open(r"temp/BLAST.html", "w") as out:

                for line in lines:

                    if "The following is used for on screen sorting" in line:

                        print ("Found!")

                        remove = False
                    
                    elif "Scroll descriptions table to the right" in line:

                        remove = True
                    
                    if not remove:
                    
                        out.write(line)
            
            # closing the stream
            result_stream.close()


            return render_template("BLASTPreview.html")
        
    else:
        
        # prepare necessary variables
        workFile = r"{}/temp/{}".format(os.getcwd(), os.listdir(r"temp/")[0])
        pageChoice = 'fastq' if os.listdir(r"temp/")[0][-5:] == "fastq" else "fasta"
        firstChar = "@" if os.listdir(r"temp/")[0][-5:] == "fastq" else ">"

        fastxReadList = []
        header = ''
                        
        # read each read into memory
        with open(workFile, 'r') as f:

            for line in f.readlines():

                if line.startswith(firstChar):

                    # dump the read into a dict if the header exists
                    if header != '':
                        
                        read = [header, data]
                        fastxReadList.append(read)

                    # clear data when new header is found
                    data = ''

                    # replace old header with a new one
                    header = line
                
                else:
                    
                    # append the line to data
                    data += line
            
        # dump the last read into the dict
        read = [header, data]
        fastxReadList.append(read)
        
        # render template that shows the quality control check and all the required info    
        return render_template("inputOverview.html", fastxReadList=fastxReadList, filetype=workFile[-5:], pageChoice=pageChoice, file=os.listdir(r"temp/")[0])  

@app.route("/FASTQCReport", methods=["GET"])
@login_required
def FASTQCReport():

    # remove previous analysis and create a new one for preview
    os.system("rm templates/inputFile_fastqc.html")
    os.system("cp temp/inputFile_fastqc.html templates/")

    return render_template("inputFile_fastqc.html")     

@app.route("/BLASTReport", methods=["GET"])
@login_required
def BLASTReport():

    # remove previous analysis and create a new one for preview
    os.system("rm templates/BLAST.html")
    os.system("cp temp/BLAST.html templates/")

    return render_template("BLAST.html")   