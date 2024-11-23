from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()

#1 entity

class ServiceProf(db.Model):
    __tablename__="service_prof"
    id=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String,unique=True,nullable=False)
    password=db.Column(db.String,nullable=False)
    full_name=db.Column(db.String,nullable=False)
    phone_no=db.Column(db.String,nullable=False)
    experience=db.Column(db.Integer,default=0)
    service_name=db.Column(db.String,nullable=False)
    address=db.Column(db.String,nullable=False)
    pincode=db.Column(db.Integer,nullable=False)
    resume_path = db.Column(db.String, nullable=True)
    service_requests=db.relationship("ServiceRequest",cascade="all,delete",backref="service_prof",lazy=True)

#2 entity
class UserInfo(db.Model):
    __tablename="user_info"
    id=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String,unique=True,nullable=False)
    password=db.Column(db.String,nullable=False)
    role=db.Column(db.Integer,default=1)
    full_name=db.Column(db.String,nullable=False)
    phone_no=db.Column(db.String,nullable=False)
    address=db.Column(db.String,nullable=False)
    pincode=db.Column(db.Integer,nullable=False)
    service_req=db.relationship("ServiceRequest",cascade="all,delete",backref="user_info",lazy=True)
    


#3 entity
class Service(db.Model):
    __tablename="service"
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String,unique=True,nullable=False)
    price=db.Column(db.Integer,nullable=False)
    descrip=db.Column(db.String,nullable=False)
    service_r=db.relationship("ServiceRequest",cascade="all,delete",backref="service",lazy=True)


#4 entity
class ServiceRequest(db.Model):
    __tablename="service_request"
    id=db.Column(db.Integer,primary_key=True)
    service_id=db.Column(db.Integer,db.ForeignKey("service.id"),nullable=False)
    customer_id=db.Column(db.Integer,db.ForeignKey("user_info.id"),nullable=False)
    proff_id=db.Column(db.Integer,db.ForeignKey("service_prof.id"),nullable=False)
    request_date=db.Column(db.DateTime,nullable=False)
    status=db.Column(db.String,default="available")
    rating=db.Column(db.Integer,nullable=False)
    feedback=db.Column(db.String,nullable=False)



