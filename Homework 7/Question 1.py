import sys
import pickle
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QTextEdit, QListView, QListWidget, QPushButton, QSpinBox, QRadioButton, QButtonGroup
from PyQt5.QtWidgets import QApplication, QDialog, QFileDialog, QMessageBox
from PyQt5.QtWidgets import QGridLayout, QHBoxLayout, QVBoxLayout, QFormLayout
from PyQt5.QtWidgets import QMenuBar, QAction

# a dialog box showing a single subject's details
class SubjectDialog(QDialog):
    
    def __init__(self, parent, data):
        super().__init__(parent)

        # Create text input fields for name and symptoms
        self.name_edit = QLineEdit(self)
        self.symptoms_edit = QLineEdit(self)

        # Create a spin box for year of birth
        self.year_spinbox = QSpinBox(self)
        # Set the range of valid years
        self.year_spinbox.setRange(1900, 2024)  # Minimum: 1900, Maximum: 2024

        # Create radio buttons for gender
        self.gender_m_radio = QRadioButton("m")
        self.gender_f_radio = QRadioButton("f")
        self.gender_unknown_radio = QRadioButton("?")

        # Group them together
        self.gender_group = QButtonGroup()
        self.gender_group.addButton(self.gender_m_radio)
        self.gender_group.addButton(self.gender_f_radio)
        self.gender_group.addButton(self.gender_unknown_radio)

        # Create OK and Cancel buttons
        ok_button = QPushButton("Ok")
        cancel_button = QPushButton("Cancel")

        # Connect Ok and Cancel buttons to their respective functions
        ok_button.clicked.connect(self.accept)  # Calls accept() when Ok is clicked
        cancel_button.clicked.connect(self.reject)  # Calls reject() when Cancel is clicked

        # Create a horizontal layout for the buttons
        button_layout = QHBoxLayout()
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)

        # Add the form layout to the dialog
        form_layout = QFormLayout() # Create a new form layout
        form_layout.addRow('Name:', self.name_edit) # Add the name input field to the layout
        form_layout.addRow('Year of Birth:', self.year_spinbox) # Add the year of birth input field to the layout
        form_layout.addRow('Gender:', self.gender_m_radio) # Add the gender radio buttons to the layout
        form_layout.addRow('Symptoms:', self.symptoms_edit) # Add the symptoms input field to the layout

        # Create a vertical layout for the form and buttons
        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)  # Add the form (labels + inputs)
        main_layout.addLayout(button_layout)  # Add the buttons (OK + Cancel)

        # Set the layout of the dialog
        self.setLayout(main_layout)
        
        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('Subject')
        self.show()
        
    def setData(self, subject):
        # unpacking the data from subject
        name, year, gender, symptoms = subject

        # setting the values in their widgets
        self.name_edit.setText(name)
        self.year_spinbox.setValue(year)

        # setting the gender radio buttons
        if gender == 'm':
            self.gender_m_radio.setChecked(True)
        if gender == 'f':
            self.gender_f_radio.setChecked(True)
        else:
            self.gender_unknown_radio.setChecked(True)

        # setting the symptom's text
        self.symptoms_edit.setText(symptoms)
    
    def getData(self):
        # getting the names
        name = self.name_edit.text()

        # getting the year value
        year = self.year_spinbox.value()

        # checking the gender button
        if self.gender_m_radio.isChecked(): gender = 'm'
        if self.gender_f_radio.isChecked(): gender = 'f'
        else: gender = '?'

        # getting the symptoms
        symptoms = self.symptoms_edit.text()

        # returning the data in a list like the commented out example below
        return [name, year, gender, symptoms]

        #return ['new name', 2001, 'm', 'new symptoms']

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
        
        # Create menu bar
        menu_bar = QMenuBar(self)

        # Create "File" menu
        file_menu = menu_bar.addMenu("File")

        # some buttons
        button_add = QPushButton('Add')
        button_edit = QPushButton('Edit')
        button_delete = QPushButton('Delete') # Add a new button called delete


        # connect buttons to their functions
        button_edit.clicked.connect(self.onEditClicked) # Connect the edit button to the onEditClicked function
        button_delete.clicked.connect(self.onDeleteClicked) # Connect the delete button to the onDeleteClicked function
        button_add.clicked.connect(self.onAddClicked)  # Connect the Add button  
        
        # horizontal box for the buttons
        hbox = QHBoxLayout()
        hbox.addWidget(button_add)
        hbox.addWidget(button_edit)
        hbox.addWidget(button_delete) # Add the delete button to the layout
        
        # Add "Load" action
        load_action = QAction("Load", self)
        load_action.triggered.connect(self.loadData)
        file_menu.addAction(load_action)

        # Add "Save" action
        save_action = QAction("Save", self)
        save_action.triggered.connect(self.saveData)
        file_menu.addAction(save_action)
        
        # Connect buttons to their functions
        button_add.clicked.connect(self.onAddClicked)
        button_edit.clicked.connect(self.onEditClicked)
        button_delete.clicked.connect(self.onDeleteClicked)
               
        # list of the subject's names
        self.list = QListWidget()
        self.list.setDragDropMode(QListWidget.InternalMove)
        self.list.model().rowsMoved.connect(self.onRowsMoved)
        self.updateList()

        # vertical layout: buttons below the list
        vbox = QVBoxLayout()
        vbox.addWidget(menu_bar)
        vbox.addWidget(self.list)
        vbox.addLayout(hbox)
        
        self.setLayout(vbox)
        
        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('Subject List')
        self.show()


    def onRowsMoved(self, parent, start, end, destination, row):
        """
        Update the self.data list to match the new order after rows are moved.
        """
        # Extract the moved items
        moved_items = self.data[start:end + 1]  # +1 because `end` is inclusive
        del self.data[start:end + 1]  # Remove the moved items from the original position

        # Adjust row index if items are moved down
        if row > start:
            row -= len(moved_items)

        # Insert the moved items at the new position
        for i, item in enumerate(moved_items):
            self.data.insert(row + i, item)

    def updateList(self): # Define a new function called updateList
        self.list.clear()  # Clear the existing items in the list
        for subject in self.data:
            self.list.addItem(subject[0])  # Add the name (first element of each subject list)

        
    def onAddClicked(self):
        # creating a new SubjectDialog instance
        dlg = SubjectDialog(self)

        # disabling the window
        self.setEnabled(False)

        # running the dialog
        if dlg.exec_() == QDialog.Accepted:
            # getting the new subject data from the dialog
            new_subject = dlg.getData()

            # adding the new data to the list
            self.data.append(new_subject)

            # updating the list based on the new data
            self.updateList()

        # enabling the main window again
        self.setEnabled(True)
    
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
    
    def onDeleteClicked(self): # Define a new function called onDeleteClicked
        current_row = self.list.currentRow()  # Get the selected row index
        if current_row < 0:
            return  # If no item is selected, do nothing
    
        # Remove the subject from the data list
        del self.data[current_row]
    
        # Remove the item from the QListWidget
        self.list.takeItem(current_row)
    
        # Update the list to reflect changes (optional in this case)
        self.updateList()

    def loadData(self):
        # Show file dialog to select a file
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Pickle Files (*.pkl);;All Files (*)")
        if file_path:
            try:
                # Load the data from the selected file
                with open(file_path, "rb") as file:
                    self.data = pickle.load(file)

                # Update the list widget
                self.updateList()
            except Exception as e:
                # Show an error message if loading fails
                QMessageBox.critical(self, "Error", f"Failed to load file: {e}")

    def saveData(self):
        # Show file dialog to select a save location
        file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Pickle Files (*.pkl);;All Files (*)")
        if file_path:
            try:
                # Save the data to the selected file
                with open(file_path, "wb") as file:
                    pickle.dump(self.data, file)
            except Exception as e:
                # Show an error message if saving fails
                QMessageBox.critical(self, "Error", f"Failed to save file: {e}")
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = ListWindow()
    app.exec_()

