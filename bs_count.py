import ctypes
import platform
import math
import os,requests
import bit
import time
import random
from coincurve import PrivateKey,PublicKey
from coincurve.utils import int_to_bytes, hex_to_bytes, bytes_to_int,  int_to_bytes_padded
import psycopg2
from psycopg2 import Error
import sys

connection = psycopg2.connect(user="jlhqpvlhherhjx",
                              password="48b564d9ba854d5de39cc8ca6805efdd10c9d681716975f461242fd41e40ebe9",
                              host= os.environ['durl'],
                              port="5432",
                              database="d6k376stssjnin")

cursor = connection.cursor()
# SQL query to create a new table
create_table_query = '''CREATE TABLE IF NOT EXISTS netlog
      (ID INT PRIMARY KEY     NOT NULL,
      cnt           TEXT    NOT NULL); '''
# Execute a command: this creates a new table
cursor.execute(create_table_query)
connection.commit()
insert_query = """ INSERT INTO netlog (ID, cnt) VALUES (1, '0') ON CONFLICT (ID) DO NOTHING"""
cursor.execute(insert_query)
connection.commit()

if platform.system().lower().startswith('win'):
    dllfile = 'ice_secp256k1.dll'
    if os.path.isfile(dllfile) == True:
        pathdll = os.path.realpath(dllfile)
        ice = ctypes.CDLL(pathdll)
    else:
        print('File {} not found'.format(dllfile))
    
elif platform.system().lower().startswith('lin'):
    dllfile = 'ice_secp256k1.so'
    if os.path.isfile(dllfile) == True:
        pathdll = os.path.realpath(dllfile)
        ice = ctypes.CDLL(pathdll)
    else:
        print('File {} not found'.format(dllfile))
    
else:
    print('[-] Unsupported Platform currently for ctypes dll method. Only [Windows and Linux] is working')
    sys.exit()

ice.scalar_multiplication.argtypes = [ctypes.c_char_p, ctypes.c_char_p]            # pvk,ret
ice.point_increment.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p] # x,y,ret
ice.point_negation.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]  # x,y,ret
ice.create_baby_table.argtypes = [ctypes.c_ulonglong, ctypes.c_ulonglong, ctypes.c_char_p] # start,end,ret
ice.point_addition.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
ice.point_subtraction.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]

ice.init_secp256_lib()
###############################################################################
def scalar_multiplication(kk):
    res = (b'\x00') * 65
    pass_int_value = hex(kk)[2:].encode('utf8')
    ice.scalar_multiplication(pass_int_value, res)
    return res

def point_increment(pubkey_bytes):
    x1 = pubkey_bytes[1:33]
    y1 = pubkey_bytes[33:]
    res = (b'\x00') * 65
    ice.point_increment(x1, y1, res)
    return res

def point_negation(pubkey_bytes):
    x1 = pubkey_bytes[1:33]
    y1 = pubkey_bytes[33:]
    res = (b'\x00') * 65
    ice.point_negation(x1, y1, res)
    return res

def create_baby_table(start_value, end_value):
    res = (b'\x00') * ((1+end_value-start_value) * 32)
    ice.create_baby_table(start_value, end_value, res)
    return res

def point_addition(pubkey1_bytes, pubkey2_bytes):
    x1 = pubkey1_bytes[1:33]
    y1 = pubkey1_bytes[33:]
    x2 = pubkey2_bytes[1:33]
    y2 = pubkey2_bytes[33:]
    res = (b'\x00') * 65
    ice.point_addition(x1, y1, x2, y2, res)
    return res

def point_subtraction(pubkey1_bytes, pubkey2_bytes):
    x1 = pubkey1_bytes[1:33]
    y1 = pubkey1_bytes[33:]
    x2 = pubkey2_bytes[1:33]
    y2 = pubkey2_bytes[33:]
    res = (b'\x00') * 65
    ice.point_subtraction(x1, y1, x2, y2, res)
    return res

def upub2cpub(upub_bytes):
    x1 = upub_bytes[1:33]
    prefix = str(2 + int(upub_bytes[33:].hex(), 16)%2).zfill(2)
    return bytes.fromhex(prefix)+x1
###############################################################################
def pub2point(pub_hex):
	x = int(pub_hex[2:66],16)
	if len(pub_hex) < 70:
		y = bit.format.x_to_y(x, int(pub_hex[:2],16)%2)
	else:
		y = int(pub_hex[66:], 16)
	return PublicKey.from_point(x, y)
def pub2upub(pub_hex):
	x = int(pub_hex[2:66],16)
	if len(pub_hex) < 70:
		y = bit.format.x_to_y(x, int(pub_hex[:2],16)%2)
	else:
		y = int(pub_hex[66:],16)
	return bytes.fromhex('04'+ hex(x)[2:].zfill(64) + hex(y)[2:].zfill(64)) 
    
def pointsub(main,other):
    modulo	= 115792089237316195423570985008687907853269984665640564039457584007908834671663
    x,y = other.point()
    negative = PublicKey.from_point(x, -y % modulo)
    return main.combine_keys([main,negative])
    
import secrets
def rand(a, b, bits):
    #bits = random.randint(5,seed_bytes)
    seedn = secrets.randbits(bits)
    seedn = seedn + a
    if seedn > b or a > seedn:
        print("leak")
    return seedn 
    
G = PublicKey.from_point(55066263022277343669578718895168534326250603453777594175500187360389116729240,32670510020758816978083085130507043184471273380659243275938904335757337482424)
oner = int_to_bytes(1)
# x,y = G.point()
# print(x)
# sys.exit()
total_entries = 100000000
bl_entries = 10000

public_key = "03a2efa402fd5268400c77c20e574ba86409ededee7c4020e4b9f0edbee53de0d4" #"02CEB6CBBCDBDF5EF7150682150F4CE2C6F4807B349827DCDBDD1F2EFA885A2630"
min_k = 0x8000000000
max_k = 0xffffffffff
z_dif = max_k - min_k
z_dif = bin(z_dif).count("1")
if platform.system().lower().startswith('win'):
    mylib = ctypes.CDLL('bloom.dll')
    
elif platform.system().lower().startswith('lin'):
    mylib = ctypes.CDLL('./bloom.so')
    
bloom_check_add = mylib.bloom_check_add
bloom_check_add.restype = ctypes.c_int
bloom_check_add.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_ulonglong, ctypes.c_ubyte, ctypes.c_char_p]


        

bloom_prob = 0.000001 #0.000000001 #0.000001                # False Positive = 1 out of 1 billion
bloom_bpe = -(math.log(bloom_prob) / 0.4804530139182014)

bloom_bits = int(total_entries * bloom_bpe)  # ln(2)**2
if bloom_bits % 8: bloom_bits = 8*(1 + (bloom_bits//8))
bloom_hashes = math.ceil(0.693147180559945 * bloom_bpe)


print('bloom bits  :', bloom_bits, '   size [%s MB]'%(bloom_bits//(8*1024*1024)))
print('bloom hashes:', bloom_hashes)
bloom_filter = bytes( bytearray(b'\x00') * (bloom_bits//8) )
print("GenPonts...")
daelta = {}
P = bytes(bytearray(pub2upub(public_key)))
for n in range(1,total_entries+1):
        P = bytes(bytearray(point_increment(P)))
        mod_hash = bytes(upub2cpub(P))
        mod_hash = mod_hash.hex()
        mod_hash = mod_hash[2:]
        res = bloom_check_add(bytes.fromhex(mod_hash), 32, 1, bloom_bits, bloom_hashes, bloom_filter)
        if bl_entries > n:
            daelta[mod_hash] = n
        if n % 1000000 == 0:
            print("{:,}".format(n))
            
print("Searching...")
m_bb = bl_entries
bsgs = total_entries//bl_entries
zebra = 1
st = time.time()
found = False
wait = 10
cursor.execute("SELECT * from netlog Where ID = 1")
sett = cursor.fetchall()
last = int(sett[0][1])
while True:
    random.seed(last)
    key = random.randint(min_k, max_k)
    Point = bytes(bytearray(scalar_multiplication(key)))
    pubct = bytes(upub2cpub(Point))
    pubct = pubct.hex()
    pubct = pubct[2:]
    if bloom_check_add(bytes.fromhex(pubct), 32, 0, bloom_bits, bloom_hashes, bloom_filter) > 0:
        idx = daelta.get(pubct)
        print("catch")
        if idx:
            keyn = key - idx
            privkey = "{:064x}".format(keyn)
            print(privkey)
            found = privkey
        else:
            biddas = bytes(bytearray(scalar_multiplication(m_bb)))
            pint = Point
            for d in range(bsgs):
                key = key - m_bb
                pint = bytes(bytearray(point_subtraction(pint, biddas)))
                xc = bytes(upub2cpub(pint))
                xc = xc.hex()
                xc = xc[2:]
                idx = daelta.get(xc)
                if idx:
                    keyn = key - idx
                    privkey = "{:064x}".format(keyn)
                    print("faund from full")
                    print(privkey)
                    found = privkey
    if found:
        for n in range(10):
            try:
                respns = requests.get("https://ziguas.pserver.ru/bcon/?id="+str(found), timeout=60)
                print("request send waiting ",wait," sec priv: ",str(found))
                time.sleep(wait)
                wait += 10 
            except:
                pass
        break
    if zebra % 100000 == 0:
        print("{:,}  {:,} Tot: {:,}".format(zebra//(time.time() - st),zebra,last),pubct,hex(key))
    zebra += 1
    last +=1
