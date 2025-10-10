# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'home1.ui'
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
    QLayout, QRadioButton, QSizePolicy, QSpacerItem,
    QToolButton, QWidget)

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
"QToolButton{\n"
"color: rgb(255,255,255);\n"
"border-radius:10px;\n"
"}\n"
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
"}")
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
        self.machineLable = QLabel(self.centralwidget)
        self.machineLable.setObjectName(u"machineLable")
        self.machineLable.setGeometry(QRect(110, 320, 320, 60))
        self.machineLable.setStyleSheet(u"  QLabel {\n"
"        background-color: transparent;\n"
"    }")
        self.machineLable.setPixmap(QPixmap(u"images/logo/prolaser-blaze.png"))
        self.machineLable.setScaledContents(True)
        self.autoButton = QToolButton(self.centralwidget)
        self.autoButton.setObjectName(u"autoButton")
        self.autoButton.setGeometry(QRect(520, 430, 151, 120))
        font = QFont()
        font.setFamilies([u"Exo 2 ExtraBold"])
        font.setPointSize(16)
        font.setBold(True)
        self.autoButton.setFont(font)
        self.autoButton.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.autoButton.setStyleSheet(u"QToolButton{\n"
"color: rgb(255,255,255);\n"
"border-radius:0px;\n"
"background-color: rgb(126, 147, 181);\n"
"}\n"
"QToolButton:pressed {\n"
"	color:rgb(0,0,0);\n"
"    background-color: rgb(57, 75, 101);   \n"
"	border-radius:0px;\n"
"}\n"
"")
        icon = QIcon()
        icon.addFile(u"images/white/ISO_7000_-_Ref-No_0992.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.autoButton.setIcon(icon)
        self.autoButton.setIconSize(QSize(70, 70))
        self.autoButton.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.leftFrame = QFrame(self.centralwidget)
        self.leftFrame.setObjectName(u"leftFrame")
        self.leftFrame.setGeometry(QRect(670, 40, 700, 600))
        self.leftFrame.setFrameShape(QFrame.Shape.Box)
        self.leftFrame.setFrameShadow(QFrame.Shadow.Sunken)
        self.leftFrame.setLineWidth(1)
        self.leftFrame.setMidLineWidth(2)
        self.layoutWidget_9 = QWidget(self.leftFrame)
        self.layoutWidget_9.setObjectName(u"layoutWidget_9")
        self.layoutWidget_9.setGeometry(QRect(70, 20, 561, 561))
        self.leftGrid = QGridLayout(self.layoutWidget_9)
        self.leftGrid.setObjectName(u"leftGrid")
        self.leftGrid.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.leftGrid.setContentsMargins(6, 6, 6, 6)
        self.verticalSpacer_6 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.leftGrid.addItem(self.verticalSpacer_6, 0, 0, 1, 1)

        self.verticalSpacer_18 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.leftGrid.addItem(self.verticalSpacer_18, 2, 0, 1, 1)

        self.verticalSpacer_21 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.leftGrid.addItem(self.verticalSpacer_21, 4, 0, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.leftGrid.addItem(self.horizontalSpacer, 1, 1, 1, 1)

        self.verticalSpacer_22 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.leftGrid.addItem(self.verticalSpacer_22, 6, 0, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.leftGrid.addItem(self.horizontalSpacer_2, 1, 3, 1, 1)

        self.prcEndButton = QToolButton(self.layoutWidget_9)
        self.prcEndButton.setObjectName(u"prcEndButton")
        self.prcEndButton.setMinimumSize(QSize(140, 120))
        self.prcEndButton.setMaximumSize(QSize(145, 120))
        font1 = QFont()
        font1.setFamilies([u"Exo 2 SemiBold"])
        font1.setPointSize(16)
        font1.setBold(True)
        self.prcEndButton.setFont(font1)
        self.prcEndButton.setStyleSheet(u"")
        icon1 = QIcon()
        icon1.addFile(u"images/white/ISO_7000_-_Ref-No_0479.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.prcEndButton.setIcon(icon1)
        self.prcEndButton.setIconSize(QSize(80, 80))
        self.prcEndButton.setCheckable(True)
        self.prcEndButton.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        self.leftGrid.addWidget(self.prcEndButton, 1, 4, 1, 1)

        self.zLockButton = QToolButton(self.layoutWidget_9)
        self.zLockButton.setObjectName(u"zLockButton")
        self.zLockButton.setMinimumSize(QSize(140, 120))
        self.zLockButton.setMaximumSize(QSize(145, 120))
        self.zLockButton.setFont(font1)
        self.zLockButton.setStyleSheet(u"")
        icon2 = QIcon()
        icon2.addFile(u"images/white/IEC_60417_-_Ref-No_5569.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.zLockButton.setIcon(icon2)
        self.zLockButton.setIconSize(QSize(80, 80))
        self.zLockButton.setCheckable(True)
        self.zLockButton.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        self.leftGrid.addWidget(self.zLockButton, 1, 0, 1, 1)

        self.cycleStartButton = QToolButton(self.layoutWidget_9)
        self.cycleStartButton.setObjectName(u"cycleStartButton")
        self.cycleStartButton.setMinimumSize(QSize(140, 120))
        self.cycleStartButton.setMaximumSize(QSize(145, 120))
        self.cycleStartButton.setFont(font1)
        self.cycleStartButton.setStyleSheet(u"")
        icon3 = QIcon()
        icon3.addFile(u"images/white/IEC_60417_-_Ref-No_5104.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.cycleStartButton.setIcon(icon3)
        self.cycleStartButton.setIconSize(QSize(80, 80))
        self.cycleStartButton.setCheckable(True)
        self.cycleStartButton.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        self.leftGrid.addWidget(self.cycleStartButton, 5, 0, 1, 1)

        self.dryRunButton = QToolButton(self.layoutWidget_9)
        self.dryRunButton.setObjectName(u"dryRunButton")
        self.dryRunButton.setMinimumSize(QSize(132, 120))
        self.dryRunButton.setMaximumSize(QSize(145, 120))
        self.dryRunButton.setFont(font1)
        self.dryRunButton.setStyleSheet(u"")
        icon4 = QIcon()
        icon4.addFile(u"images/white/IEC_60417_-_Ref-No_5659.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.dryRunButton.setIcon(icon4)
        self.dryRunButton.setIconSize(QSize(80, 80))
        self.dryRunButton.setCheckable(True)
        self.dryRunButton.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        self.leftGrid.addWidget(self.dryRunButton, 3, 2, 1, 1)

        self.offsetButton = QToolButton(self.layoutWidget_9)
        self.offsetButton.setObjectName(u"offsetButton")
        self.offsetButton.setMinimumSize(QSize(140, 120))
        self.offsetButton.setMaximumSize(QSize(145, 120))
        self.offsetButton.setFont(font1)
        self.offsetButton.setStyleSheet(u"")
        icon5 = QIcon()
        icon5.addFile(u"images/white/ISO_7000_-_Ref-No_1015.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.offsetButton.setIcon(icon5)
        self.offsetButton.setIconSize(QSize(80, 80))
        self.offsetButton.setCheckable(True)
        self.offsetButton.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        self.leftGrid.addWidget(self.offsetButton, 1, 2, 1, 1)

        self.retForButton = QToolButton(self.layoutWidget_9)
        self.retForButton.setObjectName(u"retForButton")
        self.retForButton.setMinimumSize(QSize(132, 120))
        self.retForButton.setMaximumSize(QSize(145, 120))
        self.retForButton.setFont(font1)
        self.retForButton.setStyleSheet(u"")
        icon6 = QIcon()
        icon6.addFile(u"images/white/ISO_7000_-_Ref-No_0997.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.retForButton.setIcon(icon6)
        self.retForButton.setIconSize(QSize(80, 80))
        self.retForButton.setCheckable(True)
        self.retForButton.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        self.leftGrid.addWidget(self.retForButton, 3, 0, 1, 1)

        self.retRevButton = QToolButton(self.layoutWidget_9)
        self.retRevButton.setObjectName(u"retRevButton")
        self.retRevButton.setMinimumSize(QSize(132, 120))
        self.retRevButton.setMaximumSize(QSize(145, 120))
        self.retRevButton.setFont(font1)
        self.retRevButton.setStyleSheet(u"")
        icon7 = QIcon()
        icon7.addFile(u"images/white/ISO_7000_-_Ref-No_0998.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.retRevButton.setIcon(icon7)
        self.retRevButton.setIconSize(QSize(80, 80))
        self.retRevButton.setCheckable(True)
        self.retRevButton.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        self.leftGrid.addWidget(self.retRevButton, 3, 4, 1, 1)

        self.cycleStopButton = QToolButton(self.layoutWidget_9)
        self.cycleStopButton.setObjectName(u"cycleStopButton")
        self.cycleStopButton.setMinimumSize(QSize(140, 120))
        self.cycleStopButton.setMaximumSize(QSize(145, 120))
        self.cycleStopButton.setFont(font1)
        self.cycleStopButton.setStyleSheet(u"")
        icon8 = QIcon()
        icon8.addFile(u"images/white/IEC_60417_-_Ref-No_5110A.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.cycleStopButton.setIcon(icon8)
        self.cycleStopButton.setIconSize(QSize(80, 80))
        self.cycleStopButton.setCheckable(True)
        self.cycleStopButton.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        self.leftGrid.addWidget(self.cycleStopButton, 5, 4, 1, 1)

        self.triangle = QLabel(self.leftFrame)
        self.triangle.setObjectName(u"triangle")
        self.triangle.setGeometry(QRect(-10, 440, 31, 41))
        self.triangle.setPixmap(QPixmap(u"images/white/arrow-right.png"))
        self.triangle.setScaledContents(True)
        self.jogButton = QToolButton(self.centralwidget)
        self.jogButton.setObjectName(u"jogButton")
        self.jogButton.setGeometry(QRect(520, 550, 151, 90))
        self.jogButton.setFont(font1)
        self.jogButton.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.jogButton.setStyleSheet(u"QToolButton{\n"
"color: rgb(255,255,255);\n"
"border-radius:0px;\n"
"background-color: rgb(57, 75, 101);\n"
"}")
        icon9 = QIcon()
        icon9.addFile(u"images/white/ISO_7000_-_Ref-No_0259.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.jogButton.setIcon(icon9)
        self.jogButton.setIconSize(QSize(48, 48))
        self.jogButton.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
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
        self.rightFrame.setFrameShape(QFrame.Shape.Box)
        self.rightFrame.setFrameShadow(QFrame.Shadow.Sunken)
        self.layoutWidget_8 = QWidget(self.rightFrame)
        self.layoutWidget_8.setObjectName(u"layoutWidget_8")
        self.layoutWidget_8.setGeometry(QRect(10, 10, 161, 581))
        self.rightGrid = QGridLayout(self.layoutWidget_8)
        self.rightGrid.setObjectName(u"rightGrid")
        self.rightGrid.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.rightGrid.setContentsMargins(6, 6, 6, 6)
        self.verticalSpacer_20 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.rightGrid.addItem(self.verticalSpacer_20, 6, 0, 1, 1)

        self.laserOnButton = QToolButton(self.layoutWidget_8)
        self.laserOnButton.setObjectName(u"laserOnButton")
        self.laserOnButton.setMinimumSize(QSize(140, 120))
        self.laserOnButton.setMaximumSize(QSize(145, 120))
        self.laserOnButton.setFont(font1)
        self.laserOnButton.setStyleSheet(u"QToolButton:checked {\n"
"	color: rgb(255,255,255);\n"
"  	background-color: rgb(126, 147, 181);   \n"
"   border-radius:10px;\n"
"}")
        icon10 = QIcon()
        icon10.addFile(u"images/white/ISO_7000_-_Ref-No_1330.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.laserOnButton.setIcon(icon10)
        self.laserOnButton.setIconSize(QSize(80, 80))
        self.laserOnButton.setCheckable(True)
        self.laserOnButton.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        self.rightGrid.addWidget(self.laserOnButton, 2, 0, 1, 1)

        self.verticalSpacer_19 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.rightGrid.addItem(self.verticalSpacer_19, 3, 0, 1, 1)

        self.verticalSpacer_5 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.rightGrid.addItem(self.verticalSpacer_5, 1, 0, 1, 1)

        self.resoLable = QLabel(self.layoutWidget_8)
        self.resoLable.setObjectName(u"resoLable")
        self.resoLable.setMinimumSize(QSize(20, 40))
        font2 = QFont()
        font2.setFamilies([u"Ubuntu"])
        font2.setPointSize(16)
        font2.setBold(True)
        font2.setItalic(False)
        self.resoLable.setFont(font2)
        self.resoLable.setStyleSheet(u"color:rgb(255,255,255);\n"
"")
        self.resoLable.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.rightGrid.addWidget(self.resoLable, 0, 0, 1, 1)

        self.laserReadyLed = QToolButton(self.layoutWidget_8)
        self.laserReadyLed.setObjectName(u"laserReadyLed")
        self.laserReadyLed.setMinimumSize(QSize(140, 120))
        self.laserReadyLed.setMaximumSize(QSize(145, 120))
        self.laserReadyLed.setFont(font1)
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
        self.laserReadyLed.setIcon(icon10)
        self.laserReadyLed.setIconSize(QSize(80, 80))
        self.laserReadyLed.setCheckable(True)
        self.laserReadyLed.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        self.rightGrid.addWidget(self.laserReadyLed, 4, 0, 1, 1)

        self.midFrame = QFrame(self.centralwidget)
        self.midFrame.setObjectName(u"midFrame")
        self.midFrame.setGeometry(QRect(1440, 40, 180, 600))
        self.midFrame.setFrameShape(QFrame.Shape.Box)
        self.midFrame.setFrameShadow(QFrame.Shadow.Sunken)
        self.layoutWidget_6 = QWidget(self.midFrame)
        self.layoutWidget_6.setObjectName(u"layoutWidget_6")
        self.layoutWidget_6.setGeometry(QRect(10, 10, 161, 581))
        self.midgrid = QGridLayout(self.layoutWidget_6)
        self.midgrid.setObjectName(u"midgrid")
        self.midgrid.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.midgrid.setContentsMargins(6, 6, 6, 6)
        self.almOvrButton = QToolButton(self.layoutWidget_6)
        self.almOvrButton.setObjectName(u"almOvrButton")
        self.almOvrButton.setMinimumSize(QSize(140, 120))
        self.almOvrButton.setMaximumSize(QSize(145, 120))
        self.almOvrButton.setFont(font1)
        self.almOvrButton.setStyleSheet(u"")
        icon11 = QIcon()
        icon11.addFile(u"images/white/IEC_60417_-_Ref-No_5319.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.almOvrButton.setIcon(icon11)
        self.almOvrButton.setIconSize(QSize(80, 80))
        self.almOvrButton.setCheckable(True)
        self.almOvrButton.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        self.midgrid.addWidget(self.almOvrButton, 4, 0, 1, 1)

        self.servoEnableButton = QToolButton(self.layoutWidget_6)
        self.servoEnableButton.setObjectName(u"servoEnableButton")
        self.servoEnableButton.setMinimumSize(QSize(140, 120))
        self.servoEnableButton.setMaximumSize(QSize(145, 120))
        self.servoEnableButton.setFont(font1)
        self.servoEnableButton.setStyleSheet(u"")
        icon12 = QIcon()
        icon12.addFile(u"images/white/IEC_60417_-_Ref-No_5010.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.servoEnableButton.setIcon(icon12)
        self.servoEnableButton.setIconSize(QSize(80, 80))
        self.servoEnableButton.setCheckable(True)
        self.servoEnableButton.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        self.midgrid.addWidget(self.servoEnableButton, 2, 0, 1, 1)

        self.verticalSpacer_14 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.midgrid.addItem(self.verticalSpacer_14, 8, 0, 1, 1)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.midgrid.addItem(self.verticalSpacer_3, 0, 0, 1, 1)

        self.verticalSpacer_12 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.midgrid.addItem(self.verticalSpacer_12, 5, 0, 1, 1)

        self.verticalSpacer_13 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.midgrid.addItem(self.verticalSpacer_13, 3, 0, 1, 1)

        self.almRstButton = QToolButton(self.layoutWidget_6)
        self.almRstButton.setObjectName(u"almRstButton")
        self.almRstButton.setMinimumSize(QSize(140, 120))
        self.almRstButton.setMaximumSize(QSize(145, 120))
        self.almRstButton.setFont(font1)
        self.almRstButton.setStyleSheet(u"")
        icon13 = QIcon()
        icon13.addFile(u"images/white/ISO_7000_-_Ref-No_1027.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.almRstButton.setIcon(icon13)
        self.almRstButton.setIconSize(QSize(80, 80))
        self.almRstButton.setCheckable(True)
        self.almRstButton.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        self.midgrid.addWidget(self.almRstButton, 7, 0, 1, 1)

        self.gridLayoutWidget = QWidget(self.centralwidget)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(0, 0, 171, 51))
        self.langGrid_2 = QGridLayout(self.gridLayoutWidget)
        self.langGrid_2.setObjectName(u"langGrid_2")
        self.langGrid_2.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)
        self.langGrid_2.setHorizontalSpacing(10)
        self.langGrid_2.setVerticalSpacing(6)
        self.langGrid_2.setContentsMargins(6, 6, 6, 6)
        self.lanEngBtn = QRadioButton(self.gridLayoutWidget)
        self.lanEngBtn.setObjectName(u"lanEngBtn")
        self.lanEngBtn.setMaximumSize(QSize(16777215, 16777215))
        font3 = QFont()
        font3.setPointSize(11)
        font3.setBold(True)
        self.lanEngBtn.setFont(font3)
        self.lanEngBtn.setStyleSheet(u"QRadioButton {\n"
"    color: #ffffff;\n"
"    padding: 10px;\n"
"    background-color: transparent;\n"
"    border: none;\n"
"}\n"
"\n"
"QRadioButton::indicator {\n"
"    width: 10px;\n"
"    height: 10px; \n"
"    border: 2px solid #4CAF50; \n"
"    border-radius: 7px;\n"
"    background-color: transparent; \n"
"}\n"
"\n"
"QRadioButton::indicator:checked {\n"
"    background-color: #0BDA51; \n"
"    border: 2px solid #4CAF50; \n"
"	\n"
"}\n"
"")
        self.lanEngBtn.setChecked(True)

        self.langGrid_2.addWidget(self.lanEngBtn, 0, 0, 1, 1)

        self.lanJapBtn = QRadioButton(self.gridLayoutWidget)
        self.lanJapBtn.setObjectName(u"lanJapBtn")
        self.lanJapBtn.setMinimumSize(QSize(0, 0))
        self.lanJapBtn.setMaximumSize(QSize(16777215, 16777215))
        font4 = QFont()
        font4.setPointSize(11)
        font4.setBold(True)
        self.lanJapBtn.setFont(font4)
        self.lanJapBtn.setStyleSheet(u"QRadioButton {\n"
"    color: #ffffff;\n"
"    padding: 10px;\n"
"    background-color: transparent;\n"
"    border: none;\n"
"}\n"
"\n"
"QRadioButton::indicator {\n"
"    width: 10px;\n"
"    height: 10px; \n"
"    border: 2px solid #4CAF50; \n"
"    border-radius: 7px;\n"
"    background-color: transparent; \n"
"}\n"
"\n"
"QRadioButton::indicator:checked {\n"
"    background-color: #0BDA51; \n"
"    border: 2px solid #4CAF50; \n"
"	\n"
"}\n"
"\n"
"\n"
"")

        self.langGrid_2.addWidget(self.lanJapBtn, 0, 1, 1, 1)

        self.label.raise_()
        self.machineLable.raise_()
        self.leftFrame.raise_()
        self.jogButton.raise_()
        self.logoLable.raise_()
        self.autoButton.raise_()
        self.rightFrame.raise_()
        self.midFrame.raise_()
        self.gridLayoutWidget.raise_()

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Machine Control Panel", None))
        self.label.setText("")
        self.machineLable.setText("")
        self.autoButton.setText(QCoreApplication.translate("MainWindow", u"AUTO", None))
        self.prcEndButton.setText(QCoreApplication.translate("MainWindow", u"PIERCING", None))
        self.zLockButton.setText(QCoreApplication.translate("MainWindow", u"Z-AXIS", None))
        self.cycleStartButton.setText(QCoreApplication.translate("MainWindow", u"START", None))
        self.dryRunButton.setText(QCoreApplication.translate("MainWindow", u"DRY RUN", None))
        self.offsetButton.setText(QCoreApplication.translate("MainWindow", u"OFFSETS", None))
        self.retForButton.setText(QCoreApplication.translate("MainWindow", u"RETRACE", None))
        self.retRevButton.setText(QCoreApplication.translate("MainWindow", u"RETRACE", None))
        self.cycleStopButton.setText(QCoreApplication.translate("MainWindow", u"STOP", None))
        self.triangle.setText("")
        self.jogButton.setText(QCoreApplication.translate("MainWindow", u"JOG", None))
        self.logoLable.setText("")
        self.laserOnButton.setText(QCoreApplication.translate("MainWindow", u"ON", None))
        self.resoLable.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-weight:700;\">RESONATOR</span></p></body></html>", None))
        self.laserReadyLed.setText(QCoreApplication.translate("MainWindow", u"READY", None))
        self.almOvrButton.setText(QCoreApplication.translate("MainWindow", u"OVERRIDE", None))
        self.servoEnableButton.setText(QCoreApplication.translate("MainWindow", u"SERVO", None))
        self.almRstButton.setText(QCoreApplication.translate("MainWindow", u"RESET", None))
        self.lanEngBtn.setText(QCoreApplication.translate("MainWindow", u"EN", None))
        self.lanJapBtn.setText(QCoreApplication.translate("MainWindow", u"JA", None))
    # retranslateUi

