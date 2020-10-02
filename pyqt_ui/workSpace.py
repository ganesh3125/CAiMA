from PyQt5.QtWidgets import *
import sys
from DBase import DBConnection,DBscript
from Runner.CaimaRunner import *
from PyQt5.QtCore import QTimer


class QTimer_ProgressBar(QMainWindow):

    def __init__(self):
        super().__init__()

        #self.pbar = QProgressBar(self)
        #self.pbar.setGeometry(30, 70,400, 50)
        #self.pbar.setValue(0)
        self.connection = self.connectToDB()
        self.setWindowTitle("QTimer Progressbar")

        self.setGeometry(390, 50, 600, 600)

        self.optextEdit = QPlainTextEdit(self)
        self.optextEdit.setReadOnly(True)
        self.optextEdit.setFixedHeight(100)
        self.optextEdit.setFixedWidth(500)
        self.optextEdit.move(50, 100)

        self.optextEdit2 = QPlainTextEdit(self)
        self.optextEdit2.setReadOnly(True)
        self.optextEdit2.setFixedHeight(100)
        self.optextEdit2.setFixedWidth(500)
        self.optextEdit2.move(50, 300)

        formLayout = QFormLayout()
        groupBox = QGroupBox("This Is Group Box")
        groupBox.setLayout(formLayout)
        scroll = QScrollArea()
        scroll.setWidget(groupBox)
        scroll.setWidgetResizable(True)
        scroll.setFixedHeight(400)
        layout = QVBoxLayout(self)
        layout.addWidget(scroll)

        self.show()

        self.timer = QTimer()
        self.timer.timeout.connect(self.handleTimer)
        self.timer.setTimerType(1)
        self.timer.setInterval(2)
        self.timer.start()
        self.timer.start(1000)


    def handleTimer(self):
        scrum_text = self.find_scrum_text()
        agent_text = self.find_agent_text()
        self.optextEdit.setPlainText(agent_text)
        self.optextEdit2.setPlainText(scrum_text)

    def find_agent_text(self):
        query = {"Actor": "Agent"}
        collection = self.connection.conversation_collection
        conversation = collection.find(query).sort("Time", -1)
        latest_conversation = conversation[0]
        text = latest_conversation['Text']
        return text

    def find_scrum_text(self):
        query = {"Actor": "Scrum master"}
        collection = self.connection.conversation_collection
        conversation = collection.find(query).sort("Time", -1)
        latest_conversation = conversation[0]
        text = latest_conversation['Text']
        return text

    def connectToDB(self):
        connection = DBConnection.DBConnection()
        connection.connect()
        return connection

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = QTimer_ProgressBar()
    sys.exit(app.exec_())
