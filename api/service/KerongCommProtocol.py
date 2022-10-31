#!/usr/bin/python3
import serial


class KerongCommProtocol:
    ADDRESS_ALL = 0x0A
    LOCKER_ALL = 0x30
    GET_STATUS = 0x60
    LOCKER_UNLOCK = 0x61
    LOCKER_STATUS = 0x75

    lockers = []
    sensors = []

    serial_port = None
    baudrate = None
    port = None

    bytesToRead = 18
    data_out = []
    data_in = []

    timeout = 1

    def __init__(self, port, baudrate, callback):
        self.port = port
        self.baudrate = baudrate
        self.on_data_received = callback

    def open(self):
        try:
            self.serial_port = serial.Serial(
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
        try:
            if (self.serial_port is not None) and self.serial_port.isOpen():
                dataIn = self.serial_port.read(self.bytesToRead)
                self.data_in = list(dataIn)
                if len(self.data_in) > 0:
                    self.parse()
                if self.on_data_received == callable:
                    self.on_data_received(self.lockers, self.sensors)
        except Exception as e:
                print(e)
                self.close()
                    
    def send(self, address, locker_number, data_out):
        try:
            self.data_out = [
                0x02,
                address,
                locker_number,
                data_out,
                0x03,
                0x00
            ]
            self.data_out[5] = KerongCommProtocol.checkSum(self.data_out)

            if self.serial_port:
                if self.serial_port.isOpen():
                    self.serial_port.write(bytes(self.data_out))
        except Exception as e:
            print(e)
            self.close()

    def parse(self):
        try:
            if self.data_in is None:
                raise Exception("Data is null")
            if len(self.data_in) < self.bytesToRead:
                raise Exception("Data is short")

            cloned = self.data_in.copy()
            prevCheckSum = cloned[17]
            cloned[17] = 0x00

            currentCheckSum = KerongCommProtocol.checkSum(cloned)
            if not (prevCheckSum == currentCheckSum):
                raise Exception("CheckSum is wrong")

            if not (self.data_in[3] == 0x75):
                raise Exception("Wrong command")

            self.lockers = []
            self.sensors = []

            for index in range(4,10):
                for digit in range(8): 
                    bit = (int(self.data_in[index]) >> digit) & 0x01
                    self.lockers.append(bit)

            for index in range(10,16):
                for digit in range(8):
                    bit = (int(self.data_in[index]) >> digit) & 0x01
                    self.sensors.append(bit)
        

            # self.lockers = [
            #     self.data_in[4],
            #     self.data_in[5],
            #     self.data_in[6],
            #     self.data_in[7],
            #     self.data_in[8],
            #     self.data_in[9],
            # ]

            # self.sensors = [
            #     self.data_in[10],
            #     self.data_in[11],
            #     self.data_in[12],
            #     self.data_in[13],
            #     self.data_in[14],
            #     self.data_in[15],
            # ]

            if self.on_data_received is not None:
                self.on_data_received(self.lockers, self.sensors)
        
        except Exception as e:
            print(e)
            self.close()

    def close(self):
        if self.serial_port:
            if self.serial_port.isOpen():
                self.serial_port.close()

    @staticmethod
    def checkSum(datas):
        check_sum = 0
        for data in bytes(datas):
            check_sum = check_sum + data
        return check_sum & 0xFF

    def __del__(self):
        self.isThread = False


if __name__ == "__main__":
    # cu48b = KerongCommProtocol("COM3", 19200, None)
    cu48b = KerongCommProtocol("/dev/cu.usbserial-A10LG0Y1", 19200, None)
    cu48b.open()
    # unlock-all
    # cu48b.send(0, KerongCommProtocol.LOCKER_ALL, KerongCommProtocol.LOCKER_UNLOCK)
    # get-status-all
    # cu48b.send(0, KerongCommProtocol.LOCKER_ALL, KerongCommProtocol.GET_STATUS)
    # unlock-specific
    cu48b.send(0, 4, KerongCommProtocol.LOCKER_UNLOCK)
    cu48b.read()
    print("lockers:", cu48b.lockers)
    print("sensors:", cu48b.sensors)
    cu48b.close()
