from DBase import DBConnection
from Constants import Constants

class DBscript:

    def __init__(self):
        self.connection = DBConnection.DBConnection()
        self.connection.connect()
        self.device_id = 200

    def insertStory(self,story):
        story = {
            "Story_name": story.name,
            "Story_discription": story.descripton,
            "Story_number": story.story_number,
            "Story_points": story.points,
            "Story_sprint": story.sprint,
            "developer" : story.developer,
            "dependent_stories" : story.dependent_stories
        }
        rec_id5 = self.connection.story_collection.insert_one(story)

    def insertComments(self,comment):
        comment = {
            "User_id": comment.user_id,
            "Date_Time": comment.date_time,
            "Text": comment.text,
            "Story_id": comment.story_id
        }
        rec_id6 = self.connection.comment_collection.insert_one(comment)

    def insertConversation(self,conversation):
        conversation = {
            "Actor": conversation.actor,
            "Text": conversation.text,
            "Time": conversation.time,
            "DeviceId": Constants.device_id
        }
        id = self.connection.conversation_collection.insert_one(conversation)