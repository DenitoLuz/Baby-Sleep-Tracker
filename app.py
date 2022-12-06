import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
import re
from datetime import datetime
from datetime import date
import time

from helpers import apology, login_required, avg_nap, avg_session, update_baby_rec, three_top, get_night


# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///baby.db")

def babyTable():
    babys = db.execute ("SELECT * FROM babys WHERE parent_id = ?", session["user_id"])
    for item in babys:
        sleeprec_ob = db.execute ("SELECT * FROM sleeprec WHERE baby_id = ?", item['id'])
        item['count'] = len(sleeprec_ob)
    return babys

##CONTINUE HERE
@app.route ("/viewfunc", methods =["GET","POST"])
def view_func(baby_id):
    babys = babyTable()
    babyname = db.execute ('SELECT name FROM babys WHERE id = ?', baby_id)
    baby_rec = db.execute ('SELECT * FROM sleeprec WHERE baby_id = ? ORDER BY date DESC, sleep DESC', baby_id)

    baby_rec = update_baby_rec(baby_rec)

    if baby_id == "" or not any(d['id'] == int(baby_id) for d in babys):
            return render_template ("/view.html", babys = babys, entries = -10)
    #print ("this is babyrec "  + str(baby_rec))
    if len(baby_rec) >= 5:
        avg_session_time = avg_session(baby_rec)

        avg_naptime_day = avg_nap(baby_rec)

        top_three = three_top(baby_rec)

        sleep_night = get_night (baby_rec, 'time')

        bed_time = get_night(baby_rec, 'sleep')

        wake_time = get_night(baby_rec, 'wake')

        return render_template('/view.html',entries = len(baby_rec), baby_rec = baby_rec, babys = babys, name = babyname[0]['name'],avg_session_time=avg_session_time, naptime_day= avg_naptime_day, top_three=top_three, avg_night_sleep = sleep_night, bed_time = bed_time, wake_time = wake_time)
    else:
        return render_template('/view.html', baby_rec = baby_rec, babys = babys, name = babyname[0]['name'],entries = len(baby_rec))


@app.route ("/", methods =["GET","POST"])
@login_required
def index():
    if request.method == "POST":
        babys = babyTable()
        date = request.form.get ("date")
        sleep = request.form.get ("sleep")
        wake = request.form.get ("wake")
        baby_id = request.form.get ("baby_id")

        if date == '' or date == None or sleep == '' or wake == '' or baby_id == '':
            return render_template ("index.html", babys=babys, message = "Failed. Check entries", color ="red")

        else:
            db.execute ('INSERT INTO sleeprec (baby_id, date, sleep, wake) VALUES (?,?,?,?)', baby_id, date, sleep, wake)
            return render_template ("index.html", babys=babys, message = "Success. Entry Added.", color ="green")

    else:
        babys = babyTable()
        return render_template ("index.html", babys=babys)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted

        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route ("/manage-babies", methods=["GET","POST"])
@login_required
def manage():
    if request.method == "POST":
        babyname = request.form.get ("babyname").strip()
        message =""
        babys = babyTable()
        if babyname != '':
            db.execute ('INSERT INTO babys (name, parent_id) VALUES (?,?)', babyname, session['user_id'])
            babys = babyTable()
            return render_template ("/manage-babies.html", babys = babys, message = "Success. Baby Added.", color ="green")

        else:
            return render_template ("/manage-babies.html", babys = babys, message = "Failed: no name entered", color ="red")

    else:
        babys = babyTable()
        return render_template ("/manage-babies.html", babys = babys)

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username").strip()
        password = request.form.get("password").strip()
        babyname = request.form.get("babyname").strip()
        confirmation = request.form.get("confirmation").strip()
        exists = db.execute ("SELECT username FROM users WHERE username = ?", username)
        #if the db call above does not reutrn an empty string then the username already exists
        if exists != []:
            return apology ("Choose another Username. The username " + username + " is taken")
        elif password != confirmation or password == "" or confirmation == "" or username == "" or babyname == "":
            return apology ("Empty fields OR Passwords do not match. please try again")
        else:
            password_h = generate_password_hash(password)
            db.execute ("INSERT INTO users (username, hash) VALUES (?, ?)", username, password_h)

            uid_o = db.execute ("SELECT id FROM users WHERE username = ?", username)
            print(uid_o)
            uid = uid_o[0]['id']
            print (uid)
            db.execute ("INSERT INTO babys (name, parent_id) VALUES (?, ?)", babyname, int(uid))
            return render_template ("login.html")

    else:
        return render_template("register.html")

@app.route("/import", methods=["GET", "POST"])
@login_required
def import_data(): # CONTINUE HERE --- > Matching of dates doesnt work yet!! need to find the date pattern, match it and save into db
    if request.method == 'POST':

        # for secure filenames. Read the documentation.
        file = request.files['myfile']
        filename = secure_filename(file.filename)

        # os.path.join is used so that paths work in every operating system
        file.save(os.path.join("temp",filename))

        # You should use os.path.join here too.
        with open("temp/"+filename) as f:
            file_content = f.read().split('\r')

        # splits into a new list
        new_content = re.split('\n+', file_content[0])

        # Intialise the the entries list which is needed to. collect the correctly formated data
        entries = []

        #search all items of new content list for a date, sleep time and wake time
        for item in new_content:
            founddate = re.search ('\d+\.\d+\.\d+', item)
            foundsleep = re.search ('(?<=MESZ:\s)\d+(\.|\:)\d+', item)
            foundwake = re.search ('(?<=-)(\s?)\d+(\.|:)\d+', item)

            # when all three have been found
            if founddate != None and foundsleep != None and foundwake != None:

                #create a single entry object
                entry = {'date':founddate.group()}

                #find a day
                day_obj = re.search ('\d+(?=\.)', entry['date'])
                day = day_obj.group().strip()

                #find the month
                mon_obj = re.search ('(?<=\.)\d+(?=\.)', entry['date'])
                mon = mon_obj.group().strip()

                #find the year
                year_obj = re.search ('2022', entry['date'])
                year = year_obj.group().strip()

                #make the correct format
                entry ['date'] = year + '-' + mon + '-' + day

                #Get the sleep time and format it correctly
                entry ['sleep'] = foundsleep.group().strip()
                entry ['sleep'] = re.sub ('\.',':',entry ['sleep'])
                single_dig = re.search('^\d(?=\:)', entry ['sleep'] )

                #if its not double digit then make it. eg. 7 becomes 07
                if single_dig != None:
                    double_dig = '0'+single_dig.group()
                    entry['sleep'] = re.sub ('^\d(?=\:)',str(double_dig), entry['sleep'] )

                #same as above only for wake time
                entry ['awake'] = foundwake.group().strip()
                entry ['awake'] = re.sub ('\.',':',entry ['awake'])

                single_digw = re.search('^\d(?=\:)',entry ['awake'] )
                if single_digw != None:
                    double_digw = '0'+single_digw.group()
                    print(double_digw)
                    entry ['awake']= re.sub ('^\d(?=\:)', double_digw, entry ['awake'])
                    print (entry)



                entries.append(entry)
                print (entry)

        babyid = request.form.get("baby_id").strip()
        parentid = session["user_id"]

        #now add all entries into the sleeprec table
        for item in entries:
            db.execute ('INSERT INTO sleeprec (baby_id, date, sleep, wake) VALUES (?,?,?,?)', babyid, item['date'], item['sleep'], item['awake'])

        return render_template ("/file-content.html", file_content=entries)


    else:
        return render_template ("/import.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


# THE PLAN IS TO BE ABLE TO ENABLE THE VIEW ENTRIES BUTTON. tryied to pass it as a function parameter but its not working atm
@app.route ("/view", methods=["GET","POST"])
@login_required
def view():
    if request.method=="POST":

        baby_id = request.form.get ("baby_id")
        babys = babyTable()
        print (babys)


        if baby_id == "" or not any(d['id'] == int(baby_id) for d in babys):
            return render_template ("/view.html", babys = babys, entries = -10)

        return view_func(baby_id)


    else:
        babys = babyTable()
        return render_template ("/view.html", babys = babys, entries = -8)
    #Average amount of naps per day (from 07:00 - max. 19:00)
    #Wie viele Stunden pro tag geschlafen
    #Grafische Darstellung der Schlafstunden pro tag
    #Einschlafzeit die am häufigsten Auftaucht
    #
    #
    #
#2.5#
  #2#
#STD#         ############
# 01#         #          #
# .5#         #          #                   ####
    ##################################################
    #07:00    ^     9:00    ^     11:00.    ^.    13:00