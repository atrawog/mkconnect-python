__author__ = "J0EK3R"
__version__ = "0.1"

import sys

sys.path.append("Tracer") 
from Tracer.Tracer import Tracer

sys.path.append("Advertiser") 
from Advertiser.Advertiser import IAdvertisingDevice
from Advertiser.Advertiser import Advertiser

class AdvertisingDevice(IAdvertisingDevice) :
    """
    baseclass
    """
    
    def __init__(self, identifier: str):
        """
        initializes the object and defines the fields
        """

        self._connected = False
        self._advertiser = None
        self._advertiser_registered = False
        self._tracer = None
        self._identifier = identifier

    def SetAdvertiser(self, advertiser: Advertiser) -> Advertiser:
        """
        set advertiser object
        """
        if(self._advertiser == advertiser):
            return advertiser

        reconnect = self._connected

        # unregister
        if(self._advertiser is not None and self._advertiser_registered):
            self._advertiser_registered = not self._advertiser.TryUnregisterAdvertisingDevice(self)
            self._connected = False

        self._advertiser = advertiser

        # register
        if(self._advertiser is not None and reconnect):
            self._advertiser_registered = self._advertiser.TryRegisterAdvertisingDevice(self)

        return advertiser

    def SetTracer(self, tracer: Tracer) -> Tracer:
        """
        set tracer object
        """
        self._tracer = tracer

        return tracer

    def Connect(self):
        """
        connects the device to the advertiser
        """

        if(self._advertiser is not None and not self._advertiser_registered):
            self._advertiser_registered = self._advertiser.TryRegisterAdvertisingDevice(self)

        self._connected = True

        return

    def Disconnect(self):
        """
        disconnects the device from the advertiser
        """

        if(self._advertiser is not None and self._advertiser_registered):
            self._advertiser_registered = not self._advertiser.TryUnregisterAdvertisingDevice(self)

        self._connected = False

        return

    def Stop(self) -> bytes:
        """
        stops the device
        """

        raise NotImplementedError # override this methode

    def AdvertisementSet(self, manufacturerId: bytes, rawdata: bytes):
        """
        Set Advertisement data
        """
        pass

    def GetAdvertisementIdentifier(self) -> str:
        return self._identifier
