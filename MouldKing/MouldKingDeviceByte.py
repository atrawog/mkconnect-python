__author__ = "J0EK3R"
__version__ = "0.1"

from MouldKing.MouldKingDevice import MouldKingDevice
#from MouldKingCrypt import MouldKingCrypt

class MouldKingDeviceByte(MouldKingDevice) :
    """
    baseclass handling with byte channels
    """

    def __init__(self, numberOfChannels, channelStartOffset, channelEndOffset, telegram_connect, basetelegram):
        # call baseclass init and set number of channels
        MouldKingDevice.__init__(self, numberOfChannels, channelStartOffset, channelEndOffset, telegram_connect, basetelegram)

    def Connect(self):
        # return MouldKingCrypt.Crypt(self._Telegram_connect)
        return self._Telegram_connect

    def CreateTelegram(self):
        # make a copy of the basetelegram
        currentData = self._Basetelegram.copy()

        channelDataLength = len(currentData) - self._ChannelEndOffset
        currentChannelStartOffset = 0

        # Channel A
        currentChannelStartOffset = self._ChannelStartOffset + 0

        if self._NumberOfChannels >= 1 and channelDataLength >= currentChannelStartOffset:
            if self._Channel_A_Value < 0:
                # Range [-1..0] -> 0x80 - [0x7F .. 0x00] = [0x01 .. 0x80]
                currentData[currentChannelStartOffset] = int(0x80 - min(-self._Channel_A_Value * 0x80, 0x80))
            elif self._Channel_A_Value > 0:
                # Range [0..1] -> 0x80 + [0x00 .. 0x7F] = [0x80 .. 0xFF]
                currentData[currentChannelStartOffset] = int(0x80 + min(self._Channel_A_Value * 0x7F, 0x7F))
            else:
                currentData[currentChannelStartOffset] = 0x80

        # Channel B
        currentChannelStartOffset = self._ChannelStartOffset + 1

        if self._NumberOfChannels >= 1 and channelDataLength >= currentChannelStartOffset:
            if self._Channel_B_Value < 0:
                # Range [-1..0] -> 0x80 - [0x7F .. 0x00] = [0x01 .. 0x80]
                currentData[currentChannelStartOffset] = int(0x80 - min(-self._Channel_B_Value * 0x80, 0x80))
            elif self._Channel_B_Value > 0:
                # Range [0..1] -> 0x80 + [0x00 .. 0x7F] = [0x80 .. 0xFF]
                currentData[currentChannelStartOffset] = int(0x80 + min(self._Channel_B_Value * 0x7F, 0x7F))
            else:
                currentData[currentChannelStartOffset] = 0x80

        # Channel C
        currentChannelStartOffset = self._ChannelStartOffset + 2

        if self._NumberOfChannels >= 1 and channelDataLength >= currentChannelStartOffset:
            if self._Channel_C_Value < 0:
                # Range [-1..0] -> 0x80 - [0x7F .. 0x00] = [0x01 .. 0x80]
                currentData[currentChannelStartOffset] = int(0x80 - min(-self._Channel_C_Value * 0x80, 0x80))
            elif self._Channel_C_Value > 0:
                # Range [0..1] -> 0x80 + [0x00 .. 0x7F] = [0x80 .. 0xFF]
                currentData[currentChannelStartOffset] = int(0x80 + min(self._Channel_C_Value * 0x7F, 0x7F))
            else:
                currentData[currentChannelStartOffset] = 0x80

        # Channel D
        currentChannelStartOffset = self._ChannelStartOffset + 3

        if self._NumberOfChannels >= 1 and channelDataLength >= currentChannelStartOffset:
            if self._Channel_D_Value < 0:
                # Range [-1..0] -> 0x80 - [0x7F .. 0x00] = [0x01 .. 0x80]
                currentData[currentChannelStartOffset] = int(0x80 - min(-self._Channel_D_Value * 0x80, 0x80))
            elif self._Channel_D_Value > 0:
                # Range [0..1] -> 0x80 + [0x00 .. 0x7F] = [0x80 .. 0xFF]
                currentData[currentChannelStartOffset] = int(0x80 + min(self._Channel_D_Value * 0x7F, 0x7F))
            else:
                currentData[currentChannelStartOffset] = 0x80

        # Channel E
        currentChannelStartOffset = self._ChannelStartOffset + 4

        if self._NumberOfChannels >= 1 and channelDataLength >= currentChannelStartOffset:
            if self._Channel_E_Value < 0:
                # Range [-1..0] -> 0x80 - [0x7F .. 0x00] = [0x01 .. 0x80]
                currentData[currentChannelStartOffset] = int(0x80 - min(-self._Channel_E_Value * 0x80, 0x80))
            elif self._Channel_E_Value > 0:
                # Range [0..1] -> 0x80 + [0x00 .. 0x7F] = [0x80 .. 0xFF]
                currentData[currentChannelStartOffset] = int(0x80 + min(self._Channel_E_Value * 0x7F, 0x7F))
            else:
                currentData[currentChannelStartOffset] = 0x80

        # Channel F
        currentChannelStartOffset = self._ChannelStartOffset + 5

        if self._NumberOfChannels >= 1 and channelDataLength >= currentChannelStartOffset:
            if self._Channel_F_Value < 0:
                # Range [-1..0] -> 0x80 - [0x7F .. 0x00] = [0x01 .. 0x80]
                currentData[currentChannelStartOffset] = int(0x80 - min(-self._Channel_F_Value * 0x80, 0x80))
            elif self._Channel_F_Value > 0:
                # Range [0..1] -> 0x80 + [0x00 .. 0x7F] = [0x80 .. 0xFF]
                currentData[currentChannelStartOffset] = int(0x80 + min(self._Channel_F_Value * 0x7F, 0x7F))
            else:
                currentData[currentChannelStartOffset] = 0x80

#        return MouldKingCrypt.Crypt(currentData)
        return currentData