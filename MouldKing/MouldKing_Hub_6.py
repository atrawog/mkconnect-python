__author__ = "J0EK3R"
__version__ = "0.1"

import sys
import logging

logger = logging.getLogger(__name__)

sys.path.append("MouldKing") 
from MouldKing.MouldKingHub_Byte import MouldKingHub_Byte


class MouldKing_Hub_6(MouldKingHub_Byte) :
    """ class handling the MouldKing 6.0 Hub
    """

    # static fields/constants
    __telegram_connect = bytes([0x6D, 0x7B, 0xA7, 0x80, 0x80, 0x80, 0x80, 0x92]) # Define a byte array for Telegram Connect

    __telegram_base_device_a = bytes([0x61, 0x7B, 0xA7, 0x80, 0x80, 0x80, 0x80, 0x80, 0x80, 0x9E]) # byte array for base Telegram
    __telegram_base_device_b = bytes([0x62, 0x7B, 0xA7, 0x80, 0x80, 0x80, 0x80, 0x80, 0x80, 0x9D]) # byte array for base Telegram
    __telegram_base_device_c = bytes([0x63, 0x7B, 0xA7, 0x80, 0x80, 0x80, 0x80, 0x80, 0x80, 0x9C]) # byte array for base Telegram


    def __init__(self, deviceId: int):
        """ initializes the object and defines the fields
        """
        if deviceId == 0:
            basetelegram = MouldKing_Hub_6.__telegram_base_device_a
        elif deviceId == 1:
            basetelegram = MouldKing_Hub_6.__telegram_base_device_b
        elif deviceId == 2:
            basetelegram = MouldKing_Hub_6.__telegram_base_device_c
        else:
            raise Exception('only deviceId 0..2 are allowed')

        # call baseclass init and set number of channels
        super().__init__("MK6_" + str(deviceId), 6, 3, 1, MouldKing_Hub_6.__telegram_connect, basetelegram)

        logger.debug("MouldKing_Hub_6.__init__")


    def get_typename(self) -> str:
        """ Returns the typename of the device.
        This Methode has to be overridden by the implementation of the AdvertisingDevice!

        :return: returns a string containing the typename
        """
        return 'MouldKing Hub6.0'





