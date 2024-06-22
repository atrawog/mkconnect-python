__author__ = "J0EK3R"
__version__ = "0.1"

import sys
import logging
import asyncio

logger = logging.getLogger(__name__)

sys.path.append("Advertiser") 
from IAdvertisingDevice import IAdvertisingDevice
from Advertiser.Advertiser import Advertiser

import subprocess
import time

class AdvertiserBTMgmt(Advertiser) :
    """
    baseclass
    """

    # protected static field
    _BTMgmt_path = '/usr/bin/btmgmt'

    # Number of repetitions per second
    _RepetitionsPerSecond = 4

    def __init__(self):
        """
        initializes the object and defines the member fields
        """
        super().__init__() # call baseclass

        logger.debug("AdvertiserBTMgmt.__init__")

        self._advertisement_task_Run = False
        self._advertisement_task = None
        self._advertisement_task_Lock = asyncio.Lock()

        # Table
        # * key: AdvertisementIdentifier
        # * value: advertisement-command for the call of btmgmt tool
        self._advertisementTable_Lock = asyncio.Lock()
        self._advertisementTable = dict()
        
        self._lastSetAdvertisementCommand = None

        return


    async def TryRegisterAdvertisingDevice(self, advertisingDevice: IAdvertisingDevice) -> bool:
        """
        try to register the given AdvertisingDevice
        * returns True if the AdvertisingDevice was registered successfully
        * returns False if the AdvertisingDevice wasn't registered successfully (because it still was registered)
        """
        result = await super().TryRegisterAdvertisingDevice(advertisingDevice)

        logger.debug("AdvertiserBTMgmt.TryRegisterAdvertisingDevice")

        # AdvertisingDevice was registered successfully in baseclass
        if(result):
            # register AdvertisingIdentifier -> only registered AdvertisingIdentifier will be sent
            advertisementIdentifier = advertisingDevice.GetAdvertisementIdentifier()
            await self._RegisterAdvertisementIdentifier(advertisementIdentifier)

        return result


    async def TryUnregisterAdvertisingDevice(self, advertisingDevice: IAdvertisingDevice) -> bool:
        """
        try to unregister the given AdvertisingDevice
        * returns True if the AdvertisingDevice was unregistered successfully
        * returns False if the AdvertisingDevice wasn't unregistered successfully
        """
        result = await super().TryUnregisterAdvertisingDevice(advertisingDevice)

        logger.debug("AdvertiserBTMgmt.TryUnregisterAdvertisingDevice")

        # AdvertisingDevice was unregistered successfully in baseclass
        if(result):
            # unregister AdvertisementIdentifier to remove from publishing
            advertisementIdentifier = advertisingDevice.GetAdvertisementIdentifier()
            await self._UnregisterAdvertisementIdentifier(advertisementIdentifier)

        return result


    async def AdvertisementStop(self) -> None:
        """
        stop bluetooth advertising
        """
        logger.debug("AdvertiserBTMgmt.AdvertisementStop")

        # stop publishing thread
        self._advertisement_task_Run = False
        if(self._advertisement_task is not None):
            await self._advertisement_task
            self._advertisement_task = None

        #self._advertisementTable.clear()

        advertisementCommand = self._BTMgmt_path + ' rm-adv 1' + ' &> /dev/null'
        subprocess.run(advertisementCommand, shell=True, executable="/bin/bash")

        logger.debug(f"AdvertiserBTMgmnt.AdvertisementStop: command='{advertisementCommand}'")

        return


    async def _RegisterAdvertisementIdentifier(self, advertisementIdentifier: str) -> None:
        """
        Register AdvertisementIdentifier
        """
        logger.debug("AdvertiserBTMgmt._RegisterAdvertisementIdentifier")

        async with self._advertisementTable_Lock:

            if(not advertisementIdentifier in self._advertisementTable):
                self._advertisementTable[advertisementIdentifier] = None

        return


    async def _UnregisterAdvertisementIdentifier(self, advertisementIdentifier: str) -> None:
        """
        Unregister AdvertisementIdentifier
        """
        logger.debug("AdvertiserBTMgmt._UnregisterAdvertisementIdentifier")

        async with self._registeredDeviceTable_Lock:

            foundAdvertisementIdentifier = False

            # there are devices wich share the same AdvertisementIdentifier
            # check if AdvertisementIdentifier is still present
            for currentAdvertisementIdentifier in self._registeredDeviceTable.values():
                if(currentAdvertisementIdentifier == advertisementIdentifier):
                    foundAdvertisementIdentifier = True
                    break
                    
            if(not foundAdvertisementIdentifier):
                await self._RemoveAdvertisementIdentifier(advertisementIdentifier)

        return

    async def _RemoveAdvertisementIdentifier(self, advertisementIdentifier: str) -> None:
        """
        Remove AdvertisementIdentifier
        """
        logger.debug("AdvertiserBTMgmt._RemoveAdvertisementIdentifier")

        async with self._advertisementTable_Lock:

            if(advertisementIdentifier in self._advertisementTable):
                self._advertisementTable.pop(advertisementIdentifier)

        if(len(self._advertisementTable) == 0):
            await self.AdvertisementStop()

        return

    async def AdvertisementDataSet(self, advertisementIdentifier: str, manufacturerId: bytes, rawdata: bytes) -> None:
        """
        Set Advertisement data
        """
        logger.debug("AdvertiserBTMgmt.AdvertisementDataSet")

        async with self._advertisementTable_Lock:
            
            # only registered AdvertisementIdentifier are handled
            if(advertisementIdentifier in self._advertisementTable):
                advertisementCommand = self._BTMgmt_path + ' add-adv -d ' + self._CreateTelegramForBTMgmmt(manufacturerId, rawdata) + ' --general-discov 1' + ' &> /dev/null'
                self._advertisementTable[advertisementIdentifier] = advertisementCommand

                # for quick change handle immediately
                timeSlot = self._CalcTimeSlot()
                await self._Advertise(advertisementCommand, timeSlot)

        # start publish thread if necessary
        if(not self._advertisement_task_Run):
            self._advertisement_task = asyncio.create_task(self._publish)
            self._advertisement_task_Run = True

        logger.debug('AdvertiserBTMgmnt.AdvertisementSet')

        return


    async def _publish(self) -> None:
        """
        publishing loop
        """
        logger.debug("AdvertiserBTMgmt._publish")

        # loop while field is True
        while(self._advertisement_task_Run):
            try:
                
                async with self._advertisementTable_Lock:

                    # make a copy of the table to release the lock as quick as possible
                    copy_of_advertisementTable = self._advertisementTable.copy()

                    # calc time for one publishing slot
                    timeSlot = self._CalcTimeSlot()
                
                if(len(copy_of_advertisementTable) == 0):
                    pass
                else:
                    for key, advertisementCommand in copy_of_advertisementTable.items():
                        # stop publishing?
                        if(not self._advertisement_task_Run):
                            return

                        await self._Advertise(advertisementCommand, timeSlot)
            except:
                pass


    def _CalcTimeSlot(self) -> float:
        """
        Calculates the timespan in seconds for each timeslot
        """

        # timeSlot = 1 second / repetitionsPerSecond / len(self._advertisementTable)
        timeSlot = 1 / self._RepetitionsPerSecond / max(1, len(self._advertisementTable))
        return timeSlot


    async def _Advertise(self, advertisementCommand: str, timeSlot: float) -> None:
        """
        calls the btmgmt tool as subprocess
        """
        logger.debug("AdvertiserBTMgmt._Advertise")

        async with self._advertisement_task_Lock:
            timeStart = time.time()    

            if (self._lastSetAdvertisementCommand != advertisementCommand):
                self._lastSetAdvertisementCommand = advertisementCommand

                subprocess.run(advertisementCommand, shell=True, executable="/bin/bash")

            timeEnd = time.time()    
            timeDelta = timeEnd - timeStart
            timeSlotRemain = max(0.001, timeSlot - timeDelta)

            # stop publishing?
            if(self._advertisement_task_Run):
                await asyncio.sleep(timeSlotRemain)

        return

    def _CreateTelegramForBTMgmmt(self, manufacturerId: bytes, rawDataArray: bytes) -> str:
        """
        Create input data for btmgmt 
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
