__author__ = "J0EK3R"
__version__ = "0.1"

# import hack for micro-python-simulator with flat filesystem
try:
    from MouldKing.MouldKingDevice import MouldKingDevice
    from MouldKing.MouldKingCrypt import MouldKingCrypt
except ImportError:
    from MouldKingDevice import MouldKingDevice
    from MouldKingCrypt import MouldKingCrypt

class MouldKingDeviceByte(MouldKingDevice) :
    """
    baseclass handling with byte channels
    """

    def __init__(self, numberOfChannels, channelStartOffset, channelEndOffset, telegram_connect, basetelegram):
        """
        initializes the object and defines the fields
        """

        # call baseclass init and set number of channels
        super().__init__(numberOfChannels, channelStartOffset, channelEndOffset, telegram_connect, basetelegram)

    def Connect(self):
        """
        returns the telegram to switch the MouldKing brick in bluetooth mode
        """

        self._Advertise(self._Telegram_connect)

        return self._Telegram_connect

    def CreateTelegram(self):
        """
        returns the telegram including the internal stored value from all channels
        """
        
        # make a copy of the basetelegram
        currentTelegramData = self._Basetelegram.copy()

        # calc the length to be used for channels
        channelDataLength = len(currentTelegramData) - self._ChannelEndOffset

        # Channel A
        currentChannelStartOffset = self._ChannelStartOffset + 0

        if self._NumberOfChannels >= 1 and channelDataLength >= currentChannelStartOffset:
            if self._Channel_A_Value < 0:
                # Range [-1..0] -> 0x80 - [0x7F .. 0x00] = [0x01 .. 0x80]
                currentTelegramData[currentChannelStartOffset] = int(0x80 - min(-self._Channel_A_Value * 0x80, 0x80))
            elif self._Channel_A_Value > 0:
                # Range [0..1] -> 0x80 + [0x00 .. 0x7F] = [0x80 .. 0xFF]
                currentTelegramData[currentChannelStartOffset] = int(0x80 + min(self._Channel_A_Value * 0x7F, 0x7F))
            else:
                currentTelegramData[currentChannelStartOffset] = 0x80

        # Channel B
        currentChannelStartOffset = self._ChannelStartOffset + 1

        if self._NumberOfChannels >= 2 and channelDataLength >= currentChannelStartOffset:
            if self._Channel_B_Value < 0:
                # Range [-1..0] -> 0x80 - [0x7F .. 0x00] = [0x01 .. 0x80]
                currentTelegramData[currentChannelStartOffset] = int(0x80 - min(-self._Channel_B_Value * 0x80, 0x80))
            elif self._Channel_B_Value > 0:
                # Range [0..1] -> 0x80 + [0x00 .. 0x7F] = [0x80 .. 0xFF]
                currentTelegramData[currentChannelStartOffset] = int(0x80 + min(self._Channel_B_Value * 0x7F, 0x7F))
            else:
                currentTelegramData[currentChannelStartOffset] = 0x80

        # Channel C
        currentChannelStartOffset = self._ChannelStartOffset + 2

        if self._NumberOfChannels >= 3 and channelDataLength >= currentChannelStartOffset:
            if self._Channel_C_Value < 0:
                # Range [-1..0] -> 0x80 - [0x7F .. 0x00] = [0x01 .. 0x80]
                currentTelegramData[currentChannelStartOffset] = int(0x80 - min(-self._Channel_C_Value * 0x80, 0x80))
            elif self._Channel_C_Value > 0:
                # Range [0..1] -> 0x80 + [0x00 .. 0x7F] = [0x80 .. 0xFF]
                currentTelegramData[currentChannelStartOffset] = int(0x80 + min(self._Channel_C_Value * 0x7F, 0x7F))
            else:
                currentTelegramData[currentChannelStartOffset] = 0x80

        # Channel D
        currentChannelStartOffset = self._ChannelStartOffset + 3

        if self._NumberOfChannels >= 4 and channelDataLength >= currentChannelStartOffset:
            if self._Channel_D_Value < 0:
                # Range [-1..0] -> 0x80 - [0x7F .. 0x00] = [0x01 .. 0x80]
                currentTelegramData[currentChannelStartOffset] = int(0x80 - min(-self._Channel_D_Value * 0x80, 0x80))
            elif self._Channel_D_Value > 0:
                # Range [0..1] -> 0x80 + [0x00 .. 0x7F] = [0x80 .. 0xFF]
                currentTelegramData[currentChannelStartOffset] = int(0x80 + min(self._Channel_D_Value * 0x7F, 0x7F))
            else:
                currentTelegramData[currentChannelStartOffset] = 0x80

        # Channel E
        currentChannelStartOffset = self._ChannelStartOffset + 4

        if self._NumberOfChannels >= 5 and channelDataLength >= currentChannelStartOffset:
            if self._Channel_E_Value < 0:
                # Range [-1..0] -> 0x80 - [0x7F .. 0x00] = [0x01 .. 0x80]
                currentTelegramData[currentChannelStartOffset] = int(0x80 - min(-self._Channel_E_Value * 0x80, 0x80))
            elif self._Channel_E_Value > 0:
                # Range [0..1] -> 0x80 + [0x00 .. 0x7F] = [0x80 .. 0xFF]
                currentTelegramData[currentChannelStartOffset] = int(0x80 + min(self._Channel_E_Value * 0x7F, 0x7F))
            else:
                currentTelegramData[currentChannelStartOffset] = 0x80

        # Channel F
        currentChannelStartOffset = self._ChannelStartOffset + 5

        if self._NumberOfChannels >= 6 and channelDataLength >= currentChannelStartOffset:
            if self._Channel_F_Value < 0:
                # Range [-1..0] -> 0x80 - [0x7F .. 0x00] = [0x01 .. 0x80]
                currentTelegramData[currentChannelStartOffset] = int(0x80 - min(-self._Channel_F_Value * 0x80, 0x80))
            elif self._Channel_F_Value > 0:
                # Range [0..1] -> 0x80 + [0x00 .. 0x7F] = [0x80 .. 0xFF]
                currentTelegramData[currentChannelStartOffset] = int(0x80 + min(self._Channel_F_Value * 0x7F, 0x7F))
            else:
                currentTelegramData[currentChannelStartOffset] = 0x80

        self._Advertise(currentTelegramData)
        
        return currentTelegramData