__author__ = "J0EK3R"
__version__ = "0.1"

import sys
import logging

logger = logging.getLogger(__name__)

if (sys.platform == 'rp2'):
    import _thread as thread
else:
    import threading as thread

from IAdvertiser import IAdvertiser
from IAdvertisingDevice import IAdvertisingDevice

class Advertiser(IAdvertiser) :
    """
    This is the BaseClass for all Advertiser classes.
    It implements the interface IAdvertiser.
    """

    def __init__(self):
        """
        initializes the object and defines the member fields
        """
        logger.debug(f"Advertiser.__init__")

        # dictionary to administer the registered AdvertisingDevices.
        # * key is the instance of the AdvertisingDevice
        # * value is the AdvertisementIdentifier of the AdvertisingDevice
        self._registeredDeviceTable = dict()

        if (sys.platform == 'rp2'):
            self._registeredDeviceTable_Lock = thread.allocate_lock()
        else:
            self._registeredDeviceTable_Lock = thread.Lock()
        return


    async def AdvertisementStop(self) -> None:
        """
        stop bluetooth advertising for the Advertiser
        """
        logger.debug(f"Advertiser.AdvertisementStop")

        return


    async def TryRegisterAdvertisingDevice(self, advertisingDevice: IAdvertisingDevice) -> bool:
        """
        try to register the given AdvertisingDevice
        * returns True if the AdvertisingDevice was registered successfully
        * returns False if the AdvertisingDevice wasn't registered successfully (because it still was registered)
        """
        logger.debug(f"Advertiser.TryRegisterAdvertisingDevice")

        if(advertisingDevice is None):
            return False

        try:
            # acquire lock for table
            #self._registeredDeviceTable_Lock.acquire(blocking=True)
            self._registeredDeviceTable_Lock.acquire()

            if(advertisingDevice in self._registeredDeviceTable):
                return False
            else:
                self._registeredDeviceTable[advertisingDevice] = advertisingDevice.GetAdvertisementIdentifier()
                return True
        finally:
            # release lock for table
            self._registeredDeviceTable_Lock.release()


    async def TryUnregisterAdvertisingDevice(self, advertisingDevice: IAdvertisingDevice) -> bool:
        """
        try to unregister the given AdvertisingDevice
        * returns True if the AdvertisingDevice was unregistered successfully
        * returns False if the AdvertisingDevice wasn't unregistered successfully
        """
        logger.debug(f"Advertiser.TryUnregisterAdvertisingDevice")

        if(advertisingDevice is None):
            return False

        try:
            # acquire lock for table
            #self._registeredDeviceTable_Lock.acquire(blocking=True)
            self._registeredDeviceTable_Lock.acquire()

            if(advertisingDevice in self._registeredDeviceTable):
                self._registeredDeviceTable.pop(advertisingDevice)
                return True
            else:
                return False
        finally:
            # release lock for table
            self._registeredDeviceTable_Lock.release()


    async def AdvertisementDataSet(self, advertisementIdentifier: str, manufacturerId: bytes, rawdata: bytes) -> None:
        """
        Sets Advertisement-Data for a specific AdvertisementIdentifier
        This Methode has to be overridden by the implementation of the AdvertisingDevice!
        """
        logger.debug(f"Advertiser.AdvertisementDataSet")

        return
