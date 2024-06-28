"""
The class AdvertiseringDeviceSync is a wrapper for (async) objects implementing IAdvertisingDevice
that wraps the async methodes to sync methods
"""

import sys
import logging
import asyncio

from Advertiser.IAdvertisingDevice import IAdvertisingDevice


__author__ = "J0EK3R"
__version__ = "0.1"


logger = logging.getLogger(__name__)


class AdvertisingDeviceSync :
    """ The class AdvertiseringDeviceSync is a wrapper for (async) objects implementing IAdvertisingDevice
    that wraps the async methodes to sync methods
    """

    def __init__(self, advertisingDeviceAsync: IAdvertisingDevice):
        """ initializes the object and defines the member fields
        """
        logger.debug(f"AdvertiseringDeviceSync.__init__")

        self.advertisingDeviceAsync: IAdvertisingDevice = advertisingDeviceAsync

        if sys.version_info < (3, 10):
            self._loop = asyncio.get_event_loop()
        else:
            try:
                self._loop = asyncio.get_running_loop()
            except RuntimeError:
                self._loop = asyncio.new_event_loop()

        asyncio.set_event_loop(self._loop)


    def connect(self) -> None:
        """ connects the device to the advertiser

        :return: returns nothing
        """
        return self._loop.run_until_complete(self.advertisingDeviceAsync.connect())


    def disconnect(self) -> None:
        """ disconnects the device from the advertiser

        :return: returns nothing
        """
        return self._loop.run_until_complete(self.advertisingDeviceAsync.disconnect())


    def stop(self) -> bytes:
        """ stops the device by setting the internal stored values of all channels to zero and return the telegram

        :return: returns the generated rawdata
        """
        logger.debug(f"AdvertiseringDeviceSync.stop")

        return self._loop.run_until_complete(self.advertisingDeviceAsync.stop())
    

    def set_channel(self, channelId: int, value: float) -> bytes:
        """ set internal stored value of channel with channelId to value and return the telegram

        :param channelId: identifier for the channel
        :param value: value to set for the channel
        :return: returns the generated rawdata
        """
        return self._loop.run_until_complete(self.advertisingDeviceAsync.set_channel(channelId, value))

