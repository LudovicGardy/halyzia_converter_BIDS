# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 20:54:14 2019

@author: gardy
"""
import os
import sys
import json
import numpy as np
import traceback
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QStyle, QErrorMessage,
    QTextEdit, QGridLayout, QApplication, QDialog, QPushButton,
    QVBoxLayout, QMainWindow, QMenu, QMessageBox, QSizePolicy, QAction,
    QComboBox, QHBoxLayout, QFrame, QCheckBox, QFileDialog, QTextBrowser)
from PyQt5 import QtCore
from PyQt5.QtCore import QCoreApplication
import time

#sys.path.append(r"G:\GardyL\Data_storage\EPIFAR_storage\BIDS_data\derivatives\Neuralynx_to_BIDSlike")
#sys.path.append(r"C:\Users\GARDy\Desktop\Neuralynx_to_BIDSlike")
from create_neuralynx_BIDSlike import (path_to_BIDSlikepath, ncs_to_BIDSlike, rawdata_to_BIDSlike, TRC_to_BIDSlike)

def confirm_messageBox(title, text, icon, cancel_option = True):
    msgBox = QMessageBox()
    msgBox.setWindowFlags(QtCore.Qt.Dialog | QtCore.Qt.WindowMinimizeButtonHint | QtCore.Qt.WindowMaximizeButtonHint | QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.Window )
    msgBox.setIcon(icon)
    msgBox.setWindowTitle(title)
    msgBox.setText(text)

    if cancel_option:
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    else:
        msgBox.setStandardButtons(QMessageBox.Ok)

    returnValue = msgBox.exec()
    if returnValue == QMessageBox.Ok:
        print('Confirmed.')
    return(returnValue)

class BIDSlike_creator_win(QWidget):
    def __init__(self):
        super().__init__()

        self.init_GUI()
        self.show()


    def init_GUI(self):
        ### Def window size
        left = 200
        top = 100
        width = 600
        height = 600

        self.setGeometry(left, top, width, height)
        self.setWindowTitle('BIDS-like architecture creator')

        self.path_info_dict = {}

        ### BIDS naming frame
        BIDSnaming_frame = QFrame()
        BIDSnaming_layout = QHBoxLayout()
        BIDSnaming_frame.setLayout(BIDSnaming_layout)
        BIDSnaming_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        BIDSnaming_frame.setFixedHeight(30)
        BIDSnaming_layout.setContentsMargins(0, 0, 0, 0)
        BIDSnaming_layout.setSpacing(0)

        patient_label = QLabel("  Patient-")
        self.patient_edit = QLineEdit("")
        self.patient_edit.setText("000")

        sess_label = QLabel("  Session-")
        self.sess_edit = QLineEdit()
        self.sess_edit.setText("00")

        run_label = QLabel("  Run-")
        self.run_edit = QLineEdit()
        self.run_edit.setText("00")

        json_dict = json.load(open("config_file.json"))
        possible_tasknames = json_dict["possible_tasknames"]
        possible_ext = json_dict["possible_ext"]
        possible_tasknames.append("Other")

        task_label = QLabel("  Task-")
        self.taskname_ComboBox = QComboBox()
        [self.taskname_ComboBox.addItem(taskname) for taskname in possible_tasknames]
        self.taskname_ComboBox.setCurrentIndex(0)
        self.taskname_ComboBox.currentIndexChanged.connect(self.taskname_ComboBox_fun)

        BIDSnaming_layout.addWidget(patient_label)
        BIDSnaming_layout.addWidget(self.patient_edit)
        BIDSnaming_layout.addWidget(sess_label)
        BIDSnaming_layout.addWidget(self.sess_edit)
        BIDSnaming_layout.addWidget(run_label)
        BIDSnaming_layout.addWidget(self.run_edit)
        BIDSnaming_layout.addWidget(task_label)
        BIDSnaming_layout.addWidget(self.taskname_ComboBox)

        ### Input data type frame
        input_format_frame = QFrame()
        input_format_layout = QHBoxLayout()
        input_format_frame.setLayout(input_format_layout)
        input_format_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        input_format_frame.setFixedHeight(50)
        input_format_layout.setContentsMargins(0, 0, 0, 0)
        input_format_layout.setSpacing(0)

        ##- Input data type subframe 1
        input_format_subframe1 = QFrame()
        input_format_sublayout1 = QHBoxLayout()
        input_format_subframe1.setLayout(input_format_sublayout1)
        input_format_subframe1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        input_format_subframe1.setFixedHeight(30)
        input_format_sublayout1.setContentsMargins(0, 0, 0, 0)
        input_format_sublayout1.setSpacing(0)

        input_format_label = QLabel("Input format: ")
        self.ext_ComboBox = QComboBox()
        [self.ext_ComboBox.addItem(ext) for ext in possible_ext]
        self.ext_ComboBox.setCurrentIndex(0)
        self.ext_ComboBox.currentIndexChanged.connect(self.ext_ComboBox_fun)
        self.ext_ComboBox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        input_format_sublayout1.addWidget(input_format_label)
        input_format_sublayout1.addWidget(self.ext_ComboBox)

        ##- Input data type subframe 2
        input_format_subframe2 = QFrame()
        input_format_sublayout2 = QHBoxLayout()
        input_format_subframe2.setLayout(input_format_sublayout2)
        input_format_subframe2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        input_format_subframe2.setFixedHeight(30)
        input_format_sublayout2.setContentsMargins(0, 0, 0, 0)
        input_format_sublayout2.setSpacing(0)

        microID_label = QLabel("                micro ID: ")
        self.microID_edit = QLineEdit("")
        self.microID_edit.setText("t")
        self.microID_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        microID_infoButton = QPushButton("")
        microID_infoButton.clicked.connect(self.microID_infoButton_fun)
        microID_infoButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        microID_infoButton.setFixedWidth(50)
        microID_infoButton.setIcon(self.style().standardIcon(QStyle.SP_MessageBoxInformation))

        input_format_sublayout2.addWidget(microID_label)
        input_format_sublayout2.addWidget(self.microID_edit)
        input_format_sublayout2.addWidget(microID_infoButton)

        input_format_layout.addWidget(input_format_subframe1)
        input_format_layout.addWidget(input_format_subframe2)

        ### Input data path frame
        input_path_frame = QFrame()
        input_path_layout = QHBoxLayout()
        input_path_frame.setLayout(input_path_layout)
        input_path_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        input_path_frame.setFixedHeight(30)
        input_path_layout.setContentsMargins(0, 0, 0, 0)
        input_path_layout.setSpacing(0)

        input_infoButton = QPushButton("")
        input_infoButton.clicked.connect(self.input_infoButton_fun)
        input_infoButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        input_infoButton.setFixedWidth(50)
        input_infoButton.setIcon(self.style().standardIcon(QStyle.SP_MessageBoxInformation))

        input_browseButton = QPushButton("Browse...")
        input_browseButton.clicked.connect(self.input_browseButton_fun)
        input_browseButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        input_browseButton.setFixedWidth(100)

        self.input_path_edit = QLineEdit()
        self.input_path_edit.setText("")
        self.input_path_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.input_ext_edit = QLineEdit()
        self.input_ext_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.input_ext_edit.setText(self.ext_ComboBox.currentText())
        self.input_ext_edit.setFixedWidth(50)
        #self.input_ext_edit.setStyleSheet("background-color: lightgray")
        self.input_ext_edit.setStyleSheet("background: #636363 ;color: #ffffff;")

        input_path_layout.addWidget(input_infoButton)
        input_path_layout.addWidget(input_browseButton)
        input_path_layout.addWidget(self.input_path_edit)
        input_path_layout.addWidget(self.input_ext_edit)

        ### Output data path frame
        output_path_frame = QFrame()
        output_path_layout = QHBoxLayout()
        output_path_frame.setLayout(output_path_layout)
        output_path_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        output_path_frame.setFixedHeight(30)
        output_path_layout.setContentsMargins(0, 0, 0, 0)
        output_path_layout.setSpacing(0)

        output_infoButton = QPushButton("")
        output_infoButton.clicked.connect(self.output_infoButton_fun)
        output_infoButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        output_infoButton.setFixedWidth(50)
        output_infoButton.setIcon(self.style().standardIcon(QStyle.SP_MessageBoxInformation))

        output_browseButton = QPushButton("Browse...")
        output_browseButton.clicked.connect(self.output_browseButton_fun)
        output_browseButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        output_browseButton.setFixedWidth(100)

        self.output_path_edit = QLineEdit()
        self.output_path_edit.setText("")
        self.output_path_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        output_path_layout.addWidget(output_infoButton)
        output_path_layout.addWidget(output_browseButton)
        output_path_layout.addWidget(self.output_path_edit)

        ### Validation Frame
        self.description_textbox = QTextBrowser(self)
        self.description_textbox.setObjectName("description_textbox")
        self.description_textbox.setStyleSheet("QTextBrowser#description_textbox {background: white ;border: 2px solid #000000;}")
        self.description_textbox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        validation_frame = QFrame()
        validation_layout = QVBoxLayout()
        validation_frame.setLayout(validation_layout)
        validation_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        button_check = QPushButton("Check information before final validation")
        button_check.setShortcut(QtCore.Qt.Key_Return)
        button_check.clicked.connect(self.button_check_fun)
        button_check.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        button_check.setFixedHeight(30)

        button_OK = QPushButton("OK")
        button_OK.clicked.connect(self.button_OK_fun)
        button_OK.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        button_OK.setFixedHeight(30)
        button_OK.setIcon(self.style().standardIcon(QStyle.SP_DialogApplyButton))

        validation_layout.addWidget(self.description_textbox)
        validation_layout.addWidget(button_check)
        validation_layout.addWidget(button_OK)

        # Set global layout
        title1 = QLabel("DATA STRUCTURE")
        title1.setAlignment(QtCore.Qt.AlignCenter)
        title1.setStyleSheet("background: #636363 ;border: 2px solid #000000;font-weight: bold;font-size: 18pt;color: #ffffff;")

        title2 = QLabel("DATA PATH")
        title2.setAlignment(QtCore.Qt.AlignCenter)
        title2.setStyleSheet("background: #636363 ;border: 2px solid #000000;font-weight: bold;font-size: 18pt;color: #ffffff;")

        GLOBAL_layout = QVBoxLayout(self)

        GLOBAL_layout.addWidget(title1)
        GLOBAL_layout.addWidget(BIDSnaming_frame)
        GLOBAL_layout.addWidget(input_format_frame)
        GLOBAL_layout.addWidget(title2)
        GLOBAL_layout.addWidget(input_path_frame)
        GLOBAL_layout.addWidget(output_path_frame)
        GLOBAL_layout.addWidget(validation_frame)

    def taskname_ComboBox_fun(self):
        if self.taskname_ComboBox.currentText() == "Other":
            error_dialog.setWindowTitle("Information")
            error_dialog = QErrorMessage()
            error_dialog.showMessage('If you want to add a new task name, you need to add it in the "task_names.json" file, which you can find in the root folder of this program.')
            error_dialog.exec()

    def ext_ComboBox_fun(self, callback):
        self.input_path_edit.setText("")
        self.input_ext_edit.setText(self.ext_ComboBox.currentText())

    def microID_infoButton_fun(self):
        microID_infoButton_dialog = QErrorMessage()
        microID_infoButton_dialog.setWindowTitle("Information about the 'micro ID' parameter")
        microID_infoButton_dialog.showMessage('This parameter is only necessary if the dataset include micro-electrodes. If that is the case, enter the letter(s) used to differenciate micro-channels from macro-channels.')
        microID_infoButton_dialog.exec()

    def input_infoButton_fun(self):
        input_infoButton_dialog = QErrorMessage()
        input_infoButton_dialog.setWindowTitle("Input path information")
        input_infoButton_dialog.showMessage('Search or paste the path to the data you want to turn into a BIDS-like. For .ncs choose the folder, for .trc and .nrd choose the file.')
        input_infoButton_dialog.exec()

    def input_browseButton_fun(self):
        selected_path = ""
        if ".nrd" in self.ext_ComboBox.currentText().lower() or ".trc" in self.ext_ComboBox.currentText().lower():
            selected_path = QFileDialog.getOpenFileName(self, self.tr("Select an EEG file"), '~', self.tr("EEG files (*.trc *.nrd)"))[0]
        elif ".ncs" in self.ext_ComboBox.currentText().lower():
            selected_path = QFileDialog.getExistingDirectory(self, 'Select a Neuralynx EEG folder', '~', QFileDialog.ShowDirsOnly)

        self.input_path_edit.setText(selected_path)

    def output_infoButton_fun(self):
        output_infoButton_dialog = QErrorMessage()
        output_infoButton_dialog.setWindowTitle("Output path information")
        output_infoButton_dialog.showMessage('Search or paste the path to your BIDS-like folder.')
        output_infoButton_dialog.exec()

    def output_browseButton_fun(self):
        selected_path = ""
        selected_path = QFileDialog.getExistingDirectory(self, 'Select your BIDS-like root folder', '~', QFileDialog.ShowDirsOnly)
        self.output_path_edit.setText(selected_path)

    def button_check_fun(self):

        ### Get ext
        ext = self.input_ext_edit.text().replace(".","")

        ### Get BIDS like folder path and file names
        self.path_info_dict = path_to_BIDSlikepath(int(self.patient_edit.text()), int(self.sess_edit.text()), int(self.run_edit.text()), self.output_path_edit.text(), self.taskname_ComboBox.currentText())

        ### Split path
        path_components = []
        path = os.path.normpath(self.path_info_dict[f"BIDS_tree_{ext.lower()}"])
        path = path.split(os.sep)
        [path_components.append(_comp) for _comp in path if _comp]
        path_components.append(self.path_info_dict["BIDS_full_name"])

        ### Print BIDS path tree
        self.description_textbox.append("")
        self.description_textbox.append("Original path:")
        self.description_textbox.append(self.input_path_edit.text())
        self.description_textbox.append("")
        self.description_textbox.append("BIDS-like root (destination):")
        self.description_textbox.append(self.output_path_edit.text())

        self.description_textbox.append("")
        self.description_textbox.append("BIDS-like tree:")
        tree_level = 1
        for _comp in path_components:
            self.description_textbox.append("{} {}".format( "_"*tree_level,_comp ))
            tree_level+=2

    def button_OK_fun(self):

        if not self.path_info_dict:
            self.button_check_fun()

        text = f"Format: {self.ext_ComboBox.currentText().lower()} \n\nOrigin: {self.input_path_edit.text()} \n\nDestination (root): {self.output_path_edit.text()} \n\nThis action is definitive."
        returnValue = confirm_messageBox("Please confirm", text, QMessageBox.Question, cancel_option = True)

        if returnValue == QMessageBox.Ok:
            self.proceed_BIDSlike_architecture()
        else:
            returnValue = confirm_messageBox("Procedure aborted", "Aborted.", QMessageBox.Information, cancel_option = False)

    def displayConfirm_and_resetInputPath(self):
            returnValue = confirm_messageBox("Done", "Done! BIDS-like architecture created.", QMessageBox.Information, cancel_option = False)
            self.input_path_edit.setText("")

    def proceed_BIDSlike_architecture(self):
        self.description_textbox.append("")

        try:
            if ".ncs" in self.ext_ComboBox.currentText().lower():
                ncs_destination = ncs_to_BIDSlike(self.input_path_edit.text(), self.path_info_dict, self.microID_edit.text(), process = True)
                self.description_textbox.append("Neuralynx [ncs] data processed. Data were sent to destination path.")
            elif ".nrd" in self.ext_ComboBox.currentText().lower():
                rawdata_destination = rawdata_to_BIDSlike(self.input_path_edit.text(), self.path_info_dict, process = True)
                self.description_textbox.append("Neuralynx [nrd] data processed. Data were sent to destination path.")
            elif ".trc" in self.ext_ComboBox.currentText().lower():
                TRC_destination = TRC_to_BIDSlike(self.input_path_edit.text(), self.path_info_dict, process = True)
                self.description_textbox.append("Neuralynx [trc] data processed. Data were sent to destination path.")

            self.displayConfirm_and_resetInputPath()

        except:
            var = traceback.format_exc()
            self.description_textbox.append(var)


if __name__ == "__main__":

    # Avoid python kernel from dying
    app = QCoreApplication.instance()
    if app is None:
        app = QApplication(sys.argv)

    # run
    mywindow = BIDSlike_creator_win()
    sys.exit(app.exec_())