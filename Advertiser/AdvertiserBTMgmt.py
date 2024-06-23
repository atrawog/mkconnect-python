""" This class is a Bluetooth Advertiser using the 'btmgmt'-tool on linux to set the advertisement data
"""

import sys
import logging
import asyncio
import subprocess
import time

sys.path.append("Advertiser") 
from IAdvertisingDevice import IAdvertisingDevice
from Advertiser.Advertiser import Advertiser

__author__ = "J0EK3R"
__version__ = "0.1"


logger = logging.getLogger(__name__)


class AdvertiserBTMgmt(Advertiser) :
    """ This class is a Bluetooth Advertiser using the 'btmgmt'-tool on linux to set the advertisement data
    """

    # protected static field
    _BTMgmt_path: str = '/usr/bin/btmgmt'

    # Number of repetitions per second
    _RepetitionsPerSecond: int = 4


    def __init__(self):
        """ initializes the object and defines the member fields
        """
        super().__init__() # call baseclass

        logger.debug("AdvertiserBTMgmt.__init__")

        self._advertisement_task_Run: bool = False
        self._advertisement_task = None
        self._advertisement_task_Lock: asyncio.Lock = asyncio.Lock()

        # Table
        # * key: AdvertisementIdentifier
        # * value: advertisement-command for the call of btmgmt tool
        self._advertisementTable_Lock: asyncio.Lock = asyncio.Lock()
        self._advertisementTable: dict = dict()
        
        self._last_set_advertisementCommand = None

        return


    async def try_register_advertising_device(self, advertisingDevice: IAdvertisingDevice) -> bool:
        """ try to register the given AdvertisingDevice
        * returns true if the AdvertisingDevice was registered successfully
        * returns false if the AdvertisingDevice wasn't registered successfully (because it still was registered)

        :param advertisingDevice: the advertising device to register
        :return: returns true if success
        """
        result = await super().try_register_advertising_device(advertisingDevice)

        logger.debug("AdvertiserBTMgmt.try_register_advertising_device")

        # AdvertisingDevice was registered successfully in baseclass
        if(result):
            # register AdvertisingIdentifier -> only registered AdvertisingIdentifier will be sent
            advertisementIdentifier = advertisingDevice.get_advertisement_identifier()
            await self._register_advertisementIdentifier(advertisementIdentifier)

        return result


    async def try_unregister_advertising_device(self, advertisingDevice: IAdvertisingDevice) -> bool:
        """ try to unregister the given AdvertisingDevice
        * returns True if the AdvertisingDevice was unregistered successfully
        * returns False if the AdvertisingDevice wasn't unregistered successfully

        :param advertisingDevice: the advertising device to unregister
        :return: returns true if success
        """
        result = await super().try_unregister_advertising_device(advertisingDevice)

        logger.debug("AdvertiserBTMgmt.try_unregister_advertising_device")

        # AdvertisingDevice was unregistered successfully in baseclass
        if(result):
            # unregister AdvertisementIdentifier to remove from publishing
            advertisementIdentifier = advertisingDevice.get_advertisement_identifier()
            await self._unregister_advertisementIdentifier(advertisementIdentifier)

        return result


    async def advertisement_stop(self) -> None:
        """ stop bluetooth advertising

        :return: returns nothing
        """
        logger.debug("AdvertiserBTMgmt.advertisement_stop")

        # stop publishing thread
        self._advertisement_task_Run = False
        if(self._advertisement_task is not None):
            await self._advertisement_task
            self._advertisement_task = None

        #self._advertisementTable.clear()

        advertisementCommand = self._BTMgmt_path + ' rm-adv 1' + ' &> /dev/null'
        subprocess.run(advertisementCommand, shell=True, executable="/bin/bash")

        logger.debug(f"AdvertiserBTMgmnt.advertisement_stop: command='{advertisementCommand}'")

        return


    async def _register_advertisementIdentifier(self, advertisementIdentifier: str) -> None:
        """ Register AdvertisementIdentifier

        :param advertisementIdentifier: the advertisementIdentifier to register
        :return: returns nothing
        """
        logger.debug("AdvertiserBTMgmt._register_advertisementIdentifier")

        async with self._advertisementTable_Lock:
            if(not advertisementIdentifier in self._advertisementTable):
                self._advertisementTable[advertisementIdentifier] = None

        return


    async def _unregister_advertisementIdentifier(self, advertisementIdentifier: str) -> None:
        """ Unregister AdvertisementIdentifier

        :param advertisementIdentifier: the advertisementIdentifier to unregister
        :return: returns nothing
        """
        logger.debug("AdvertiserBTMgmt._unregister_advertisementIdentifier")

        async with self._registeredDeviceTable_Lock:
            foundAdvertisementIdentifier = False

            # there are devices wich share the same AdvertisementIdentifier
            # check if AdvertisementIdentifier is still present
            for currentAdvertisementIdentifier in self._registeredDeviceTable.values():
                if(currentAdvertisementIdentifier == advertisementIdentifier):
                    foundAdvertisementIdentifier = True
                    break
                    
            if(not foundAdvertisementIdentifier):
                await self._remove_advertisementIdentifier(advertisementIdentifier)

        return

    async def _remove_advertisementIdentifier(self, advertisementIdentifier: str) -> None:
        """ Remove AdvertisementIdentifier

        :param advertisementIdentifier: the advertisementIdentifier to remove
        :return: returns nothing
        """
        logger.debug("AdvertiserBTMgmt._remove_advertisementIdentifier")

        async with self._advertisementTable_Lock:
            if(advertisementIdentifier in self._advertisementTable):
                self._advertisementTable.pop(advertisementIdentifier)

        if(len(self._advertisementTable) == 0):
            await self.advertisement_stop()

        return

    async def set_advertisement_data(self, advertisementIdentifier: str, manufacturerId: bytes, rawdata: bytes) -> None:
        """ Set Advertisement data

        :param advertisementIdentifier: the advertisementIdentifier
        :param manufacturerId: manufacturerId
        :param rawdata: rawdata
        :return: returns nothing
        """
        logger.debug("AdvertiserBTMgmt.set_advertisement_data")

        async with self._advertisementTable_Lock:
            
            # only registered AdvertisementIdentifier are handled
            if(advertisementIdentifier in self._advertisementTable):
                advertisementCommand = self._BTMgmt_path + ' add-adv -d ' + self._create_telegram_for_BTMgmmt(manufacturerId, rawdata) + ' --general-discov 1' + ' &> /dev/null'
                self._advertisementTable[advertisementIdentifier] = advertisementCommand

                # for quick change handle immediately
                timeSlot = self._calc_timeSlot_s()
                await self._advertise(advertisementCommand, timeSlot)

        # start publish thread if necessary
        if(not self._advertisement_task_Run):
            self._advertisement_task = asyncio.create_task(self._publish_loop())
            self._advertisement_task_Run = True

            logger.debug('AdvertiserBTMgmnt.set_advertisement_data: task created')

        return


    async def _publish_loop(self) -> None:
        """ publishing loop

        :return: returns nothing
        """
        logger.debug("AdvertiserBTMgmt._publish_loop started")

        # loop while field is True
        while(self._advertisement_task_Run):
            try:
                
                async with self._advertisementTable_Lock:

                    # make a copy of the table to release the lock as quick as possible
                    copy_of_advertisementTable = self._advertisementTable.copy()

                    # calc time for one publishing slot
                    timeSlot = self._calc_timeSlot_s()
                
                if(len(copy_of_advertisementTable) == 0):
                    pass
                else:
                    for key, advertisementCommand in copy_of_advertisementTable.items():
                        # stop publishing?
                        if(not self._advertisement_task_Run):
                            return

                        await self._advertise(advertisementCommand, timeSlot)
            except:
                pass


    async def _advertise(self, advertisementCommand: str, timeSlot: float) -> None:
        """ calls the btmgmt tool as subprocess

        :return: returns nothing
        """
        logger.debug("AdvertiserBTMgmt._Advertise")

        async with self._advertisement_task_Lock:
            timeStart = time.time()    

            if (self._last_set_advertisementCommand != advertisementCommand):
                self._last_set_advertisementCommand = advertisementCommand

                subprocess.run(advertisementCommand, shell=True, executable="/bin/bash")

            timeEnd = time.time()    
            timeDelta = timeEnd - timeStart
            timeSlotRemain = max(0.001, timeSlot - timeDelta)

            # stop publishing?
            if(self._advertisement_task_Run):
                await asyncio.sleep(timeSlotRemain)

        return


    def _calc_timeSlot_s(self) -> float:
        """ Calculates the timespan in seconds for each timeslot

        :return: returns the timespan for the slot in seconds
        """

        # timeSlot = 1 second / repetitionsPerSecond / len(self._advertisementTable)
        timeSlot = 1 / self._RepetitionsPerSecond / max(1, len(self._advertisementTable))
        return timeSlot


    def _create_telegram_for_BTMgmmt(self, manufacturerId: bytes, rawDataArray: bytes) -> str:
        """ Create input data for btmgmt 

        :return: returns the command string
        """
        rawDataArrayLen = len(rawDataArray)
        
        resultArray = bytearray(4 + rawDataArrayLen)
        resultArray[0] = rawDataArrayLen + 3 # len
        resultArray[1] = 0xFF                # type manufacturer specific
        resultArray[2] = manufacturerId[1]   # companyId
        resultArray[3] = manufacturerId[0]   # companyId
        for index in range(rawDataArrayLen):
            resultArray[index + 4] = rawDataArray[index]

        return ''.join(f'{x:02x}' for x in resultArray)
