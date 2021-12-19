from flask import request,render_template,flash,redirect
from app import app,db
from app.models import Credential
from scipy.stats import t
import math

@app.route("/")
def index():
    return redirect("/register")

@app.route("/login",methods=['GET','POST'])
def login():
    if(request.method == "POST"):

        sampleMeanDwell = float(request.form['dwellAvg'])
        sampleMeanFlight = float(request.form['flightAvg'])
        sampleSDDwell = float(request.form['dwellSD'])
        sampleSDFlight = float(request.form['flightSD'])
        v1 = int(request.form['n1']) - 1
        v2 = int(request.form['n2']) - 1

        retrieved = Credential.query.filter_by(email=request.form['email']).first()
        if(retrieved is None):
            flash("Invalid Email and/or Password")
            return redirect("/login")

        tStatisticDwell = (sampleMeanDwell - retrieved.dwellAvg) / (sampleSDDwell / math.sqrt(v1))
        tStatisticFlight = (sampleMeanFlight - retrieved.flightAvg) / (sampleSDFlight / math.sqrt(v2))
        
        criticalDwell = t.ppf(0.99,v1)
        criticalFlight = t.ppf(0.99,v2)
            
        percentage1 = abs(tStatisticDwell) / criticalDwell
        percentage2 = abs(tStatisticDwell) / criticalDwell
        percentage = (((1 - percentage1) * 100) + ((1 - percentage2) * 100)) / 2
        string = "Confidence "+str(int(percentage))+"%"
        flash(string)
        return redirect("/login")
        
    return render_template("login.html",title="Login")

@app.route("/register",methods=['GET','POST'])
def register():
    if(request.method == "POST"):
        if request.form['email1'] == "":
                return regError("Please type an email.")
        if request.form['email2'] == "":
                return regError("Please type an email.")
        if request.form['email3'] == "":
                return regError("Please type an email.")
        if request.form['password1'] == "":
                return regError("Please enter a password.")
        if request.form['password2'] == "":
                return regError("Please confirm password.")
        if request.form['password3'] == "":
                return regError("Please confirm password.")
        if request.form['password1'] != request.form['password2']:
                return regError("Passwords did not match. Please enter passwords again.")
        if request.form['password1'] != request.form['password3']:
                return regError("Passwords did not match. Please enter passwords again.")
        if request.form['email1'] != request.form['email2']:
                return regError("Passwords did not match. Please enter passwords again.")
        if request.form['email1'] != request.form['email3']:
                return regError("Passwords did not match. Please enter passwords again.")



        username = request.form['email1']
        password = request.form['password1']

        dwellAvg =  float(request.form['dwellAvg'])
        dwellSD =  float(request.form['dwellSD'])
        flightAvg =  float(request.form['flightAvg'])
        flightSD =  float(request.form['flightSD'])


        retrieved = Credential.query.filter_by(email=request.form['email1']).first()
        if(retrieved):
            flash("Invalid Email")
            return redirect("/register")

        c = Credential(username,password,dwellAvg,flightAvg,dwellSD,flightSD)
        db.session.add(c)
        db.session.commit()
        flash("Successfully registered")
        return redirect("/register")
    return render_template("register.html",title="Register")

def regError(message):
    flash(message)
    return render_template("register.html",pageType=['register'],flashType="danger")


if(__name__ == "__main__"):
    app.run(debug=True,port=80)