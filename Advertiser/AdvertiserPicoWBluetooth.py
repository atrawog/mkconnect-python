__author__ = "J0EK3R"
__version__ = "0.1"

# import hack for micro-python-simulator with flat filesystem
try:
    from Advertiser.Advertiser import Advertiser
    from Tracer.Tracer import Tracer
except ImportError:
    from Advertiser import Advertiser
    from Tracer import Tracer

class AdvertiserPicoWBluetooth(Advertiser) :
    """
    baseclass
    """

    def __init__(self):
        """
        initializes the object and defines the fields
        """

        super().__init__()

    def AdvertismentStop(self, tracer: Tracer=None):
        """
        stop bluetooth advertising

        """

        # todo

        if (tracer != None):
            pass

        return

    def AdvertisementStart(self, identifier: str, manufacturerId: bytes, rawdata: bytes, tracer: Tracer=None):
        """
        send the bluetooth connect telegram to switch the MouldKing hubs in bluetooth mode
        press the button on the hub(s) and the flashing of status led should switch from blue-green to blue
        """
        data = self._CreateTelegramForPicoW(manufacturerId, rawdata)

        # todo

        if (tracer != None):
            pass

        return

    def AdvertisementSet(self, identifier: str, manufacturerId: bytes, rawdata: bytes, tracer: Tracer=None):
        """
        Set Advertisment data
        """
        data = self._CreateTelegramForPicoW(manufacturerId, rawdata)

        # todo

        if (tracer != None):
            pass

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

