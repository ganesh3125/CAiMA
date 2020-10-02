from PyQt5.QtWidgets import *
import sys
from DBase import DBConnection,DBscript
from PyQt5.uic.properties import QtGui
from PyQt5 import QtGui
from Utils import Story

class Window:

    def __init__(self):
        self.project_name = "Cognition based Artificial intelligent meeting assistant"
        self.project_description = "the proposed system explores to implement an intelligent software agent that can be used to substitute a participant in the routine cooperative information exchange in an organization that provides a vigorous collaboration in the management and explores to provide imperative information to users so that facts can known in a fruitful way"
        self.stories = []
        self.connection = self.connectToDB()
        self.dev_name = ''

    def returner(self):
        return self.project_name, self.project_description

    def connectToDB(self):
        connection = DBConnection.DBConnection()
        connection.connect()
        return connection

    def edit_project_name(self, win):
        edit_dialog = QDialog(win)
        edit_dialog.setGeometry(600, 500, 400, 100)
        edit_dialog.setWindowTitle("edit project name")

        edit_desc_box = QLineEdit(edit_dialog)
        edit_desc_box.move(25, 10)
        edit_desc_box.setFixedWidth(350)

        update_button = QPushButton(edit_dialog)
        update_button.setText("update")
        update_button.move(162, 50)
        update_button.clicked.connect(lambda: self.change_projectName_popup(edit_desc_box.text(), win))
        edit_dialog.show()

    def change_description_popup(self, update, window):
        msg = QMessageBox(window)
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("note")
        self.project_description = update
        msg.setText("updated!")
        msg.exec()

    def change_projectName_popup(self, projectName, window):
        msg = QMessageBox(window)
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("note")
        self.project_name = projectName
        msg.setText("updated!")
        msg.exec()

    def edit_project_desc(self, win):
        edit_dialog = QDialog(win)
        edit_dialog.setGeometry(600, 500, 400, 100)
        edit_dialog.setWindowTitle("edit project description")

        edit_desc_box = QLineEdit(edit_dialog)
        edit_desc_box.move(25, 10)
        edit_desc_box.setFixedWidth(350)

        update_button = QPushButton(edit_dialog)
        update_button.setText("update")
        update_button.move(162, 50)
        update_button.clicked.connect(lambda: self.change_description_popup(edit_desc_box.text(), win))
        edit_dialog.show()

    def showProjectDisc(self, win):
        msg = QMessageBox()
        msg.setFixedWidth(500)
        msg.setIcon(QMessageBox.Information)
        msg.setText(self.project_description)
        msg.setWindowTitle("project description")
        msg.setDetailedText(self.project_description)
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Close)
        # msg.buttonClicked.connect(msgbtn)
        msg.exec_()

    def showStoryDisc(self, description):
        msg = QMessageBox()
        msg.setFixedWidth(500)
        msg.setIcon(QMessageBox.Information)
        lite_description = description
        msg.setText(lite_description)
        msg.setInformativeText("")
        msg.setWindowTitle("view Story description")
        detailed_str = description
        msg.setDetailedText(detailed_str)
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Close)
        # msg.buttonClicked.connect(msgbtn)
        msg.exec()

    def showComments(self, key_string):
        query = {"Story_id": key_string}
        collection = self.connection.comment_collection
        count = collection.find(query).count()
        list_of_data = collection.find(query).sort("Date_Time", -1)
        if count >= 1:
            msg = QMessageBox()
            msg.setFixedWidth(500)
            msg.setIcon(QMessageBox.Information)
            latest_comment = list_of_data[0]
            msg.setText(latest_comment['Text'])
            msg.setInformativeText(str(latest_comment['Date_Time']))
            msg.setWindowTitle("view Story comments")
            detailed_str = ""
            for comment in list_of_data:
                detailed_str = detailed_str + "\n\n" + comment['Text']
            msg.setDetailedText(str(detailed_str))
        else:
            msg = QMessageBox()
            msg.setFixedWidth(500)
            msg.setIcon(QMessageBox.Information)
            msg.setText("no comments")

        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Close)
        # msg.buttonClicked.connect(msgbtn)
        msg.exec_()

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
        participant = cursor2[0]
        dev_name = participant['name']
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
        sdesc_button.clicked.connect(lambda: self.showStoryDisc(story_item['Story_discription']))

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

        print("entered")
        story_comment_views.clicked.connect(lambda: self.showComments(storynum))
        story_comment_views.setFixedWidth(70)

        story_dialog.show()
    def getStories(self):
        collection = self.connection.story_collection
        stories = []
        cursor = collection.find({}).sort("Story_name", 1)
        for story in cursor:
            stories.append(story['Story_name'])
        return stories

    def geParticipants(self):
        collection = self.connection.developer_collection
        participants = []
        cursor = collection.find().sort("developer_id", 1)
        for item in cursor:
            participants.append(item['name'] + ", " + str(item['developer_id']))
        return participants

    def addStory(self,name,description,story_number,points,sprint,dependentstories,assigned_to,story_giving_dialog):
        dependent_stories = dependentstories.split(",")
        story = Story.Story(name=name, description=description, story_number=story_number, points=points,
                            sprint=sprint, developer=assigned_to, dependent_stories=dependent_stories)
        dbscript = DBscript.DBscript()
        dbscript.insertStory(story)
        self.stories = self.getStories()
        print("updated")
        msg = QMessageBox(story_giving_dialog)
        msg.setWindowTitle("update!")
        msg.setText("updated")
        msg.show()



    def give_Stories(self, name_id, win):
        participant = name_id.split(", ")
        participant_name = participant[0]
        participant_id = participant[1]

        story_giving_dialog = QDialog(win)
        grid = QGridLayout(story_giving_dialog)

        strname_lable = QLabel(story_giving_dialog)
        strname_lable.setText("Stroy name: ")

        story_number_lab = QLabel(story_giving_dialog)
        story_number_lab.setText("Stroy number: ")

        assigneto_lab = QLabel(story_giving_dialog)
        assigneto_lab.setText("Assign to: ")

        desc_lab = QLabel(story_giving_dialog)
        desc_lab.setText("Description: ")

        sprint_lab = QLabel(story_giving_dialog)
        sprint_lab.setText('Sprint: ')

        points_lab = QLabel(story_giving_dialog)
        points_lab.setText('points: ')

        dep_stories_lab = QLabel(story_giving_dialog)
        dep_stories_lab.setText("Dependent stories: ")

        strname_line = QLineEdit(story_giving_dialog)
        strnum_line = QLineEdit(story_giving_dialog)
        assigneto_line = QLineEdit(story_giving_dialog)
        desc_line = QLineEdit(story_giving_dialog)
        sprint_line = QLineEdit(story_giving_dialog)
        points_line = QLineEdit(story_giving_dialog)
        dep_str_line = QLineEdit(story_giving_dialog)

        grid.addWidget(strname_lable, 0, 0)
        grid.addWidget(strname_line, 0, 1)

        grid.addWidget(story_number_lab, 1, 0)
        grid.addWidget(strnum_line,1,1)

        grid.addWidget(assigneto_lab,2,0)
        grid.addWidget(assigneto_line,2,1)

        grid.addWidget(desc_lab,3,0)
        grid.addWidget(desc_line,3,1)

        grid.addWidget(sprint_lab,4,0)
        grid.addWidget(sprint_line,4,1)

        grid.addWidget(points_lab,5,0)
        grid.addWidget(points_line,5,1)

        grid.addWidget(dep_stories_lab,6,0)
        grid.addWidget(dep_str_line,6,1)

        submit = QPushButton(story_giving_dialog)
        submit.setFixedWidth(350)
        submit.setText("submit")
        grid.addWidget(submit,7,1)
        submit.clicked.connect(lambda : self.addStory(name = strname_line.text(),description = desc_line.text(),
                story_number = strnum_line.text(),points = int(points_line.text()),sprint = int(sprint_line.text()),
                dependentstories=dep_str_line.text(),assigned_to=int(assigneto_line.text()),story_giving_dialog=story_giving_dialog))

        story_giving_dialog.show()

    def main(self):
        app = QApplication(sys.argv)
        win = QMainWindow()
        win.setGeometry(50, 50, 1920, 1080)
        win.setWindowTitle("Project view")

        label = QLabel(win)
        label.setText("Scrum Master")
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
        descButton.clicked.connect(self.showProjectDisc)
        descButton.setFixedWidth(120)

        desc_edit_Button = QPushButton(win)
        desc_edit_Button.setText("edit")
        #desc_edit_Button.hide()
        desc_edit_Button.move(590, 267)
        desc_edit_Button.setFixedWidth(65)
        desc_edit_Button.clicked.connect(lambda: self.edit_project_desc(win))

        Pstory = QLabel(win)
        Pstory.setText("View Stories: ")
        Pstory.setGeometry(30, 30, 700, 100)
        Pstory.move(260, 280)
        Pstory.setFont(QtGui.QFont('Times New Roman', 18))
        Pstory.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        cb_stories = QComboBox(win)
        self.stories = self.getStories()
        cb_stories.addItems(self.stories)
        cb_stories.move(400, 315)
        cb_stories.setFixedWidth(130)
        cb_stories.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        story_button = QPushButton(win)
        story_button.setText("view")
        story_button.move(540, 315)
        story_button.clicked.connect(lambda: self.showStory(cb_stories.currentText(), win))
        story_button.setFixedWidth(70)

        mystory = QLabel(win)
        mystory.setText("Participants: ")
        mystory.setGeometry(30, 30, 700, 100)
        mystory.move(260, 340)
        mystory.setFont(QtGui.QFont('Times New Roman', 18))
        mystory.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        cb_participants = QComboBox(win)
        list_of_participants = self.geParticipants()
        cb_participants.addItems(list_of_participants)
        cb_participants.move(385, 375)
        cb_participants.setFixedWidth(170)
        cb_participants.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        story_button = QPushButton(win)
        story_button.setText("Give story")
        story_button.move(565, 375)
        story_button.clicked.connect(lambda: self.give_Stories(cb_participants.currentText(), win))
        story_button.setFixedWidth(100)

        win.show()
        sys.exit(app.exec_())


if __name__ == '__main__':
    window_obj = Window()
    window_obj.main()
