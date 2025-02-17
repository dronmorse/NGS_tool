#!/usr/bin/env python3

from flask import render_template, session, redirect
from functools import wraps
import os
import sqlite3

# placeholder render for future sections
def sorry(text, code=400):

    return render_template("sorry.html", text=text, code=code)


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function

# function that saves the uploaded file to temp and adds it to the database
def seqtoDB(file):

    prefix = ''
    data = ''
    filetype = "fasta" if file[-5:] == "fasta" else "fastq"

    # fetch data from the file
    with open(file, 'r') as f:
        for line in f.readlines():

            if line.startswith(">") or line.startswith("@"):

                prefix += line

            # catching not properly formatted first line
            elif prefix == '':

                return("This is not a proper file format, please provide a FASTA or FASTQ file in a proper format!")

            else:

                data += line
    
    # enable sqlite database
    con = sqlite3.connect("data.db")
    db = con.cursor()

    # check if the sequence has been already added to the database
    content = db.execute("SELECT prefix, content FROM seq where content = ?;", (data,))
    contentData = list(content)

    if contentData != []:
        return("This sequence has been already found under the name: {}".format(contentData[0][0].strip(">")))
        

    # add data to the database
    db.execute("INSERT INTO seq (prefix, content, filetype, user_id) VALUES (?, ?, ?, ?);", (prefix, data, filetype, session.get("user_id")))
    con.commit()

    # close connection
    con.close()

# clearing a directory, e.g. temp
def delete_files_in_directory(directory_path):
   try:
     
     files = os.listdir(directory_path)

     for file in files:
       
       file_path = os.path.join(directory_path, file)

       if os.path.isfile(file_path):
         
         os.remove(file_path)

     print("All files deleted successfully.")

   except OSError:
     
     print("Error occurred while deleting files.")