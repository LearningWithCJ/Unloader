import sys
import os
import platform
import time
import socket
import base64



IP = ""
PORT = 0
SOC = None
banner = """\033[1m\033[97m
  _    _       _                 _
 | |  | |     | |               | |
 | |  | |_ __ | | ___   __ _  __| | ___  _ __
 | |  | | '_ \| |/ _ \ / _` |/ _` |/ _ \| '__|
 | |__| | | | | | (_) | (_| | (_| |  __/| |
  \____/|_| |_|_|\___/ \__,_|\__,_|\___||_|

                               -  By CJ
"""


def stdOutPut(type, text):
    if type == "info": return "\033[0m\033[1m[\033[33mINFO\033[39m]\033[1m%s\033[0m" % text
    elif type == "error": return "\033[0m[\033[31mERROR\033[0m]\033[1m%s\033[0m" % text
    elif type == "warning": return "\033[0m[\033[33mWARNING\033[0m]\033[1m%s\033[0m" % text
    elif type == "success": return "\033[0m[\033[32mSUCCESS\033[0m]\033[1m%s\033[0m" % text


def ClearDirec():
    if (platform.system() == 'Windows'):
        clear = lambda: os.system('cls')
        direc = "\\"
    else:
        clear = lambda: os.system('clear')
        direc = "/"
    return clear, direc

clear, direc = ClearDirec()


def GSF(size):
    text = ""
    if size < 1024:
        text = str(size) + " B"
    elif size >= 1024 and size < 1048576:
        text = str(round(size / 1024, 2)) + " KB"
    elif size >= 1048576 and size < 1073741824:
        text = str(round(size / 1024 ** 2, 2)) + " M"
    elif size >= 1073741824 and size < 1099511627776:
        text = str(round(size / 1024 ** 3, 2)) + " G"
    return text


def getcwd(name):
    return os.getcwd() + direc + name


def saveFile(addr, data):
    timestr = time.strftime("%Y-%m-%d_%H-%M-%S")
    dir = getcwd("Dumps")
    maindirip = dir + direc + str(addr[0])
    maindirport = maindirip + direc + str(addr[1])
    path = maindirport + direc + os.path.splitext(data.split('\n')[1])[0] + "(" + timestr + ")" + os.path.splitext(data.split('\n')[1])[1]
    if not os.path.exists(dir):
        try:
            os.mkdir(dir)
        except:
            print(stdOutPut('error', f"Not able to make directory ({dir})"))
            return
    if not os.path.exists(maindirip):
        try:
            os.mkdir(maindirip)
        except:
            print(stdOutPut('error', f"Not able to make directory ({maindirip})")) 
            return
    if not os.path.exists(maindirport):
        try:
            os.mkdir(maindirport)
        except:
            print(stdOutPut('error', f"Not able to make directory ({maindirport})")) 
            return
    with open(path, "wb") as file:
        try:
            fileData = base64.b64decode(data.split('\n')[0])
            file.write(fileData)
            print(stdOutPut('success', f"Saved in {path}"))
        except:
            print(stdOutPut('error', "Not able to save the file"))   
        file.close()


def recvall():
    msg, addr = SOC.recvfrom(1024)
    if msg.decode() == "COKJ":
        SOC.sendto("COKJ".encode(), addr)

        data = ""
        buff = ""
        msg, addr = SOC.recvfrom(1024)
        len_data = int(msg.decode("UTF-8"))
        max_text = "[100%] [{}] [{}/{}]".format("-" * int(100 / 3), str(len_data) + " B", str(len_data) + " B")
        print(stdOutPut('info', "Downloading...") + "\n", end='\r', flush=True)
        while "END123" not in data:
            data, addr = SOC.recvfrom(4096)
            data = data.decode("UTF-8", "ignore")
            buff += data
            done = int(100 * (len(buff) / len_data))
            text = "[{}%] [{}{}] [{}/{}]".format(str(done), "-" * (int(done / 3)), " " * (int(100 / 3) - int(done / 3)), GSF(len(buff)), GSF(len_data))
            sys.stdout.write("\r{}{}".format(text, " " * (len(max_text) - len(text))))
            sys.stdout.flush()
        print("\033[F\033[K" + stdOutPut('success', "Downloaded") + "\033[1B")
        return buff.strip().replace("END123", "").strip(), addr
        


def get_shell1(ip, port):
    try:
        soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        except Exception as e:
            print(stdOutPut("error", "%s" % e)); sys.exit()
        soc.bind((str(ip), int(port)))
        global IP
        IP = str(ip)
        global PORT
        PORT = int(port)
        global SOC
        SOC = soc
        get_shell2()
    except Exception as e:
        print(stdOutPut("error", "%s" % e))


def get_shell2():
    print(banner)
    clear()
    print(banner)
    while True:
        data, addr = recvall()
        saveFile(addr, data)