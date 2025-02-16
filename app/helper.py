#!/usr/bin/env python3

from flask import render_template, session, redirect
from functools import wraps
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

def seqtoDB(file):

    prefix = ''
    data = ''
    filetype = "fasta" if file[-5:] == "fasta" else "fastq"

    # fetch data from the file
    with open(file, 'r') as f:
        for line in f.readlines():

            if line.startswith(">") or line.startswith("@"):

                prefix += line
            
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