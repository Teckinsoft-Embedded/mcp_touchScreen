#structure modified and current working code version05.02.2025
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtWidgets, QtCore , QtGui
from PyQt5.QtCore import Qt, QThread, pyqtSlot
from PyQt5.QtGui import QCursor
import ctypes
import sys
import time
import psutil
import threading
import os
from ctypes import c_uint32
from Ethercat import EtherCATInterface
from home import Ui_MainWindow
from gpio import GPIOControl


#Constants for button presses as bitwise value
ALL_BUTTONS_RELEASED = 0
CYCLE_START = 1 << 0
CYCLE_STOP = 1 << 1
DRV = 1 << 2
JOG = 1 << 3
X = 1 << 4
PLUS = 1 << 5
Z_LOCK = 1 << 6
MDI = 1 << 7
Y = 1 << 8
VVV = 1 << 9
DRY_RUN = 1 << 10
AUTO = 1 << 11
Z = 1 << 12
MINUS = 1 << 13
NC_REF = 1 << 14
NC_OFFSET = 1 << 15
RET_FOR = 1 << 16
RET_REV = 1 << 17
PRC_END = 1 << 18
ALM_OVR = 1 << 19
ALM_RST = 1 << 20
LOCK_RST = 1 << 21
LASER_ON = 1 << 22

etc_out = c_uint32(0)

#-----------------------------------Ethercat Thread-----------------------------------
class EtherCATThread(QThread):
    # Define a signal to send the etc_out value to the main thread
    data_ready = QtCore.pyqtSignal(int)
    gpio_data = QtCore.pyqtSignal(int)

    def __init__(self, cpu_core=[0, 1, 2], parent=None):
        super().__init__(parent)
        self.etc_interface = EtherCATInterface()
        self.etc_init_ok = False
        self.shared_lock = threading.Lock()  # Lock for thread-safe updates
        self.cpu_core = cpu_core  # Assign CPU core for affinity
        self.gpio_ctrl = GPIOControl()

    def run(self):
       
        try:
            pid = os.getpid()  # Get process ID
            process = psutil.Process(pid)  # Get process object
            process.cpu_affinity(int [self.cpu_core])  # Set affinity to selected core
            print(f"EtherCAT Thread running on CPU {self.cpu_core}")
        except Exception as e:
            print(f"Error setting CPU affinity: {e}")        
        self.etc_init_ok = self.etc_interface.etc_init()
        etc_out_value = 0
        pre_etc_out_value = 0
        etc_out_gpio_value =0
        pre_etc_out_gpio_value = 0
        while True:
            if self.etc_init_ok:
                with self.shared_lock:
                    gpio_value = (self.gpio_ctrl.gpio_input_scan() & 0xFF) << 24
                    button_value = self.etc_interface.Etc_Buffer_In.LANLong[0] & 0x00FFFFFF
                    self.etc_interface.Etc_Buffer_In.LANLong[0] =  button_value | gpio_value
                    self.etc_interface.etc_scan()
                    etc_out_value = self.etc_interface.Etc_Buffer_Out.LANLong[0]
                    etc_out_gpio_value = (self.etc_interface.Etc_Buffer_Out.LANLong[0] >> 24) & 0xFF
                if etc_out_value != pre_etc_out_value:
                    self.data_ready.emit(etc_out_value)
                if etc_out_gpio_value != pre_etc_out_gpio_value:
                    self.gpio_data.emit(etc_out_gpio_value)                           
            else:
                self.etc_init_ok = self.etc_interface.etc_init()               
            pre_etc_out_value = etc_out_value
            pre_etc_out_gpio_value = etc_out_gpio_value                
            time.sleep(0.20)  

# region----------------------------Main Thread-----------------------------------
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setCursor(QCursor(Qt.BlankCursor))
        self.ethercatThread = EtherCATThread()
        self.shared_lock = threading.Lock()
        self.etc_interface = EtherCATInterface()
        self.gpio_ctrl = GPIOControl()
        
        self.ethercatThread.data_ready.connect(self.update_ui)
        self.ethercatThread.gpio_data.connect(self.gpio_ctrl.gpio_output_control)
        self.ethercatThread.start()
        
        self.init_buttons()
    
    def init_buttons(self):
        # Connect button signals to functions when button pressed
        self.ui.cycleStartButton.pressed.connect(lambda: self.handle_button_pressed(CYCLE_START))
        self.ui.cycleStopButton.pressed.connect(lambda: self.handle_button_pressed(CYCLE_STOP))
        self.ui.drvButton.pressed.connect(lambda: self.handle_button_pressed(DRV))
        self.ui.zLockButton.pressed.connect(lambda: self.handle_button_pressed(Z_LOCK))
        self.ui.dryRunButton.pressed.connect(lambda: self.handle_button_pressed(DRY_RUN))
        self.ui.jogButton.pressed.connect(lambda: self.handle_button_pressed(JOG))
        self.ui.mdiButton.pressed.connect(lambda: self.handle_button_pressed(MDI))
        self.ui.autoButton.pressed.connect(lambda: self.handle_button_pressed(AUTO))
        self.ui.xButton.pressed.connect(lambda: self.handle_button_pressed(X))
        self.ui.yButton.pressed.connect(lambda: self.handle_button_pressed(Y))
        self.ui.zButton.pressed.connect(lambda: self.handle_button_pressed(Z))
        self.ui.plusButton.pressed.connect(lambda: self.handle_button_pressed(PLUS))
        self.ui.vvvButton.pressed.connect(lambda: self.handle_button_pressed(VVV))
        self.ui.minusButton.pressed.connect(lambda: self.handle_button_pressed(MINUS))
        self.ui.ncRefButton.pressed.connect(lambda: self.handle_button_pressed(NC_REF))
        self.ui.ncOffsetButton.pressed.connect(lambda: self.handle_button_pressed(NC_OFFSET))
        self.ui.retForButton.pressed.connect(lambda: self.handle_button_pressed(RET_FOR))
        self.ui.retRevButton.pressed.connect(lambda: self.handle_button_pressed(RET_REV))
        self.ui.prcEndButton.pressed.connect(lambda: self.handle_button_pressed(PRC_END))
        self.ui.almOvrButton.pressed.connect(lambda: self.handle_button_pressed(ALM_OVR))
        self.ui.almRstButton.pressed.connect(lambda: self.handle_button_pressed(ALM_RST))
        self.ui.lockRstButton.pressed.connect(lambda: self.handle_button_pressed(LOCK_RST))
        self.ui.laserOnButton.toggled.connect(lambda checked: self.on_laserOnButton_toggled(checked))

        # Connect button signals to functions when button released
        self.ui.cycleStartButton.released.connect(lambda: self.handle_button_released(CYCLE_START))
        self.ui.cycleStopButton.released.connect(lambda: self.handle_button_released(CYCLE_STOP))
        self.ui.drvButton.released.connect(lambda: self.handle_button_released(DRV))
        self.ui.zLockButton.released.connect(lambda: self.handle_button_released(Z_LOCK))
        self.ui.dryRunButton.released.connect(lambda: self.handle_button_released(DRY_RUN))
        self.ui.jogButton.released.connect(lambda: self.handle_button_released(JOG))
        self.ui.mdiButton.released.connect(lambda: self.handle_button_released(MDI))
        self.ui.autoButton.released.connect(lambda: self.handle_button_released(AUTO))
        self.ui.xButton.released.connect(lambda: self.handle_button_released(X))
        self.ui.yButton.released.connect(lambda: self.handle_button_released(Y))
        self.ui.zButton.released.connect(lambda: self.handle_button_released(Z))
        self.ui.plusButton.released.connect(lambda: self.handle_button_released(PLUS))
        self.ui.vvvButton.released.connect(lambda: self.handle_button_released(VVV))
        self.ui.minusButton.released.connect(lambda: self.handle_button_released(MINUS))
        self.ui.ncRefButton.released.connect(lambda: self.handle_button_released(NC_REF))
        self.ui.ncOffsetButton.released.connect(lambda: self.handle_button_released(NC_OFFSET))
        self.ui.retForButton.released.connect(lambda: self.handle_button_released(RET_FOR))
        self.ui.retRevButton.released.connect(lambda: self.handle_button_released(RET_REV))
        self.ui.prcEndButton.released.connect(lambda: self.handle_button_released(PRC_END))
        self.ui.almOvrButton.released.connect(lambda: self.handle_button_released(ALM_OVR))
        self.ui.almRstButton.released.connect(lambda: self.handle_button_released(ALM_RST))
        self.ui.lockRstButton.released.connect(lambda: self.handle_button_released(LOCK_RST))


    @pyqtSlot(int)
    def handle_button_pressed(self, button_value):
       # print(f"Button Pressed: {button_value}")
        with self.shared_lock:
            self.ethercatThread.etc_interface.Etc_Buffer_In.LANLong[0] |= button_value
            #self.etc_interface.etc_scan()
        
    @pyqtSlot()
    def handle_button_released(self, button_value):
        # print("Button Released")
        with self.shared_lock:
            self.ethercatThread.etc_interface.Etc_Buffer_In.LANLong[0] &= ~button_value
            #self.etc_interface.etc_scan()

    @pyqtSlot()
    def on_laserOnButton_toggled(self, checked):
        if checked:
            #print("laser on")
            self.ui.laserOnButton.setStyleSheet("background-color: rgb(250, 122, 72);color: rgb(48, 48, 48); border-radius: 0px")
            with self.shared_lock:
                self.ethercatThread.etc_interface.Etc_Buffer_In.LANLong[0] |= LASER_ON
                #self.etc_interface.etc_scan()            
        else:
            #print("laser off")
            self.ui.laserOnButton.setStyleSheet("background-color: rgb(96, 96, 96);color: rgb(48, 48, 48);")
            with self.shared_lock:
                self.ethercatThread.etc_interface.Etc_Buffer_In.LANLong[0] &= ~LASER_ON
                #self.etc_interface.etc_scan()
    
    # Connect the EtherCAT thread signal to update UI elements
    @pyqtSlot(int)
    def update_ui(self, etc_out_value):
        if etc_out_value & (1 << 0):
            self.ui.cycleStartButton.setStyleSheet("background-color: rgb(250, 122, 72); color: rgb(48, 48, 48); border-radius: 0px")
        else:
            self.ui.cycleStartButton.setStyleSheet("background-color: rgb(96, 96, 96); color: rgb(48, 48, 48);")
            
        if etc_out_value & (1 << 1):
            self.ui.cycleStopButton.setStyleSheet("background-color: rgb(250, 122, 72); color: rgb(48, 48, 48); border-radius: 0px")
        else:
            self.ui.cycleStopButton.setStyleSheet("background-color: rgb(96, 96, 96); color: rgb(48, 48, 48);")

        if etc_out_value & (1 << 2):
            self.ui.drvButton.setStyleSheet("background-color: rgb(250, 122, 72); color: rgb(48, 48, 48); border-radius: 65px")
        else:
            self.ui.drvButton.setStyleSheet("background-color: rgb(96, 96, 96); color: rgb(48, 48, 48);")

        if etc_out_value & (1 << 3):
            self.ui.jogButton.setStyleSheet("background-color: rgb(250, 122, 72); color: rgb(48, 48, 48); border-radius: 65px")
        else:
            self.ui.jogButton.setStyleSheet("background-color: rgb(96, 96, 96); color: rgb(48, 48, 48); ")

        if etc_out_value & (1 << 4):
            self.ui.xButton.setStyleSheet("background-color: rgb(250, 122, 72); color: rgb(48, 48, 48); border-radius: 65px")
        else:
            self.ui.xButton.setStyleSheet("background-color: rgb(96, 96, 96); color: rgb(48, 48, 48); ")

        if etc_out_value & (1 << 5):
            self.ui.plusButton.setStyleSheet("background-color: rgb(250, 122, 72); color: rgb(48, 48, 48); border-radius: 65px")
        else:
            self.ui.plusButton.setStyleSheet("background-color: rgb(96, 96, 96); color: rgb(48, 48, 48); ")

        if etc_out_value & (1 << 6):
            self.ui.zLockButton.setStyleSheet("background-color: rgb(250, 122, 72); color: rgb(48, 48, 48); border-radius: 65px")
        else:
            self.ui.zLockButton.setStyleSheet("background-color: rgb(96, 96, 96); color: rgb(48, 48, 48); ")
   
        if etc_out_value & (1 << 7):
            self.ui.mdiButton.setStyleSheet("background-color: rgb(250, 122, 72); color: rgb(48, 48, 48); border-radius: 65px")
        else:
            self.ui.mdiButton.setStyleSheet("background-color: rgb(96, 96, 96); color: rgb(48, 48, 48); ")

        if etc_out_value & (1 << 8):
            self.ui.yButton.setStyleSheet("background-color: rgb(250, 122, 72); color: rgb(48, 48, 48); border-radius: 65px")
        else:
            self.ui.yButton.setStyleSheet("background-color: rgb(96, 96, 96); color: rgb(48, 48, 48); ")
      
        if etc_out_value & (1 << 9):
            self.ui.vvvButton.setStyleSheet("background-color: rgb(250, 122, 72); color: rgb(48, 48, 48); border-radius: 65px")
        else:
            self.ui.vvvButton.setStyleSheet("background-color: rgb(96, 96, 96); color: rgb(48, 48, 48); ")
       
        if etc_out_value & (1 << 10):
            self.ui.dryRunButton.setStyleSheet("background-color: rgb(250, 122, 72); color: rgb(48, 48, 48); border-radius: 65px")
        else:
            self.ui.dryRunButton.setStyleSheet("background-color: rgb(96, 96, 96); color: rgb(48, 48, 48); ")
       
        if etc_out_value & (1 << 11):
            self.ui.autoButton.setStyleSheet("background-color: rgb(250, 122, 72); color: rgb(48, 48, 48); border-radius: 65px")
        else:
            self.ui.autoButton.setStyleSheet("background-color: rgb(96, 96, 96); color: rgb(48, 48, 48); ")

        if etc_out_value & (1 << 12):
            self.ui.zButton.setStyleSheet("background-color: rgb(250, 122, 72); color: rgb(48, 48, 48); border-radius: 65px")
        else:
            self.ui.zButton.setStyleSheet("background-color: rgb(96, 96, 96); color: rgb(48, 48, 48); ")

        if etc_out_value & (1 << 13):
            self.ui.minusButton.setStyleSheet("background-color: rgb(250, 122, 72); color: rgb(48, 48, 48); border-radius: 65px")
        else:
            self.ui.minusButton.setStyleSheet("background-color: rgb(96, 96, 96); color: rgb(48, 48, 48); ")

        if etc_out_value & (1 << 14):
            self.ui.ncRefButton.setStyleSheet("background-color: rgb(250, 122, 72); color: rgb(48, 48, 48); border-radius: 65px")
        else:
            self.ui.ncRefButton.setStyleSheet("background-color: rgb(96, 96, 96); color: rgb(48, 48, 48); ")

        if etc_out_value & (1 << 15):
            self.ui.ncOffsetButton.setStyleSheet("background-color: rgb(250, 122, 72); color: rgb(48, 48, 48); border-radius: 65px")
        else:
            self.ui.ncOffsetButton.setStyleSheet("background-color: rgb(96, 96, 96); color: rgb(48, 48, 48); ")

        if etc_out_value & (1 << 16):
            self.ui.retForButton.setStyleSheet("background-color: rgb(250, 122, 72); color: rgb(48, 48, 48); border-radius: 65px")
        else:
            self.ui.retForButton.setStyleSheet("background-color: rgb(96, 96, 96); color: rgb(48, 48, 48);")
      
        if etc_out_value & (1 << 17):
            self.ui.retRevButton.setStyleSheet("background-color: rgb(250, 122, 72); color: rgb(48, 48, 48); border-radius: 65px")
        else:
            self.ui.retRevButton.setStyleSheet("background-color: rgb(96, 96, 96); color: rgb(48, 48, 48);")

        if etc_out_value & (1 << 18):
            self.ui.prcEndButton.setStyleSheet("background-color: rgb(250, 122, 72); color: rgb(48, 48, 48); border-radius: 65px")
        else:
            self.ui.prcEndButton.setStyleSheet("background-color: rgb(96, 96, 96); color: rgb(48, 48, 48);")

        if etc_out_value & (1 << 19):
            self.ui.almOvrButton.setStyleSheet("background-color: rgb(250, 122, 72); color: rgb(48, 48, 48); border-radius: 65px")
        else:
            self.ui.almOvrButton.setStyleSheet("background-color: rgb(96, 96, 96); color: rgb(48, 48, 48); ")

        if etc_out_value & (1 << 20):
            self.ui.almRstButton.setStyleSheet("background-color: rgb(250, 122, 72); color: rgb(48, 48, 48); border-radius: 65px")
        else:
            self.ui.almRstButton.setStyleSheet("background-color: rgb(96, 96, 96); color: rgb(48, 48, 48); ")

        if etc_out_value & (1 << 21):
            self.ui.lockRstButton.setStyleSheet("background-color: rgb(250, 122, 72); color: rgb(48, 48, 48); border-radius: 65px")
        else:
            self.ui.lockRstButton.setStyleSheet("background-color: rgb(96, 96, 96); color: rgb(48, 48, 48); ")

        if etc_out_value & (1 << 23):
            self.ui.laserReadyLamp.setStyleSheet("background-color: rgb(250, 122, 72); color: rgb(48, 48, 48); border-radius: 65px")
        else:
            self.ui.laserReadyLamp.setStyleSheet("background-color: rgb(96, 96, 96); color: rgb(48, 48, 48); border-radius: 65px")

 #-----------------------------------Close Event-----------------------------------
    def closeEvent(self, event):
        self.ethercat.running = False
        self.ethercatThread.quit()
        self.ethercatThread.wait()
        self.gpio_ctrl.gpio_release()
        event.accept()
# endregion

# Run the application
if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowFlags(Qt.FramelessWindowHint)
    window.showFullScreen()
    sys.exit(app.exec())
