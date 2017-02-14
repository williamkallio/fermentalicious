# WK 2/12/2017 - Removing Tilt-specific knowledge into own class.
# blescan knows how to:
# Look for BLE Devices around here and filter out advertising reports
# Retrieve an advertising report for a specific UID
# Removed Tilt-specific knowledge
# Hat tip to https://github.com/jimmayhugh/TiltRPi/blob/master/blescan.py 
# BLE iBeaconScanner based on https://github.com/adamf/BLE/blob/master/ble-scanner.py
# BLE scanner based on https://github.com/adamf/BLE/blob/master/ble-scanner.py
# BLE scanner, based on https://code.google.com/p/pybluez/source/browse/trunk/examples/advanced/inquiry-with-rssi.py
# https://github.com/pauloborges/bluez/blob/master/tools/hcitool.c for lescan
# https://kernel.googlesource.com/pub/scm/bluetooth/bluez/+/5.6/lib/hci.h for opcodes
# https://github.com/pauloborges/bluez/blob/master/lib/hci.c#L2782 for functions used by lescan

# performs a simple device inquiry, and returns a list of ble advertizements 
# discovered device

# NOTE: Python's struct.pack() will add padding bytes unless you make the endianness explicit. Little endian
# should be used for BLE. Always start a struct.pack() format string with "<"

from objects.genericevent import GenericEvent
from datetime import datetime
import packetutils
import os
import sys
import struct
import bluetooth._bluetooth as bluez


LE_META_EVENT = 0x3e
LE_PUBLIC_ADDRESS=0x00
LE_RANDOM_ADDRESS=0x01
LE_SET_SCAN_PARAMETERS_CP_SIZE=7
OGF_LE_CTL=0x08
OCF_LE_SET_SCAN_PARAMETERS=0x000B
OCF_LE_SET_SCAN_ENABLE=0x000C
OCF_LE_CREATE_CONN=0x000D

LE_ROLE_MASTER = 0x00
LE_ROLE_SLAVE = 0x01

# these are actually subevents of LE_META_EVENT
EVT_LE_CONN_COMPLETE=0x01
EVT_LE_ADVERTISING_REPORT=0x02
EVT_LE_CONN_UPDATE_COMPLETE=0x03
EVT_LE_READ_REMOTE_USED_FEATURES_COMPLETE=0x04

# Advertisment event types
ADV_IND=0x00
ADV_DIRECT_IND=0x01
ADV_SCAN_IND=0x02
ADV_NONCONN_IND=0x03
ADV_SCAN_RSP=0x04

def hci_enable_le_scan(sock):
    hci_toggle_le_scan(sock, 0x01)

def hci_disable_le_scan(sock):
    hci_toggle_le_scan(sock, 0x00)

def hci_toggle_le_scan(sock, enable):
    cmd_pkt = struct.pack("<BB", enable, 0x00)
    bluez.hci_send_cmd(sock, OGF_LE_CTL, OCF_LE_SET_SCAN_ENABLE, cmd_pkt)

def hci_le_set_scan_parameters(sock):
    old_filter = sock.getsockopt( bluez.SOL_HCI, bluez.HCI_FILTER, 14)

    SCAN_RANDOM = 0x01
    OWN_TYPE = SCAN_RANDOM
    SCAN_TYPE = 0x01

def initialize_sockets(sock):
    #There is no documentation on what these settings are or how they work \/(*-*)\/
    flt = bluez.hci_filter_new()
    bluez.hci_filter_all_events(flt)
    bluez.hci_filter_set_ptype(flt, bluez.HCI_EVENT_PKT)
    sock.setsockopt( bluez.SOL_HCI, bluez.HCI_FILTER, flt )

def scan_for_device_advertisement(sock):
    event = None
    subevent = None
    
    while(event != LE_META_EVENT and subevent != EVT_LE_ADVERTISING_REPORT):
        pkt = sock.recv(255)
        event, = struct.unpack("B", pkt[1])

        if event == LE_META_EVENT:
            subevent, = struct.unpack("B", pkt[3])

            if subevent == EVT_LE_ADVERTISING_REPORT:
                return pkt

#Retrieve all meta events happening around here
def meta_event_search(sock):
    old_filter = sock.getsockopt( bluez.SOL_HCI, bluez.HCI_FILTER, 14)
    initialize_sockets(sock)
    packet = scan_for_device_advertisement(sock)
    report_packet_offset = 0
    
    uid = packetutils.return_string_packet(packet[report_packet_offset -22: report_packet_offset - 6]).upper()
    sock.setsockopt( bluez.SOL_HCI, bluez.HCI_FILTER, old_filter )
     
    return uid

#Retrieve a specific device's meta event data for processing
def get_device_advertisement(sock, uid):
    old_filter = sock.getsockopt( bluez.SOL_HCI, bluez.HCI_FILTER, 14)
    initialize_sockets(sock)
    packet = scan_for_device_advertisement(sock)
    report_pkt_offset = 0

    current_uid = None
    device_event = None
    
    while(current_uid != uid):
        packet = scan_for_device_advertisement(sock)
        mac_address =(packetutils.packed_bdaddr_to_string(packet[report_pkt_offset + 3:report_pkt_offset + 9]))
        current_uid = packetutils.return_string_packet(packet[report_pkt_offset -22: report_pkt_offset - 6]).upper()
       
        if(current_uid == uid):
            device_event = GenericEvent(datetime.now(), mac_address, uid)
        
    sock.setsockopt( bluez.SOL_HCI, bluez.HCI_FILTER, old_filter )

    return [device_event, packet]





