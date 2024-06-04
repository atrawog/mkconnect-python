__author__ = "J0EK3R"
__version__ = "0.1"

import sys

sys.path.append("MouldKing") 
from MouldKing.MouldKingDevice import MouldKingDevice
from MouldKing.MouldKing_4_Hubs import MouldKing_4_Hubs

class MouldKing_4_Hub(MouldKingDevice) :

    # static fields/constants
    MouldKing_4_Hubs = MouldKing_4_Hubs()

    def __init__(self, deviceId: int):
        """
        initializes the object and defines the fields
        """

        if deviceId > 2:
            raise Exception('only deviceId 0..2 are allowed')
        
        self._deviceId = deviceId

        # call baseclass init and set number of channels
        super().__init__(None, 4, None, None, None, None)

    def Connect(self) -> bytes:
        """
        returns the telegram to switch the MouldKing Hubs in bluetooth mode
        """

        return MouldKing_4_Hub.MouldKing_4_Hubs.Connect()

    def Stop(self) -> bytes:
        """
        set internal stored value of all channels to zero and return the telegram
        """

        return MouldKing_4_Hub.MouldKing_4_Hubs.Stop(self._deviceId, self._NumberOfChannels)

    def SetChannel(self, channelId: int, value: float) -> bytes:
        """
        set internal stored value of channel with channelId to value and return the telegram
        """

        if channelId > self._NumberOfChannels - 1:
            raise Exception("only channelId 0.." + int(self._NumberOfChannels - 1) + "are allowed")

        return MouldKing_4_Hub.MouldKing_4_Hubs.SetChannel(self._deviceId, self._NumberOfChannels, channelId, value)

