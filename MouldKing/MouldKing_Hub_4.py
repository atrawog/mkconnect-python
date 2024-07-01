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
    """ class handling a MouldKing 4.0 Hub
    """

    # static fields/constants
    _MouldKing_4_Hubs = MouldKing_Hubs_4_12Ch()


    def __init__(self, deviceId: int):
        """ initializes the object and defines the fields
        """
        logger.debug("MouldKing_Hub_4.__init__")

        if deviceId > 2:
            raise Exception('only deviceId 0..2 are allowed')
        
        self._deviceId = deviceId
        self._connected: bool = False
        self._NumberOfChannels = 4


    def get_number_of_channels(self) -> int:
        """ Returns the number of channels.
        This Methode has to be overridden by the implementation of the AdvertisingDevice!

        :return: returns the number of channels
        """
        logger.debug("MouldKing_Hub_4.get_number_of_channels")

        return self._NumberOfChannels


    def get_advertisement_identifier(self) -> str:
        """ Returns the AdvertisementIdentifier to differentiate the Advertising-Data.
        The AdvertisementIdentifier is used to register the Advertising-Data object.
        This Methode has to be overridden by the implementation of the AdvertisingDevice!

        Some AdvertisingDevices like MouldKing 4.0 Hub use only one Advertising telegram for all 
        (three possible) devices. So each AdvertisingDevices returns the same AdvertisementIdentifier

        :return: returns the AdvertisementIdentifier
        """
        logger.debug("MouldKing_Hub_4.set_channel")

        return MouldKing_Hub_4._MouldKing_4_Hubs.get_advertisement_identifier()


    async def connect(self) -> None:
        """ returns the telegram to switch the MouldKing Hubs in bluetooth mode
        """
        await MouldKing_Hub_4._MouldKing_4_Hubs.subDevice_register(self)   

        self._connected = True

        return 


    async def disconnect(self) -> None:
        """ disconnects the device from the advertiser
        """
        await MouldKing_Hub_4._MouldKing_4_Hubs.subDevice_unregister(self)

        self._connected = True

        return 


    async def stop(self) -> bytes:
        """ stops the device by setting the internal stored values of all channels to zero and return the telegram

        :return: returns the generated rawdata
        """

        return await MouldKing_Hub_4._MouldKing_4_Hubs.subDevice_stop(self._deviceId, self._NumberOfChannels)


    async def set_channel(self, channelId: int, value: float) -> bytes:
        """ set internal stored value of channel with channelId to value and return the telegram

        :param channelId: identifier for the channel
        :param value: value to set for the channel
        :return: returns the generated rawdata
        """
        logger.debug("MouldKing_Hub_4.set_channel")

        if channelId > self._NumberOfChannels - 1:
            raise Exception("only channelId 0.." + str(self._NumberOfChannels - 1) + "are allowed")

        return await MouldKing_Hub_4._MouldKing_4_Hubs.subDevice_setChannel(self._deviceId, self._NumberOfChannels, channelId, value)


    def get_channel(self, channelId: int) -> float:
        """ get internal stored value of channel with channelId

        :param channelId: identifier for the channel
        :param value: value to set for the channel
        :return: returns the internal stored value
        """
        logger.debug("MouldKing_Hub_4.get_channel")

        if channelId > self._NumberOfChannels - 1:
            raise Exception("only channelId 0.." + str(self._NumberOfChannels - 1) + "are allowed")

        return MouldKing_Hub_4._MouldKing_4_Hubs.subDevice_getChannel(self._deviceId, self._NumberOfChannels, channelId)


    def get_is_connected(self) -> bool:
        """ Returns true if device is connected.
        This Methode has to be overridden by the implementation of the AdvertisingDevice!

        :return: returns true if device is connected
        """
        logger.debug("MouldKing_Hub_4.get_is_connected")

        return self._connected
