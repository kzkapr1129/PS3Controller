#!/usr/bin/python3

"""
How to use:
Before use this class, following the procedure below
1. Connect the PS3 controller with USB
2. Type the following commands
  $ lsus
  ...
  Bus 001 Device 010: ID 054c:0268 Sony Corp. Batoh Device / PlayStation 3 Controller
  ...
  $ hcitool dev
  Devices:
    hci0  B8:27:EB:04:B1:A0
  $ sudo bluetoothctl
  [bluetooth]# discoverable on
  [bluetooth]# agent on
3. Disconnect USB
4. Push PS button for a while
5. The following outputs are shown
  [CHG] Device 60:38:0E:7D:7E:0C Connected: yes
  [CHG] Device 60:38:0E:7D:7E:0C Connected: no
  [CHG] Device 60:38:0E:7D:7E:0C Connected: yes
  [CHG] Device 60:38:0E:7D:7E:0C Connected: no
  ...
6. Type the following commands
  [bluetooth]# connect 60:38:0E:7D:7E:0C
  Device 60:38:0E:7D:7E:0C not available
  [bluetooth]# trust 60:38:0E:7D:7E:0C
  [CHG] Device 60:38:0E:7D:7E:0C Trusted: yes
  Changing 60:38:0E:7D:7E:0C trust succeeded
  [bluetooth]# quit
"""

import struct
import threading
from enum import IntEnum

class Controller:
    class ButtonType(IntEnum):
        DIGITAL = 1
        ANALOG = 2
    
    class AButton(IntEnum):
        LAXIS_LR = 0
        LAXIS_TB = 1
        L2 = 2
        RAXIS_LR = 3
        RAXIS_TB = 4
        R2 = 5
        NUM = 6
        
    class DButton(IntEnum):
        CROSS = 0
        CIRCLE = 1
        TRIANGLE = 2
        SQUARE = 3
        L1 = 4
        R1 = 5
        L2 = 6
        R2 = 7
        SELECT = 8
        START = 9
        PS = 10
        LAXIS = 11
        RAXIS = 12
        TOP = 13
        BUTTOM = 14
        LEFT = 15
        RIGHT = 16
        NUM = 17
    
    def __init__(self, device_path):
        self.device_path = device_path
        self.isDActive = [False] * int(self.DButton.NUM)
        self.analogVal = [0] * int(self.AButton.NUM)
    
    def start(self):
        self.device = open(self.device_path, "rb")
        self.thread = threading.Thread(target=self.update)
        self.running = True
        self.thread.start()
        print("started")

    def stop(self):
        self.running = False
        self.thread.join()
        self.device.close()
        print("stopped")

    def update(self):
        EVENT_FORMAT = "LhBB"
        EVENT_SIZE = struct.calcsize(EVENT_FORMAT)
        event = self.device.read(EVENT_SIZE)
        while self.running and event:
            (ds3_time, ds3_val, ds3_type, ds3_num) = struct.unpack(EVENT_FORMAT, event)
            self.updateKeyState(ds3_time, ds3_val, ds3_type, ds3_num)
            event = self.device.read(EVENT_SIZE)
        print("finished update()")

    def updateKeyState(self, ds3_time, ds3_val, ds3_type, ds3_num):
        if ds3_type == self.ButtonType.ANALOG :
            if ds3_num == self.AButton.LAXIS_LR:
                self.analogVal[self.AButton.LAXIS_LR] = ds3_val
            elif ds3_num == self.AButton.LAXIS_TB:
                self.analogVal[self.AButton.LAXIS_TB] = ds3_val
            elif ds3_num == self.AButton.L2:
                self.analogVal[self.AButton.L2] = ds3_val
            elif ds3_num == self.AButton.RAXIS_LR:
                self.analogVal[self.AButton.RAXIS_LR] = ds3_val
            elif ds3_num == self.AButton.RAXIS_TB:
                self.analogVal[self.AButton.RAXIS_TB] = ds3_val
            elif ds3_num == self.AButton.R2:
                self.analogVal[self.AButton.R2] = ds3_val
        elif ds3_type == self.ButtonType.DIGITAL:
            if ds3_num == self.DButton.CROSS:
                self.isDActive[self.DButton.CROSS] = (ds3_val != 0)
            elif ds3_num == self.DButton.CIRCLE:
                self.isDActive[self.DButton.CIRCLE] = (ds3_val != 0)
            elif ds3_num == self.DButton.TRIANGLE:
                self.isDActive[self.DButton.TRIANGLE] = (ds3_val != 0)
            elif ds3_num == self.DButton.SQUARE:
                self.isDActive[self.DButton.SQUARE] = (ds3_val != 0)
            elif ds3_num == self.DButton.L1:
                self.isDActive[self.DButton.L1] = (ds3_val != 0)
            elif ds3_num == self.DButton.R1:
                self.isDActive[self.DButton.R1] = (ds3_val != 0)
            elif ds3_num == self.DButton.L2:
                self.isDActive[self.DButton.L2] = (ds3_val != 0)
            elif ds3_num == self.DButton.R2:
                self.isDActive[self.DButton.R2] = (ds3_val != 0)
            elif ds3_num == self.DButton.SELECT:
                self.isDActive[self.DButton.SELECT] = (ds3_val != 0)
            elif ds3_num == self.DButton.START:
                self.isDActive[self.DButton.START] = (ds3_val != 0)
            elif ds3_num == self.DButton.PS:
                self.isDActive[self.DButton.PS] = (ds3_val != 0)
            elif ds3_num == self.DButton.LAXIS:
                self.isDActive[self.DButton.LAXIS] = (ds3_val != 0)
            elif ds3_num == self.DButton.RAXIS:
                self.isDActive[self.DButton.RAXIS] = (ds3_val != 0)
            elif ds3_num == self.DButton.TOP:
                self.isDActive[self.DButton.TOP] = (ds3_val != 0)
            elif ds3_num == self.DButton.BUTTOM:
                self.isDActive[self.DButton.BUTTOM] = (ds3_val != 0)
            elif ds3_num == self.DButton.LEFT:
                self.isDActive[self.DButton.LEFT] = (ds3_val != 0)
            elif ds3_num == self.DButton.RIGHT:
                self.isDActive[self.DButton.RIGHT] = (ds3_val != 0)

