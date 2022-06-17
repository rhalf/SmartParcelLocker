#!/usr/bin/python3
from serial.tools.list_ports import comports

def getAvailablePorts():
    ports = []
    for port, desc, hwid in sorted(comports()):
        ports.append(port)
    return ports

if __name__ == "__main__":
    print("List of available ports")
    print(getAvailablePorts())
