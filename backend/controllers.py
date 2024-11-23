from flask import Flask, render_template,request,redirect,url_for
from flask import current_app as app
from .models import *
from werkzeug.utils import secure_filename 
import os 

@app.route("/")
def house():
    return render_template("main.html")

@app.route("/login")
def signin():
    return render_template("login.html")

@app.route("/dashboard",methods=["GET","POST"])
def dashboardc():
    if request.method=="POST":
        uname=request.form.get("user_name")
        pwd=request.form.get("password")
        if uname=="admin123@iitm.ac.in" and pwd=="admin123":
            return render_template("admin_dashboard.html",msg="Welcome")
        if UserInfo.query.filter_by(email=uname,password=pwd).first():
            return render_template("customer_dashboard.html",msg="Welcome")
        if ServiceProf.query.filter_by(email=uname,password=pwd).first():
            return render_template("prof_dashboard.html",msg="Welcome")
        if UserInfo.query.filter_by(email=uname).first() or ServiceProf.query.filter_by(email=uname).first() :
            return render_template("login.html", msg="Invalid credentials. Please try again.")
        return render_template("login.html",msg="You are not registered yet!!!")

@app.route("/registerc",methods=["GET","POST"])
def signupc():
    if request.method=="POST":
        uname=request.form.get("user_name")
        pwd=request.form.get("password")
        fullname=request.form.get("full_name")
        phoneno=request.form.get("phone_no")
        address=request.form.get("address")
        pincode=request.form.get("pincode")
        usr=UserInfo.query.filter_by(email=uname).first()
        if usr:
            return render_template("customer_signup.html",msg="Sorry,this mail is already registred!!!")
        new_usr=UserInfo(email=uname,password=pwd,full_name=fullname,phone_no=phoneno,address=address,pincode=pincode)
        db.session.add(new_usr)
        db.session.commit()
        return render_template("login.html",msg="Registration successfull, you can now login.")
    
    return render_template("customer_signup.html",msg="")

UPLOAD_FOLDER = 'uploads/resumes'  # Directory to store uploaded files
ALLOWED_EXTENSIONS = {'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/registers",methods=["GET","POST"])
def signups():
    if request.method=="POST":
        uname=request.form.get("user_name")
        pwd=request.form.get("password")
        fullname=request.form.get("fullname")
        phoneno=request.form.get("phone_no")
        service=request.form.get("service")
        exp=request.form.get("exp")
        address=request.form.get("address")
        pincode=request.form.get("pincode")

        file = request.files.get("resume")
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
        else:
            return render_template("ser_proff_signup.html", msg="Invalid file type. Only PDFs are allowed.")


        usr=ServiceProf.query.filter_by(email=uname).first()
        if usr:
            return render_template("ser_proff_signup.html",msg="Sorry,this mail is already registred!!!")
        new_usr=ServiceProf(email=uname,password=pwd,full_name=fullname,phone_no=phoneno,experience=exp,service_name=service,address=address,pincode=pincode,resume_path=file_path)
        db.session.add(new_usr)
        db.session.commit()
        return render_template("login.html",msg="Resgistration successfull, try login now!!")
    return render_template("ser_proff_signup.html",msg="")