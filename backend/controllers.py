from flask import Flask, render_template,request,redirect,url_for,session
from flask import current_app as app
from .models import *
from werkzeug.utils import secure_filename 
import os 
from flask import send_from_directory
from datetime import datetime
import matplotlib.pyplot as plt

@app.route("/")
def house():
    return render_template("main.html")

@app.route("/login")
def signin():
    return render_template("login.html")

@app.route('/uploads/image/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER_'], filename)

@app.route('/uploads/resume/<filename>')
def uploaded_resume(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route("/dashboard",methods=["GET","POST"])
def dashboardc():
    if request.method=="POST":
        uname=request.form.get("user_name")
        pwd=request.form.get("password")
        if uname=="admin123@iitm.ac.in" and pwd=="admin123":
            return redirect(url_for("admin_dashboard",name=uname))
        if UserInfo.query.filter_by(email=uname,password=pwd).first():
            user = UserInfo.query.filter_by(email=uname, password=pwd).first()
            return redirect(url_for("customer_dashboard", name=uname, id=user.id))
        if ServiceProf.query.filter_by(email=uname,password=pwd).first():
            user = ServiceProf.query.filter_by(email=uname, password=pwd).first()
            return redirect(url_for("prof_dashboard", name=uname, id=user.id))
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


UPLOAD_FOLDER_ = 'static/service_images'  # Directory for service images
ALLOWED_EXTENSIONS_ = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER_'] = UPLOAD_FOLDER_

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

if not os.path.exists(app.config['UPLOAD_FOLDER_']):
    os.makedirs(app.config['UPLOAD_FOLDER_'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def allowed_file_(filename_):
    return '.' in filename_ and filename_.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_

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
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename).replace("\\","/")
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

#common route for admin dashboard
@app.route("/admin/<name>")
def admin_dashboard(name):
    service=get_services()
    p=get_professionals()
    ser_req=get_service_requests()
    return render_template("admin_dashboard.html",name=name,service=service,prof=p,ser_req=ser_req)

#common route for customer dashboard
@app.route("/customer/<name>/<id>")
def customer_dashboard(name,id):
    user = UserInfo.query.filter_by(id=id).first()
    service=get_services()
    service_requests = user.service_req if user else []
    return render_template("customer_dashboard.html",id=id,name=name,service=service,service_requests=service_requests)

#common route for professional dashboard
@app.route("/professional/<name>/<id>")
def prof_dashboard(name,id):
    user = ServiceProf.query.filter_by(id=id).first()
    if user:
        service_requests = user.service_requests
        for request in service_requests:
            customer = UserInfo.query.filter_by(id=request.customer_id).first()
            request.customer = customer 
    else:
        service_requests = []
    return render_template("prof_dashboard.html",id=id,name=name,ser_req=service_requests)

@app.route("/professional/<name>/<id>/accept_request/<request_id>")
def accept_request(name, id, request_id):
    service_request = ServiceRequest.query.filter_by(id=request_id).first()
    service_request.status = "accepted"
    db.session.commit()
    return redirect(url_for("prof_dashboard", name=name, id=id))

@app.route("/professional/<name>/<id>/reject_request/<request_id>")
def reject_request(name, id, request_id):
    service_request = ServiceRequest.query.filter_by(id=request_id).first()
    service_request.status = "rejected"
    db.session.commit()        
    return redirect(url_for("prof_dashboard", name=name, id=id))


@app.route("/customer/book/<name>/<id>/<sname>")
def book_proff(name,id,sname):
    prof=get_proff(sname)
    user = UserInfo.query.filter_by(id=id).first()
    return render_template("request_service.html",name=name,sname=sname,servicesubtype=prof,id=id)

@app.route("/customer/book/<name>/<pid>")
def gen_req(name,pid):
    prof=get_p(pid)
    a=prof.service_name
    service = Service.query.filter_by(name=a).first()
    c=UserInfo.query.filter_by(email=name).first()
    new_req=ServiceRequest(service_id=service.id,customer_id=c.id,proff_id=pid,request_date=datetime.now())
    db.session.add(new_req)
    db.session.commit()
    return redirect(url_for("customer_dashboard",name=name,id=c.id))


@app.route("/servicess/<name>",methods=["POST","GET"])
def add_service(name):
    if request.method=="POST":
        sname=request.form.get("name")
        price=request.form.get("price")
        descp=request.form.get("description")
        time_required=request.form.get("time_required")
        file = request.files.get('service_image')
        file_path = None  # Initialize file path
        if file and allowed_file_(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join('service_images', filename).replace("\\","/")
            file.save(os.path.join(app.config['UPLOAD_FOLDER_'], filename))


        new_service=Service(name=sname,price=price,descrip=descp,image_path=file_path,time_required=time_required)
        db.session.add(new_service)
        db.session.commit()
        return redirect(url_for("admin_dashboard",name=name))


    return render_template("add_service.html",name=name)

@app.route("/search/<name>", methods=["GET", "POST"])
def search(name):
    search_type = request.form.get('search_type')
    search_term = request.form.get('search_term')
    results = []

    if request.method == "POST":
        if search_type == "service":
            results = Service.query.filter(Service.name.ilike(f"%{search_term}%")).all()
        elif search_type == "customer":
            results = UserInfo.query.filter((UserInfo.full_name.ilike(f"%{search_term}%"))|(UserInfo.pincode.ilike(f"%{search_term}%"))).all()
        elif search_type == "professional":
            results = ServiceProf.query.filter((ServiceProf.full_name.ilike(f"%{search_term}%"))|(ServiceProf.pincode.ilike(f"%{search_term}%"))|(ServiceProf.rating.ilike(f"%{search_term}%"))).all()
        elif search_type == "service_request":
            results = ServiceRequest.query.filter((ServiceRequest.status.ilike(f"%{search_term}%"))|(ServiceRequest.rating.ilike(f"%{search_term}%"))).all()
    return render_template("admin_search.html",name=name,results=results,search_type=search_type,search_term=search_term)

@app.route("/customer/search/<name>/<id>", methods=["GET", "POST"])
def search_cus(name,id):
    search_type = request.form.get('search_type')
    search_term = request.form.get('search_term')
    results = []
    if request.method == "POST":
        if search_type == "service":
            results = Service.query.filter(Service.name.ilike(f"%{search_term}%")).all()
        elif search_type == "professional":
            results = ServiceProf.query.filter((ServiceProf.full_name.ilike(f"%{search_term}%"))|(ServiceProf.pincode.ilike(f"%{search_term}%"))|(ServiceProf.rating.ilike(f"%{search_term}%"))).all()
    return render_template( "customer_search.html",name=name,results=results,search_type=search_type,search_term=search_term,id=id)


@app.route("/professional/search/<name>/<id>", methods=["GET", "POST"])
def search_prof(name, id):
    search_term = request.form.get('search_term')
    results = []
    if request.method == "POST":
        results = ServiceRequest.query.filter(ServiceRequest.status.ilike(f"%{search_term}%"),ServiceRequest.proff_id == id).all()
    return render_template("prof_search.html",name=name, id=id,results=results,search_term=search_term)



@app.route("/edit_service/<id>/<name>",methods=["GET","POST"])
def edit_service(id,name):
    s=get_service(id)
    if request.method=="POST":
        name=request.form.get("name")
        price=request.form.get("price")
        time_required=request.form.get("time_required")
        descp=request.form.get("description")
        s.name=name
        s.price=price
        s.descrip=descp
        s.time_required=time_required
        db.session.commit()
        return redirect(url_for("admin_dashboard",name=name))
    return render_template("edit_service.html",service=s,name=name)


@app.route("/edit_admin_profile/<name>",methods=["GET","POST"])
def edit_admin_profile(name):
    s=UserInfo.query.filter_by(email=name).first()
    if request.method=="POST":
        aname=request.form.get("aname")
        phoneno=request.form.get("phoneno")
        address=request.form.get("address")
        pincode=request.form.get("pincode")
        s.full_name=aname
        s.phone_no=phoneno
        s.address=address
        s.pincode=pincode
        db.session.commit()
        return redirect(url_for("admin_dashboard",name=name))
    return render_template("edit_admin_profile.html",service=s,name=name)


@app.route("/edit_customer_profile/<name>/<id>",methods=["GET","POST"])
def edit_customer_profile(name,id):
    s=UserInfo.query.filter_by(email=name).first()
    if request.method=="POST":
        aname=request.form.get("aname")
        phoneno=request.form.get("phoneno")
        address=request.form.get("address")
        pincode=request.form.get("pincode")
        s.full_name=aname
        s.phone_no=phoneno
        s.address=address
        s.pincode=pincode
        db.session.commit()
        return redirect(url_for("customer_dashboard",name=name,id=id))
    return render_template("edit_customer_profile.html",service=s,name=name,id=id)


@app.route("/edit_prof_profile/<name>/<id>",methods=["GET","POST"])
def edit_prof_profile(name,id):
    s=ServiceProf.query.filter_by(email=name).first()
    if request.method=="POST":
        aname=request.form.get("aname")
        phoneno=request.form.get("phoneno")
        address=request.form.get("address")
        pincode=request.form.get("pincode")
        s.full_name=aname
        s.phone_no=phoneno
        s.address=address
        s.pincode=pincode
        db.session.commit()
        return redirect(url_for("prof_dashboard",name=name,id=id))
    return render_template("edit_prof_profile.html",service=s,name=name,id=id)

           

@app.route("/edit_proffess/<id>/<name>",methods=["GET","POST"])
def edit_p(id,name):
    p=get_p(id)
    if request.method=="POST":
        name=request.form.get("name")
        email=request.form.get("email")
        phone_no=request.form.get("phone")
        exp=request.form.get("exp")
        p.full_name=name
        p.email=email
        p.phone_no=phone_no
        p.experience=exp
        db.session.commit()
        return redirect(url_for("admin_dashboard",name=name))
    return render_template("edit_proff.html",service_prof=p,name=name)





@app.route("/delete_service/<id>/<name>",methods=["GET","POST"])
def delete_service(id,name):
    s=get_service(id)
    db.session.delete(s)
    db.session.commit()
    return redirect(url_for("admin_dashboard",name=name))


@app.route("/approve_prof/<id>/<name>",methods=["GET","POST"])
def approv_prof(id,name):
    s=get_p(id)
    s.approv_status="Approved"
    db.session.commit()
    return redirect(url_for("admin_dashboard",name=name))


@app.route("/delete_prof/<id>/<name>",methods=["GET","POST"])
def delete_prof(id,name):
    s=get_p(id)
    db.session.delete(s)
    db.session.commit()
    return redirect(url_for("admin_dashboard",name=name))


@app.route("/close_request/<name>/<id>/<int:request_id>", methods=["GET", "POST"])
def close_request(request_id,name,id):
    r=ServiceRequest.query.filter_by(id=request_id).first()
    r.status = "completed"
    r.done_date = datetime.now()
    db.session.commit()
    return render_template("feedback.html",request_id=r.id,name=name,id=id)

@app.route("/feedback_form/<name>/<id>/<int:request_id>", methods=["GET", "POST"])
def feedback_form(request_id, name, id):
    r = ServiceRequest.query.filter_by(id=request_id).first()
    if request.method == "POST":
        request_rating = int(request.form['rating'])
        feedback = request.form['feedback']
        r.rating = request_rating
        r.feedback = feedback
        db.session.commit()
        service_prof = ServiceProf.query.get(r.proff_id)
        existing_rating = service_prof.rating
        past_ratings_count = ServiceRequest.query.filter_by(proff_id=r.proff_id).count()
        if past_ratings_count > 0:
            new_rating_weighted = request_rating * request_rating
            total_weighted_rating = (existing_rating * past_ratings_count) + new_rating_weighted
            total_count = past_ratings_count + request_rating
            new_avg_rating = total_weighted_rating / total_count
        else:
            new_avg_rating = request_rating
        service_prof.rating = new_avg_rating
        db.session.commit()
        return redirect(url_for("customer_dashboard", name=name, id=id))
    return render_template("feedback.html", request_id=r.id, name=name, id=id)


@app.route("/admin_summary/<name>")
def put_admin_summary(name):
    plot=get_service_request_summary()
    plot.savefig("./static/images/service_req_summary.jpeg")
    plot.clf()
    return render_template("admin_summary.html",name=name)


@app.route("/customer/summary/<name>/<id>")
def put_customer_summary(name,id):
    dir_path=f"./static/images/{name}"
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    plot=get_service_request_summary_c(id)
    plot_file_path=os.path.join(dir_path,"c_summary.jpeg")
    plot.savefig(plot_file_path)
    plot.clf()
    return render_template("customer_summary.html",name=name,id=id)

@app.route("/professional/summary/<name>/<id>")
def put_professional_summary(name,id):
    dir_path=f"./static/images/{name}"
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    plot=get_service_request_summary_p(id)
    plot_file_path=os.path.join(dir_path,"c_summary.jpeg")
    plot.savefig(plot_file_path)
    plot.clf()
    return render_template("prof_summary.html",name=name,id=id)

#other functions
def get_services():
    services=Service.query.all()
    return services

def get_professionals():
    p=ServiceProf.query.all()
    return p


def get_service_requests():
    return ServiceRequest.query.all()

def search_by_service(search_txt):
    services=Service.query.filter(Service.name.ilike(f"{search_txt}")).all()
    return services 


def search_by_customer(search_txt):
    cus=UserInfo.query.filter(UserInfo.full_name.ilike(f"{search_txt}")).all()
    return cus

def search_by_proff(search_txt):
    prof=ServiceProf.query.filter(ServiceProf.full_name.ilike(f"{search_txt}")).all()
    return prof 

def get_service(id):
    service=Service.query.filter_by(id=id).first()
    return service

def get_p(id):
    service=ServiceProf.query.filter_by(id=id).first()
    return service

def get_servicesub(id):
    service=ServiceSub.query.filter_by(service_id=id).first()
    return service


def get_proff(name):
    return ServiceProf.query.filter(ServiceProf.service_name.ilike(f"{name}"), ServiceProf.status == "available",ServiceProf.approv_status!="pending").all()

def get_service_request_summary():
    s=get_service_requests()
    summary={"rejected":0,"requested":0,"accepted":0,"completed":0}
    for i in s:
        if i.status=='rejected':
            summary["rejected"]+=1
        elif i.status=='requested':
            summary["requested"]+=1
        elif i.status=='accepted':
            summary["accepted"]+=1
        elif i.status=='completed':
            summary["completed"]+=1        
    x_names=list(summary.keys())
    y_names=list(summary.values())
    fig,ax=plt.subplots()
    ax.bar(x_names, y_names, color="blue", width=0.4)
    ax.set_title("Service Request Stats")
    ax.set_xlabel("Status")
    ax.set_ylabel("No. of Requests")
    return fig

def get_service_request_summary_c(id):
    s = ServiceRequest.query.filter_by(customer_id=id).all()
    summary={"rejected":0,"requested":0,"accepted":0,"completed":0}
    for i in s:
        if i.status=='rejected':
            summary["rejected"]+=1
        elif i.status=='requested':
            summary["requested"]+=1
        elif i.status=='accepted':
            summary["accepted"]+=1   
        elif i.status=='completed':
            summary["completed"]+=1    
    x_names=list(summary.keys())
    y_names=list(summary.values())
    fig,ax=plt.subplots()
    ax.bar(x_names, y_names, color="blue", width=0.4)
    ax.set_title("Service Request Stats")
    ax.set_xlabel("Status")
    ax.set_ylabel("No. of Requests")
    return fig

def get_service_request_summary_p(id):
    s = ServiceRequest.query.filter_by(proff_id=id).all()
    summary={"rejected":0,"requested":0,"accepted":0,"completed":0}
    for i in s:
        if i.status=='rejected':
            summary["rejected"]+=1
        elif i.status=='requested':
            summary["requested"]+=1
        elif i.status=='accepted':
            summary["accepted"]+=1 
        elif i.status=='completed':
            summary["completed"]+=1      
    x_names=list(summary.keys())
    y_names=list(summary.values())
    fig,ax=plt.subplots()
    ax.bar(x_names, y_names, color="blue", width=0.4)
    ax.set_title("Service Request Stats")
    ax.set_xlabel("Status")
    ax.set_ylabel("No. of Requests")
    return fig
