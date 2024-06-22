__author__ = "J0EK3R"
__version__ = "0.1"

import sys
import time
import logging

logger = logging.getLogger(__name__)

if (sys.platform == 'rp2'):
    import _thread as thread
else:
    import threading as thread

sys.path.append("Advertiser") 
from IAdvertisingDevice import IAdvertisingDevice
from Advertiser.Advertiser import Advertiser

try:
    import bluetooth
except ImportError as err:
    print("AdvertiserMicroPython: " + str(err))


class AdvertiserMicroPythonThread(Advertiser) :
    """
    Advertiser using bluetooth library from MicroPython
    """

    # Number of repetitions per second
    _RepetitionsPerSecond = 4


    def __init__(self):
        """
        initializes the object and defines the fields
        """
        super().__init__()

        logger.debug(f"AdvertiserMicroPython.__init__")

        # Activate bluetooth
        try:
            self.ble = bluetooth.BLE()
            self.ble.active(True)
        except Exception as exception:
            self.ble = None
            logger.error("AdvertiserMicroPython.init: " + str(exception))

        self._advertisement_thread_Run = False
        self._advertisement_thread_IsRunning = False
        self._advertisement_thread = None
        self._advertisement_thread_Lock = thread.allocate_lock()

        # Table
        # * key: AdvertisementIdentifier
        # * value: advertisement-command for the call of btmgmt tool
        self._advertisementTable_thread_Lock = thread.allocate_lock()
        self._advertisementTable = dict()
        
        self._lastSetAdvertisementCommand = None

        return


    def TryRegisterAdvertisingDevice(self, advertisingDevice: IAdvertisingDevice) -> bool:
        """
        try to register the given AdvertisingDevice
        * returns True if the AdvertisingDevice was registered successfully
        * returns False if the AdvertisingDevice wasn't registered successfully (because it still was registered)
        """
        result = super().TryRegisterAdvertisingDevice(advertisingDevice)

        logger.debug(f"AdvertiserMicroPython.TryRegisterAdvertisingDevice")

        # AdvertisingDevice was registered successfully in baseclass
        if(result):
            # register AdvertisingIdentifier -> only registered AdvertisingIdentifier will be sent
            advertisementIdentifier = advertisingDevice.GetAdvertisementIdentifier()
            self._RegisterAdvertisementIdentifier(advertisementIdentifier)

        return result


    def TryUnregisterAdvertisingDevice(self, advertisingDevice: IAdvertisingDevice) -> bool:
        """
        try to unregister the given AdvertisingDevice
        * returns True if the AdvertisingDevice was unregistered successfully
        * returns False if the AdvertisingDevice wasn't unregistered successfully
        """
        result = super().TryUnregisterAdvertisingDevice(advertisingDevice)

        logger.debug(f"AdvertiserMicroPython.TryUnregisterAdvertisingDevice")

        # AdvertisingDevice was unregistered successfully in baseclass
        if(result):
            # unregister AdvertisementIdentifier to remove from publishing
            advertisementIdentifier = advertisingDevice.GetAdvertisementIdentifier()
            self._UnregisterAdvertisementIdentifier(advertisementIdentifier)

        return result


    def AdvertisementStop(self) -> None:
        """
        stop bluetooth advertising

        """
        logger.debug(f"AdvertiserMicroPython.AdvertisementStop")

        # stop publishing thread
        self._advertisement_thread_Run = False
        if(self._advertisement_thread is not None):
            while(self._advertisement_thread_IsRunning):
                time.sleep(0.1)
            self._advertisement_thread = None

        if(self.ble is not None):
            self.ble.gap_advertise(None)

            logger.info("AdvertiserMicroPython.AdvertisementStop")
        else:
            logger.info("AdvertiserMicroPython.AdvertisementStop: self.ble is None")

        return


    def _RegisterAdvertisementIdentifier(self, advertisementIdentifier: str) -> None:
        """
        Register AdvertisementIdentifier
        """

        try:
            self._advertisementTable_thread_Lock.acquire()

            if(not advertisementIdentifier in self._advertisementTable):
                self._advertisementTable[advertisementIdentifier] = None

                logger.debug(f"AdvertiserMicroPython._RegisterAdvertisementIdentifier: '{advertisementIdentifier}'")
            else:
                logger.debug(f"AdvertiserMicroPython._RegisterAdvertisementIdentifier: '{advertisementIdentifier}' exists")

        finally:
            self._advertisementTable_thread_Lock.release()

        return


    def _UnregisterAdvertisementIdentifier(self, advertisementIdentifier: str) -> None:
        """
        Unregister AdvertisementIdentifier
        """
        try:
            self._registeredDeviceTable_Lock.acquire()

            foundAdvertisementIdentifier = False

            # there are devices wich share the same AdvertisementIdentifier
            # check if AdvertisementIdentifier is still present
            for currentAdvertisementIdentifier in self._registeredDeviceTable.values():
                if(currentAdvertisementIdentifier == advertisementIdentifier):
                    foundAdvertisementIdentifier = True
                    break
                    
            if(not foundAdvertisementIdentifier):
                self._RemoveAdvertisementIdentifier(advertisementIdentifier)

                logger.info(f"AdvertiserMicroPython._UnregisterAdvertisementIdentifier: '{advertisementIdentifier}'")

            else:
                logger.info(f"AdvertiserMicroPython._UnregisterAdvertisementIdentifier: '{advertisementIdentifier}' not exists")

        finally:
            self._registeredDeviceTable_Lock.release()
        return

    def _RemoveAdvertisementIdentifier(self, advertisementIdentifier: str) -> None:
        """
        Remove AdvertisementIdentifier
        """

        try:
            self._advertisementTable_thread_Lock.acquire()

            if(advertisementIdentifier in self._advertisementTable):
                self._advertisementTable.pop(advertisementIdentifier)
            
                logger.info(f"AdvertiserMicroPython._RemoveAdvertisementIdentifier: '{advertisementIdentifier}'")

            else:
                logger.info(f"AdvertiserMicroPython._RemoveAdvertisementIdentifier: '{advertisementIdentifier}' not exists")

        finally:
            self._advertisementTable_thread_Lock.release()

        if(len(self._advertisementTable) == 0):
            self.AdvertisementStop()

        return
    

    def AdvertisementDataSet(self, advertisementIdentifier: str, manufacturerId: bytes, rawdata: bytes) -> None:
        """
        Set Advertisement data
        """
        try:
            self._advertisementTable_thread_Lock.acquire()
            
            # only registered AdvertisementIdentifier are handled
            if(advertisementIdentifier in self._advertisementTable):
                advertisementCommand = self._CreateTelegramForPicoW(manufacturerId, rawdata)
                self._advertisementTable[advertisementIdentifier] = advertisementCommand

                logger.info(f"AdvertiserMicroPython.AdvertisementDataSet: '{advertisementIdentifier}' changed")

                # for quick change handle immediately
                timeSlot = self._CalcTimeSlot()
                self._Advertise(advertisementCommand, timeSlot)
            else:
                logger.info(f"AdvertiserMicroPython.AdvertisementDataSet: '{advertisementIdentifier}' not registered")
        finally:
            self._advertisementTable_thread_Lock.release()

        # start publish thread if necessary
        if(not self._advertisement_thread_Run):
            self._advertisement_thread_Run = True
            self._advertisement_thread = thread.start_new_thread(self._publishloop, ())
            # self._advertisement_thread.daemon = True
            # self._advertisement_thread.start()

        return


    def _publishloop(self) -> None:
        """
        publishing loop
        """

        logger.info('AdvertiserMicroPython._publishloop: started')

        self._advertisement_thread_IsRunning = True

        # loop while field is True
        loopcounter = 0
        while(self._advertisement_thread_Run):
            logger.debug(f'AdvertiserMicroPython._publishloop: loop[{loopcounter}]')
            try:
                try:
                    logger.debug('AdvertiserMicroPython._publishloop: acquire before')

                    self._advertisementTable_thread_Lock.acquire()

                    logger.debug('AdvertiserMicroPython._publishloop: acquire after')

                    # make a copy of the table to release the lock as quick as possible
                    copy_of_advertisementTable = self._advertisementTable.copy()

                    logger.debug('AdvertiserMicroPython._publishloop: copy')
                finally:
                    self._advertisementTable_thread_Lock.release()
                
                if(len(copy_of_advertisementTable) == 0):
                    logger.debug('AdvertiserMicroPython._publishloop: copy_of_advertisementTable is empty')
                    pass
                else:
                    # calc time for one publishing slot
                    timeSlot = self._CalcTimeSlot()

                    for key, advertisementCommand in copy_of_advertisementTable.items():
                        # stop publishing?
                        if(not self._advertisement_thread_Run):
                            logger.debug('AdvertiserMicroPython._publishloop: quit loop')
                            return

                        self._Advertise(advertisementCommand, timeSlot)
            except:
                pass

            loopcounter = loopcounter + 1

        logger.info('AdvertiserMicroPython._publishloop: exit')
        self._advertisement_thread_IsRunning = False


    def _CalcTimeSlot(self) -> float:
        """
        Calculates the timespan in seconds for each timeslot
        """

        # timeSlot = 1 second / repetitionsPerSecond / len(self._advertisementTable)
        timeSlot = 1 / self._RepetitionsPerSecond / max(1, len(self._advertisementTable))
        return timeSlot


    def _Advertise(self, advertisementCommand: bytes, timeSlot: float) -> None:
        """
        calls the btmgmt tool as subprocess
        """

        try:
            self._advertisement_thread_Lock.acquire()
            timeStart = time.time()    

            logger.debug('AdvertiserMicroPython._Advertise: try')

            if (self._lastSetAdvertisementCommand != advertisementCommand):
                self._lastSetAdvertisementCommand = advertisementCommand
    
                logger.info('AdvertiserMicroPython._Advertise: new command')

                if(self.ble is not None):
                    logger.debug('AdvertiserMicroPython._Advertise: before')

                    self.ble.gap_advertise(100, advertisementCommand)

                    logger.debug('AdvertiserMicroPython._Advertise: after')
                else:
                    logger.debug('AdvertiserMicroPython._Advertise: else')
            else:
                logger.debug('AdvertiserMicroPython._Advertise: no new command')

            timeEnd = time.time()    
            timeDelta = timeEnd - timeStart
            timeSlotRemain = max(0.001, timeSlot - timeDelta)

            # stop publishing?
            if(self._advertisement_thread_Run):
                logger.debug(f'AdvertiserMicroPython._Advertise: sleep: {str(timeSlotRemain)} s')
                time.sleep(timeSlotRemain)

        except Exception as err:
            logger.warning(f"AdvertiserMicroPython._Advertise: except '{str(err)}'")
        finally:
            logger.debug('AdvertiserMicroPython._Advertise: finally')

            self._advertisement_thread_Lock.release()
        return
    

    def _CreateTelegramForPicoW(self, manufacturerId: bytes, rawDataArray: bytes) -> bytes:
        """
        Create input data for bluetooth lib for Pico W 
        """
        rawDataArrayLen = len(rawDataArray)

        btdata = bytearray(2 + rawDataArrayLen)
        btdata[0] = manufacturerId[1]
        btdata[1] = manufacturerId[0]
        for index in range(rawDataArrayLen):
            btdata[index + 2] = rawDataArray[index]

        btcrypteddata = bytearray(b'\x02\x01\x02') + bytearray((len(btdata) + 1, 0xFF)) + btdata

        return bytes(btcrypteddata)

