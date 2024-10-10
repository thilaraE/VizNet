import sys
import os
from PyQt6.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QWidget, QGridLayout, QFileDialog, QLabel, QPushButton, QCheckBox
from PyQt6.QtCore import QPropertyAnimation, QEasingCurve, pyqtSignal, Qt
from PyQt6.QtGui import QIcon, QPixmap

# Import the UI class from the `main_ui_ui.py`
from ui.ui_ui import Ui_MainWindow

class NetworkParameterWindow(QWidget):
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
        self.layout.addWidget(self.ok_button, alignment=Qt.AlignmentFlag.AlignCenter)

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
            # mode 0 is directed graph
            options = [
                "Density","Sender","Receiver","Contagion","Reciprocity","ContagionReciprocity","EgoInTwoStar","EgoOutTwoStar","MixedTwoStar","MixedTwoStarSource","MixedTwoStarSink","TransitiveTriangleT1","TransitiveTriangleT3","TransitiveTriangleD1","TransitiveTriangleU1","CyclicTriangleC1","CyclicTriangleC3","AlterInTwoStar2","AlterOutTwoStar2"
            ]
        else:
            # mode 1 is non-directed graph
            options = [
                "Density", "Activity", "Contagion", "TwoStar","ThreeStar","PartnerActivityTwoPath","IndirectPartnerAttribute","PartnerAttributeActivity","PartnerPartnerAttribute","TriangleT1","TriangleT2","TriangleT3"
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

class MainWindow(QMainWindow):
    # Define the signals at the class level
    networkSignal = pyqtSignal(object)  # Signal to emit mode for the network window
    binarySignal = pyqtSignal(object)  # Signal to emit binary data
    continiousSignal = pyqtSignal(object)  # Signal to emit continuous data
    categoricalSignal = pyqtSignal(object)  # Signal to emit categorical data

    def __init__(self):
        super(MainWindow, self).__init__()

        # UI setup
        self.setup_ui()

        # Initialise signals and slots
        self.init_signal_slot()

        # Select attribute file
        self.browse_edge_list.clicked.connect(self.selectEdgeFile)
        self.browse_outcome.clicked.connect(self.selectOutcomeFile)
        # Miss the set parameter ######## -------------
        # Connect button to function to open second window
        self.parameter_network_btn.clicked.connect(self.open_network_parameter_window)

        # Initially disable all buttons by default
        self.browse_binary_attr.setEnabled(False)
        self.parameter_binary_btn.setEnabled(False)

        self.browse_continuous_attr.setEnabled(False)
        self.parameter_continuous_btn.setEnabled(False)

        self.browse_categorical_attr.setEnabled(False)
        self.parameter_categorical_btn.setEnabled(False)

        # Connect checkbox state to button enabling/disabling
        self.checkBox_binary_attr.stateChanged.connect(self.check_checkboxes_state)
        self.checkBox_continuous_attr.stateChanged.connect(self.check_checkboxes_state)
        self.checkBox_categorical_attr.stateChanged.connect(self.check_checkboxes_state)

        # Connect the file selection button to the file dialog
        self.browse_binary_attr.clicked.connect(self.selectBinaryFile)
        self.browse_continuous_attr.clicked.connect(self.selectContinousFile)
        self.browse_categorical_attr.clicked.connect(self.selectCategoricalFile)

    def setup_ui(self):
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Text "VizNet" as the title
        self.logo_label = self.ui.logo_label_3
        self.logo_label.setText("VizNet")

        # Create a sidebar container in code to contain both sidebars
        self.sidebar_container = QWidget(self)
        self.sidebar_layout = QVBoxLayout(self.sidebar_container)
        self.sidebar_layout.setContentsMargins(0, 0, 0, 0)
        self.sidebar_layout.setSpacing(0)
        
        # Add icon_only_widget and full_menu_widget to sidebar_container
        self.sidebar_layout.addWidget(self.ui.icon_only_widget)
        self.sidebar_layout.addWidget(self.ui.full_menu_widget)

        # Add the sidebar container to the grid layout in the main window
        self.ui.gridLayout.addWidget(self.sidebar_container, 0, 0)

        # By default, hide the icon-only sidebar and show the full sidebar
        self.ui.icon_only_widget.hide()
        self.ui.full_menu_widget.show()
        self.sidebar_container.setMaximumWidth(self.ui.full_menu_widget.sizeHint().width())

        # Set Create Button 2 as the default active page
        self.ui.create_btn_2.setChecked(True)
        self.pages = self.ui.stackedWidget
        self.pages.setCurrentIndex(0)

        # Initialise objects from create page
        ## Initalise objects in network detail group box
        self.browse_edge_list = self.ui.browse_edge_list
        self.input_edge_list_file = self.ui.input_edge_list_file

        self.browse_outcome = self.ui.browse_outcome
        self.input_outcome_file = self.ui.input_outcome_file
        
        self.directed_graph_checkBox = self.ui.directed_graph_checkBox
        self.parameter_network_btn = self.ui.parameter_network_btn

        ## Initalise objects in attribute covariates group box
        ### Binary attribute
        self.checkBox_binary_attr = self.ui.checkBox_binary_attr
        self.input_binary_attr = self.ui.input_binary_attr
        self.browse_binary_attr = self.ui.browse_binary_attr
        self.parameter_binary_btn = self.ui.parameter_binary_btn

        ### Continuoue attribute
        self.checkBox_continuous_attr = self.ui.checkBox_continuous_attr
        self.input_continuous_attr = self.ui.input_continuous_attr
        self.browse_continuous_attr = self.ui.browse_continuous_attr
        self.parameter_continuous_btn = self.ui.parameter_continuous_btn

        ### Categorical attribute
        self.checkBox_categorical_attr = self.ui.checkBox_categorical_attr
        self.input_categorical_attr = self.ui.input_categorical_attr
        self.browse_categorical_attr = self.ui.browse_categorical_attr
        self.parameter_categorical_btn = self.ui.parameter_categorical_btn

    def init_signal_slot(self):
        # Set icon images for buttons and labels
        self.ui.logo_label_1.setPixmap(QPixmap("ui/icon/logo.png"))
        self.ui.logo_label_2.setPixmap(QPixmap("ui/icon/logo.png"))

        self.ui.create_btn_1.setIcon(QIcon("ui/icon/edit.png"))
        self.ui.static_report_btn_1.setIcon(QIcon("ui/icon/file.png"))
        self.ui.interactive_report_btn_1.setIcon(QIcon("ui/icon/interactive.png"))
        self.ui.export_btn_1.setIcon(QIcon("ui/icon/export.png"))

        self.ui.create_btn_2.setIcon(QIcon("ui/icon/edit.png"))
        self.ui.static_report_btn_2.setIcon(QIcon("ui/icon/file.png"))
        self.ui.interactive_report_btn_2.setIcon(QIcon("ui/icon/interactive.png"))
        self.ui.export_btn_2.setIcon(QIcon("ui/icon/export.png"))

        self.ui.change_btn.setIcon(QIcon("ui/icon/more.png"))

        # Connect buttons for changing pages
        buttons = [
            (self.ui.create_btn_1, 0),
            (self.ui.create_btn_2, 0),
            (self.ui.static_report_btn_1, 1),
            (self.ui.static_report_btn_2, 1),
            (self.ui.interactive_report_btn_1, 2),
            (self.ui.interactive_report_btn_2, 2)
        ]

        for button, page_index in buttons:
            button.toggled.connect(lambda checked, index=page_index: self.on_page_button_toggled(checked, index))

        # Change button visibility and layout based on sidebar toggle button
        self.ui.change_btn.toggled.connect(self.on_change_btn_toggled)

        # Handle Export button clicks to close the application
        self.ui.export_btn_1.clicked.connect(self.close)
        self.ui.export_btn_2.clicked.connect(self.close)


    def on_page_button_toggled(self, checked, index):
        if checked:
            self.pages.setCurrentIndex(index)

    def on_change_btn_toggled(self, checked):
        # Sidebar animation for expanding or collapsing
        self.animation = QPropertyAnimation(self.sidebar_container, b"maximumWidth")
        self.animation.setDuration(500)  # Duration in milliseconds
        self.animation.setEasingCurve(QEasingCurve.Type.InOutQuad)

        if checked:
            # Collapse to icon-only view
            target_width = self.ui.icon_only_widget.sizeHint().width()
            self.ui.icon_only_widget.show()
            self.ui.full_menu_widget.hide()
        else:
            # Expand to full view
            target_width = self.ui.full_menu_widget.sizeHint().width()
            self.ui.full_menu_widget.show()
            self.ui.icon_only_widget.hide()

        # Set animation end value and start animation
        self.animation.setEndValue(target_width)
        self.animation.start()

    # Event handling to provide smooth hover scaling effect on change_btn
    def enterEvent(self, event):
        self.animation = QPropertyAnimation(self.ui.change_btn, b"geometry")
        self.animation.setDuration(300)
        self.animation.setStartValue(self.ui.change_btn.geometry())
        new_geometry = self.ui.change_btn.geometry().adjusted(-5, -5, 5, 5)  # Increase size by 5px on each side
        self.animation.setEndValue(new_geometry)
        self.animation.setEasingCurve(QEasingCurve.Type.OutBack)
        self.animation.start()
        super(MainWindow, self).enterEvent(event)

    def leaveEvent(self, event):
        self.animation = QPropertyAnimation(self.ui.change_btn, b"geometry")
        self.animation.setDuration(300)
        new_geometry = self.ui.change_btn.geometry().adjusted(5, 5, -5, -5)  # Restore original size
        self.animation.setEndValue(new_geometry)
        self.animation.setEasingCurve(QEasingCurve.Type.InBack)
        self.animation.start()
        super(MainWindow, self).leaveEvent(event)
    
    # Function to get data from text file
    def selectOutcomeFile(self):
        outcomeFile = QFileDialog.getOpenFileName(self, 'Open file','','txt files (*.txt)')
        self.input_outcome_file.setText(outcomeFile[0])

    def selectEdgeFile(self):
        edgeFile = QFileDialog.getOpenFileName(self, 'Open file','','txt files (*.txt)')
        self.input_edge_list_file.setText(edgeFile[0])
    
    def selectBinaryFile(self):
        # Open file dialog to select the binary attribute file
        binaryFile, _ = QFileDialog.getOpenFileName(self, 'Open Binary Attribute File', '', 'Text Files (*.txt);;All Files (*)')
        if binaryFile:
            self.input_binary_attr.setText(binaryFile)
            # Read the column names from the first line of the binary attribute file
            with open(binaryFile, 'r') as file:
                first_line = file.readline().strip()
                column_names = first_line.split()
            # Store binary attributes
            self.binattr = {col: [] for col in column_names}
            print("Binary Attribute File Columns:", column_names)
            return column_names

    def selectContinousFile(self):
        # Open file dialog to select the continuous attribute file
        continousFile, _ = QFileDialog.getOpenFileName(self, 'Open Continuous Attribute File', '', 'Text Files (*.txt);;All Files (*)')
        if continousFile:
            self.input_continuous_attr.setText(continousFile)
            # Read the column names from the first line of the continuous attribute file
            with open(continousFile, 'r') as file:
                first_line = file.readline().strip()
                column_names = first_line.split()
            # Store continuous attributes
            self.contattr = {col: [] for col in column_names}
            print("Continuous Attribute File Columns:", column_names)
            return column_names

    def selectCategoricalFile(self):
        # Open file dialog to select the categorical attribute file
        categoricalFile, _ = QFileDialog.getOpenFileName(self, 'Open Categorical Attribute File', '', 'Text Files (*.txt);;All Files (*)')
        if categoricalFile:
            self.input_categorical_attr.setText(categoricalFile)
            # Read the column names from the first line of the categorical attribute file
            with open(categoricalFile, 'r') as file:
                first_line = file.readline().strip()
                column_names = first_line.split()
            # Store categorical attributes
            self.catattr = {col: [] for col in column_names}
            print("Categorical Attribute File Columns:", column_names)
            return column_names

    def check_checkboxes_state(self):
        # Enable or disable the button for the binary attribute
        if self.checkBox_binary_attr.isChecked():
            self.browse_binary_attr.setEnabled(True)
            self.parameter_binary_btn.setEnabled(True)
        else:
            self.browse_binary_attr.setEnabled(False)
            self.parameter_binary_btn.setEnabled(False)
            self.input_binary_attr.clear()  # Clear the binary input field if unchecked

        # Enable or disable the button for the continuous attribute
        if self.checkBox_continuous_attr.isChecked():
            self.browse_continuous_attr.setEnabled(True)
            self.parameter_continuous_btn.setEnabled(True)
        else:
            self.browse_continuous_attr.setEnabled(False)
            self.parameter_continuous_btn.setEnabled(False)
            self.input_continuous_attr.clear()  # Clear the continuous input field if unchecked

        # Enable or disable the button for the categorical attribute
        if self.checkBox_categorical_attr.isChecked():
            self.browse_categorical_attr.setEnabled(True)
            self.parameter_categorical_btn.setEnabled(True)
        else:
            self.browse_categorical_attr.setEnabled(False)
            self.parameter_categorical_btn.setEnabled(False)
            self.input_categorical_attr.clear()  # Clear the categorical input field if unchecked

    def open_network_parameter_window(self):
        # Create and show the second window (as a normal widget)
        self.second_window = NetworkParameterWindow()
        self.networkSignal.connect(self.second_window.createCheckboxes)
        mode = "0"
        if self.directed_graph_checkBox.isChecked():
            mode = "0"
        else:
            mode = "1"
        print(f"Selected mode: {mode}")  # Debug: Print the mode value
        self.networkSignal.emit(mode)
        self.second_window.selectedSignal.connect(self.handleSelectedParameters)
        self.second_window.show()  # Non-modal, so both windows can be used simultaneously       

    def handleSelectedParameters(self, selected):
        # Handle the result from the networkWindow (selected checkboxes)
        self.parameters_list = selected
        print("Selected parameters:", selected)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Load style.qss file if exists
    if os.path.exists("style.qss"):
        with open("style.qss") as f:
            style_str = f.read()
        app.setStyleSheet(style_str)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
