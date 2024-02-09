import sys
import os
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QLabel, QGridLayout, QLineEdit, QPushButton, QCheckBox, QRadioButton, QMessageBox, QScrollArea, QVBoxLayout, QSlider, QSpinBox, QDoubleSpinBox, QFileDialog
import json
from glob import glob
import platform

class RowWidget(QWidget):
    def __init__(self, name, desc, val, default_val, input_type, choices=None, range=None, extras={}, parent=None):
        super(RowWidget, self).__init__(parent)
        self.name = name
        self.val = val
        self.default_val = default_val
        self.input_type = input_type
        self.choices = choices
        self.range = range
        self.extras = extras

        if "slider" in self.extras and self.extras["slider"] and (self.input_type == "integer" or self.input_type == "float"):
            self.sliderExists = True
        else:
            self.sliderExists = False

        if "multi" in self.extras and self.extras["multi"] and self.input_type == "list":
            self.multi_choice = True
        else:
            self.multi_choice = False

        self.title_label = QLabel(name)
        self.description_label = QLabel(desc)
        self.error = False

        if self.input_type == "integer" or self.input_type == "float":
            restrictions = []
            if type(self.range[0]) == int or type(self.range[0]) == float:
                restrictions.append("Min: " + str(self.range[0]))
            else:
                self.range[0] = -2**30
                self.sliderExists = False
            if type(self.range[1]) == int or type(self.range[1]) == float:
                restrictions.append("Max: " + str(self.range[1]))
            else:
                self.range[1] = 2**30
                self.sliderExists = False
            if self.range[2] and (type(self.range[2]) == int or type(self.range[2]) == float):
                restrictions.append("Step: " + str(self.range[2]))
            else:
                self.range[2] = 1.0
                self.sliderExists = False

            if self.input_type == "integer":
                self.input_box = QSpinBox()
            elif self.input_type == "float":
                self.input_box = QDoubleSpinBox()
                if "precision" in self.extras:
                    self.input_box.setDecimals(extras["precision"])
                else:
                    self.input_box.setDecimals(str(range[2])[::-1].find('.'))
                

            self.input_box.setFixedHeight(25)

            self.input_box.setRange(range[0], range[1])
            self.input_box.setSingleStep(self.range[2])
                            
            if self.sliderExists:
                self.slider = QSlider()
                self.slider.setOrientation(Qt.Horizontal)
                self.slider.valueChanged.connect(self.slider_value_changed)
                if self.input_type == "float":
                    self.slider_precision = str(range[2])[::-1].find('.')
                    newMin = self.floatToInt(range[0])
                    newMax = self.floatToInt(range[1])
                    newStep = self.floatToInt(range[2])
                    self.slider.setRange(newMin, newMax)
                    self.slider.setTickInterval(newStep)
                    
                else:
                    self.slider.setRange(range[0], range[1])
                    self.slider.setTickInterval(range[2])

            self.valid_inputs_label = QLabel(", ".join(restrictions))
            self.input_box.valueChanged.connect(self.input_box_text_changed)
            self.input_box.setValue(self.val)

   
        elif self.input_type == "boolean":
            self.checkbox = QCheckBox()
            self.checkbox.setChecked(self.val)
            self.checkbox.stateChanged.connect(self.checkbox_state_changed)


        elif self.input_type == "string":
            self.radios = []
            for c in self.choices:
                self.radios.append(QRadioButton(c))

        elif self.input_type == "list":
            self.checkboxes = []
            for c in self.choices:
                self.checkboxes.append(QCheckBox(c))
        
        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self.click_reset)
        self.reset_button.setFixedHeight(25)
        self.setup_ui()
        
    def setup_ui(self):
        grid = QGridLayout()
        grid.addWidget(self.title_label, 0, 0)
        grid.addWidget(self.description_label, 1, 0)

        items = 0
        if self.input_type == "integer" or self.input_type == "float":
            boxgrid = QGridLayout()
            boxgrid.addWidget(self.valid_inputs_label, 0, 0)
            if self.sliderExists:
                boxgrid.addWidget(self.slider, 0, 1)
                boxgrid.setColumnStretch(2, 999)
            boxgrid.addWidget(self.input_box, 0, int(self.sliderExists) + 1)
            boxgrid.setColumnStretch(1, 999)
            grid.addLayout(boxgrid, 2, 0)
            items += 1


        elif self.input_type == "boolean":
            grid.addWidget(self.checkbox, 2, items)
            items += 1


        elif self.input_type == "string":
            radiogrid = QGridLayout()
            for r in self.radios:
                radiogrid.addWidget(r, 0, items)
                if r.text() == self.val:
                    r.setChecked(True)
                r.toggled.connect(self.radiobutton_toggled)

                radiogrid.setColumnStretch(items, 1)
                items += 1
            
            radiogrid.setColumnStretch(items, 999)

            grid.addLayout(radiogrid, 2, 0)

        elif self.input_type == "list":
            checkboxgrid = QGridLayout()
            for cb in self.checkboxes:
                checkboxgrid.addWidget(cb, 0, items)
                if cb.text() in self.val:
                    cb.setChecked(True)
                cb.toggled.connect(self.multi_checkbox_state_changed)

                checkboxgrid.setColumnStretch(items, 1)
                items += 1
            
            checkboxgrid.setColumnStretch(items, 999)

            grid.addLayout(checkboxgrid, 2, 0)

        grid.addWidget(self.reset_button, 2, items, Qt.AlignRight)
 

        self.setLayout(grid)

    def input_box_text_changed(self, value):
        self.val = value
        if self.sliderExists:
            if self.input_type == "float":
                self.slider.setValue(self.floatToInt(value))
            else:
                self.slider.setValue(value)

    def slider_value_changed(self, value):
        if self.input_type == "float":
            self.input_box.setValue(self.intToFloat(value))
        else:
            self.input_box.setValue(value)

    
    def checkbox_state_changed(self, state):
        self.val = self.checkbox.isChecked()


    def radiobutton_toggled(self, checked):
        if checked:
            self.val = self.sender().text()

    def multi_checkbox_state_changed(self, state):
        if (self.sender().text() in self.val) != state:
            if state:
                self.val.append(self.sender().text())
            else:
                self.val.remove(self.sender().text())


    def click_reset(self):
        if self.input_type == "integer" or self.input_type == "float":
            self.val = self.default_val
            self.input_box.setValue(self.default_val)

        elif self.input_type == "boolean":
            self.val = self.default_val
            self.checkbox.setChecked(self.default_val)

        elif self.input_type == "string":
            self.val = self.default_val
            for r in self.radios:
                if r.text() == self.default_val:
                    r.setChecked(True)

        elif self.input_type == "list":
            self.val = self.default_val
            for cb in self.checkboxes:
                if cb.text() in self.default_val:
                    cb.setChecked(True)
                else:
                    cb.setChecked(False)

    def error_color(self):
        self.setStyleSheet("background-color: red;")


    def clamp(num, min_value, max_value):
        return max(min(num, max_value), min_value)
    

    def floatToInt(self, num):
        return int(self.slider_precision*10*num)
    

    def intToFloat(self, num):
        return num/(self.slider_precision*10)


class MyGUI(QMainWindow):
    def __init__(self, config_list, game_data_path):
        super().__init__()

        self.config_list = config_list
        self.game_data_path = game_data_path


        self.database = {}
        self.allWidgets = []

        self.warning = False

        self.setWindowTitle("Cephelos Mod Configurator")
        self.setGeometry(100, 100, 1280, 720)
        self.run_init()
        
    def run_init(self):
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)

        self.mod_tabs_widget = QTabWidget(self)
        self.mod_tabs_layout = QVBoxLayout(self.mod_tabs_widget)

        self.central_widget_dict = {}
        

        self.create_mod_tabs()

        bottom_buttons = QGridLayout()

        self.reset_button = QPushButton("Change Appdata Path")
        self.reset_button.clicked.connect(self.change_path)
        bottom_buttons.addWidget(self.reset_button, 1, 1, alignment=Qt.AlignRight)

        self.reset_button = QPushButton("Reset All")
        self.reset_button.clicked.connect(self.click_reset)
        bottom_buttons.addWidget(self.reset_button, 1, 2, alignment=Qt.AlignRight)

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.click_save)
        bottom_buttons.addWidget(self.save_button, 1, 3, alignment=Qt.AlignRight)

        bottom_buttons.setColumnStretch(0, 999)



        self.mod_tabs_widget.setLayout(self.mod_tabs_layout)
        main_layout.addWidget(self.mod_tabs_widget)
        main_layout.addLayout(bottom_buttons)
        
        self.setCentralWidget(main_widget)

    def create_mod_tabs(self):
        for mod_config_path in self.config_list:
            if self.create_tabs(mod_config_path):
                self.mod_tabs_widget.addTab(self.central_widget_dict[os.path.basename(os.path.dirname(mod_config_path))], os.path.basename(os.path.dirname(mod_config_path)))

    def create_tabs(self, mod_config_path):
        mod_config = json_read(mod_config_path)
        if not mod_config:
            return False
        else:
            self.central_widget_dict[os.path.basename(os.path.dirname(mod_config_path))] = QTabWidget(self.mod_tabs_widget)
        for page in mod_config:
            self.database[mod_config_path] = mod_config
            tab = QWidget()
            scroll_area = QScrollArea()
            scroll_layout = QGridLayout(tab)
            index = 0
            if "__CephelosModConfig" in page:
                continue

            for o in mod_config[page]:
                val = mod_config[page][o]["value"]
                default_val = mod_config[page][o]["default"]
                choices = None
                range = ["None", "None", "None"]
                
                if "extras" in mod_config[page][o]:
                    extras = mod_config[page][o]["extras"]
                else:
                    extras = {}

                if type(default_val) == int or type(default_val) == float:

                    if type(default_val) == int:
                        input_type = "integer"

                    elif type(default_val) == float:
                        input_type = "float"
                    
                    if "range" in mod_config[page][o]:
                        range = mod_config[page][o]["range"]

                    else:
                        raise KeyError
                    
                elif type(default_val) == bool:
                    input_type = "boolean"

                elif type(default_val) == str:
                    choices = mod_config[page][o]["choices"]
                    input_type = "string"

                elif type(default_val) == list:
                    choices = mod_config[page][o]["choices"]
                    input_type = "list"
                    extras["mutli"] = True

                row_widget = RowWidget(o, mod_config[page][o]["description"], val, default_val, input_type, choices, range, extras)
                scroll_layout.addWidget(row_widget, index, 0)
                self.allWidgets.append((mod_config_path, page, row_widget))
                index += 1

            scroll_layout.setRowStretch(index, 999)

            tab.setLayout(scroll_layout)
            scroll_area.setWidgetResizable(True)
            scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
            scroll_area.horizontalScrollBar().setEnabled(False)
            scroll_area.setWidget(tab)
            self.central_widget_dict[os.path.basename(os.path.dirname(mod_config_path))].addTab(scroll_area, page)
        return True


    def click_save(self):
        error_list = self.check_for_errors()
        if self.warning:
            QMessageBox.question(self, 'Warning!', "Fix errors in " + ", ".join(error_list) + " before trying to save!", QMessageBox.Ok, QMessageBox.Ok)
            return
            
        for w in self.allWidgets:
            file = w[0]
            page = w[1]
            widget = w[2]
            self.database[file][page][widget.name]['value'] = widget.val

        for f in self.database:
            json_write(f, self.database[f])
        
        QMessageBox.question(self, 'Success!', "Saving Complete!", QMessageBox.Ok, QMessageBox.Ok)


    def click_reset(self):
        for w in self.allWidgets:
            widget = w[2]
            if widget.input_type == "integer" or widget.input_type == "float":
                widget.val = widget.default_val
                widget.input_box.setValue(widget.default_val)

            elif widget.input_type == "boolean":
                widget.val = widget.default_val
                widget.checkbox.setChecked(widget.default_val)

            elif widget.input_type == "string":
                widget.val = widget.default_val
                for r in widget.radios:
                    if r.text() == widget.default_val:
                        r.setChecked(True)
            
            elif widget.input_type == "list":
                widget.val = widget.default_val
                for cb in widget.checkboxes:
                    if cb.text() in widget.default_val:
                        cb.setChecked(True)
                    else:
                        cb.setChecked(False)

    def change_path(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.Directory)
        file_dialog.setViewMode(QFileDialog.Detail)
        file_dialog.setDirectory(self.game_data_path)

        
        if file_dialog.exec_():
            file_paths = file_dialog.selectedFiles()
            if file_paths:
                self.configList = glob(file_paths[0] + "/*/*.json")
                self.run_init()
    
    

    def check_for_errors(self):
        no_errors = True
        error_pages = []
        for w in self.allWidgets:
            widget = w[2]
            if widget.error == True:
                self.warning = True
                no_errors = False
                error_pages.append(w[1])

        if no_errors:
            self.warning = False
        return error_pages
    
def main():
    app = QApplication(sys.argv)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    if platform.system() == "Windows":
        game_data_path = os.getenv("LOCALAPPDATA") + "\\Larian Studios\\Baldur's Gate 3\\"
    elif platform.system() == "Darwin":
        game_data_path = "$HOME/Documents/Larian Studios/Baldur's Gate 3/"
    else:  
        # If you're using Linux you're smart enough to find it yourself
        game_data_path = None

    if not game_data_path or not os.path.exists(game_data_path):
        if os.path.exists(os.getenv("LOCALAPPDATA") + "\\JSONModConfigurator\\path.config"):
            config = open(os.getenv("LOCALAPPDATA") + "\\JSONModConfigurator\\path.config", "r").read()
            game_data_path = config[6:]

        if not game_data_path or not os.path.exists(game_data_path):
            QMessageBox.warning(None, "Game Data Directory Not Found", "Your game data directory couldn't be found. Please navigate to it now.", QMessageBox.Ok)
            game_data_path = None

    jsons, game_data_path = find_jsons(game_data_path)
    gui = MyGUI(jsons, game_data_path)
    gui.show()
    sys.exit(app.exec_())


def find_jsons(game_data_path):
    if not game_data_path:
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.Directory)
        file_dialog.setViewMode(QFileDialog.Detail)
        
        if file_dialog.exec_():
            file_paths = file_dialog.selectedFiles()
            if file_paths:
                game_data_path = file_paths[0]
                if not os.path.exists(os.getenv("LOCALAPPDATA") + "\\JSONModConfigurator"):
                    os.mkdir(os.getenv("LOCALAPPDATA") + "\\JSONModConfigurator")
                f = open(os.getenv("LOCALAPPDATA") + "\\JSONModConfigurator\\path.config", "w")
                f.write("Path: " + game_data_path)
                f.close()
    json_list = glob(game_data_path + "Script Extender/*/*.json")
    
    return json_list, game_data_path


def json_read(file):
    with open(file,"r") as file_handler:
        file_handler.seek(0)
        json_data = json.load(file_handler)
        if "__CephelosModConfig" not in json_data:
            return None
    file_handler.close
    print('file has been read and closed')
    return json_data



def json_write(file, json_data):
    with open(file, "w") as file_handler:
        json.dump(json_data, file_handler, indent=4)
    file_handler.close
    print('file has been written to and closed')

def find_deepest_parent(path):
    while path != os.path.dirname(path):
        if os.path.exists(path):
            return path
        path = os.path.dirname(path)
    return path



if __name__ == "__main__":
    main()
