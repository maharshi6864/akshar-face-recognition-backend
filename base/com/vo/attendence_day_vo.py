from bson.objectid import ObjectId
from flask import config
from pymongo import MongoClient

from base import app,db

# attendence day object structure
# {
#   _id,timestamp,(student_class id will be added later)
# }

class AttendenceDayVo(object):

    def __init__(self):
        self.collection=db.attendence_day_collection

    def insert_attendence_for_day(self, attendence_day):
        return self.collection.insert_one(attendence_day)

    def find_attendence_day_by_id(self, attendence_day_id):
        return self.collection.find_one({"_id": ObjectId(attendence_day_id)})
    
    def find_attendence_by_timestamp(self, attendence_day_timestamp):
        return self.collection.find_one({"timestamp": attendence_day_timestamp})

    def update_student(self, student_id, updated_data):
        self.collection.update_one({"_id": ObjectId(student_id)}, {"$set": updated_data})

    def delete_student(self, student_id):
        self.collection.delete_one({"_id": ObjectId(student_id)})

    def list_students(self):
        return list(self.collection.find())