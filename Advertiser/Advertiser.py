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
        self._tracer = None
        return

    def SetTracer(self, tracer: Tracer) -> Tracer:
        """
        set tracer object
        """
        self._tracer = tracer
        return tracer

    def BlueToothStop():
        """
        stop bluetooth advertising
        """
        return

    def AdvertisementStart(self, identifier: str, manufacturerId: bytes, rawdata: bytes):
        return

    def AdvertisementSet(self, identifier: str, manufacturerId: bytes, rawdata: bytes):
        return
