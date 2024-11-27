from flask_restful import Resource,Api
from flask import request
from .models import *


api=Api()

class ServiceApi(Resource):
    def get(self):
        service=UserInfo.query.all()
        service_json=[]
        for s in service:
            service_json.append({'id':s.id,'email':s.email,'password':s.password,'role':s.role,'full_name':s.full_name,'phone_no':s.phone_no,'address':s.address,'pincode':s.pincode})
        return service_json

    def post(self):
        id=request.json.get('id')
        email=request.json.get('email')
        password=request.json.get('password')
        role=request.json.get('role')
        full_name=request.json.get('full_name')
        phone_no=request.json.get('phone_no')
        address=request.json.get('address')
        pincode=request.json.get('pincode')
        new_usr=UserInfo(id=id,email=email,password=password,role=role,full_name=full_name,phone_no=phone_no,address=address,pincode=pincode)
        db.session.add(new_usr)
        db.session.commit()

        return{"message":"new user added!!"},200
    def put(self,id):
        user=UserInfo.query.filter_by(id=id).first()
        if user:
            user.password=request.json.get('password')
            user.email=request.json.get('email')
            user.role=request.json.get('role')
            user.full_name=request.json.get('full_name')
            user.phone_no=request.json.get('phone_no')
            user.address=request.json.get('address')
            user.pincode=request.json.get('pincode')
            db.session.commit()
            return{"message":"User details updated!!"},200
        return{"message":"User not found!!"},404
        
    def delete(self,id):
        user=UserInfo.query.filter_by(id=id).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            return{"message":"User Deleted!!"},200
        return{"message":"User not found!!"},404



api.add_resource(ServiceApi,"/api/get_user","/api/add_user","/api/edit_user/<id>","/api/delete_user/<id>")