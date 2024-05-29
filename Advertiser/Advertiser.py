__author__ = "J0EK3R"
__version__ = "0.1"

import sys

sys.path.append("Tracer") 
from Tracer.Tracer import Tracer

class Advertiser :
    """
    baseclass
    """
    def __init__(self):
        """
        initializes the object and defines the fields
        """
        pass

    def BlueToothStop(tracer: Tracer=None):
        """
        stop bluetooth advertising
        """
        pass

    def AdvertisementStart(self, identifier: str, manufacturerId: bytes, rawdata: bytes, tracer: Tracer=None):
        pass

    def AdvertisementSet(self, identifier: str, manufacturerId: bytes, rawdata: bytes, tracer: Tracer=None):
        pass
