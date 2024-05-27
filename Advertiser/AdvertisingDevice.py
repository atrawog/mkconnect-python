__author__ = "J0EK3R"
__version__ = "0.1"

# import hack for micro-python-simulator with flat filesystem
try:
    from Advertiser.Advertiser import Advertiser
    from Tracer.Tracer import Tracer
except ImportError:
    from Advertiser import Advertiser
    from Tracer import Tracer

class AdvertisingDevice :
    """
    baseclass
    """
    
    def __init__(self):
        """
        initializes the object and defines the fields
        """

        self._advertiser = None
        self._tracer = None

    def SetAdvertiser(self, advertiser: Advertiser):
        """
        set advertiser object
        """
        self._advertiser = advertiser

    def SetTracer(self, tracer: Tracer):
        """
        set tracer object
        """
        self._tracer = tracer

    def AdvertismentStart(self, manufacturerId: bytes, rawdata: bytes, tracer: Tracer=None):
        """
        send the bluetooth connect telegram to switch the MouldKing hubs in bluetooth mode
        press the button on the hub(s) and the flashing of status led should switch from blue-green to blue
        """
        pass

    def AdvertismentSet(self, manufacturerId: bytes, rawdata: bytes, tracer: Tracer=None):
        """
        Set Advertisment data
        """
        pass
