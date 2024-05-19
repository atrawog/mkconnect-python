__author__ = "J0EK3R"
__version__ = "0.1"

from MouldKingDeviceByte import MouldKingDeviceByte

class MouldKing_6(MouldKingDeviceByte) :
    """
    class handling the MouldKing 6.0 Module
    """

    # static fields/constants
    __telegram_connect = [0x6D, 0x7B, 0xA7, 0x80, 0x80, 0x80, 0x80, 0x92] # Define a byte array for Telegram Connect

    __telegram_base_device_a = [0x61, 0x7B, 0xA7, 0x80, 0x80, 0x80, 0x80, 0x80, 0x80, 0x9E] # byte array for base Telegram
    __telegram_base_device_b = [0x62, 0x7B, 0xA7, 0x80, 0x80, 0x80, 0x80, 0x80, 0x80, 0x9D] # byte array for base Telegram
    __telegram_base_device_c = [0x63, 0x7B, 0xA7, 0x80, 0x80, 0x80, 0x80, 0x80, 0x80, 0x9C] # byte array for base Telegram

    def __init__(self, deviceId):
        if deviceId == 0:
            basetelegram = MouldKing_6.__telegram_base_device_a
        elif deviceId == 1:
            basetelegram = MouldKing_6.__telegram_base_device_b
        elif deviceId == 2:
            basetelegram = MouldKing_6.__telegram_base_device_c
        else:
            raise Exception('only deviceId 0..2 are allowed')

        # call baseclass init and set number of channels
        MouldKingDeviceByte.__init__(self, 6, 3, 1, MouldKing_6.__telegram_connect, basetelegram)




