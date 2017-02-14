class GenericEvent(object):
    def __init__(self, event_timestamp, mac_address, uid):
        self.event_timestamp = event_timestamp
        self.mac_address = mac_address
        self.uid = uid
