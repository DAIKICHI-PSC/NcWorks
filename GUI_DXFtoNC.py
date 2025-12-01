# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'GUI_DXFtoNC.ui'
##
## Created by: Qt User Interface Compiler version 6.2.4
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QGridLayout,
    QGroupBox, QMainWindow, QMenuBar, QPlainTextEdit,
    QPushButton, QSizePolicy, QStatusBar, QWidget)

class Ui_MainWindow2(object):
    def setupUi(self, MainWindow2):
        if not MainWindow2.objectName():
            MainWindow2.setObjectName(u"MainWindow2")
        MainWindow2.resize(881, 551)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow2.sizePolicy().hasHeightForWidth())
        MainWindow2.setSizePolicy(sizePolicy)
        MainWindow2.setMinimumSize(QSize(881, 551))
        icon = QIcon()
        icon.addFile(u"PLANET.ico", QSize(), QIcon.Normal, QIcon.Off)
        MainWindow2.setWindowIcon(icon)
        self.centralwidget = QWidget(MainWindow2)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.groupBox1 = QGroupBox(self.centralwidget)
        self.groupBox1.setObjectName(u"groupBox1")
        self.groupBox1.setMinimumSize(QSize(291, 61))
        self.pushButton1 = QPushButton(self.groupBox1)
        self.pushButton1.setObjectName(u"pushButton1")
        self.pushButton1.setGeometry(QRect(10, 20, 131, 31))
        self.pushButton2 = QPushButton(self.groupBox1)
        self.pushButton2.setObjectName(u"pushButton2")
        self.pushButton2.setGeometry(QRect(150, 20, 131, 31))

        self.gridLayout.addWidget(self.groupBox1, 1, 0, 1, 1)

        self.groupBox3 = QGroupBox(self.centralwidget)
        self.groupBox3.setObjectName(u"groupBox3")
        self.groupBox3.setMinimumSize(QSize(121, 61))
        self.comboBox2 = QComboBox(self.groupBox3)
        self.comboBox2.setObjectName(u"comboBox2")
        self.comboBox2.setGeometry(QRect(10, 20, 101, 22))

        self.gridLayout.addWidget(self.groupBox3, 1, 2, 1, 1)

        self.groupBox2 = QGroupBox(self.centralwidget)
        self.groupBox2.setObjectName(u"groupBox2")
        self.groupBox2.setMinimumSize(QSize(135, 61))
        self.comboBox1 = QComboBox(self.groupBox2)
        self.comboBox1.setObjectName(u"comboBox1")
        self.comboBox1.setGeometry(QRect(10, 20, 101, 22))

        self.gridLayout.addWidget(self.groupBox2, 1, 1, 1, 1)

        self.groupBox4 = QGroupBox(self.centralwidget)
        self.groupBox4.setObjectName(u"groupBox4")
        self.groupBox4.setMinimumSize(QSize(121, 61))
        self.comboBox3 = QComboBox(self.groupBox4)
        self.comboBox3.setObjectName(u"comboBox3")
        self.comboBox3.setGeometry(QRect(10, 20, 101, 22))

        self.gridLayout.addWidget(self.groupBox4, 1, 3, 1, 1)

        self.groupBox5 = QGroupBox(self.centralwidget)
        self.groupBox5.setObjectName(u"groupBox5")
        self.groupBox5.setMinimumSize(QSize(161, 61))
        self.comboBox4 = QComboBox(self.groupBox5)
        self.comboBox4.setObjectName(u"comboBox4")
        self.comboBox4.setGeometry(QRect(10, 20, 101, 22))
        self.checkBox1 = QCheckBox(self.groupBox5)
        self.checkBox1.setObjectName(u"checkBox1")
        self.checkBox1.setGeometry(QRect(120, 20, 41, 16))
        self.checkBox1.setChecked(True)

        self.gridLayout.addWidget(self.groupBox5, 1, 4, 1, 1)

        self.plainTextEdit = QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.setObjectName(u"plainTextEdit")
        self.plainTextEdit.setMinimumSize(QSize(781, 201))
        font = QFont()
        font.setFamilies([u"\u6e38\u30b4\u30b7\u30c3\u30af"])
        font.setPointSize(12)
        self.plainTextEdit.setFont(font)

        self.gridLayout.addWidget(self.plainTextEdit, 0, 0, 1, 5)

        MainWindow2.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow2)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 881, 22))
        MainWindow2.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow2)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow2.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow2)

        QMetaObject.connectSlotsByName(MainWindow2)
    # setupUi

    def retranslateUi(self, MainWindow2):
        MainWindow2.setWindowTitle(QCoreApplication.translate("MainWindow2", u"NcWorks DXFtoNC ", None))
        self.groupBox1.setTitle(QCoreApplication.translate("MainWindow2", u"\u5b9f\u884c", None))
        self.pushButton1.setText(QCoreApplication.translate("MainWindow2", u"DXF\u30c7\u30fc\u30bf\u306e\u8aad\u307f\u8fbc\u307f", None))
        self.pushButton2.setText(QCoreApplication.translate("MainWindow2", u"\u30d7\u30ed\u30b0\u30e9\u30e0\u3092\u4fdd\u5b58", None))
        self.groupBox3.setTitle(QCoreApplication.translate("MainWindow2", u"\u7e26\u6a2a\u65b9\u5411\u306e\u9001\u308a", None))
        self.groupBox2.setTitle(QCoreApplication.translate("MainWindow2", u"\u30c6\u30fc\u30d1\u30fc\u3068R\u306e\u9001\u308a", None))
        self.groupBox4.setTitle(QCoreApplication.translate("MainWindow2", u"\u56de\u8ee2\u6570", None))
        self.groupBox5.setTitle(QCoreApplication.translate("MainWindow2", u"\u30c9\u30a5\u30a6\u30a7\u30eb", None))
        self.checkBox1.setText(QCoreApplication.translate("MainWindow2", u"\u30aa\u30f3", None))
    # retranslateUi

