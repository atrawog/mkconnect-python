__author__ = "J0EK3R"
__version__ = "0.1"

import sys
import logging

logger = logging.getLogger(__name__)

sys.path.append("Advertiser") 
from Advertiser.IAdvertisingDevice import IAdvertisingDevice

sys.path.append("MouldKing") 
#from MouldKing.MouldKingDevice import MouldKingDevice
from MouldKing.MouldKing_Hubs_4_12Ch import MouldKing_Hubs_4_12Ch

class MouldKing_Hub_4(IAdvertisingDevice) :
    """
    class handling a MouldKing 4.0 Hub
    """

    # static fields/constants
    _MouldKing_4_Hubs = MouldKing_Hubs_4_12Ch()


    def __init__(self, deviceId: int):
        """
        initializes the object and defines the fields
        """
        logger.debug("MouldKing_Hub_4.__init__")

        if deviceId > 2:
            raise Exception('only deviceId 0..2 are allowed')
        
        self._deviceId = deviceId
        self._NumberOfChannels = 4


    async def connect(self) -> None:
        """
        returns the telegram to switch the MouldKing Hubs in bluetooth mode
        """
        await MouldKing_Hub_4._MouldKing_4_Hubs.subDevice_register(self)   

        return 


    async def disconnect(self) -> None:
        """
        disconnects the device from the advertiser
        """
        await MouldKing_Hub_4._MouldKing_4_Hubs.subDevice_unregister(self)

        return 


    async def stop(self) -> bytes:
        """ stops the device by setting the internal stored values of all channels to zero and return the telegram

        :return: returns the generated rawdata
        """

        return await MouldKing_Hub_4._MouldKing_4_Hubs.subDevice_stop(self._deviceId, self._NumberOfChannels)


    async def set_channel(self, channelId: int, value: float) -> bytes:
        """
        set internal stored value of channel with channelId to value and return the telegram

        :param channelId: identifier for the channel
        :param value: value to set for the channel
        :return: returns the generated rawdata
        """
        logger.debug("MouldKing_Hub_4.set_channel")

        if channelId > self._NumberOfChannels - 1:
            raise Exception("only channelId 0.." + str(self._NumberOfChannels - 1) + "are allowed")

        return await MouldKing_Hub_4._MouldKing_4_Hubs.subDevice_setChannel(self._deviceId, self._NumberOfChannels, channelId, value)

