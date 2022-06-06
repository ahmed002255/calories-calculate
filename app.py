from flask import Flask, render_template, session, request, redirect
from flask_session import Session
from cs50 import SQL
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required


#make the flask app
app = Flask(__name__)

#make the data base table
db = SQL("sqlite:///database.db")


#make the session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
#make sure that all template auto play
app.config["TEMPLATES_AUTO_RELOAD"] = True



#make the login page
@app.route("/")
def index():
    return render_template("login.html")



#make the portfolio page
@app.route("/profile")
def profile():
    user_id = session["user_id"]
    profile = db.execute("SELECT name FROM users WHERE id = ?", user_id)
    return render_template("profile.html" , profile=profile)


#make the home page
@app.route("/index", methods=["GET","POST"])
@login_required
def homepage():
    Gender = [
             "male",
            "female"
            ]
    daily_in_take =[
            "little to no",
            "light 1 to 3",
            "moderate 3 to 5",
            "heavy 6 to 7",
            "very heavy twice per day"
        ]

    if request.method == "POST":
        name = request.form.get("name")
        Gender = request.form.get("Gender")
        daily_in_take = request.form.get("daily_in_take")

        if not name:
            return render_template("sorry.html")
        elif not Gender:
            return render_template("sorry.html")
        try:
            weight = float(request.form.get("weight"))
            age = int(request.form.get("age"))
            height = float(request.form.get("height"))
        except:
            return render_template("sorry.html")
        if Gender == "male" and daily_in_take =="little to no":
            return render_template("theresult.html", result=float((10 * weight) + (6.25 * height) - (5 * age) + 5)*1.2)

        elif (Gender == "male" and daily_in_take =="light 1 to 3"):
            return render_template("theresult.html", result=float((10 * weight) + (6.25 * height) - (5 * age) + 5)*1.375)

        elif (Gender == "male" and daily_in_take =="moderate 3 to 5"):
            return render_template("theresult.html", result=float((10 * weight) + (6.25 * height) - (5 * age) + 5)*1.55)

        elif (Gender == "male"and daily_in_take =="heavy 6 to 7"):
            return render_template("theresult.html", result=float((10 * weight) + (6.25 * height) - (5 * age) + 5)*1.725)

        elif (Gender == "male" and daily_in_take =="very heavy twice per day"):
            return render_template("theresult.html", result=float((10 * weight) + (6.25 * height) - (5 * age) + 5)*1.9)


        elif (Gender == "female" and daily_in_take =="little to no"):
            return render_template("theresult.html", result=float((10 * weight) + (6.25 * height) - (5 * age) - 161)*1.2)

        elif (Gender == "female" and daily_in_take =="light 1 to 3"):
            return render_template("theresult.html", result=float((10 * weight) + (6.25 * height) - (5 * age) - 161)*1.375)

        elif (Gender == "female" and daily_in_take =="moderate 3 to 5"):
            return render_template("theresult.html", result=float((10 * weight) + (6.25 * height) - (5 * age) - 161)*1.55)

        elif (Gender == "female" and daily_in_take =="heavy 6 to 7"):
            return render_template("theresult.html", result=float((10 * weight) + (6.25 * height) - (5 * age) - 161)*1.725)

        elif (Gender == "female" and daily_in_take =="very heavy twice per day"):
            return render_template("theresult.html", result=float((10 * weight) + (6.25 * height) - (5 * age) - 161)*1.9)

    else:
        return render_template("index.html")

#make the log in data
@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure name was submitted
        if not request.form.get("name"):
            return render_template("sorry.html")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("sorry.html")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE name = ?", request.form.get("name"))

        # Ensure name exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return render_template("sorry.html")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/index")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")



# make all register data needed
@app.route("/register", methods=["GET","POST"])
def register():
    #register make the name and the password
    if request.method == "POST":
        name = request.form.get("name")
        password = request.form.get("password")
        confirm = request.form.get("confirm")
        if not name:
            return render_template("sorry.html")
        elif not password:
            return render_template("sorry.html")
        elif not confirm:
            return render_template("sorry.html")
        if password != confirm:
            return render_template("sorry.html")
        #generate the password
        hash = generate_password_hash(password)
        try:
            db.execute("INSERT INTO users(name, hash) VALUES(?, ?)", name, hash)
            return redirect("/")
        except:
            return render_template("login.html")
    else:
        return render_template("register.html")


#make the logout page
@app.route("/logout")
def logout():

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")