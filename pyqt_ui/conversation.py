from PyQt5.QtWidgets import *
import sys
from DBase import DBConnection, DBscript
from PyQt5.QtCore import QTimer
from Runner import CaimaRunner
import os
from Constants import Constants


class QTimer_ProgressBar(QMainWindow):

    def __init__(self):
        super().__init__()

        # self.pbar = QProgressBar(self)
        # self.pbar.setGeometry(30, 70,400, 50)
        # self.pbar.setValue(0)
        self.connection = self.connectToDB()
        self.setWindowTitle("Conversation")

        self.start_nain_loop_flag = False
        self.setGeometry(390, 50, 600, 600)

        self.agent_count = 0
        self.actor_count = 0
        self.agent_conv_count = 0
        self.actor_conv_count = 0
        self.prev_agent_txt = ''
        self.prev_actor_text = ''

        self.oplabel_primary_actor = QLabel(self)
        self.oplabel_primary_actor.setText("Conversation: ")
        self.oplabel_primary_actor.move(50, 40)
        self.optextEdit = QPlainTextEdit(self)
        self.optextEdit.setGeometry(50, 50, 50, 50)
        self.optextEdit.setReadOnly(True)
        self.optextEdit.setFixedHeight(400)
        self.optextEdit.setFixedWidth(500)
        self.optextEdit.move(50, 90)

        # self.oplabel_agent = QLabel(self)
        # self.oplabel_agent.setText("Agent: ")
        # self.oplabel_agent.move(50, 260)
        # self.optextEdit2.setGeometry(50, 50, 50, 50)
        # self.optextEdit2.setReadOnly(True)
        # self.optextEdit2.setFixedHeight(100)
        # self.optextEdit2.setFixedWidth(500)
        # self.optextEdit2.move(50, 300)

        self.start_button = QPushButton(self)
        self.start_button.setText("Start conversation")
        self.start_button.move(50, 550)
        self.start_button.setFixedWidth(200)
        self.start_button.clicked.connect(self.start_conversation)

        self.stop_button = QPushButton(self)
        self.stop_button.setText("Clear conversation")
        self.stop_button.move(350, 550)
        self.stop_button.setFixedWidth(200)
        self.stop_button.clicked.connect(self.stop_conversation)


        self.show()

        self.timer = QTimer()
        self.timer.timeout.connect(self.handleTimer)
        self.timer.setTimerType(1)
        self.timer.setInterval(1000)
        self.timer.start()
        self.caima_runner = CaimaRunner.Runner()

    def start_conversation(self):
        self.start_button.hide()
        if not self.start_nain_loop_flag:
            self.start_nain_loop_flag = True
            self.caima_runner.start_runner()
        else:
            self.caima_runner.continue_runner()

    def stop_conversation(self):
        self.delete_conversation()
        #self.caima_runner.stop_runner()
        self.optextEdit.setPlainText("")
        self.actor_conv_count = 0
        self.agent_conv_count = 0

    def delete_conversation(self):
        collection = self.connection.conversation_collection
        collection.delete_many({"DeviceId":Constants.device_id})

    def handleTimer(self):
        # print("inside text update")
        actor_text = self.find_scrum_text()
        agent_text = self.find_agent_text()
        if actor_text != "" or agent_text != "":
            print(actor_text)
            final_text = actor_text + os.linesep + agent_text
            self.optextEdit.appendPlainText(final_text)
        # self.optextEdit.setPlainText(actor_text )

    def find_agent_text(self):
        query = {"Actor": "Agent","DeviceId":Constants.device_id}
        collection = self.connection.conversation_collection
        count = collection.find(query).count()
        prev_agent_txt = ""
        if count > 0 and self.agent_count <= count:
            #self.agent_count += 1
            conversation = collection.find(query).sort("Time", -1)
            latest_conversation = conversation[0]
            text = latest_conversation['Text']
            # self.optextEdit2.insertPlainText('\n' + 'Agent: \n' + text + '\n')
            txt = '\n' + 'Ganesh: \n' + text + '\n'
            prev_agent_txt = txt
        if count != self.agent_conv_count:
            self.agent_conv_count = count
            print(prev_agent_txt)
            return prev_agent_txt
        else:
            return ""

    def find_scrum_text(self):
        query = {"Actor": "Primary interactor","DeviceId":Constants.device_id}
        collection = self.connection.conversation_collection
        prev_actor_text = ""
        count = collection.find(query).count()
        if count > 0 and self.actor_count <= count:
            #self.actor_count += 1
            conversation = collection.find(query).sort("Time", -1)
            latest_conversation = conversation[0]
            text = latest_conversation['Text']
            # self.optextEdit.insertPlainText('\n' + 'Primary Actor: \n' + text + '\n')
            text = '\n' + 'Primary Actor: \n' + text + '\n'
            prev_actor_text = text
        if count != self.actor_conv_count:
            self.actor_conv_count = count
            return prev_actor_text
        else:
            return ""

    def connectToDB(self):
        connection = DBConnection.DBConnection()
        connection.connect()
        return connection


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = QTimer_ProgressBar()
    sys.exit(app.exec_())
