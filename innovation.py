import sys
sys.path.insert(1,"C:/Users/thila/Downloads/TIP-Project/ALAAMEE/python")
import estimateALAAMSA
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget,
    QTextEdit, QFileDialog, QTableWidget, QTableWidgetItem, QCheckBox, 
    QHBoxLayout, QDialogButtonBox, QDialog, QLabel
)
from PyQt6.QtWebEngineWidgets import *
from changeStatisticsALAAM import *
from changeStatisticsALAAMbipartite import *
from changeStatisticsALAAMdirected import *
from basicALAAMsampler import basicALAAMsampler
from AnalysisReport import AnalysisReport
from PyQt6.QtCore import QSize


class Ui_Form(QWidget):
    networkSignal = pyqtSignal(object)
    binarySignal = pyqtSignal(object)
    continiousSignal = pyqtSignal(object)
    categoricalSignal = pyqtSignal(object)
    dyadicSignal = pyqtSignal(object)
    # Dictionary for directed network functions and their names
    directed_stat_funcs = {
        "Sender": changeSender,
        "Receiver": changeReceiver,
        "Reciprocity": changeReciprocity,
        "EgoInTwoStar": changeEgoInTwoStar,
        "EgoOutTwoStar": changeEgoOutTwoStar,
        "MixedTwoStar": changeMixedTwoStar,
        "MixedTwoStarSource": changeMixedTwoStarSource,
        "MixedTwoStarSink": changeMixedTwoStarSink,
        "Contagion": changeContagion,
        "ContagionReciprocity": changeContagionReciprocity,
        "TransitiveTriangleT1": changeTransitiveTriangleT1,
        "TransitiveTriangleT3": changeTransitiveTriangleT3,
        "TransitiveTriangleD1": changeTransitiveTriangleD1,
        "TransitiveTriangleU1": changeTransitiveTriangleU1,
        "CyclicTriangleC1": changeCyclicTriangleC1,
        "CyclicTriangleC3": changeCyclicTriangleC3,
        "AlterInTwoStar2": changeAlterInTwoStar2,
        "AlterOutTwoStar2": changeAlterOutTwoStar2
    }

    # Dictionary for undirected network functions and their names
    undirected_stat_funcs = {
        "TwoStar": changeTwoStar,
        "ThreeStar": changeThreeStar,
        "PartnerActivityTwoPath": changePartnerActivityTwoPath,
        "TriangleT1": changeTriangleT1,
        "Contagion": changeStatisticsALAAM.changeContagion,  # Change this based on your function
        "IndirectPartnerAttribute": changeIndirectPartnerAttribute,
        "PartnerAttributeActivity": changePartnerAttributeActivity,
        "PartnerPartnerAttribute": changePartnerPartnerAttribute,
        "TriangleT2": changeTriangleT2,
        "TriangleT3": changeTriangleT3
    }
    parameters_list = []
    def __init__(self):
        super(Ui_Form, self).__init__()
        self.setupUi(self)
        # Store headers
        self.headers = []
    
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(626, 379)
        self.groupBox = QtWidgets.QGroupBox(parent=Form)
        self.groupBox.setGeometry(QtCore.QRect(20, 10, 401, 51))
        self.groupBox.setObjectName("groupBox")
        self.label = QtWidgets.QLabel(parent=self.groupBox)
        self.label.setGeometry(QtCore.QRect(20, 20, 81, 16))
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(parent=self.groupBox)
        self.lineEdit.setGeometry(QtCore.QRect(100, 20, 200, 20))
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton = QtWidgets.QPushButton(parent=self.groupBox)
        self.pushButton.setGeometry(QtCore.QRect(310, 20, 75, 24))
        self.pushButton.setObjectName("pushButton")

        ##select attribute File
        self.pushButton.clicked.connect(self.selectAttributeFile)

        self.groupBox_2 = QtWidgets.QGroupBox(parent=Form)
        self.groupBox_2.setGeometry(QtCore.QRect(20, 70, 401, 101))
        self.groupBox_2.setObjectName("groupBox_2")
        self.label_2 = QtWidgets.QLabel(parent=self.groupBox_2)
        self.label_2.setGeometry(QtCore.QRect(10, 20, 81, 16))
        self.label_2.setObjectName("label_2")
        self.lineEdit_2 = QtWidgets.QLineEdit(parent=self.groupBox_2)
        self.lineEdit_2.setGeometry(QtCore.QRect(90, 20, 200, 20))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.pushButton_2 = QtWidgets.QPushButton(parent=self.groupBox_2)
        self.pushButton_2.setGeometry(QtCore.QRect(300, 20, 75, 24))
        self.pushButton_2.setObjectName("pushButton_2")

        ##select network File
        self.pushButton_2.clicked.connect(self.selectNetworkFile)

        self.radioButton = QtWidgets.QRadioButton(parent=self.groupBox_2)
        self.radioButton.setGeometry(QtCore.QRect(20, 50, 95, 20))
        self.radioButton.setObjectName("radioButton")
        self.radioButton_2 = QtWidgets.QRadioButton(parent=self.groupBox_2)
        self.radioButton_2.setGeometry(QtCore.QRect(110, 50, 95, 20))
        self.radioButton_2.setObjectName("radioButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(parent=self.groupBox_2)
        self.pushButton_3.setGeometry(QtCore.QRect(220, 50, 121, 24))
        self.pushButton_3.setObjectName("pushButton_3")

        ##select parameter
        self.pushButton_3.clicked.connect(self.openNetworkWindow)


        self.groupBox_3 = QtWidgets.QGroupBox(parent=Form)
        self.groupBox_3.setGeometry(QtCore.QRect(20, 180, 591, 151))
        self.groupBox_3.setObjectName("groupBox_3")
        self.label_3 = QtWidgets.QLabel(parent=self.groupBox_3)
        self.label_3.setGeometry(QtCore.QRect(10, 20, 121, 16))
        self.label_3.setObjectName("label_3")
        self.lineEdit_3 = QtWidgets.QLineEdit(parent=self.groupBox_3)
        self.lineEdit_3.setGeometry(QtCore.QRect(160, 20, 200, 20))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.pushButton_4 = QtWidgets.QPushButton(parent=self.groupBox_3)
        self.pushButton_4.setGeometry(QtCore.QRect(370, 20, 75, 24))
        self.pushButton_4.setObjectName("pushButton_4")

        ##select Binary File
        self.pushButton_4.clicked.connect(self.selectBinaryFile)

        self.lineEdit_4 = QtWidgets.QLineEdit(parent=self.groupBox_3)
        self.lineEdit_4.setGeometry(QtCore.QRect(160, 50, 200, 20))
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.pushButton_5 = QtWidgets.QPushButton(parent=self.groupBox_3)
        self.pushButton_5.setGeometry(QtCore.QRect(370, 50, 75, 24))
        self.pushButton_5.setObjectName("pushButton_5")

        ##select continous File
        self.pushButton_5.clicked.connect(self.selectContinousFile)

        self.label_4 = QtWidgets.QLabel(parent=self.groupBox_3)
        self.label_4.setGeometry(QtCore.QRect(10, 50, 151, 16))
        self.label_4.setObjectName("label_4")
        self.lineEdit_5 = QtWidgets.QLineEdit(parent=self.groupBox_3)
        self.lineEdit_5.setGeometry(QtCore.QRect(160, 80, 200, 20))
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.pushButton_6 = QtWidgets.QPushButton(parent=self.groupBox_3)
        self.pushButton_6.setGeometry(QtCore.QRect(370, 80, 75, 24))
        self.pushButton_6.setObjectName("pushButton_6")

        ##select categorical File
        self.pushButton_6.clicked.connect(self.selectCategoricalFile)

        self.label_5 = QtWidgets.QLabel(parent=self.groupBox_3)
        self.label_5.setGeometry(QtCore.QRect(10, 80, 151, 16))
        self.label_5.setObjectName("label_5")
        self.lineEdit_6 = QtWidgets.QLineEdit(parent=self.groupBox_3)
        self.lineEdit_6.setGeometry(QtCore.QRect(160, 110, 200, 20))
        self.lineEdit_6.setObjectName("lineEdit_6")
        self.pushButton_7 = QtWidgets.QPushButton(parent=self.groupBox_3)
        self.pushButton_7.setGeometry(QtCore.QRect(370, 110, 75, 24))
        self.pushButton_7.setObjectName("pushButton_7")

        ##select Dyadic File
        self.pushButton_7.clicked.connect(self.selectDyadicFile)

        self.label_6 = QtWidgets.QLabel(parent=self.groupBox_3)
        self.label_6.setGeometry(QtCore.QRect(10, 110, 131, 16))
        self.label_6.setObjectName("label_6")
        self.pushButton_9 = QtWidgets.QPushButton(parent=self.groupBox_3)
        self.pushButton_9.setGeometry(QtCore.QRect(450, 20, 121, 24))
        self.pushButton_9.setObjectName("pushButton_9")
        self.pushButton_10 = QtWidgets.QPushButton(parent=self.groupBox_3)
        self.pushButton_10.setGeometry(QtCore.QRect(450, 50, 121, 24))
        self.pushButton_10.setObjectName("pushButton_10")
        self.pushButton_11 = QtWidgets.QPushButton(parent=self.groupBox_3)
        self.pushButton_11.setGeometry(QtCore.QRect(450, 80, 121, 24))
        self.pushButton_11.setObjectName("pushButton_11")
        self.pushButton_12 = QtWidgets.QPushButton(parent=self.groupBox_3)
        self.pushButton_12.setGeometry(QtCore.QRect(450, 110, 121, 24))
        self.pushButton_12.setObjectName("pushButton_12")
        self.groupBox_4 = QtWidgets.QGroupBox(parent=Form)
        self.groupBox_4.setGeometry(QtCore.QRect(450, 10, 161, 161))
        self.groupBox_4.setObjectName("groupBox_4")
        self.label_7 = QtWidgets.QLabel(parent=self.groupBox_4)
        self.label_7.setGeometry(QtCore.QRect(10, 30, 54, 16))
        self.label_7.setObjectName("label_7")
        self.spinBox = QtWidgets.QSpinBox(parent=self.groupBox_4)
        self.spinBox.setGeometry(QtCore.QRect(70, 30, 71, 21))
        self.spinBox.setMaximum(1000000)
        self.spinBox.setProperty("value", 100)
        self.spinBox.setObjectName("spinBox")
        self.label_8 = QtWidgets.QLabel(parent=self.groupBox_4)
        self.label_8.setGeometry(QtCore.QRect(10, 70, 61, 16))
        self.label_8.setObjectName("label_8")
        self.spinBox_2 = QtWidgets.QSpinBox(parent=self.groupBox_4)
        self.spinBox_2.setGeometry(QtCore.QRect(70, 70, 71, 21))
        self.spinBox_2.setMaximum(10000000)
        self.spinBox_2.setProperty("value", 100)
        self.spinBox_2.setObjectName("spinBox_2")
        self.label_9 = QtWidgets.QLabel(parent=self.groupBox_4)
        self.label_9.setGeometry(QtCore.QRect(10, 100, 54, 16))
        self.label_9.setObjectName("label_9")
        self.spinBox_3 = QtWidgets.QSpinBox(parent=self.groupBox_4)
        self.spinBox_3.setGeometry(QtCore.QRect(70, 100, 71, 21))
        self.spinBox_3.setMaximum(1000000)
        self.spinBox_3.setProperty("value", 100)
        self.spinBox_3.setObjectName("spinBox_3")
        self.pushButton_8 = QtWidgets.QPushButton(parent=self.groupBox_4)
        self.pushButton_8.setGeometry(QtCore.QRect(20, 130, 121, 24))
        self.pushButton_8.setObjectName("pushButton_8")


        ##analysis
        self.pushButton_8.clicked.connect(self.analysis)

        self.progressBar = QtWidgets.QProgressBar(parent=Form)
        self.progressBar.setGeometry(QtCore.QRect(20, 340, 118, 23))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.groupBox.setTitle(_translate("Form", "Attribute"))
        self.label.setText(_translate("Form", "Attribute file: "))
        self.pushButton.setText(_translate("Form", "Browse.."))
        self.groupBox_2.setTitle(_translate("Form", "Network"))
        self.label_2.setText(_translate("Form", "Network file: "))
        self.pushButton_2.setText(_translate("Form", "Browse.."))
        self.radioButton.setText(_translate("Form", "Directed"))
        self.radioButton_2.setText(_translate("Form", "Undirected"))

        self.radioButton.setChecked(True)

        self.pushButton_3.setText(_translate("Form", "Select Prameters"))
        self.groupBox_3.setTitle(_translate("Form", "Attribute/Dyadic covariates"))
        self.label_3.setText(_translate("Form", "Binary Atrribute file: "))
        self.pushButton_4.setText(_translate("Form", "Browse.."))
        self.pushButton_5.setText(_translate("Form", "Browse.."))
        self.label_4.setText(_translate("Form", "Continious Atrribute file: "))
        self.pushButton_6.setText(_translate("Form", "Browse.."))
        self.label_5.setText(_translate("Form", "Categorical Atrribute file: "))
        self.pushButton_7.setText(_translate("Form", "Browse.."))
        self.label_6.setText(_translate("Form", "Dyadic Atrribute file: "))
        self.pushButton_9.setText(_translate("Form", "Select Prameters"))
        self.pushButton_10.setText(_translate("Form", "Select Prameters"))
        self.pushButton_11.setText(_translate("Form", "Select Prameters"))
        self.pushButton_12.setText(_translate("Form", "Select Prameters"))
        self.groupBox_4.setTitle(_translate("Form", "Analysis"))
        self.label_7.setText(_translate("Form", "Burn-in:"))
        self.label_8.setText(_translate("Form", "Iterations:"))
        self.label_9.setText(_translate("Form", "Samples:"))
        self.pushButton_8.setText(_translate("Form", "Analysis"))

#########################functions#########################################################
    def selectAttributeFile(self):
        attributeFile = QFileDialog.getOpenFileName(self, 'Open file','','txt files (*.txt)')
        self.lineEdit.setText(attributeFile[0])

    def selectNetworkFile(self):
        networkFile = QFileDialog.getOpenFileName(self, 'Open file','','txt files (*.txt)')
        self.lineEdit_2.setText(networkFile[0])
    
    def selectBinaryFile(self):
        binaryFile = QFileDialog.getOpenFileName(self, 'Open file','','txt files (*.txt)')
        self.lineEdit_3.setText(binaryFile[0])
    
    def selectContinousFile(self):
        continousFile = QFileDialog.getOpenFileName(self, 'Open file','','txt files (*.txt)')
        self.lineEdit_4.setText(continousFile[0])

    def selectCategoricalFile(self):
        categoricalFile = QFileDialog.getOpenFileName(self, 'Open file','','txt files (*.txt)')
        self.lineEdit_5.setText(categoricalFile[0])    

    def selectDyadicFile(self):
        dyadicFile = QFileDialog.getOpenFileName(self, 'Open file','','txt files (*.txt)')
        self.lineEdit_6.setText(dyadicFile[0])

    def openNetworkWindow(self):
        self.networkWindow = networkWindow()
        self.networkSignal.connect(self.networkWindow.createCheckboxes)
        mode = "0"
        if self.radioButton.isChecked():
            mode = "0"
        elif self.radioButton_2.isChecked():
            mode = "1"
        print(f"Selected mode: {mode}")  # Debug: Print the mode value
        self.networkSignal.emit(mode)
        self.networkWindow.selectedSignal.connect(self.handleSelectedParameters)
        self.networkWindow.show()

    def handleSelectedParameters(self, selected):
        # Handle the result from the networkWindow (selected checkboxes)
        self.parameters_list = selected
        print("Selected parameters:", selected)
    
    ##### Loading Analysis report html content to a mainwindow #############    
    def loadHTMLContent(self, html_content):
        self.mainWindow = MainWindow()
        # Create a QWebEngineView to display HTML content
        layout = QVBoxLayout()
        view = QWebEngineView()
        layout.addWidget(view)
        view.setHtml(html_content)
        self.setFixedSize(QSize(974, 667))
        self.setLayout(layout)
        self.show()



    def analysis(self):
        attributeFilepath = self.lineEdit.text() 
        networkFilepath = self.lineEdit_2.text()
        binaryFilepath = self.lineEdit_3.text()
        continousFilepath = self.lineEdit_4.text()
        categoricalFilepath = self.lineEdit_5.text()
        dyadicFilepath = self.lineEdit_6.text()
        burnIn = self.spinBox.value()
        iterations = self.spinBox_2.value()
        samples = self.spinBox_3.value()

        # Check if the filepaths are empty strings, and assign None if they are
        binaryFilepath = None if binaryFilepath == "" else binaryFilepath
        continousFilepath = None if continousFilepath == "" else continousFilepath
        categoricalFilepath = None if categoricalFilepath == "" else categoricalFilepath
        dyadicFilepath = None if dyadicFilepath == "" else dyadicFilepath
        # Check whether the network is directed or undirected (for example, using a checkbox)
        is_directed = self.radioButton.isChecked()


        # Prepare lists for functions and corresponding names
        selected_funcs = []
        selected_names = []

        # Choose the correct dictionary based on the network type
        if is_directed:
            func_dict = self.directed_stat_funcs
        else:
            func_dict = self.undirected_stat_funcs
        
        # Iterate through selected parameters to map them to functions
        for param in self.parameters_list:
            if param in func_dict:
                selected_funcs.append(func_dict[param])  # Add the corresponding function
                selected_names.append(param)  # Add the corresponding name

        # Creating the inputs of ALAAM function to be passed to AnalysisReport 
        alaam_inputs = {}
        alaam_inputs["edgelist_filename"] = networkFilepath
        alaam_inputs["param_func_list"] = selected_funcs
        alaam_inputs["labels"] = selected_names
        alaam_inputs["outcome_bin_filename"] = attributeFilepath
        alaam_inputs["binattr_filename"] = binaryFilepath
        alaam_inputs["contattr_filename"] = continousFilepath
        alaam_inputs["catattr_filename"] = categoricalFilepath
        alaam_inputs["sampler_func"] = basicALAAMsampler
        alaam_inputs["zone_filename"] = None
        alaam_inputs["directed"] = is_directed
        alaam_inputs["bipartite"] = False
        alaam_inputs["GoFiterationInStep"] = iterations
        alaam_inputs["GoFburnIn"] = burnIn
        alaam_inputs["bipartiteGoFfixedMode"] = None
        alaam_inputs["add_gof_param_func_list"] = None
        alaam_inputs["outputGoFstatsFilename"] = "outputGoFstatsFile.txt"
        alaam_inputs["outputObsStatsFilename"] = "outputObsStatsFile.txt"

        analysisReport = AnalysisReport()
        html_content = analysisReport.setHtmlContent(alaam_inputs)
        self.loadHTMLContent(html_content)


################sub window#################################
class networkWindow(QWidget):
    selectedSignal = pyqtSignal(list)

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Select Parameters")
        self.layout = QVBoxLayout(self)

        # Set some padding around the window
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(10)

        # OK button to confirm selection
        self.ok_button = QPushButton("OK", self)
        self.ok_button.clicked.connect(self.sendSelection)

        # Add the OK button to the layout
        self.layout.addStretch()
        self.layout.addWidget(self.ok_button, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

        self.setLayout(self.layout)
        self.checkboxes = []  # To store checkboxes

        # Optionally set a maximum height
        self.setMaximumHeight(400)

    def createCheckboxes(self, mode):
        # Clear any existing checkboxes by removing them from the layout
        for checkbox in self.checkboxes:
            self.layout.removeWidget(checkbox)  # Remove from layout
            checkbox.deleteLater()  # Delete the checkbox
        self.checkboxes.clear()

        # Create checkboxes based on the mode
        print(f"Mode received in createCheckboxes: {mode}") 
        if mode == "0":
            options = [
                "Sender","Receiver","EgoInTwoStar","EgoOutTwoStar","MixedTwoStar","MixedTwoStarSource","MixedTwoStarSink","Contagion","ContagionReciprocity","TransitiveTriangleT1","TransitiveTriangleT3","TransitiveTriangleD1","TransitiveTriangleU1","CyclicTriangleC1","CyclicTriangleC3","AlterInTwoStar2","AlterOutTwoStar2"
            ]
        else:
            options = [
                "TwoStar","ThreeStar","PartnerActivityTwoPath","TriangleT1","Contagion","IndirectPartnerAttribute","PartnerAttributeActivity","PartnerPartnerAttribute","TriangleT2","TriangleT3"
            ]

        # Create and add new checkboxes based on the selected mode
        for option in options:
            checkbox = QCheckBox(option, self)
            checkbox.setStyleSheet("margin: 5px;")  # Add some margin to checkboxes
            self.layout.insertWidget(self.layout.count() - 1, checkbox)  # Insert before the OK button
            self.checkboxes.append(checkbox)

    def sendSelection(self):
        # Get selected checkboxes
        selected = [cb.text() for cb in self.checkboxes if cb.isChecked()]

        # Emit the selected checkboxes back to the main window
        self.selectedSignal.emit(selected)

        # Close the window after selection
        self.close()

################end sub window#######################################





####################### Main Window ######################################
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        
        # Create an instance of Ui_Form and load it into a QWidget
        self.ui_form = Ui_Form()
        widget = QtWidgets.QWidget()  # Create a QWidget that will be the central widget
        self.ui_form.setupUi(widget)  # Set up the Ui_Form on this QWidget
        
        # Set the central widget of the QMainWindow to be this QWidget
        self.setCentralWidget(widget)
        self.setFixedSize(QSize(974, 667))

        self.setWindowTitle("Main Window with Form")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = Ui_Form()
    mainWin.show()
    sys.exit(app.exec())