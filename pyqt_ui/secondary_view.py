from pyqt_ui.projevt_view import Window
from PyQt5.QtWidgets import *
import sys
from Utils import Comments
from PyQt5.uic.properties import QtGui
from PyQt5 import QtGui
from DBase import DBConnection, DBscript
from datetime import datetime

class SecondaryWindow:
    def __init__(self):
        self.primary_window = Window()
        self.user_id = 1001
        self.connection = self.connectToDB()
        self.project_name, self.project_description = self.primary_window.returner()

    def connectToDB(self):
        connection = DBConnection.DBConnection()
        connection.connect()
        return connection

    def find_story_id(self,story):
        collection = self.connection.story_collection
        query = {'Story_name':story}
        curser = collection.find(query)
        for item in curser:
            print(item['Story_number'])
            return item['Story_number']

    def status_update_popup(self,win,update,story):
        msg = QMessageBox(win)
        msg.setText("Updated ststus")
        date: datetime = datetime.utcnow()
        story_id = self.find_story_id(story)
        comment = Comments.Comments(self.user_id, date,update, story_id)
        dbscript = DBscript.DBscript()
        dbscript.insertComments(comment)
        msg.show()

    def update_status(self,story,win):
        update_status_dialogue = QDialog(win)
        update_status_dialogue.setGeometry(600,500,400,100)
        update_status_dialogue.setWindowTitle(story)

        edit_desc_box = QLineEdit(update_status_dialogue)
        edit_desc_box.move(25,10)
        edit_desc_box.setFixedWidth(350)

        update_button = QPushButton(update_status_dialogue)
        update_button.setText("update")
        update_button.move(162,50)
        update_button.clicked.connect(lambda :self.status_update_popup(win, edit_desc_box.text(), story))
        update_status_dialogue.show()


    def getMyStories(self):
        query = {"developer": self.user_id}
        collection = self.connection.story_collection
        cursor = collection.find(query).sort('Story_name',1)
        list_of_my_stories = []
        for item in cursor:
            list_of_my_stories.append(item['Story_name'])
        return list_of_my_stories

    def showStory(self,story,win):
        story_dialog = QDialog(win)
        story_dialog.setWindowTitle("Story view")
        collection = self.connection.story_collection
        querry = {"Story_name": story}
        cursor = collection.find(querry)
        story_item = cursor[0]
        storynum = story_item['Story_number']
        dev_id = story_item['developer']
        str_points = story_item['Story_points']
        story_dialog.setGeometry(550, 100, 500, 500)

        collection = self.connection.developer_collection
        querry = {"developer_id": dev_id}
        cursor2 = collection.find(querry)
        developer_item = cursor2[0]
        dev_name = developer_item['name']

        Sname = QLabel(story_dialog)
        Sname.setText("Story Number: ")
        Sname.setGeometry(30, 30, 300, 100)
        Sname.move(140, 10)
        Sname.setFont(QtGui.QFont('Times New Roman', 15))
        Sname.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        SnameT = QLabel(story_dialog)
        SnameT.setText(storynum)
        SnameT.setGeometry(30, 30, 300, 100)
        SnameT.move(270, 10)
        SnameT.setFont(QtGui.QFont('Times New Roman', 15))
        SnameT.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        sdesc_button = QPushButton(story_dialog)
        sdesc_button.setText("see description")
        sdesc_button.move(190, 93)
        sdesc_button.setFixedWidth(120)
        sdesc_button.clicked.connect(lambda: self.primary_window.showStoryDisc(story_item['Story_discription']))

        sdev = QLabel(story_dialog)
        sdev.setText("Developer: ")
        sdev.setGeometry(30, 30, 300, 100)
        sdev.move(167, 118)
        sdev.setFont(QtGui.QFont('Times New Roman', 15))
        sdev.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        sdeN = QLabel(story_dialog)
        sdeN.setText(dev_name)
        sdeN.setGeometry(30, 30, 300, 100)
        sdeN.move(272, 118)
        sdeN.setFont(QtGui.QFont('Times New Roman', 15))
        sdeN.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        spts = QLabel(story_dialog)
        spts.setText("Story points: ")
        spts.setGeometry(30, 30, 300, 100)
        spts.move(182, 155)
        spts.setFont(QtGui.QFont('Times New Roman', 15))
        spts.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        spt = QLabel(story_dialog)
        points = str(str_points)
        spt.setText(points)
        spt.setGeometry(30, 30, 300, 100)
        spt.move(302, 155)
        spt.setFont(QtGui.QFont('Times New Roman', 15))
        spt.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        spts = QLabel(story_dialog)
        spts.setText("Story comments: ")
        spts.setGeometry(30, 30, 300, 100)
        spts.move(150, 190)
        spts.setFont(QtGui.QFont('Times New Roman', 15))
        spts.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        story_comment_views = QPushButton(story_dialog)
        story_comment_views.setText("view")
        story_comment_views.move(295, 228)
        story_comment_views.clicked.connect(lambda: self.primary_window.showComments(storynum))
        story_comment_views.setFixedWidth(70)

        story_dialog.show()


    def main(self):
        app = QApplication(sys.argv)
        win = QMainWindow()
        win.setGeometry(50, 50, 1920, 1080)
        win.setWindowTitle("Project view")

        label = QLabel(win)
        label.setText("Ganesh's Stories")
        label.setGeometry(30, 30, 700, 100)
        label.move(575, 0)
        label.setFont(QtGui.QFont('Times New Roman', 30))
        label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        Pname = QLabel(win)
        Pname.setText("Project name: ")
        Pname.setGeometry(30, 30, 700, 100)
        Pname.move(260, 180)
        Pname.setFont(QtGui.QFont('Times New Roman', 18))
        Pname.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        PnameT = QLabel(win)
        pnamet = self.project_name
        PnameT.setText(pnamet)
        PnameT.setGeometry(30, 30, 700, 100)
        PnameT.move(440, 180)
        PnameT.setFont(QtGui.QFont('Monaco', 18))
        PnameT.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        Pdesc = QLabel(win)
        Pdesc.setText("Project Description: ")
        Pdesc.setGeometry(30, 30, 700, 100)
        Pdesc.move(260, 230)
        Pdesc.setFont(QtGui.QFont('Times New Roman', 18))
        Pdesc.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        descButton = QPushButton(win)
        descButton.setText("see description")
        descButton.move(460, 267)
        descButton.clicked.connect(self.primary_window.showProjectDisc)
        descButton.setFixedWidth(120)


        vstory = QLabel(win)
        vstory.setText("View Stories: ")
        vstory.setGeometry(30, 30, 700, 100)
        vstory.move(260, 280)
        vstory.setFont(QtGui.QFont('Times New Roman', 18))
        vstory.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        cbview = QComboBox(win)
        list_of_stories = self.primary_window.getStories()
        cbview.addItems(list_of_stories)
        cbview.move(400, 315)
        cbview.setFixedWidth(130)
        cbview.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        story_button = QPushButton(win)
        story_button.setText("view")
        story_button.move(540, 315)
        story_button.clicked.connect(lambda: self.showStory(cbview.currentText(),win))
        story_button.setFixedWidth(70)

        mystory = QLabel(win)
        mystory.setText("My Stories: ")
        mystory.setGeometry(30, 30, 700, 100)
        mystory.move(260, 340)
        mystory.setFont(QtGui.QFont('Times New Roman', 18))
        mystory.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        cb = QComboBox(win)
        list_of_my_stories = self.getMyStories()
        cb.addItems(list_of_my_stories)
        cb.move(385, 375)
        cb.setFixedWidth(130)
        cb.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        story_button = QPushButton(win)
        story_button.setText("Update status")
        story_button.move(525, 375)
        story_button.clicked.connect(lambda: self.update_status(cb.currentText(),win))
        story_button.setFixedWidth(100)


        win.show()
        sys.exit(app.exec_())

if __name__ == '__main__':
    window = SecondaryWindow()
    window.main()