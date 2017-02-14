#WK 2/13/2017
#Utility for doing things with Packets
import struct

def return_number_packet(pkt):
    integer = 0
    multiple = 256
    for c in pkt:
        integer +=  struct.unpack("B",c)[0] * multiple
        multiple = 1
    return integer 

def return_string_packet(pkt):
    string = "";
    for c in pkt:
        string +=  "%02x" %struct.unpack("B",c)[0]
    return string 

def print_packet(pkt):
    for c in pkt:
        sys.stdout.write("%02x " % struct.unpack("B",c)[0])

def get_packed_bdaddr(bdaddr_string):
    packable_addr = []
    addr = bdaddr_string.split(':')
    addr.reverse()
    for b in addr: 
        packable_addr.append(int(b, 16))
    return struct.pack("<BBBBBB", *packable_addr)

def packed_bdaddr_to_string(bdaddr_packed):
    return ':'.join('%02x'%i for i in struct.unpack("<BBBBBB", bdaddr_packed[::-1]))
