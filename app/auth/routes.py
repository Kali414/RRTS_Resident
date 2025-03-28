from app.auth import auth
from flask import render_template,url_for,request,session,redirect

from db import resident

@auth.route('/signup',methods=["GET","POST"])
def signup():
    if(request.method=="POST"):
        first_name=request.form.get("first")
        last_name=request.form.get("last")
        email=request.form.get("email")
        number=request.form.get("number")
        city=request.form.get("city")
        state=request.form.get("state")
        password=request.form.get("password")

        if(first_name and last_name and email and number and city and state and password):

            data={
                "name": first_name+" "+last_name,
                "email":email,
                "number":number,
                "city":city,
                "state":state,
                "password":password,
                "role":"Resident"
            }
            user = resident.find_one({"email": email, "password": password})
            if user:
                return redirect(url_for("auth.login"))
            # Attempt to find the document with the highest _id
            last_doc = resident.find_one(sort=[("_id", -1)])

            if last_doc is None:
                # If no document is found, start with "R001"
                new_id = "R001"
            else:
                # Get the last _id and increment its numeric part
                last_id = last_doc.get("_id")
                # Extract numeric part, increment it, and format with zero-padding for 3 digits
                new_num = int(last_id[1:]) + 1
                new_id = "R" + str(new_num).zfill(3)

            # Add the new _id to the data dictionary
            data["_id"] = new_id

            # Insert the new document into the collection
            resident.insert_one(data)
            session["name"]=first_name+" "+last_name
            session["role"]="Resident"
            session["email"]=email
            session["number"]=number
            session["city"]=city
            session["state"]=state
            session['_id']=new_id
            return redirect(url_for("home"))
        
        else:
            return render_template("signup.html")

    return render_template("signup.html")

@auth.route('/login',methods=["GET","POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        role="Resident"
            
        user = resident.find_one({"email": email, "password": password})
        
        if user:
            session["name"] = user["name"]
            session["role"]=user["role"]
            session["email"]=user["email"]
            session["number"]=user["number"]
            session["city"]=user["city"]
            session["state"]=user["state"]
            session['_id']=user["_id"]

            return redirect(url_for("home"))
        
        else:
            return redirect(url_for("auth.signup"))

    
    return render_template("login.html")


@auth.route("/logout")
def clear_session():
    session.clear()
    return redirect("https://rrts-login.onrender.com")

        