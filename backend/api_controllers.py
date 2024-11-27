from flask_restful import Resource,Api
from flask import request
from .models import *


api=Api()

class ServiceApi(Resource):
    def get(self):
        pass
    def post(self):
        pass
    def put(self):
        pass
    def delete(self):
        pass


api.add_resource (ServiceApi,"/api/get_service")