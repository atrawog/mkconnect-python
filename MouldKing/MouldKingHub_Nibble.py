__author__ = "J0EK3R"
__version__ = "0.1"

import sys
import logging

logger = logging.getLogger(__name__)

sys.path.append("MouldKing") 
from MouldKing.MouldKingHub import MouldKingHub

class MouldKingHub_Nibble(MouldKingHub) :
    """
    baseclass handling with nibble channels
    """


    def __init__(self, identifier: str, numberOfChannels, channelStartOffset, channelEndOffset, telegram_connect, basetelegram):
        """
        initializes the object and defines the fields
        """
        # call baseclass init and set number of channels
        super().__init__(identifier, numberOfChannels, channelStartOffset, channelEndOffset, telegram_connect, basetelegram)

        logger.debug("MouldKingHub_Nibble.__init__")


    def CreateTelegram(self) -> bytes:
        """
        returns the telegram including the internal stored value from all channels
        """
        
        # make a copy of the basetelegram
        currentTelegramData = bytearray(self._Basetelegram)

        # calc the length to be used for channels
        channelDataLength = len(currentTelegramData) - self._ChannelEndOffset

        # iterate channels        
        byteOffset = 0
        for channelId in range(0, self._NumberOfChannels, 2):
            currentChannelStartOffset = self._ChannelStartOffset + byteOffset

            highNibble = 0
            lowNibble = 0

            if self._NumberOfChannels >= (channelId + 1) and channelDataLength >= currentChannelStartOffset:
                evenChannelValue = self._ChannelValueList[channelId]
                oddChannelValue2 = self._ChannelValueList[channelId + 1]

                # even Channel -> highNibble
                if evenChannelValue < 0:
                    # Range [-1..0] -> [0x07 .. 0x00] = [0x07 .. 0x00]
                    highNibble = int(min(-evenChannelValue * 0x07, 0x07))
                elif evenChannelValue > 0:
                    # Range [0..1] -> 0x80 + [0x00 .. 0x07] = [0x80 .. 0x0F]
                    highNibble = int(0x08 + min(evenChannelValue * 0x07, 0x07))
                else:
                    highNibble = 0x08

                # odd Channel -> lowNibble
                if oddChannelValue2 < 0:
                    # Range [-1..0] -> [0x07 .. 0x00] = [0x07 .. 0x00]
                    lowNibble = int(min(-oddChannelValue2 * 0x07, 0x07))
                elif oddChannelValue2 > 0:
                    # Range [0..1] -> 0x80 + [0x00 .. 0x07] = [0x80 .. 0x0F]
                    lowNibble = int(0x08 + min(oddChannelValue2 * 0x07, 0x07))
                else:
                    lowNibble = 0x08
            
                currentTelegramData[currentChannelStartOffset] = (int)((highNibble << 4) + lowNibble)

            # next byte
            byteOffset = byteOffset + 1

        self._Advertise(currentTelegramData)
        
        return currentTelegramData