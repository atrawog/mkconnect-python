__author__ = "J0EK3R"
__version__ = "0.1"

import sys

sys.path.append("Tracer") 
from Tracer.Tracer import Tracer

sys.path.append("Advertiser") 
from Advertiser.AdvertisingDevice import AdvertisingDevice

sys.path.append("MouldKing") 
from MouldKing.MouldKingCrypt import MouldKingCrypt

class MouldKingDevice(AdvertisingDevice) :
    """
    baseclass
    """

    ManufacturerID = bytes([0xFF, 0xF0])

    def __init__(self, identifier: str, numberOfChannels: int, channelStartOffset: int, channelEndOffset: int, telegram_connect: bytes, basetelegram: bytes):
        """
        initializes the object and defines the fields
        """

        super().__init__(identifier)

        if telegram_connect is not None:
            maxArrayOffset = len(telegram_connect) - 1

            if channelStartOffset > maxArrayOffset:
                raise Exception("max channelStartOffset:" + maxArrayOffset)

            if channelEndOffset > (maxArrayOffset - 1):
                raise Exception("max channelEndOffset:" + maxArrayOffset)

        self._NumberOfChannels = numberOfChannels
        self._ChannelStartOffset = channelStartOffset
        self._ChannelEndOffset = channelEndOffset

        self._Telegram_connect = telegram_connect
        self._Basetelegram = basetelegram

        # create array 
        self._ChannelValueList = [float(0)] * self._NumberOfChannels

        return

    def Connect(self) -> bytes:
        """
        returns the telegram to switch the MouldKing Hubs in bluetooth mode
        """

        # call baseClass to register at Advertiser
        super().Connect()

        self._Advertise(self._Telegram_connect)

        return self._Telegram_connect

    def Disconnect(self):
        """
        disconnects the device from the advertiser
        """

        self.Stop()
        
        super().Disconnect()

        return
    
    def Stop(self) -> bytes:
        """
        set internal stored value of all channels to zero and return the telegram
        """

        # init channels        
        for channelId in range(0, self._NumberOfChannels):
            self._ChannelValueList[channelId] = float(0)
        
        return self.CreateTelegram()

    def SetChannel(self, channelId: int, value: float) -> bytes:
        """
        set internal stored value of channel with channelId to value and return the telegram
        """

        if channelId > self._NumberOfChannels - 1:
            raise Exception("only channelId 0.." + int(self._NumberOfChannels - 1) + "are allowed")

        self._ChannelValueList[channelId] = value
        
        return self.CreateTelegram()

    def CreateTelegram(self) -> bytes:
        """
        returns a telegram including the internal stored value from all channels
        """
        
        raise NotImplementedError # override this methode
    
    def _Advertise(self, rawdata: bytes) -> bytes:
        """
        sends the data to the advertiser
        """

        if(self._tracer is not None):
            self._tracer.TraceInfo("Advertise")

        if(self._advertiser is not None):
            cryptedData = MouldKingCrypt.Crypt(rawdata)
            self._advertiser.AdvertisementDataSet(self._identifier, self.ManufacturerID, cryptedData)

        return self._Telegram_connect

