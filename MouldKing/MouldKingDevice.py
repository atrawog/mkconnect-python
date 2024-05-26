__author__ = "J0EK3R"
__version__ = "0.1"

# import hack for micro-python-simulator with flat filesystem
try:
    from Advertiser.AdvertisingDevice import AdvertisingDevice
    from MouldKing.MouldKingCrypt import MouldKingCrypt
except ImportError:
    from AdvertisingDevice import AdvertisingDevice
    from MouldKingCrypt import MouldKingCrypt

class MouldKingDevice(AdvertisingDevice) :
    """
    baseclass
    """

    ManufacturerID = bytes([0xFF, 0xF0])

    def __init__(self, numberOfChannels, channelStartOffset, channelEndOffset, telegram_connect, basetelegram):
        """
        initializes the object and defines the fields
        """

        super().__init__()

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

    def Connect(self) -> bytes:
        """
        returns the telegram to switch the MouldKing brick to bluetooth mode
        """

        raise NotImplementedError # override this methode

    def Stop(self) -> bytes:
        """
        set internal stored value of all channels to zero and return the telegram
        """

        # init channels        
        self._Channel_A_Value = float(0)
        self._Channel_B_Value = float(0)
        self._Channel_C_Value = float(0)
        self._Channel_D_Value = float(0)
        self._Channel_E_Value = float(0)
        self._Channel_F_Value = float(0)

        return self.CreateTelegram();

    def SetChannel(self, channelId: int, value: float) -> bytes:
        """
        set internal stored value of channel with channelId to value and return the telegram
        """

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
        """
        returns a telegram including the internal stored value from all channels
        """
        
        raise NotImplementedError # override this methode
    
    def _Advertise(self, rawdata: bytes) -> bytes:
        """
        sends the data to the advertiser
        """

        if(self._advertiser != None):
            cryptedData = MouldKingCrypt.Crypt(rawdata)
            self._advertiser.AdvertismentStart(self.ManufacturerID, cryptedData)

        return self._Telegram_connect

