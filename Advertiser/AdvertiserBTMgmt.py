__author__ = "J0EK3R"
__version__ = "0.1"

import sys

sys.path.append("Tracer") 
from Tracer.Tracer import Tracer

sys.path.append("Advertiser") 
from IAdvertisingDevice import IAdvertisingDevice
from Advertiser.Advertiser import Advertiser

import subprocess
import threading
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
        
        self._advertisement_thread_Run = False
        self._advertisement_thread = None
        self._advertisement_thread_Lock = threading.Lock()

        # Table
        # * key: AdvertisementIdentifier
        # * value: advertisement-command for the call of btmgmt tool
        self._advertisementTable_thread_Lock = threading.Lock()
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

        # AdvertisingDevice was registered successfully in baseclass
        if(result):
            # register AdvertisindIdentifier -> only registered AdvertisindIdentifier will be sent
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

        # AdvertisingDevice was unregistered successfully in baseclass
        if(result):
            # unregister AdvertisementIdentifier to remove from publishing
            advertisementIdentifier = advertisingDevice.GetAdvertisementIdentifier()
            self._UnregisterAdvertisementIdentifier(advertisementIdentifier)

        return result


    def AdvertisementStop(self):
        """
        stop bluetooth advertising
        """

        # stop publishing thread
        self._advertisement_thread_Run = False
        if(self._advertisement_thread is not None):
            self._advertisement_thread.join()
            self._advertisement_thread = None

        #self._advertisementTable.clear()

        advertisementCommand = self._BTMgmt_path + ' rm-adv 1' + ' &> /dev/null'
        subprocess.run(advertisementCommand, shell=True, executable="/bin/bash")

        if (self._tracer is not None):
            self._tracer.TraceInfo('AdvertiserBTMgmnt.AdvertisementStop')
            self._tracer.TraceInfo(advertisementCommand)

        return


    def _RegisterAdvertisementIdentifier(self, advertisementIdentifier: str):
        """
        Register AdvertisementIdentifier
        """

        try:
            self._advertisementTable_thread_Lock.acquire(blocking=True)

            if(not advertisementIdentifier in self._advertisementTable):
                self._advertisementTable[advertisementIdentifier] = None
        finally:
            self._advertisementTable_thread_Lock.release()

        return


    def _UnregisterAdvertisementIdentifier(self, advertisementIdentifier: str):
        """
        Unregister AdvertisementIdentifier
        """
        try:
            self._registeredDeviceTable_Lock.acquire(blocking=True)

            foundAdvertisementIdentifier = False

            # there are devices wich share the same AdvertisementIdentifier
            # check if AdvertisementIdentifier is still present
            for currentAdvertisementIdentifier in self._registeredDeviceTable.values():
                if(currentAdvertisementIdentifier == advertisementIdentifier):
                    foundAdvertisementIdentifier = True
                    break
                    
            if(not foundAdvertisementIdentifier):
                self._RemoveAdvertisementIdentifier(advertisementIdentifier)

        finally:
            self._registeredDeviceTable_Lock.release()
        return

    def _RemoveAdvertisementIdentifier(self, advertisementIdentifier: str):
        """
        Remove AdvertisementIdentifier
        """

        try:
            self._advertisementTable_thread_Lock.acquire(blocking=True)

            if(advertisementIdentifier in self._advertisementTable):
                self._advertisementTable.pop(advertisementIdentifier)
            
        finally:
            self._advertisementTable_thread_Lock.release()

        if(len(self._advertisementTable) == 0):
            self.AdvertisementStop()

        return

    def AdvertisementDataSet(self, advertisementIdentifier: str, manufacturerId: bytes, rawdata: bytes):
        """
        Set Advertisement data
        """

        try:
            self._advertisementTable_thread_Lock.acquire(blocking=True)
            
            # only registered AdvertisementIdentifier are handled
            if(advertisementIdentifier in self._advertisementTable):
                advertisementCommand = self._BTMgmt_path + ' add-adv -d ' + self._CreateTelegramForBTMgmmt(manufacturerId, rawdata) + ' --general-discov 1' + ' &> /dev/null'
                self._advertisementTable[advertisementIdentifier] = advertisementCommand

                # for quick change handle immediately
                timeSlot = self._CalcTimeSlot()
                self._Advertise(advertisementCommand, timeSlot)
        finally:
            self._advertisementTable_thread_Lock.release()

        # start publish thread if necessary
        if(not self._advertisement_thread_Run):
            self._advertisement_thread = threading.Thread(target=self._publish)
            self._advertisement_thread.daemon = True
            self._advertisement_thread.start()
            self._advertisement_thread_Run = True

        if (self._tracer is not None):
            self._tracer.TraceInfo('AdvertiserBTMgmnt.AdvertisementSet')

        return


    def _publish(self):
        """
        publishing loop
        """

        if (self._tracer is not None):
            self._tracer.TraceInfo('AdvertiserBTMgmnt._publish')

        # loop while field is True
        while(self._advertisement_thread_Run):
            try:
                try:
                    self._advertisementTable_thread_Lock.acquire(blocking=True)

                    # make a copy of the table to release the lock as quick as possible
                    copy_of_advertisementTable = self._advertisementTable.copy()

                    # calc time for one publishing slot
                    timeSlot = self._CalcTimeSlot()
                finally:
                    self._advertisementTable_thread_Lock.release()
                
                if(len(copy_of_advertisementTable) == 0):
                    pass
                else:
                    for key, advertisementCommand in copy_of_advertisementTable.items():
                        # stop publishing?
                        if(not self._advertisement_thread_Run):
                            return

                        self._Advertise(advertisementCommand, timeSlot)
            except:
                pass


    def _CalcTimeSlot(self) -> float:
        """
        Calculates the timespan in seconds for each timeslot
        """

        # timeSlot = 1 second / repetitionsPerSecond / len(self._advertisementTable)
        timeSlot = 1 / self._RepetitionsPerSecond / max(1, len(self._advertisementTable))
        return timeSlot


    def _Advertise(self, advertisementCommand: str, timeSlot: float):
        """
        calls the btmgmt tool as subprocess
        """

        try:
            self._advertisement_thread_Lock.acquire(blocking=True)
            timeStart = time.time()    

            if (self._lastSetAdvertisementCommand != advertisementCommand):
                self._lastSetAdvertisementCommand = advertisementCommand

                subprocess.run(advertisementCommand, shell=True, executable="/bin/bash")

            timeEnd = time.time()    
            timeDelta = timeEnd - timeStart
            timeSlotRemain = max(0.001, timeSlot - timeDelta)

            # stop publishing?
            if(self._advertisement_thread_Run):
                time.sleep(timeSlotRemain)
        finally:
            self._advertisement_thread_Lock.release()

        return

    def _CreateTelegramForBTMgmmt(self, manufacturerId: bytes, rawDataArray: bytes):
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
