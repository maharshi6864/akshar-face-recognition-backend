from bson.objectid import ObjectId
from flask import config
from pymongo import MongoClient

from base import app,db

class UserVo(object):

    def __init__(self):
        self.collection=db.user_vo

    def insert_user(self, user_data):
        self.collection.insert_one(user_data)

    def find_user_by_id(self, user_id):
        return self.collection.find_one({"_id": ObjectId(user_id)})

    def update_user(self, user_id, updated_data):
        self.collection.update_one({"_id": ObjectId(user_id)}, {"$set": updated_data})

    def delete_user(self, student_id):
        self.collection.delete_one({"_id": ObjectId(student_id)})

    def list_user(self):
        return list(self.collection.find())
    
    
    # Don't delete this 
    # sub_category_id = db.Column('sub_category_id', db.Integer,
    #                             db.ForeignKey(SubCategoryVo.sub_category_id, ondelete='CASCADE', onupdate='CASCADE'),
    #                             nullable=False)
   