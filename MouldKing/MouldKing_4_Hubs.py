__author__ = "J0EK3R"
__version__ = "0.1"

import sys

sys.path.append("Advertiser") 
from Advertiser.IAdvertisingDevice import IAdvertisingDevice

sys.path.append("MouldKing") 
from MouldKing.MouldKingDeviceNibble import MouldKingDeviceNibble

class MouldKing_4_Hubs(MouldKingDeviceNibble) :
    """
    class handling 3 x MouldKing 4.0 Module
    Only one telegram addresses all possible 3 x MK4 the same time
    """

    # static fields/constants
    __telegram_connect = bytes([0xAD, 0x7B, 0xA7, 0x80, 0x80, 0x80, 0x4F, 0x52]) # Define a byte array for Telegram Connect

    __telegram_base = bytes([0x7D, 0x7B, 0xA7, 0x88, 0x88, 0x88, 0x88, 0x88, 0x88, 0x82]) # byte array for base Telegram


    def __init__(self):
        """
        initializes the object and defines the fields
        """
        # call baseclass init and set number of channels
        super().__init__("MK4", 12, 3, 1, MouldKing_4_Hubs.__telegram_connect, MouldKing_4_Hubs.__telegram_base)

        self._connectedSubDevices = list()


    def SubDevice_Register(self, subDevice: IAdvertisingDevice) -> None:
        """
        returns the telegram to switch the MouldKing Hubs in bluetooth mode
        """
        connectedSubDevicesLen = len(self._connectedSubDevices)

        if(not subDevice is None and not subDevice in self._connectedSubDevices):
            self._connectedSubDevices.append(subDevice)

            # first subDevice was added
            if(connectedSubDevicesLen == 0):
               self.Connect() 

        return


    def SubDevice_Unregister(self, subDevice: IAdvertisingDevice) -> None:
        """
        disconnects the device from the advertiser
        """
        if(not subDevice is None and subDevice in self._connectedSubDevices):
            self._connectedSubDevices.remove(subDevice)

            # last subDevice was removed
            if(len(self._connectedSubDevices) == 0):
                self.Disconnect()

        return


    def SubDevice_Stop(self, hubDeviceId: int, hubNumberOfChannels: int) -> bytes:
        """
        set internal stored value of all channels to zero and return the telegram
        """
        # deviceId = 0
        # -> channelId 0..4
        # deviceId = 2
        # -> channelId 5..8
        # deviceId = 3
        # -> channelId 9..12
        channelIdHubs = hubDeviceId * hubNumberOfChannels

        # init channels        
        for channelId in range(channelIdHubs, hubNumberOfChannels):
            if channelId < self._NumberOfChannels:
                self._ChannelValueList[channelId] = float(0)
        
        return self.CreateTelegram()
    

    def SubDevice_SetChannel(self, hubDeviceId: int, hubNumberOfChannels: int, hubChannelId: int, value: float) -> bytes:
        """
        set internal stored value of channel with channelId to value and return the telegram
        """

        # deviceId = 0
        # -> channelId 0..4
        # deviceId = 2
        # -> channelId 5..8
        # deviceId = 3
        # -> channelId 9..12
        channelIdHubs = hubDeviceId * hubNumberOfChannels + hubChannelId

        if channelIdHubs > self._NumberOfChannels - 1:
            raise Exception("only channelId 0.." + int(self._NumberOfChannels - 1) + "are allowed")

        self._ChannelValueList[channelIdHubs] = value
        
        return self.CreateTelegram()
