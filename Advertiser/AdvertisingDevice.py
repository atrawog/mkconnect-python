__author__ = "J0EK3R"
__version__ = "0.1"

import sys

sys.path.append("Tracer") 
from Tracer.Tracer import Tracer

sys.path.append("Advertiser") 
from Advertiser.Advertiser import Advertiser

class AdvertisingDevice :
    """
    baseclass
    """
    
    def __init__(self, identifier: str):
        """
        initializes the object and defines the fields
        """

        self._advertiser = None
        self._tracer = None
        self._identifier = identifier

    def SetAdvertiser(self, advertiser: Advertiser) -> Advertiser:
        """
        set advertiser object
        """
        self._advertiser = advertiser

        return advertiser

    def SetTracer(self, tracer: Tracer) -> Tracer:
        """
        set tracer object
        """
        self._tracer = tracer

        return tracer

    def AdvertisementSet(self, manufacturerId: bytes, rawdata: bytes):
        """
        Set Advertisment data
        """
        pass
