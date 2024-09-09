from bson.objectid import ObjectId
from flask import config
from pymongo import MongoClient

from base import app,db

# attendence day object structure
# {
#   _id,attendence_marked_timestamp,student_id,status,attendence_day_id
# }

class AttendenceVo(object):

    def __init__(self):
        self.collection=db.attendence_vo

    def insert_attendence(self, attendence_vo):
        return self.collection.insert_one(attendence_vo)

    def find_one(self, attendence_id):
        return self.collection.find_one({"_id": ObjectId(attendence_id)})
    
    def find_one_by_student_id(self, student_id):
        return self.collection.find_one({"student_id": student_id})

    def update_student(self, attendence_id, updated_data):
        self.collection.update_one({"_id": ObjectId(attendence_id)}, {"$set": updated_data})

    def update_student_by_student_id(self, student_id, updated_data):
        self.collection.update_one({"student_id": student_id}, {"$set": updated_data})

    def delete_student(self, student_id):
        self.collection.delete_one({"_id": ObjectId(student_id)})

    def list_students(self):
        return list(self.collection.find())