__author__ = "J0EK3R"
__version__ = "0.1"

class MouldKingDevice :
    """
    baseclass
    """

    ManufacturerID = [0xFF, 0xF0]

    def __init__(self, numberOfChannels, channelStartOffset, channelEndOffset, telegram_connect, basetelegram):
        if numberOfChannels > 6:
            raise Exception("max 6 channels")

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

        self._Channel_A_Value = 0
        self._Channel_B_Value = 0
        self._Channel_C_Value = 0
        self._Channel_D_Value = 0
        self._Channel_E_Value = 0
        self._Channel_F_Value = 0

    def Connect(self):
        pass

    def Stop(self):
        # init channels        
        self._Channel_A_Value = 0
        self._Channel_B_Value = 0
        self._Channel_C_Value = 0
        self._Channel_D_Value = 0
        self._Channel_E_Value = 0
        self._Channel_F_Value = 0

        return self.CreateTelegram();

    def SetChannel(self, channelId, value):
        if channelId > self._NumberOfChannels - 1:
            raise Exception("only channelId 0.." + int(self._NumberOfChannels - 1) + "are allowed")
        elif channelId == 0:
            self._Channel_A_Value = value
        elif channelId == 1:    
            self._Channel_B_Value = value
        elif channelId == 2:    
            self._Channel_C_Value = value
        elif channelId == 3:    
            self._Channel_D_Value = value
        elif channelId == 4:    
            self._Channel_E_Value = value
        elif channelId == 5:    
            self._Channel_F_Value = value
        
        return self.CreateTelegram();

    def CreateTelegram(self):
        pass