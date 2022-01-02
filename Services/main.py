#!/usr/bin/python3

from serial.tools.list_ports import comports
from Cu48b import Cu48b

portName = "COM3"
baudrate = 19200
cu48b = None


def cbStatus(lockers, sensors):
    print("lockers:", lockers)
    print("sensors:", sensors)

  
def main():
    getStatus()


def getStatus():
    cu48b = Cu48b(portName, baudrate, cbStatus)
    cu48b.open()
    cu48b.send(0, Cu48b.LOCKER_ALL, Cu48b.GET_STATUS)
    cu48b.read()
    cu48b.close()

def setLock():
    cu48b = Cu48b(portName, baudrate, None)
    cu48b.open()
    cu48b.send(0, 0, Cu48b.LOCKER_UNLOCK)
    cu48b.close()

def unlockAll():
    cu48b = Cu48b(portName, baudrate, None)
    cu48b.open()
    cu48b.send(0, Cu48b.LOCKER_ALL, Cu48b.LOCKER_UNLOCK)
    cu48b.close()

def getAvailablePorts():
    ports = []
    for port, desc, hwid in sorted(comports()):
        ports.append(port)
    return ports



try:
    main()
except Exception as exception:
    print(exception)