#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QTextEdit, QListView, QListWidget, QPushButton, QSpinBox, QRadioButton, QButtonGroup
from PyQt5.QtWidgets import QApplication, QDialog, QFileDialog
from PyQt5.QtWidgets import QGridLayout, QHBoxLayout, QVBoxLayout, QFormLayout

# a dialog box showing a single subject's details
class SubjectDialog(QDialog):
    
    def __init__(self, parent, data):
        super().__init__(parent)

        # TODO create GUI elements and layouts
        
        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('Subject')
        self.show()
        
    def setData(self, subject):
        # TODO fill out the GUI elements
        pass

    
    def getData(self):
        # TODO read out the GUI elements
        return ['new name', 2001, 'm', 'new symptoms']


# window showing a list with all subject names
class ListWindow(QWidget):
    
    def __init__(self):
        super().__init__()
        
        # subject data stored as a list
        #     each subject is also a list containing
        #         name (string)
        #         year of birth (number)
        #         gender (string 'm', 'f' or '?')
        #         symptoms (string)
        self.data = [['Dummy Name', 1900, 'm', 'some symptoms'],
                     ['Other Dummy Name', 1970, 'f', 'other symptoms']]
        
        # some buttons
        button_add = QPushButton('Add')
        button_edit = QPushButton('Edit')
        
        # horizontal box for the buttons
        hbox = QHBoxLayout()
        hbox.addWidget(button_add)
        hbox.addWidget(button_edit)
        
        # TODO add 'Load' and 'Save' buttons
        
        
        # TODO connect functions to the buttons,
        # so they are called when the user clicks a button
        
        # list of the subject's names
        self.list = QListWidget()
        self.updateList()

        # vertical layout: buttons below the list
        vbox = QVBoxLayout()
        vbox.addWidget(self.list)
        vbox.addLayout(hbox)
        
        self.setLayout(vbox)
        
        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('Subject List')
        self.show()
        
    def updateList(self):
        # TODO populate list with the subject's names
        pass
        
    def onEditClicked(self):
        
        # which row is selected/current?
        current_row = self.list.currentRow()
        if current_row < 0:
            return
        
        # create the subject dialog box
        dlg = SubjectDialog(self)
        
        # fill the dialog box with our data
        dlg.setData(self.data[current_row])
        
        # don't allow any user input as long as the dialog box is visible
        self.setEnabled(False)
        
        # run the dialog
        if dlg.exec_() == dlg.Accepted:
            
            # get the edited data from the dialog box
            self.data[current_row] = dlg.getData()
            self.updateList()
         
        # ok, user input again
        self.setEnabled(True)
        
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = ListWindow()
    app.exec_()

