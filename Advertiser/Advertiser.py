__author__ = "J0EK3R"
__version__ = "0.1"

import sys
import threading

from IAdvertiser import IAdvertiser
from IAdvertisingDevice import IAdvertisingDevice

sys.path.append("Tracer") 
from Tracer.Tracer import Tracer

class Advertiser(IAdvertiser) :
    """
    This is the BaseClass for all Advertiser classes.
    It implements the interface IAdvertiser.
    """

    def __init__(self):
        """
        initializes the object and defines the member fields
        """
        self._tracer = None

        # dictionary to administer the registered AdvertisingDevices.
        # * key is the instance of the AdvertisingDevice
        # * value is the AdvertisementIdentifier of the AdvertisingDevice
        self._registeredDeviceTable = dict()
        self._registeredDeviceTable_Lock = threading.Lock()
        return


    def SetTracer(self, tracer: Tracer) -> Tracer:
        """
        set tracer object
        """
        self._tracer = tracer
        return tracer


    def AdvertisementStop(self) -> None:
        """
        stop bluetooth advertising for the Advertiser
        """
        return


    def TryRegisterAdvertisingDevice(self, advertisingDevice: IAdvertisingDevice) -> bool:
        """
        try to register the given AdvertisingDevice
        * returns True if the AdvertisingDevice was registered successfully
        * returns False if the AdvertisingDevice wasn't registered successfully (because it still was registered)
        """
        if(advertisingDevice is None):
            return False

        try:
            # acquire lock for table
            self._registeredDeviceTable_Lock.acquire(blocking=True)

            if(advertisingDevice in self._registeredDeviceTable):
                return False
            else:
                self._registeredDeviceTable[advertisingDevice] = advertisingDevice.GetAdvertisementIdentifier()
                return True
        finally:
            # release lock for table
            self._registeredDeviceTable_Lock.release()


    def TryUnregisterAdvertisingDevice(self, advertisingDevice: IAdvertisingDevice) -> bool:
        """
        try to unregister the given AdvertisingDevice
        * returns True if the AdvertisingDevice was unregistered successfully
        * returns False if the AdvertisingDevice wasn't unregistered successfully
        """
        if(advertisingDevice is None):
            return False

        try:
            # acquire lock for table
            self._registeredDeviceTable_Lock.acquire(blocking=True)

            if(advertisingDevice in self._registeredDeviceTable):
                self._registeredDeviceTable.pop(advertisingDevice)
                return True
            else:
                return False
        finally:
            # release lock for table
            self._registeredDeviceTable_Lock.release()


    def AdvertisementDataSet(self, advertisementIdentifier: str, manufacturerId: bytes, rawdata: bytes) -> None:
        """
        Sets Advertisement-Data for a specific AdvertisementIdentifier
        This Methode has to be overridden by the implementation of the AdvertisingDevice!
        """
        return
