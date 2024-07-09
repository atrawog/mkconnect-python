"""
Advertiser using bluetooth library from MicroPython
"""

import sys
import time
import asyncio
import logging
try:
    import bluetooth
except ImportError as err:
    print("AdvertiserMicroPython: " + str(err))

sys.path.append("Advertiser") 
from IAdvertisingDevice import IAdvertisingDevice
from Advertiser.Advertiser import Advertiser


__author__ = "J0EK3R"
__version__ = "0.1"


logger = logging.getLogger(__name__)


class AdvertiserMicroPython(Advertiser) :
    """ Advertiser using bluetooth library from MicroPython
    """

    # Number of repetitions per second
    _repetitions_per_second = 50


    def __init__(self):
        """ initializes the object and defines the fields
        """
        super().__init__()

        logger.debug(f"AdvertiserMicroPython.__init__")

        # global loop
        # loop = asyncio.get_running_loop()

        # Activate bluetooth
        try:
            self.ble = bluetooth.BLE()
            self.ble.active(True)
        except Exception as exception:
            self.ble = None
            logger.error("AdvertiserMicroPython.init: " + str(exception))

        self._advertisement_task_Run: bool = False
        self._advertisement_task_IsRunning: bool = False
        self._advertisement_task = None
        self._advertisement_task_Lock: asyncio.Lock = asyncio.Lock()

        # Table
        # * key: AdvertisementIdentifier
        # * value: advertisement-command for the call of btmgmt tool
        self._advertisementTable_Lock: asyncio.Lock = asyncio.Lock()
        self._advertisementTable: dict = dict()
        
        self._last_set_advertisementData = None

        return


    async def try_register_advertising_device(self, advertisingDevice: IAdvertisingDevice) -> bool:
        """ try to register the given AdvertisingDevice
        * returns true if the AdvertisingDevice was registered successfully
        * returns false if the AdvertisingDevice wasn't registered successfully (because it still was registered)

        :param advertisingDevice: the advertising device to register
        :return: returns true if success
        """
        result = await super().try_register_advertising_device(advertisingDevice)

        logger.debug(f"AdvertiserMicroPython.try_register_advertising_device")

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

        logger.debug(f"AdvertiserMicroPython.try_unregister_advertising_device")

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
        logger.debug(f"AdvertiserMicroPython.advertisement_stop")

        # stop publishing thread
        self._advertisement_task_Run = False

        if(self._advertisement_task is not None):
            await self._advertisement_task
            self._advertisement_task = None

        if(self.ble is not None):
            self.ble.gap_advertise(None)

            logger.info("AdvertiserMicroPython.advertisement_stop")
        else:
            logger.info("AdvertiserMicroPython.advertisement_stop: self.ble is None")


    async def _register_advertisementIdentifier(self, advertisementIdentifier: str) -> None:
        """ Register AdvertisementIdentifier

        :param advertisementIdentifier: the advertisementIdentifier to register
        :return: returns nothing
        """

        async with self._advertisementTable_Lock:

            if(not advertisementIdentifier in self._advertisementTable):
                self._advertisementTable[advertisementIdentifier] = None

                logger.debug(f"AdvertiserMicroPython._register_advertisementIdentifier: '{advertisementIdentifier}'")
            else:
                logger.debug(f"AdvertiserMicroPython._register_advertisementIdentifier: '{advertisementIdentifier}' exists")

        return


    async def _unregister_advertisementIdentifier(self, advertisementIdentifier: str) -> None:
        """ Unregister AdvertisementIdentifier

        :param advertisementIdentifier: the advertisementIdentifier to unregister
        :return: returns nothing
        """
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

                logger.info(f"AdvertiserMicroPython._unregister_advertisementIdentifier: '{advertisementIdentifier}'")

            else:
                logger.info(f"AdvertiserMicroPython._unregister_advertisementIdentifier: '{advertisementIdentifier}' not exists")

        return


    async def _remove_advertisementIdentifier(self, advertisementIdentifier: str) -> None:
        """ Remove AdvertisementIdentifier

        :param advertisementIdentifier: the advertisementIdentifier to remove
        :return: returns nothing
        """

        async with self._advertisementTable_Lock:
            if(advertisementIdentifier in self._advertisementTable):
                self._advertisementTable.pop(advertisementIdentifier)
            
                logger.info(f"AdvertiserMicroPython._remove_advertisementIdentifier: '{advertisementIdentifier}'")

            else:
                logger.info(f"AdvertiserMicroPython._remove_advertisementIdentifier: '{advertisementIdentifier}' not exists")

        if(len(self._advertisementTable) == 0):
            await self.advertisement_stop()

        return
    

    async def set_advertisement_data(self, advertisementIdentifier: str, manufacturerId: bytes, rawdata: bytes) -> None:
        """  Set AdvertisementData

        :param advertisementIdentifier: the advertisementIdentifier
        :param manufacturerId: manufacturerId
        :param rawdata: rawdata
        :return: returns nothing
        """
        async with self._advertisementTable_Lock:
            
            # only registered AdvertisementIdentifier are handled
            if(advertisementIdentifier in self._advertisementTable):
                advertisementCommand = self._create_telegram_for_picoW(manufacturerId, rawdata)
                self._advertisementTable[advertisementIdentifier] = advertisementCommand

                logger.info(f"AdvertiserMicroPython.set_advertisement_data: '{advertisementIdentifier}' changed")

                # for quick change handle immediately
                timeSlot = self._calc_timeSlot_s()
                await self._advertise(advertisementCommand, timeSlot)
            else:
                logger.info(f"AdvertiserMicroPython.set_advertisement_data: '{advertisementIdentifier}' not registered")

        # start publish thread if necessary
        if(not self._advertisement_task_Run):
            self._advertisement_task_Run = True
            self._advertisement_task = asyncio.create_task(self._publishloop())

        return


    async def _publishloop(self) -> None:
        """ publishing loop

        :return: returns nothing
        """

        logger.info('AdvertiserMicroPython._publishloop: started')

        self._advertisement_task_IsRunning = True

        # loop while field is True
        loopcounter = 0
        while(self._advertisement_task_Run):
            try:
                async with self._advertisementTable_Lock:
                    # make a copy of the table to release the lock as quick as possible
                    copy_of_advertisementTable = self._advertisementTable.copy()
                
                if(len(copy_of_advertisementTable) == 0):
                    pass
                else:
                    # calc time for one publishing slot
                    timeSlot = self._calc_timeSlot_s()

                    for key, advertisementCommand in copy_of_advertisementTable.items():
                        # stop publishing?
                        if(not self._advertisement_task_Run):
                            logger.debug('AdvertiserMicroPython._publishloop: quit loop')
                            return

                        await self._advertise(advertisementCommand, timeSlot)
            except:
                pass

            loopcounter = loopcounter + 1

        logger.info('AdvertiserMicroPython._publishloop: exit')
        self._advertisement_task_IsRunning = False


    async def _advertise(self, advertisementData: bytes, timeSlot_s: float) -> None:
        """ set advertisement data to to ble

        :param advertisementData: advertisementData
        :param timeSlot_s: timespab for the timeslot
        :return: returns nothing
        """

        async with self._advertisement_task_Lock:
            timeStart = time.time()    

            if (self._last_set_advertisementData != advertisementData):
                self._last_set_advertisementData = advertisementData
    
                logger.debug('AdvertiserMicroPython._advertise: new command')

                if(self.ble is not None):
                    self.ble.gap_advertise(100, advertisementData)
                else:
                    pass
            else:
                logger.debug('AdvertiserMicroPython._advertise: no new command')

            timeEnd = time.time()    
            timeDelta = timeEnd - timeStart
            timeSlotRemain = max(0.001, timeSlot_s - timeDelta)

            # stop publishing?
            if(self._advertisement_task_Run):
                logger.debug(f'AdvertiserMicroPython._advertise: sleep: {str(timeSlotRemain)} s')
                await asyncio.sleep(timeSlotRemain)

        return
    

    def _calc_timeSlot_s(self) -> float:
        """ Calculates the timespan in seconds for each timeslot

        :return: returns the timespan for the slot in seconds
        """

        # timeSlot = 1 second / repetitionsPerSecond / len(self._advertisementTable)
        timeSlot = 1 / self._repetitions_per_second / max(1, len(self._advertisementTable))
        return timeSlot


    def _create_telegram_for_picoW(self, manufacturerId: bytes, rawDataArray: bytes) -> bytes:
        """ Create input data for bluetooth lib for Pico W 

        :param manufacturerId: manufacturerId
        :param rawDataArray: rawDataArray
        :return: returns the rawdata array
        """
        rawDataArrayLen = len(rawDataArray)

        btdata = bytearray(2 + rawDataArrayLen)
        btdata[0] = manufacturerId[1]
        btdata[1] = manufacturerId[0]
        for index in range(rawDataArrayLen):
            btdata[index + 2] = rawDataArray[index]

        btcrypteddata = bytearray(b'\x02\x01\x02') + bytearray((len(btdata) + 1, 0xFF)) + btdata

        return bytes(btcrypteddata)

