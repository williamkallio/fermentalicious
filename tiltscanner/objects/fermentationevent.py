from genericevent import GenericEvent

class FermentationEvent(GenericEvent):
    def __init__(self, event_timestamp, mac_address, uid, specific_gravity, temperature):
        super(FermentationEvent, self).__init__(event_timestamp, mac_address, uid)
        self.specific_gravity = specific_gravity
        self.temperature = temperature
