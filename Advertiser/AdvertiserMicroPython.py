__author__ = "J0EK3R"
__version__ = "0.1"

import sys

sys.path.append("Tracer") 
from Tracer.Tracer import Tracer

sys.path.append("Advertiser") 
from Advertiser.Advertiser import Advertiser

try:
    import bluetooth
except ImportError as err:
    print("AdvertiserMicroPython: " + str(err))

class AdvertiserMicroPython(Advertiser) :
    """
    Advertiser using bluetooth library from MicroPython
    """

    def __init__(self):
        """
        initializes the object and defines the fields
        """

        super().__init__()

        # Activate bluetooth
        try:
            self.ble = bluetooth.BLE()
            self.ble.active(True)
        except Exception as exception:
            self.ble = None
            print("AdvertiserMicroPython.init: " + str(exception))

        return

    def AdvertismentStop(self):
        """
        stop bluetooth advertising

        """

        if(self.ble is not None):
            self.ble.gap_advertise(None)

            if (self._tracer != None):
                self._tracer.TraceInfo("AdvertisementSet")
        else:
            if (self._tracer != None):
                self._tracer.TraceInfo("self.ble is None")

        if (self._tracer != None):
            pass

        return

    def AdvertisementSet(self, identifier: str, manufacturerId: bytes, rawdata: bytes):
        """
        Set Advertisment data
        """
        data = self._CreateTelegramForPicoW(manufacturerId, rawdata)

        if(self.ble is not None):
            self.ble.gap_advertise(100, data)

            if (self._tracer != None):
                self._tracer.TraceInfo("AdvertisementSet")
        else:
            if (self._tracer != None):
                self._tracer.TraceInfo("self.ble is None")

        return
    
    def _CreateTelegramForPicoW(self, manufacturerId: bytes, rawDataArray: bytes) -> bytes:
        """
        Create input data for bluetooth lib for Pico W 
        """
        rawDataArrayLen = len(rawDataArray)

        btdata = bytearray(2 + rawDataArrayLen)
        btdata[0] = 0x00
        btdata[1] = 0xFF
        for index in range(rawDataArrayLen):
            btdata[index + 2] = rawDataArray[index]

        btcrypteddata = bytearray(b'\x02\x01\x02') + bytearray((len(btdata) + 1, 0xFF)) + btdata

        return bytes(btcrypteddata)

