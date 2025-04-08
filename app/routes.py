from flask import render_template,url_for,request,redirect,session,flash,jsonify
from datetime import datetime,timedelta
from bson import ObjectId

from db import complaint, resident,issues

from app import app


@app.route('/')
def home():
    return render_template('home.html')


@app.route("/report_issue", methods=["GET", "POST"])
def report_issue():
    if not session.get("name"):
        return redirect(url_for("auth.login"))
        
    if request.method == "GET" :
        return render_template("report_issue.html")


    issue_title = request.form.get("title")
    state=request.form.get("state")
    city=request.form.get("city")
    location = request.form.get("location")
    description = request.form.get("description")
    issue_type = request.form.get("issue_type")
    severity_level = request.form.get("severity")
    image = request.files.get("images")
    status="Pending"


    if issue_title and location and description and issue_type and severity_level and image:
        data = {
            "resident_id":session["_id"],
            "email":session["email"],
            "title": issue_title,
            "location": location,
            "description": description,
            "issueType": issue_type,
            "state":state,
            "city":city,
            "issueDate":datetime.now(),
            "completionDate":datetime.now()+timedelta(days=7),
            "severity": severity_level,
            "image":image.read(),
            "status":status,
            "manpower":0,
            "resources":{},
            "machines":0


        }
        complaint.insert_one(data)
        flash("Issue reported successfully!", "success")
        return redirect(url_for("home"))
    else:
        flash("All fields are required!", "danger")

    return render_template("report_issue.html")

@app.route("/track-repair")
def track_repair():
    if not session.get("name"):
        return redirect(url_for("auth.login"))

    return render_template("track_repair.html")



@app.route("/contact",methods=["GET","POST"])
def contact():
    return render_template("contact.html")


from flask import jsonify
from bson import ObjectId
@app.route("/get_repairs", methods=["GET"])
def get_repairs():
    if not session.get("name"):
        return redirect(url_for("auth.login"))

    repairs_cursor = complaint.find({"email": session["email"]})  # Get cursor from MongoDB
    repair_data = [
        {
            "resident_id": str(repair.get("resident_id", "")),  
            "title": repair.get("title", ""),
            "issueDate": repair.get("issueDate").isoformat() if repair.get("issueDate") else None,
            "completionDate": repair.get("completionDate").isoformat() if repair.get("completionDate") else None,
            "status": repair.get("status", "Pending"),
            "severity": repair.get("severity", ""),
            "issueType": repair.get("issueType", ""),
            "location": repair.get("location", "")
        }
        for repair in repairs_cursor  # Iterate over cursor
    ]

    return jsonify(repair_data), 200  # Return JSON response
