__author__ = "J0EK3R"
__version__ = "0.1"

import sys
import logging

logger = logging.getLogger(__name__)

sys.path.append("Advertiser") 
from Advertiser.AdvertisingDevice import AdvertisingDevice

sys.path.append("MouldKing") 
from MouldKing.MouldKingCrypt import MouldKingCrypt


class MouldKingHub(AdvertisingDevice) :
    """
    baseclass
    """

    ManufacturerID = bytes([0xFF, 0xF0])


    def __init__(self, identifier: str, numberOfChannels: int, channelStartOffset: int, channelEndOffset: int, telegram_connect: bytes, basetelegram: bytes):
        """
        initializes the object and defines the fields
        """
        super().__init__(identifier)

        logger.debug("MouldKingHub.__init__")

        if telegram_connect is not None:
            maxArrayOffset = len(telegram_connect) - 1

            if channelStartOffset > maxArrayOffset:
                raise Exception("max channelStartOffset:" + str(maxArrayOffset))

            if channelEndOffset > (maxArrayOffset - 1):
                raise Exception("max channelEndOffset:" + str(maxArrayOffset))

        self._NumberOfChannels = numberOfChannels
        self._ChannelStartOffset = channelStartOffset
        self._ChannelEndOffset = channelEndOffset

        self._Telegram_connect = telegram_connect
        self._Basetelegram = basetelegram

        # create array 
        self._ChannelValueList = [float(0)] * self._NumberOfChannels

        return


    async def Connect(self) -> None:
        """
        returns the telegram to switch the MouldKing Hubs in bluetooth mode
        """
        # call baseClass to register at Advertiser
        await super().Connect()

        logger.debug("MouldKingHub.Connect")

        await self._Advertise(self._Telegram_connect)

        return


    async def Disconnect(self) -> None:
        """
        disconnects the device from the advertiser
        """
        await self.Stop()
        
        await super().Disconnect()

        logger.debug("MouldKingHub.Disconnect")

        return
    

    async def Stop(self) -> bytes:
        """
        set internal stored value of all channels to zero and return the telegram
        """
        logger.debug("MouldKingHub.Stop")

        # init channels        
        for channelId in range(0, self._NumberOfChannels):
            self._ChannelValueList[channelId] = float(0)
        
        return await self.CreateTelegram()


    async def SetChannel(self, channelId: int, value: float) -> bytes:
        """
        set internal stored value of channel with channelId to value and return the telegram
        """
        logger.debug("MouldKingHub.SetChannel")

        if channelId > self._NumberOfChannels - 1:
            raise Exception("only channelId 0.." + str(self._NumberOfChannels - 1) + "are allowed")

        self._ChannelValueList[channelId] = value
        
        return await self.CreateTelegram()


    async def CreateTelegram(self) -> bytes:
        """
        returns a telegram including the internal stored value from all channels
        """
        
        raise NotImplementedError # override this methode
    

    async def _Advertise(self, rawdata: bytes) -> bytes:
        """
        sends the data to the advertiser
        """
        logger.debug("MouldKingHub._Advertise: start")

        if(self._advertiser is not None):
            cryptedData = MouldKingCrypt.Crypt(rawdata)
            await self._advertiser.AdvertisementDataSet(self._identifier, self.ManufacturerID, cryptedData)

        logger.debug("MouldKingHub._Advertise: finished")

        return self._Telegram_connect

