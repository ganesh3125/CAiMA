from pymongo import MongoClient


class DBConnection:

    def __init__(self):
        self.conn = None
        self.developer_collection = None
        self.db = None

    def connect(self):
        try:
            self.conn = MongoClient()
            print("Connected to MongoDB successfully!!!")
        except:
            print("Could not connect to MongoDB")

        db = self.conn.CAiMA_collection
        self.developer_collection = db.developer
        self.story_collection =  db.story
        self.ba_collection = db.ba
        self.qa_collection = db.qa
        self.manager_collection = db.manager
        self.comment_collection = db.comment
        self.timelog_collection = db.timelog
        self.conversation_collection = db.conversation

#db.createCollection("name")