"""
The class Advertiser is the BaseClass for all Advertisers.
It implements the interface IAdvertiser.
"""

import logging
import asyncio
from IAdvertiser import IAdvertiser
from IAdvertisingDevice import IAdvertisingDevice


__author__ = "J0EK3R"
__version__ = "0.1"


logger = logging.getLogger(__name__)


class Advertiser(IAdvertiser) :
    """
    This is the BaseClass for all Advertiser classes.
    It implements the interface IAdvertiser.
    """

    def __init__(self):
        """ initializes the object and defines the member fields
        """
        logger.debug(f"Advertiser.__init__")

        # dictionary to administer the registered AdvertisingDevices.
        # * key is the instance of the AdvertisingDevice
        # * value is the AdvertisementIdentifier of the AdvertisingDevice
        self._registeredDeviceTable = dict()
        self._registeredDeviceTable_Lock = asyncio.Lock()


    async def advertisement_stop(self) -> None:
        """ stop bluetooth advertising for the Advertiser
        
        :return: returns nothing
        """
        logger.debug(f"Advertiser.advertisement_stop")

        return


    async def try_register_advertising_device(self, advertisingDevice: IAdvertisingDevice) -> bool:
        """
        try to register the given AdvertisingDevice
        * returns true if the AdvertisingDevice was registered successfully
        * returns false if the AdvertisingDevice wasn't registered successfully (because it still was registered)

        :param advertisingDevice: the advertising device to register
        :return: returns true if success
        """
        logger.debug(f"Advertiser.try_register_advertising_device")

        if(advertisingDevice is None):
            return False

        # acquire lock for table
        #self._registeredDeviceTable_Lock.acquire(blocking=True)
        async with self._registeredDeviceTable_Lock:

            if(advertisingDevice in self._registeredDeviceTable):
                return False
            else:
                self._registeredDeviceTable[advertisingDevice] = advertisingDevice.get_advertisement_identifier()
                return True


    async def try_unregister_advertising_device(self, advertisingDevice: IAdvertisingDevice) -> bool:
        """
        try to unregister the given AdvertisingDevice
        * returns True if the AdvertisingDevice was unregistered successfully
        * returns False if the AdvertisingDevice wasn't unregistered successfully

        :param advertisingDevice: the advertising device to unregister
        :return: returns true if success
        """
        logger.debug(f"Advertiser.try_unregister_advertising_device")

        if(advertisingDevice is None):
            return False

        # acquire lock for table
        #self._registeredDeviceTable_Lock.acquire(blocking=True)
        async with self._registeredDeviceTable_Lock:

            if(advertisingDevice in self._registeredDeviceTable):
                self._registeredDeviceTable.pop(advertisingDevice)
                return True
            else:
                return False


    async def set_advertisement_data(self, advertisementIdentifier: str, manufacturerId: bytes, rawdata: bytes) -> None:
        """
        Sets Advertisement-Data for a specific AdvertisementIdentifier
        This Methode has to be overridden by the implementation of the AdvertisingDevice!

        :param advertisementIdentifier: identifier for the advertisement
        :param manufacturerId: manifacturerId
        :param rawdata: rawdata
        :return: returns nothing
        """
        logger.debug(f"Advertiser.set_advertisement_data")

        return
