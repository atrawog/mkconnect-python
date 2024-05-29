__author__ = "J0EK3R"
__version__ = "0.1"

import sys

sys.path.append("Tracer") 
from Tracer.Tracer import Tracer

sys.path.append("Advertiser") 
from Advertiser.Advertiser import Advertiser

import bluetooth

class AdvertiserPicoWBluetooth(Advertiser) :
    """
    baseclass
    """

    def __init__(self):
        """
        initializes the object and defines the fields
        """

        super().__init__()
        self.BLE = bluetooth.BLE()
        self.BLE.active(True)

    def AdvertismentStop(self, tracer: Tracer=None):
        """
        stop bluetooth advertising

        """

        self.BLE.active(False)

        if (tracer != None):
            pass

        return

    def AdvertisementStart(self, identifier: str, manufacturerId: bytes, rawdata: bytes, tracer: Tracer=None):
        """
        send the bluetooth connect telegram to switch the MouldKing hubs in bluetooth mode
        press the button on the hub(s) and the flashing of status led should switch from blue-green to blue
        """
        self.AdvertisementSet(identifier, manufacturerId, rawdata, tracer)

        if (tracer != None):
            pass

        return

    def AdvertisementSet(self, identifier: str, manufacturerId: bytes, rawdata: bytes, tracer: Tracer=None):
        """
        Set Advertisment data
        """
        data = self._CreateTelegramForPicoW(manufacturerId, rawdata)

        self.BLE.gap_advertise(100, data)

        if (tracer != None):
            tracer.TraceInfo("AdvertisementSet")

        return
    
    def _CreateTelegramForPicoW(self, manufacturerId: bytes, rawDataArray: bytes) -> bytes:
        """
        Create input data for bluetooth lib for Pico W 
        """
        rawDataArrayLen = len(rawDataArray)

        resultArray = bytearray(2 + rawDataArrayLen)
        resultArray[0] = 0x00
        resultArray[1] = 0xFF
        for index in range(rawDataArrayLen):
            resultArray[index + 2] = rawDataArray[index]

        return resultArray

