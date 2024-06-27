__author__ = "J0EK3R"
__version__ = "0.1"

import sys
import logging

logger = logging.getLogger(__name__)

sys.path.append("MouldKing") 
from MouldKing.MouldKingHub import MouldKingHub

class MouldKingHub_Byte(MouldKingHub) :
    """
    baseclass handling with byte channels
    """


    def __init__(self, identifier: str, numberOfChannels, channelStartOffset, channelEndOffset, telegram_connect, basetelegram):
        """
        initializes the object and defines the fields
        """
        # call baseclass init and set number of channels
        super().__init__(identifier, numberOfChannels, channelStartOffset, channelEndOffset, telegram_connect, basetelegram)

        logger.debug("MouldKingHub_Byte.__init__")


    async def create_telegram(self) -> bytes:
        """
        returns the telegram including the internal stored value from all channels
        """
        
        # make a copy of the basetelegram
        currentTelegramData = bytearray(self._Basetelegram)

        # calc the length to be used for channels
        channelDataLength = len(currentTelegramData) - self._ChannelEndOffset

        # iterate channels        
        for channelId in range(0, self._NumberOfChannels):
            currentChannelStartOffset = self._ChannelStartOffset + channelId

            if self._NumberOfChannels >= (channelId + 1) and channelDataLength >= currentChannelStartOffset:
                channelValue = self._ChannelValueList[channelId]

                if channelValue < 0:
                    # Range [-1..0] -> 0x80 - [0x7F .. 0x00] = [0x01 .. 0x80]
                    currentTelegramData[currentChannelStartOffset] = int(0x80 - min(-channelValue * 0x80, 0x80))
                elif channelValue > 0:
                    # Range [0..1] -> 0x80 + [0x00 .. 0x7F] = [0x80 .. 0xFF]
                    currentTelegramData[currentChannelStartOffset] = int(0x80 + min(channelValue * 0x7F, 0x7F))
                else:
                    currentTelegramData[currentChannelStartOffset] = 0x80

        await self._advertise(currentTelegramData)
        
        return currentTelegramData