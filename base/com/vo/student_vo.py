from bson.objectid import ObjectId
from flask import config
from pymongo import MongoClient

from base import app,db

class StudentVo(object):

    def __init__(self):
        self.collection=db.student_collection

    def insert_student(self, student_data):
        self.collection.insert_one(student_data)

    def find_student_by_id(self, student_id):
        return self.collection.find_one({"_id": ObjectId(student_id)})

    def update_student(self, student_id, updated_data):
        self.collection.update_one({"_id": ObjectId(student_id)}, {"$set": updated_data})

    def delete_student(self, student_id):
        self.collection.delete_one({"_id": ObjectId(student_id)})

    def list_students(self):
        return list(self.collection.find())
    
    
    # Don't delete this 
    # sub_category_id = db.Column('sub_category_id', db.Integer,
    #                             db.ForeignKey(SubCategoryVo.sub_category_id, ondelete='CASCADE', onupdate='CASCADE'),
    #                             nullable=False)
   