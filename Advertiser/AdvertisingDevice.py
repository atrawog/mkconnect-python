"""
baseclass for all advertising devices
"""

import sys
import logging
sys.path.append("Advertiser") 
from Advertiser.Advertiser import IAdvertisingDevice
from Advertiser.Advertiser import Advertiser


__author__ = "J0EK3R"
__version__ = "0.1"


logger = logging.getLogger(__name__)


class AdvertisingDevice(IAdvertisingDevice) :
    """ baseclass for all advertising devices
    """
    
    def __init__(self, identifier: str):
        """ initializes the object and defines the fields
        """
        logger.debug("AdvertisingDevice.__init__")

        self._connected: bool = False
        self._advertiser = None
        self._advertiser_registered: bool = False
        self._identifier: str = identifier


    async def set_advertiser(self, advertiser: Advertiser) -> Advertiser:
        """ set advertiser object

        :param advertiser: advertiser
        :return: returns advertiser
        """
        logger.debug("AdvertisingDevice.set_advertiser")

        if(self._advertiser == advertiser):
            return advertiser

        reconnect = self._connected

        # unregister
        if(self._advertiser is not None and self._advertiser_registered):
            self._advertiser_registered = not await self._advertiser.try_unregister_advertising_device(self)
            self._connected = False

        self._advertiser = advertiser

        # register
        if(self._advertiser is not None and reconnect):
            self._advertiser_registered = await self._advertiser.try_register_advertising_device(self)

        return advertiser


    async def connect(self) -> None:
        """ connects the device to the advertiser

        :return: returns nothing
        """
        logger.debug("AdvertisingDevice.connect")

        if(self._advertiser is not None and not self._advertiser_registered):
            self._advertiser_registered = await self._advertiser.try_register_advertising_device(self)

        self._connected = True

        return


    async def disconnect(self) -> None:
        """ disconnects the device from the advertiser

        :return: returns nothing
        """
        logger.debug("AdvertisingDevice.disconnect")

        if(self._advertiser is not None and self._advertiser_registered):
            self._advertiser_registered = not await self._advertiser.try_unregister_advertising_device(self)

        self._connected = False

        return


    async def stop(self) -> bytes:
        """ stops the device by setting the internal stored values of all channels to zero and return the telegram

        :return: returns the generated rawdata
        """
        logger.debug("AdvertisingDevice.stop")

        raise NotImplementedError # override this methode


    async def set_advertisement_data(self, manufacturerId: bytes, rawdata: bytes) -> None:
        """ Set AdvertisementData

        :param manufacturerId: advertiser
        :param rawdata: advertiser
        :return: returns nothing
        """
        logger.debug("AdvertisingDevice.set_advertisement_data")
        return


    def get_advertisement_identifier(self) -> str:
        """ Get AdvertisementIdentifier

        :return: returns the Advertisement Identifier string
        """
        logger.debug("AdvertisingDevice.get_advertisement_identifier")

        return self._identifier


    def get_is_connected(self) -> bool:
        """ Returns true if device is connected.
        This Methode has to be overridden by the implementation of the AdvertisingDevice!

        :return: returns true if device is connected
        """
        logger.debug("AdvertisingDevice.get_is_connected")

        return self._connected
