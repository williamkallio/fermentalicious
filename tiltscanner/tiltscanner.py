#!/usr/bin/env python
# test BLE Scanning software
# jcs 6/8/2014
# bk 2/12/2017 refactoring - separating concerns, adding discovery of multiple devices

# See https://kvurd.com/blog/tilt-hydrometer-ibeacon-data-format/ as reference - explained below
# Tilt sends 2 different messages:
#1 is some kind of scan status - no relevant data
#2 is fermentation data. This message's UID is specific to device color (allows for multiple devices at once)
# Scanner needs to smartly differentiate devices. UID device mappings below:
#Red:    A495BB10C5B14B44B5121370F02D74DE
#Green:  A495BB20C5B14B44B5121370F02D74DE
#Black:  A495BB30C5B14B44B5121370F02D74DE
#Purple: A495BB40C5B14B44B5121370F02D74DE
#Orange: A495BB50C5B14B44B5121370F02D74DE
#Blue:   A495BB60C5B14B44B5121370F02D74DE
#Yellow: A495BB70C5B14B44B5121370F02D74DE
#Pink:   A495BB80C5B14B44B5121370F02D74DE

import tiltpacketprocessor
import blescan
import sys

import bluetooth._bluetooth as bluez

tilt_dict = {'A495BB10C5B14B44B5121370F02D74DE':'Red', 'A495BB20C5B14B44B5121370F02D74DE':'Green', 'A495BB30C5B14B44B5121370F02D74DE':'Black',
             'A495BB40C5B14B44B5121370F02D74DE':'Purple', 'A495BB50C5B14B44B5121370F02D74DE':'Orange', 'A495BB60C5B14B44B5121370F02D74DE':'Blue',
             'A495BB70C5B14B44B5121370F02D74DE':'Yellow', 'A495BB80C5B14B44B5121370F02D74DE':'Pink'}
dev_id = 0
try:
        print('Scanning for Tilts...')
        sock = bluez.hci_open_dev(dev_id)

except:
        print('error accessing bluetooth device...')
        sys.exit(1)

blescan.hci_le_set_scan_parameters(sock)
blescan.hci_enable_le_scan(sock)

#We care only about Tilt UIDs. Let's search for available Tilts
available_tilts = set()

#This should be enough scans to detect all of the broadcasting tilts.
#A little hacky - but need to sample the air for a while to find all of the right devices.
for i in range(0, 20):
        uid = blescan.meta_event_search(sock)

        if(uid in tilt_dict):
                available_tilts.add(tilt_dict[uid])

if(len(available_tilts) == 0):
        print('We couldn\'t find any Tilts :(')
        exit
else:
        print('The following Tilts were found:')

        for tilt in available_tilts:
                print(tilt)

tilt_to_activate = input('Which Tilt Should We Activate? ')

if(tilt_to_activate in available_tilts):
        fermentation_name = input('Fantastic! Give this Fermentation a Name: ')

        #TODO: Validate fermentation name is unique
        print('Confirm the Following Fermentation Details: Tilt - ' + tilt_to_activate + ', Fermentation Name - ' + fermentation_name)
        confirm_fermentation = input('Proceed with this Fermentation? ')

        if(confirm_fermentation.upper() == "Y" or "YES"):
                initiating_device_uid = None
                for k, v in tilt_dict.items():
                        if(v == tilt_to_activate):
                                initiating_device_uid = k

                if(initiating_device_uid == None):
                        print('Unable to Activate Device')
                        exit

                event = blescan.get_device_advertisement(sock, initiating_device_uid)
                fermentation_event = tiltpacketprocessor.parse_tilt_data(event[0], event[1])

                print(fermentation_event.event_timestamp)
                print(fermentation_event.uid)
                print(fermentation_event.mac_address)
                print(fermentation_event.specific_gravity)
                print(fermentation_event.temperature)
        else:
                print('Cancelling Action')
                exit
else:
        print('The Given Tilt is Not Active or Could Not be Found :(')
        exit

        























        

