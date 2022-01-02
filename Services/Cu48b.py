#!/usr/bin/python3
import serial, threading

class Cu48b:

    ADDRESS_ALL = 0x0A
    LOCKER_ALL = 0x30
    GET_STATUS = 0x60
    LOCKER_UNLOCK = 0x61
    LOCKER_STATUS = 0x75
    
    lockers = []
    sensors = []

    serialPort = None
    baudrate = None
    port = None

    bytesToRead = 18
    dataOut = []
    dataIn = []

    timeout = 1

    def __init__(self,  port, baudrate, callback):
        self.port = port
        self.baudrate = baudrate
        self.onDataReceived = callback

    def open(self):
        try:
            self.serialPort = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=self.timeout,
                write_timeout=self.timeout,
                inter_byte_timeout=None,
                xonxoff=False,
                rtscts=True,
                dsrdtr=True
            )

        except Exception as e:
            print(e)
            self.close()

    def read(self):
        if ((not self.serialPort == None) and self.serialPort.isOpen()):
            dataIn = self.serialPort.read(self.bytesToRead)
            self.dataIn = list(dataIn)
            if (len(self.dataIn) > 0): self.parse()
            if (self.onDataReceived == callable):
                self.onDataReceived(self.lockers, self.sensors)

    def send (self, address, lockerNumber, dataOut):
        self.dataOut = [ 
            0x02,
            address,
            lockerNumber,
            dataOut,
            0x03,
            0x00
        ]
        self.dataOut[5] = self.checkSum(self.dataOut)

        if (self.serialPort.isOpen()):
            self.serialPort.write(bytes(self.dataOut))

    def parse(self):
        if (self.dataIn == None) : raise Exception("Data is null")
        if (len(self.dataIn) < self.bytesToRead): raise Exception("Data is short")

        cloned = self.dataIn.copy()
        prevCheckSum = cloned[17]
        cloned[17] = 0x00

        currentCheckSum = self.checkSum(cloned)
        if not (prevCheckSum == currentCheckSum): raise Exception("CheckSum is wrong")

        if not (self.dataIn[3] == 0x75): raise Exception("Wrong command")

        self.lockers = [
            self.dataIn[4],
            self.dataIn[5],
            self.dataIn[6],
            self.dataIn[7],
            self.dataIn[8],
            self.dataIn[9],
        ]

        self.sensors = [
            self.dataIn[10],
            self.dataIn[11],
            self.dataIn[12],
            self.dataIn[13],
            self.dataIn[14],
            self.dataIn[15],
        ]
        
        if not self.onDataReceived == None:
            self.onDataReceived(self.lockers, self.sensors)

    def close(self):
        if self.serialPort.isOpen(): self.serialPort.close()

    def checkSum(self, datas):
        sum = 0
        for data in bytes(datas):
            sum = sum + data
        return (sum & 0xFF)

    def __del__(self):
        self.isThread = False

if (__name__ == "__main__"):
    cu48b = Cu48b("COM3", 19200, None)
    cu48b.open()
    # unlock-all
    # cu48b.send(0, Cu48b.LOCKER_ALL, Cu48b.LOCKER_UNLOCK)
    # get-status-all
    cu48b.send(0, Cu48b.LOCKER_ALL, Cu48b.GET_STATUS)
    # unlock-specific
    # cu48b.send(0, 0, Cu48b.LOCKER_UNLOCK)
    cu48b.read()
    print("lockers:", cu48b.lockers)
    print("sensors:", cu48b.sensors)
    cu48b.close()