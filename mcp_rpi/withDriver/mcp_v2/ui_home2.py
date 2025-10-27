# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'home2.ui'
##
## Created by: Qt User Interface Compiler version 6.9.2
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
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QLabel,
    QLayout, QSizePolicy, QSpacerItem, QToolButton,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1920, 720)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet(u"background-color: rgb(38, 54, 76);")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setGeometry(QRect(0, 0, 1920, 720))
        self.centralwidget.setStyleSheet(u"QToolButton{\n"
"color: rgb(255,255,255);\n"
"border-radius:10px;\n"
"background-color: rgb(57, 75, 101);\n"
"}\n"
"\n"
"\n"
"QToolButton:pressed {\n"
"    background-color: rgb(126, 147, 181);   \n"
"	border-radius:10px;\n"
"}\n"
"\n"
"QToolButton:checked {\n"
"	color: rgb(255,255,255);\n"
"  	background-color: rgb(126, 147, 181);   \n"
"   border-radius:10px;\n"
"}\n"
"")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(0, 0, 1920, 720))
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy1)
        self.label.setPixmap(QPixmap(u"images/home_bg.png"))
        self.label.setScaledContents(True)
        self.m = QLabel(self.centralwidget)
        self.m.setObjectName(u"m")
        self.m.setGeometry(QRect(110, 320, 320, 60))
        self.m.setStyleSheet(u"  QLabel {\n"
"        background-color: transparent;\n"
"    }")
        self.m.setPixmap(QPixmap(u"images/logo/prolaser-blaze.png"))
        self.m.setScaledContents(True)
        self.midFrame = QFrame(self.centralwidget)
        self.midFrame.setObjectName(u"midFrame")
        self.midFrame.setGeometry(QRect(1310, 40, 180, 600))
        self.midFrame.setFrameShape(QFrame.Shape.Box)
        self.midFrame.setFrameShadow(QFrame.Shadow.Sunken)
        self.gridLayoutWidget = QWidget(self.midFrame)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(10, 10, 161, 571))
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalSpacer_6 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_6, 4, 1, 1, 1)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_4, 2, 1, 1, 1)

        self.almRstButton = QToolButton(self.gridLayoutWidget)
        self.almRstButton.setObjectName(u"almRstButton")
        self.almRstButton.setMinimumSize(QSize(140, 120))
        self.almRstButton.setMaximumSize(QSize(145, 120))
        font = QFont()
        font.setFamilies([u"Exo 2 SemiBold"])
        font.setPointSize(16)
        font.setBold(True)
        self.almRstButton.setFont(font)
        self.almRstButton.setStyleSheet(u"")
        icon = QIcon()
        icon.addFile(u"images/white/ISO_7000_-_Ref-No_1027.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.almRstButton.setIcon(icon)
        self.almRstButton.setIconSize(QSize(80, 80))
        self.almRstButton.setCheckable(True)
        self.almRstButton.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        self.gridLayout.addWidget(self.almRstButton, 5, 1, 1, 1)

        self.almOvrButton = QToolButton(self.gridLayoutWidget)
        self.almOvrButton.setObjectName(u"almOvrButton")
        self.almOvrButton.setMinimumSize(QSize(140, 120))
        self.almOvrButton.setMaximumSize(QSize(145, 120))
        self.almOvrButton.setFont(font)
        self.almOvrButton.setStyleSheet(u"")
        icon1 = QIcon()
        icon1.addFile(u"images/white/IEC_60417_-_Ref-No_5319.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.almOvrButton.setIcon(icon1)
        self.almOvrButton.setIconSize(QSize(80, 80))
        self.almOvrButton.setCheckable(True)
        self.almOvrButton.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        self.gridLayout.addWidget(self.almOvrButton, 3, 1, 1, 1)

        self.verticalSpacer_7 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_7, 6, 1, 1, 1)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_3, 0, 1, 1, 1)

        self.servoEnableButton = QToolButton(self.gridLayoutWidget)
        self.servoEnableButton.setObjectName(u"servoEnableButton")
        self.servoEnableButton.setMinimumSize(QSize(140, 120))
        self.servoEnableButton.setFont(font)
        self.servoEnableButton.setStyleSheet(u"")
        icon2 = QIcon()
        icon2.addFile(u"images/white/IEC_60417_-_Ref-No_5010.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.servoEnableButton.setIcon(icon2)
        self.servoEnableButton.setIconSize(QSize(80, 80))
        self.servoEnableButton.setCheckable(True)
        self.servoEnableButton.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        self.gridLayout.addWidget(self.servoEnableButton, 1, 1, 1, 1)

        self.leftFrame = QFrame(self.centralwidget)
        self.leftFrame.setObjectName(u"leftFrame")
        self.leftFrame.setGeometry(QRect(580, 40, 700, 600))
        self.leftFrame.setStyleSheet(u"border-color: rgb(126, 147, 181);")
        self.leftFrame.setFrameShape(QFrame.Shape.Box)
        self.leftFrame.setFrameShadow(QFrame.Shadow.Sunken)
        self.leftFrame.setLineWidth(1)
        self.leftFrame.setMidLineWidth(2)
        self.triangle = QLabel(self.leftFrame)
        self.triangle.setObjectName(u"triangle")
        self.triangle.setGeometry(QRect(-10, 530, 31, 41))
        self.triangle.setPixmap(QPixmap(u"images/white/arrow-right.png"))
        self.triangle.setScaledContents(True)
        self.layoutWidget_10 = QWidget(self.leftFrame)
        self.layoutWidget_10.setObjectName(u"layoutWidget_10")
        self.layoutWidget_10.setGeometry(QRect(70, 20, 561, 560))
        self.gridLayout_8 = QGridLayout(self.layoutWidget_10)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.gridLayout_8.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.gridLayout_8.setContentsMargins(6, 6, 6, 6)
        self.zeroButton = QToolButton(self.layoutWidget_10)
        self.zeroButton.setObjectName(u"zeroButton")
        self.zeroButton.setMinimumSize(QSize(140, 120))
        self.zeroButton.setFont(font)
        self.zeroButton.setStyleSheet(u"")
        icon3 = QIcon()
        icon3.addFile(u"images/white/ISO_7000_-_Ref-No_1011.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.zeroButton.setIcon(icon3)
        self.zeroButton.setIconSize(QSize(80, 80))
        self.zeroButton.setCheckable(True)
        self.zeroButton.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        self.gridLayout_8.addWidget(self.zeroButton, 4, 2, 1, 1)

        self.minusButton = QToolButton(self.layoutWidget_10)
        self.minusButton.setObjectName(u"minusButton")
        self.minusButton.setMinimumSize(QSize(140, 120))
        font1 = QFont()
        font1.setFamilies([u"Exo 2 SemiBold"])
        font1.setPointSize(48)
        font1.setBold(True)
        self.minusButton.setFont(font1)
        self.minusButton.setStyleSheet(u"")
        self.minusButton.setIconSize(QSize(50, 50))
        self.minusButton.setCheckable(True)
        self.minusButton.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        self.gridLayout_8.addWidget(self.minusButton, 4, 4, 1, 1)

        self.plusButton = QToolButton(self.layoutWidget_10)
        self.plusButton.setObjectName(u"plusButton")
        self.plusButton.setMinimumSize(QSize(140, 120))
        self.plusButton.setFont(font1)
        self.plusButton.setStyleSheet(u"")
        self.plusButton.setIconSize(QSize(50, 50))
        self.plusButton.setCheckable(True)
        self.plusButton.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        self.gridLayout_8.addWidget(self.plusButton, 4, 0, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_8.addItem(self.horizontalSpacer, 2, 1, 1, 1)

        self.zButton = QToolButton(self.layoutWidget_10)
        self.zButton.setObjectName(u"zButton")
        self.zButton.setMinimumSize(QSize(140, 120))
        font2 = QFont()
        font2.setFamilies([u"Exo 2 SemiBold"])
        font2.setPointSize(32)
        font2.setBold(True)
        self.zButton.setFont(font2)
        self.zButton.setStyleSheet(u"")
        self.zButton.setIconSize(QSize(50, 50))
        self.zButton.setCheckable(True)
        self.zButton.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        self.gridLayout_8.addWidget(self.zButton, 2, 4, 1, 1)

        self.xButton = QToolButton(self.layoutWidget_10)
        self.xButton.setObjectName(u"xButton")
        self.xButton.setMinimumSize(QSize(140, 120))
        self.xButton.setFont(font2)
        self.xButton.setStyleSheet(u"")
        self.xButton.setIconSize(QSize(50, 50))
        self.xButton.setCheckable(True)
        self.xButton.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        self.gridLayout_8.addWidget(self.xButton, 2, 0, 1, 1)

        self.yButton = QToolButton(self.layoutWidget_10)
        self.yButton.setObjectName(u"yButton")
        self.yButton.setMinimumSize(QSize(140, 120))
        self.yButton.setFont(font2)
        self.yButton.setStyleSheet(u"")
        self.yButton.setIconSize(QSize(50, 50))
        self.yButton.setCheckable(True)
        self.yButton.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        self.gridLayout_8.addWidget(self.yButton, 2, 2, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_8.addItem(self.horizontalSpacer_4, 2, 3, 1, 1)

        self.cleanButton = QToolButton(self.layoutWidget_10)
        self.cleanButton.setObjectName(u"cleanButton")
        self.cleanButton.setMinimumSize(QSize(140, 120))
        self.cleanButton.setFont(font)
        self.cleanButton.setStyleSheet(u"")
        icon4 = QIcon()
        icon4.addFile(u"images/white/ISO_7000_-_Ref-No_0423.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.cleanButton.setIcon(icon4)
        self.cleanButton.setIconSize(QSize(80, 80))
        self.cleanButton.setCheckable(True)
        self.cleanButton.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        self.gridLayout_8.addWidget(self.cleanButton, 6, 0, 1, 1)

        self.nozzleBoxButton = QToolButton(self.layoutWidget_10)
        self.nozzleBoxButton.setObjectName(u"nozzleBoxButton")
        self.nozzleBoxButton.setMinimumSize(QSize(140, 120))
        self.nozzleBoxButton.setFont(font)
        self.nozzleBoxButton.setStyleSheet(u"")
        icon5 = QIcon()
        icon5.addFile(u"images/white/ISO_7000_-_Ref-No_0024.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.nozzleBoxButton.setIcon(icon5)
        self.nozzleBoxButton.setIconSize(QSize(80, 80))
        self.nozzleBoxButton.setCheckable(True)
        self.nozzleBoxButton.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        self.gridLayout_8.addWidget(self.nozzleBoxButton, 6, 4, 1, 1)

        self.verticalSpacer_18 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_8.addItem(self.verticalSpacer_18, 3, 0, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_8.addItem(self.verticalSpacer_2, 0, 0, 1, 1)

        self.verticalSpacer_9 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_8.addItem(self.verticalSpacer_9, 7, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_8.addItem(self.verticalSpacer, 5, 0, 1, 1)

        self.logoLable = QLabel(self.centralwidget)
        self.logoLable.setObjectName(u"logoLable")
        self.logoLable.setGeometry(QRect(-60, 10, 650, 450))
        self.logoLable.setStyleSheet(u"  QLabel {\n"
"        background-color: transparent;\n"
"    }")
        self.logoLable.setPixmap(QPixmap(u"images/logo/CompanyName.png"))
        self.logoLable.setScaledContents(True)
        self.rightFrame = QFrame(self.centralwidget)
        self.rightFrame.setObjectName(u"rightFrame")
        self.rightFrame.setGeometry(QRect(1690, 40, 180, 600))
        font3 = QFont()
        font3.setBold(True)
        self.rightFrame.setFont(font3)
        self.rightFrame.setFrameShape(QFrame.Shape.Box)
        self.rightFrame.setFrameShadow(QFrame.Shadow.Sunken)
        self.layoutWidget_8 = QWidget(self.rightFrame)
        self.layoutWidget_8.setObjectName(u"layoutWidget_8")
        self.layoutWidget_8.setGeometry(QRect(10, 10, 161, 581))
        self.rightGrid = QGridLayout(self.layoutWidget_8)
        self.rightGrid.setObjectName(u"rightGrid")
        self.rightGrid.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.rightGrid.setContentsMargins(6, 6, 6, 6)
        self.laserReadyLed = QToolButton(self.layoutWidget_8)
        self.laserReadyLed.setObjectName(u"laserReadyLed")
        self.laserReadyLed.setMinimumSize(QSize(145, 120))
        self.laserReadyLed.setMaximumSize(QSize(145, 120))
        self.laserReadyLed.setFont(font)
#if QT_CONFIG(statustip)
        self.laserReadyLed.setStatusTip(u"")
#endif // QT_CONFIG(statustip)
        self.laserReadyLed.setStyleSheet(u"QToolButton{\n"
"color: rgb(255,255,255);\n"
"border-radius:10px;\n"
"background-color: rgb(57, 75, 101);\n"
"}\n"
"\n"
"QToolButton:checked {\n"
"	color: rgb(255,255,255);\n"
"  	background-color: rgb(126, 147, 181);   \n"
"   border-radius:10px;\n"
"}")
        icon6 = QIcon()
        icon6.addFile(u"images/white/ISO_7000_-_Ref-No_1330.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.laserReadyLed.setIcon(icon6)
        self.laserReadyLed.setIconSize(QSize(80, 80))
        self.laserReadyLed.setCheckable(True)
        self.laserReadyLed.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        self.rightGrid.addWidget(self.laserReadyLed, 5, 0, 1, 1)

        self.laserOnButton = QToolButton(self.layoutWidget_8)
        self.laserOnButton.setObjectName(u"laserOnButton")
        self.laserOnButton.setMinimumSize(QSize(140, 120))
        self.laserOnButton.setMaximumSize(QSize(145, 120))
        self.laserOnButton.setFont(font)
        self.laserOnButton.setStyleSheet(u"QToolButton:checked {\n"
"	color: rgb(255,255,255);\n"
"  	background-color: rgb(126, 147, 181);   \n"
"   border-radius:10px;\n"
"}")
        self.laserOnButton.setIcon(icon6)
        self.laserOnButton.setIconSize(QSize(80, 80))
        self.laserOnButton.setCheckable(True)
        self.laserOnButton.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        self.rightGrid.addWidget(self.laserOnButton, 3, 0, 1, 1)

        self.verticalSpacer_5 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.rightGrid.addItem(self.verticalSpacer_5, 1, 0, 1, 1)

        self.verticalSpacer_19 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.rightGrid.addItem(self.verticalSpacer_19, 4, 0, 1, 1)

        self.verticalSpacer_20 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.rightGrid.addItem(self.verticalSpacer_20, 6, 0, 1, 1)

        self.resoLable = QLabel(self.layoutWidget_8)
        self.resoLable.setObjectName(u"resoLable")
        self.resoLable.setMinimumSize(QSize(20, 40))
        font4 = QFont()
        font4.setFamilies([u"Ubuntu"])
        font4.setPointSize(16)
        font4.setBold(True)
        font4.setItalic(False)
        self.resoLable.setFont(font4)
        self.resoLable.setStyleSheet(u"color:rgb(255,255,255);\n"
"")
        self.resoLable.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.rightGrid.addWidget(self.resoLable, 0, 0, 1, 1)

        self.autoButton = QToolButton(self.centralwidget)
        self.autoButton.setObjectName(u"autoButton")
        self.autoButton.setGeometry(QRect(430, 430, 151, 90))
        self.autoButton.setFont(font)
        self.autoButton.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.autoButton.setStyleSheet(u"QToolButton{\n"
"color: rgb(255,255,255);\n"
"border-radius:0px;\n"
"background-color: rgb(57, 75, 101);\n"
"}")
        icon7 = QIcon()
        icon7.addFile(u"images/white/ISO_7000_-_Ref-No_0992.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.autoButton.setIcon(icon7)
        self.autoButton.setIconSize(QSize(48, 48))
        self.autoButton.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.jogButton = QToolButton(self.centralwidget)
        self.jogButton.setObjectName(u"jogButton")
        self.jogButton.setGeometry(QRect(430, 520, 151, 120))
        font5 = QFont()
        font5.setFamilies([u"Exo 2 ExtraBold"])
        font5.setPointSize(16)
        font5.setBold(True)
        self.jogButton.setFont(font5)
        self.jogButton.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.jogButton.setStyleSheet(u"QToolButton{\n"
"color: rgb(255,255,255);\n"
"background-color: rgb(126, 147, 181);\n"
"border-radius:0px;\n"
"}\n"
"\n"
"QToolButton:pressed {\n"
"	color:rgb(0,0,0);\n"
"    background-color: rgb(57, 75, 101);   \n"
"	border-radius:0px;\n"
"}\n"
"	")
        icon8 = QIcon()
        icon8.addFile(u"images/white/ISO_7000_-_Ref-No_0259.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.jogButton.setIcon(icon8)
        self.jogButton.setIconSize(QSize(72, 72))
        self.jogButton.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.settingButton = QToolButton(self.centralwidget)
        self.settingButton.setObjectName(u"settingButton")
        self.settingButton.setGeometry(QRect(0, 0, 61, 51))
        icon9 = QIcon()
        icon9.addFile(u"images/white/setting.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.settingButton.setIcon(icon9)
        self.settingButton.setIconSize(QSize(30, 30))
        self.rightFrame_2 = QFrame(self.centralwidget)
        self.rightFrame_2.setObjectName(u"rightFrame_2")
        self.rightFrame_2.setGeometry(QRect(1500, 40, 180, 600))
        self.rightFrame_2.setFont(font3)
        self.rightFrame_2.setFrameShape(QFrame.Shape.Box)
        self.rightFrame_2.setFrameShadow(QFrame.Shadow.Sunken)
        self.layoutWidget_9 = QWidget(self.rightFrame_2)
        self.layoutWidget_9.setObjectName(u"layoutWidget_9")
        self.layoutWidget_9.setGeometry(QRect(10, 10, 161, 581))
        self.rightGrid_2 = QGridLayout(self.layoutWidget_9)
        self.rightGrid_2.setObjectName(u"rightGrid_2")
        self.rightGrid_2.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.rightGrid_2.setContentsMargins(6, 6, 6, 6)
        self.panelDownButton = QToolButton(self.layoutWidget_9)
        self.panelDownButton.setObjectName(u"panelDownButton")
        self.panelDownButton.setMinimumSize(QSize(140, 120))
        self.panelDownButton.setFont(font)
        self.panelDownButton.setStyleSheet(u"")
        icon10 = QIcon()
        icon10.addFile(u"images/white/window_down_icon.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.panelDownButton.setIcon(icon10)
        self.panelDownButton.setIconSize(QSize(80, 80))
        self.panelDownButton.setCheckable(True)
        self.panelDownButton.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        self.rightGrid_2.addWidget(self.panelDownButton, 4, 0, 1, 1)

        self.verticalSpacer_22 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.rightGrid_2.addItem(self.verticalSpacer_22, 5, 0, 1, 1)

        self.verticalSpacer_21 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.rightGrid_2.addItem(self.verticalSpacer_21, 3, 0, 1, 1)

        self.verticalSpacer_8 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.rightGrid_2.addItem(self.verticalSpacer_8, 1, 0, 1, 1)

        self.panelLable = QLabel(self.layoutWidget_9)
        self.panelLable.setObjectName(u"panelLable")
        self.panelLable.setMinimumSize(QSize(20, 40))
        self.panelLable.setFont(font4)
        self.panelLable.setStyleSheet(u"color:rgb(255,255,255);\n"
"")
        self.panelLable.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.rightGrid_2.addWidget(self.panelLable, 0, 0, 1, 1)

        self.panelUpButton = QToolButton(self.layoutWidget_9)
        self.panelUpButton.setObjectName(u"panelUpButton")
        self.panelUpButton.setMinimumSize(QSize(140, 120))
        self.panelUpButton.setFont(font)
        self.panelUpButton.setStyleSheet(u"")
        icon11 = QIcon()
        icon11.addFile(u"images/white/window_up_icon.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.panelUpButton.setIcon(icon11)
        self.panelUpButton.setIconSize(QSize(80, 80))
        self.panelUpButton.setCheckable(True)
        self.panelUpButton.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        self.rightGrid_2.addWidget(self.panelUpButton, 2, 0, 1, 1)


        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Machine Control Panel", None))
        self.label.setText("")
        self.m.setText("")
        self.almRstButton.setText(QCoreApplication.translate("MainWindow", u"RESET", None))
        self.almOvrButton.setText(QCoreApplication.translate("MainWindow", u"OVERRIDE", None))
        self.servoEnableButton.setText(QCoreApplication.translate("MainWindow", u"SERVO", None))
        self.triangle.setText("")
        self.zeroButton.setText(QCoreApplication.translate("MainWindow", u"ZERO", None))
        self.minusButton.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.plusButton.setText(QCoreApplication.translate("MainWindow", u"+", None))
        self.zButton.setText(QCoreApplication.translate("MainWindow", u"Z ", None))
        self.xButton.setText(QCoreApplication.translate("MainWindow", u"X ", None))
        self.yButton.setText(QCoreApplication.translate("MainWindow", u"Y ", None))
        self.cleanButton.setText(QCoreApplication.translate("MainWindow", u"CLEAN", None))
        self.nozzleBoxButton.setText(QCoreApplication.translate("MainWindow", u"OPEN", None))
        self.logoLable.setText("")
        self.laserReadyLed.setText(QCoreApplication.translate("MainWindow", u"READY", None))
        self.laserOnButton.setText(QCoreApplication.translate("MainWindow", u"ON", None))
        self.resoLable.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-weight:700;\">RESONATOR</span></p></body></html>", None))
        self.autoButton.setText(QCoreApplication.translate("MainWindow", u"AUTO", None))
        self.jogButton.setText(QCoreApplication.translate("MainWindow", u"JOG", None))
        self.settingButton.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.panelDownButton.setText(QCoreApplication.translate("MainWindow", u"DOWN", None))
        self.panelLable.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>PANEL</p></body></html>", None))
        self.panelUpButton.setText(QCoreApplication.translate("MainWindow", u"UP", None))
    # retranslateUi

