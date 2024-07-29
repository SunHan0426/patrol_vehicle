# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'F:\MyProject\my_whole_project\complete_script_with_pyqt5.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1408, 1000)
        font = QtGui.QFont()
        font.setPointSize(10)
        MainWindow.setFont(font)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.line = QtWidgets.QFrame(self.centralWidget)
        self.line.setGeometry(QtCore.QRect(720, 10, 20, 971))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.ZED_Image_Box = QtWidgets.QGroupBox(self.centralWidget)
        self.ZED_Image_Box.setGeometry(QtCore.QRect(10, 10, 711, 491))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.ZED_Image_Box.setFont(font)
        self.ZED_Image_Box.setObjectName("ZED_Image_Box")
        self.RGB_Left = QtWidgets.QLabel(self.ZED_Image_Box)
        self.RGB_Left.setGeometry(QtCore.QRect(10, 30, 340, 191))
        self.RGB_Left.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.RGB_Left.setText("")
        self.RGB_Left.setObjectName("RGB_Left")
        self.RGB_Right = QtWidgets.QLabel(self.ZED_Image_Box)
        self.RGB_Right.setGeometry(QtCore.QRect(360, 30, 340, 191))
        self.RGB_Right.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.RGB_Right.setText("")
        self.RGB_Right.setObjectName("RGB_Right")
        self.Trunk_detect_res = QtWidgets.QLabel(self.ZED_Image_Box)
        self.Trunk_detect_res.setGeometry(QtCore.QRect(10, 260, 340, 191))
        self.Trunk_detect_res.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.Trunk_detect_res.setText("")
        self.Trunk_detect_res.setObjectName("Trunk_detect_res")
        self.Distance_map = QtWidgets.QLabel(self.ZED_Image_Box)
        self.Distance_map.setGeometry(QtCore.QRect(360, 260, 340, 191))
        self.Distance_map.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.Distance_map.setText("")
        self.Distance_map.setObjectName("Distance_map")
        self.label_1 = QtWidgets.QLabel(self.ZED_Image_Box)
        self.label_1.setGeometry(QtCore.QRect(100, 230, 141, 21))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_1.setFont(font)
        self.label_1.setObjectName("label_1")
        self.label_2 = QtWidgets.QLabel(self.ZED_Image_Box)
        self.label_2.setGeometry(QtCore.QRect(450, 230, 151, 21))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.ZED_Image_Box)
        self.label_3.setGeometry(QtCore.QRect(80, 460, 201, 21))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.ZED_Image_Box)
        self.label_4.setGeometry(QtCore.QRect(460, 460, 121, 21))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralWidget)
        self.textBrowser.setGeometry(QtCore.QRect(10, 671, 701, 301))
        self.textBrowser.setStyleSheet("font: 12pt \"Times New Roman\";")
        self.textBrowser.setObjectName("textBrowser")
        self.HK_Image_Box = QtWidgets.QGroupBox(self.centralWidget)
        self.HK_Image_Box.setGeometry(QtCore.QRect(740, 10, 651, 961))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.HK_Image_Box.setFont(font)
        self.HK_Image_Box.setObjectName("HK_Image_Box")
        self.RGB_1 = QtWidgets.QLabel(self.HK_Image_Box)
        self.RGB_1.setGeometry(QtCore.QRect(20, 30, 300, 300))
        self.RGB_1.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.RGB_1.setText("")
        self.RGB_1.setObjectName("RGB_1")
        self.Detect_res_1 = QtWidgets.QLabel(self.HK_Image_Box)
        self.Detect_res_1.setGeometry(QtCore.QRect(340, 30, 300, 300))
        self.Detect_res_1.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.Detect_res_1.setText("")
        self.Detect_res_1.setObjectName("Detect_res_1")
        self.RGB_2 = QtWidgets.QLabel(self.HK_Image_Box)
        self.RGB_2.setGeometry(QtCore.QRect(20, 340, 300, 300))
        self.RGB_2.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.RGB_2.setText("")
        self.RGB_2.setObjectName("RGB_2")
        self.RGB_3 = QtWidgets.QLabel(self.HK_Image_Box)
        self.RGB_3.setGeometry(QtCore.QRect(20, 650, 300, 300))
        self.RGB_3.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.RGB_3.setText("")
        self.RGB_3.setObjectName("RGB_3")
        self.Detect_res_2 = QtWidgets.QLabel(self.HK_Image_Box)
        self.Detect_res_2.setGeometry(QtCore.QRect(340, 340, 300, 300))
        self.Detect_res_2.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.Detect_res_2.setText("")
        self.Detect_res_2.setObjectName("Detect_res_2")
        self.Detect_res_3 = QtWidgets.QLabel(self.HK_Image_Box)
        self.Detect_res_3.setGeometry(QtCore.QRect(340, 650, 300, 300))
        self.Detect_res_3.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.Detect_res_3.setText("")
        self.Detect_res_3.setObjectName("Detect_res_3")
        self.Rod_Voltage = QtWidgets.QGroupBox(self.centralWidget)
        self.Rod_Voltage.setGeometry(QtCore.QRect(10, 520, 161, 61))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        self.Rod_Voltage.setFont(font)
        self.Rod_Voltage.setObjectName("Rod_Voltage")
        self.Volt_1 = QtWidgets.QRadioButton(self.Rod_Voltage)
        self.Volt_1.setGeometry(QtCore.QRect(10, 30, 61, 19))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        self.Volt_1.setFont(font)
        self.Volt_1.setObjectName("Volt_1")
        self.Volt_2 = QtWidgets.QRadioButton(self.Rod_Voltage)
        self.Volt_2.setGeometry(QtCore.QRect(90, 30, 61, 19))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        self.Volt_2.setFont(font)
        self.Volt_2.setChecked(True)
        self.Volt_2.setObjectName("Volt_2")
        self.get_distance = QtWidgets.QPushButton(self.centralWidget)
        self.get_distance.setGeometry(QtCore.QRect(200, 540, 131, 28))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        self.get_distance.setFont(font)
        self.get_distance.setCheckable(True)
        self.get_distance.setObjectName("get_distance")
        self.Rod_Return = QtWidgets.QPushButton(self.centralWidget)
        self.Rod_Return.setEnabled(False)
        self.Rod_Return.setGeometry(QtCore.QRect(590, 540, 131, 28))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        self.Rod_Return.setFont(font)
        self.Rod_Return.setCheckable(True)
        self.Rod_Return.setObjectName("Rod_Return")
        self.Get_Leaf_Images = QtWidgets.QPushButton(self.centralWidget)
        self.Get_Leaf_Images.setEnabled(False)
        self.Get_Leaf_Images.setGeometry(QtCore.QRect(400, 540, 131, 28))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        self.Get_Leaf_Images.setFont(font)
        self.Get_Leaf_Images.setCheckable(False)
        self.Get_Leaf_Images.setChecked(False)
        self.Get_Leaf_Images.setObjectName("Get_Leaf_Images")
        self.Analyze_Current = QtWidgets.QPushButton(self.centralWidget)
        self.Analyze_Current.setEnabled(False)
        self.Analyze_Current.setGeometry(QtCore.QRect(10, 620, 201, 28))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        self.Analyze_Current.setFont(font)
        self.Analyze_Current.setCheckable(True)
        self.Analyze_Current.setObjectName("Analyze_Current")
        self.Analyze_All = QtWidgets.QPushButton(self.centralWidget)
        self.Analyze_All.setEnabled(False)
        self.Analyze_All.setGeometry(QtCore.QRect(260, 620, 201, 28))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        self.Analyze_All.setFont(font)
        self.Analyze_All.setCheckable(True)
        self.Analyze_All.setObjectName("Analyze_All")
        self.Generate_Heat_Map = QtWidgets.QPushButton(self.centralWidget)
        self.Generate_Heat_Map.setEnabled(False)
        self.Generate_Heat_Map.setGeometry(QtCore.QRect(520, 620, 201, 28))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        self.Generate_Heat_Map.setFont(font)
        self.Generate_Heat_Map.setCheckable(True)
        self.Generate_Heat_Map.setObjectName("Generate_Heat_Map")
        MainWindow.setCentralWidget(self.centralWidget)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.ZED_Image_Box.setTitle(_translate("MainWindow", "ZED Camera Images"))
        self.label_1.setText(_translate("MainWindow", "ZED Left Image"))
        self.label_2.setText(_translate("MainWindow", "ZED Right Image"))
        self.label_3.setText(_translate("MainWindow", "Trunk Detection Result"))
        self.label_4.setText(_translate("MainWindow", "Distance Map"))
        self.HK_Image_Box.setTitle(_translate("MainWindow", "HD Camera Images and Results"))
        self.Rod_Voltage.setStatusTip(_translate("MainWindow", "Control the speed of rod."))
        self.Rod_Voltage.setTitle(_translate("MainWindow", "Rod Voltage"))
        self.Volt_1.setText(_translate("MainWindow", "16v"))
        self.Volt_2.setText(_translate("MainWindow", "24v"))
        self.get_distance.setStatusTip(_translate("MainWindow", "Start ZED2i, detect the tree trunk and obtain the distance between the camera and the fruit tree."))
        self.get_distance.setText(_translate("MainWindow", "Get Distance"))
        self.Rod_Return.setStatusTip(_translate("MainWindow", "Reset rod."))
        self.Rod_Return.setText(_translate("MainWindow", "Rod Return"))
        self.Get_Leaf_Images.setStatusTip(_translate("MainWindow", "Control the rod to approach the leaves according to distance and take images of the current position."))
        self.Get_Leaf_Images.setText(_translate("MainWindow", "Get Leaf Images"))
        self.Analyze_Current.setStatusTip(_translate("MainWindow", "Detect pests and diseases in current location."))
        self.Analyze_Current.setText(_translate("MainWindow", "Analyze current location"))
        self.Analyze_All.setStatusTip(_translate("MainWindow", "Detect pests and diseases in all location."))
        self.Analyze_All.setText(_translate("MainWindow", "Analyze all locations"))
        self.Generate_Heat_Map.setStatusTip(_translate("MainWindow", "Generate current map visualization of pests and diseases."))
        self.Generate_Heat_Map.setText(_translate("MainWindow", "Generate heat map"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())