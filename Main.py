#Just a warning this code isnt pretty, as this is my first proper python project

from PyQt4 import *
from PyQt4 import QtGui, QtCore
import os, sys
from xml.etree import ElementTree

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8


    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(823, 654)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))

        self.table = QtGui.QTableWidget()
        self.tableItem = QtGui.QTableWidgetItem()
        self.table.setObjectName(_fromUtf8("table"))
        self.gridLayout.addWidget(self.table, 3, 0, 1, 2)

        self.comboBox = QtGui.QComboBox(self.centralwidget)
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.comboBox.activated[str].connect(self.selected)
        self.gridLayout.addWidget(self.comboBox, 1, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.createDropdownBoxes(MainWindow)
        self.createButton(MainWindow)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Rimworld History Inspector", None))

    def createDropdownBoxes(self, MainWindow):
        self.save_folder = os.path.expanduser("~") + '\AppData\LocalLow\Ludeon Studios\RimWorld\Saves'
        saves = os.listdir(self.save_folder)

        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.setItemText(0, _translate("MainWindow", 'Choose Save:', None))
        
        for save in range(len(saves)):
            self.comboBox.addItem(_fromUtf8(""))
            self.comboBox.setItemText(save + 1, _translate("MainWindow", saves[save].strip('.rws'), None))

    def selected(self, text):
        self.selected_text = text
        self.current_save = self.selected_text

    def createButton(self, MainWindow):
        self.pushButton = QtGui.QPushButton(self.centralwidget)
        self.gridLayout.addWidget(self.pushButton, 1, 1, 1, 1)
        self.pushButton.setText('Load Save')
        self.pushButton.clicked.connect(self.printTable)

    def printTable(self, MainWindow):
        self.table.setRowCount(0)

        self.full_file = self.save_folder + '\\' + self.current_save + '.rws'

        dom = ElementTree.parse(self.full_file)
        tales = dom.findall('game/taleManager/tales/')

        tale_types = []
        dates = []
        temps = []
        room_types = []
        weathers = []
        n = 0

        for t in tales:

            self.table.setRowCount(n + 1)
            self.table.setColumnCount(8)
            self.table.setHorizontalHeaderLabels(['Events', 'Date', 'Pawn 1', 'Pawn 2', 'Faction', 'Temperature', 'Location', 'Weather'])
            self.table.setColumnWidth(0, 150)
            self.table.setColumnWidth(3, 150)
            self.table.setColumnWidth(4, 150)
            
            tale_types.append(t.find('def').text)
            dates.append(t.find('date').text)
            temps.append(t.find('surroundings/temperature'))
            room_types.append(t.find('surroundings/roomRole'))
            weathers.append(t.find('surroundings/weather'))

            if 'Double' in str(t.attrib):
                first_colonist = t.find('firstPawnData/name/nick')
                first_kind = t.find('firstPawnData/kind')

                second_colonist = t.find('secondPawnData/name/nick')
                second_kind = t.find('secondPawnData/kind')
                second_faction = t.find('secondPawnData/faction')

            elif 'Single' in str(t.attrib):
                first_colonist = t.find('pawnData/name/nick')
                first_kind = t.find('pawnData/kind')

                second_colonist = ''
                second_kind = ''
                second_faction = ''
            else:
                first_colonist = ''
                first_kind = ''

                second_colonist = ''
                second_kind = ''
                second_faction = ''

            try:
                first_colonist = first_colonist.text
            except AttributeError:
                pass
            try:
                first_kind = first_kind.text
            except AttributeError:
                pass
            try:
                second_colonist = second_colonist.text
            except AttributeError:
                pass
            try:
                second_kind = second_kind.text
            except AttributeError:
                pass
            try:
                second_faction = second_faction.text
            except AttributeError:
                pass

            if first_colonist == None:
                first_colonist = ''
            if first_kind == None:
                first_kind = ''
            if second_colonist == None:
                second_colonist = ''
            if second_kind == None:
                second_kind = ''
            if second_faction == None:
                second_faction = ''

            #Parse Faction Data
            if second_faction == '' or None:
                second_faction = ' - '
            else:
                second_faction = second_faction.strip('Faction_')
                factions1 = []
                factions = dom.findall('game/world/factionManager/allFactions/')
                for f in factions:
                    try:
                        factions1.append(f.find('name').text)
                    except AttributeError:
                        factions1.append(' - ')
                second_faction = factions1[int(second_faction)]


            
            if first_colonist == '':
                if first_kind != '':
                    self.table.setItem(n, 2, QtGui.QTableWidgetItem(first_kind))
                else:
                    self.table.setItem(n, 2, QtGui.QTableWidgetItem(first_colonist + ' - ' + first_kind))
            else:
                    self.table.setItem(n, 2, QtGui.QTableWidgetItem(first_colonist + ' - ' + first_kind))
                
            if second_colonist == '':
                if second_kind != '':
                    self.table.setItem(n, 3, QtGui.QTableWidgetItem(second_kind))
                else:
                    self.table.setItem(n, 3, QtGui.QTableWidgetItem(second_colonist + ' - ' + second_kind))
                    self.table.setItem(n, 4, QtGui.QTableWidgetItem(second_faction))
            else:
                    self.table.setItem(n, 3, QtGui.QTableWidgetItem(second_colonist + ' - ' + second_kind))
                    self.table.setItem(n, 4, QtGui.QTableWidgetItem(second_faction))

            n += 1
        for t in range(len(tales)):

            self.table.setItem(t, 0, QtGui.QTableWidgetItem(tale_types[t]))

            #TICKS --> DATES (Unimplemented)
            #startTick = int(dates[0])
            #numTicks = int(dates[t]) - startTick
            #years = (int(numTicks) / 3600000)
            #num = numTicks - int(years) * 3600000
            #seasons = num / 900000
            #num -= int(seasons) * 900000
            #days = int(num) / 60000
            #num -= int(days) * 60000
            #hoursFloat = float(num) / 2500
            #print(int(years), int(seasons), int(days), int(hoursFloat))

            self.table.setItem(t, 1, QtGui.QTableWidgetItem(dates[t]))
            if 'Element' in str(temps[t]):
                self.table.setItem(t, 5, QtGui.QTableWidgetItem(temps[t].text))
            else:
                self.table.setItem(t, 5, QtGui.QTableWidgetItem(' - '))
            if 'Element' in str(room_types[t]):
                if str(room_types[t].text) == 'None':
                    self.table.setItem(t, 6, QtGui.QTableWidgetItem('Outside'))
                else:
                    self.table.setItem(t, 6, QtGui.QTableWidgetItem(room_types[t].text))
            else:
                self.table.setItem(t, 6, QtGui.QTableWidgetItem(' - '))
            if 'Element' in str(weathers[t]):
                self.table.setItem(t, 7, QtGui.QTableWidgetItem(weathers[t].text))
            else:
                self.table.setItem(t, 7, QtGui.QTableWidgetItem(' - '))

if __name__ == "__main__":
    import sys

    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

