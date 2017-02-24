# WK 2/13/2017 - I know how to interpret Tilt packets and parse them into
# Tilt Fermentation Objects
from objects.fermentationevent import FermentationEvent
import packetutils
from decimal import *

def parse_tilt_data(generic_event, packet):

    report_pkt_offset = 0
    specific_gravity = Decimal(packetutils.return_number_packet(packet[report_pkt_offset -4: report_pkt_offset - 2])) / 1000
                
    temperature = packetutils.return_number_packet(packet[report_pkt_offset -6: report_pkt_offset - 4])

    return FermentationEvent(generic_event.event_timestamp, generic_event.mac_address,
                             generic_event.uid, specific_gravity, temperature)
