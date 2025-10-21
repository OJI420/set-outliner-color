from maya import cmds, OpenMayaUI

MAYA_VERSION = cmds.about(v=True)

if int(MAYA_VERSION) <= 2024:
    from PySide2 import QtWidgets, QtCore, QtGui
    from shiboken2 import wrapInstance

elif int(MAYA_VERSION) >= 2025:
    from PySide6 import QtWidgets, QtCore, QtGui
    from shiboken6 import wrapInstance

MAYA_MAIN_WINDOW = wrapInstance(int(OpenMayaUI.MQtUtil.mainWindow()), QtWidgets.QWidget)
TITLE = "Set Outliner Color"

class Gui(QtWidgets.QWidget):
    def __init__(self, parent=MAYA_MAIN_WINDOW):
        super().__init__(parent)
        self.pre_close()
        self.setWindowTitle(TITLE)
        self.setObjectName(f"YS_{TITLE}_Gui")
        self.setWindowFlags(QtCore.Qt.Window)

        main_layout = QtWidgets.QGridLayout(self)

        color_layout = QtWidgets.QGridLayout(self)
        color_layout.setSpacing(10)
        color_layout.setContentsMargins(10, 10, 10, 10)

        col =[
            "255, 0, 0",
            "255, 127, 0",
            "255, 255, 0",
            "127, 255, 0",
            "0, 255, 0",
            "0, 255, 127",
            "0, 255, 255",
            "0, 127, 255",
            "0, 0, 255",
            "127, 0, 255",
            "255, 0, 255",
            "255, 0, 127",
            "127, 127, 127",
            "255, 127, 127",
            "255, 191, 127",
            "255, 255, 127",
            "191, 255, 127",
            "127, 255, 127",
            "127, 255, 191",
            "127, 255, 255",
            "127, 191, 255",
            "127, 127, 255",
            "191, 127, 255",
            "255, 127, 255",
            "255, 127, 191",
            "255, 255, 255",
            "127, 0, 0",
            "127, 63, 0",
            "127, 127, 0",
            "63, 127, 0",
            "0, 127, 0",
            "0, 127, 63",
            "0, 127, 127",
            "0, 63, 127",
            "0, 0, 127",
            "63, 0, 127",
            "127, 0, 127",
            "127, 0, 63",
            "0, 0, 0"
        ]

        j = 0
        k = 0
        for i in range(39):
            button = QtWidgets.QPushButton()
            button.setMinimumSize(40, 40)
            button.setMaximumSize(40, 40)
            button.setStyleSheet(f"background-color: rgb({col[i]});")
            if i == 13 or i == 26:
                j += 1
                k += 13
            color_layout.addWidget(button, j, i - k)
            button.clicked.connect(self.set_color)

        reset = QtWidgets.QPushButton("Reset Color")
        reset.clicked.connect(self.reset_color)
        main_layout.addLayout(color_layout, 0, 0, 1, 1)
        main_layout.addWidget(reset, 1, 0, 1, 1)

    def set_color(self):
        click_button = self.sender()
        col = click_button.palette().button().color()
        col = [col.red() / 255.0, col.green() / 255.0, col.blue() / 255.0]

        for s in cmds.ls(sl=True):
            cmds.setAttr(f"{s}.useOutlinerColor", True)
            cmds.setAttr(f"{s}.outlinerColor", *col)

    def reset_color(self):
        click_button = self.sender()
        col = click_button.palette().button().color()
        col = [col.red() / 255.0, col.green() / 255.0, col.blue() / 255.0]

        for s in cmds.ls(sl=True):
            cmds.setAttr(f"{s}.useOutlinerColor", False)

    def pre_close(self):
        for widget in QtWidgets.QApplication.allWidgets():
            if widget.objectName() == f"YS_{TITLE}_Gui":
                widget.close()
                widget.deleteLater()

def main():
    win = Gui()
    win.show()