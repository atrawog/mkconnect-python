__author__ = "J0EK3R"
__version__ = "0.1"

import sys

sys.path.append("Tracer") 
from Tracer.Tracer import Tracer

sys.path.append("Advertiser") 
from Advertiser.Advertiser import Advertiser

import subprocess
import threading
import time

class AdvertiserBTMgmt(Advertiser) :
    """
    baseclass
    """

    BTMgmt_path = '/usr/bin/btmgmt'

    def __init__(self):
        """
        initializes the object and defines the fields
        """

        super().__init__()
        
        self._isInitialized = False
        self._ad_thread_Run = False
        self._ad_thread = None
        self._ad_thread_Lock = threading.Lock()
        self._advertisementTable_thread_Lock = threading.Lock()
        self._advertisementTable = dict()
        self._lastSetAdvertisementCommand = None

        return

    def AdvertisementStop_(self):
        """
        stop bluetooth advertising
        """

        self._ad_thread_Run = False
        if(self._ad_thread is not None):
            self._ad_thread.join()
            self._ad_thread = None
            self._isInitialized = False

        if (self._tracer is not None):
            self._tracer.TraceInfo('AdvertiserBTMgmt.AdvertisementStop')

        for key, advertisementNumber in self._advertisementTable.items():
            advertisementCommand = self.BTMgmt_path + ' rm-adv ' + str(advertisementNumber)
            subprocess.run(advertisementCommand + ' &> /dev/null', shell=True, executable="/bin/bash")

            if (self._tracer is not None):
                self._tracer.TraceInfo(advertisementCommand)

        self._advertisementTable.clear()
        return

    def _AdvertisementSet_(self, identifier: str, manufacturerId: bytes, rawdata: bytes):
        """
        Set Advertisement data
        """

        try:
            self._advertisementTable_thread_Lock.acquire(blocking=True)
            advertisementNumber = self._advertisementTable.get(identifier)
            if(advertisementNumber is None):
                advertisementNumber = len(self._advertisementTable) + 1
                self._advertisementTable[identifier] = advertisementNumber
        finally:
            self._advertisementTable_thread_Lock.release()

        advertisementCommand = self.BTMgmt_path + ' add-adv -d ' + self._CreateTelegramForBTMgmmt(manufacturerId, rawdata) + ' --general-discov ' + str(advertisementNumber)
        subprocess.run(advertisementCommand + ' &> /dev/null', shell=True, executable="/bin/bash")

        if (self._tracer is not None):
            self._tracer.TraceInfo(advertisementCommand)

        # if(not self._ad_thread_Run):
        #     self._ad_thread = threading.Thread(target=self._publish)
        #     self._ad_thread.daemon = True
        #     self._ad_thread.start()
        #     self._ad_thread_Run = True

        if (self._tracer is not None):
            self._tracer.TraceInfo('AdvertiserBTMgmt.AdvertisementSet')

        return

    def AdvertisementStop(self):
        """
        stop bluetooth advertising
        """

        self._ad_thread_Run = False
        if(self._ad_thread is not None):
            self._ad_thread.join()
            self._ad_thread = None
            self._isInitialized = False

        self._advertisementTable.clear()

        hcitool_args_0x08_0x000a = self.BTMgmt_path + ' rm-adv 1'

        subprocess.run(hcitool_args_0x08_0x000a + ' &> /dev/null', shell=True, executable="/bin/bash")

        if (self._tracer is not None):
            self._tracer.TraceInfo('AdvertiserBTMgmnt.AdvertisementStop')
            self._tracer.TraceInfo(hcitool_args_0x08_0x000a)

        return

    def _AdvertisementSet(self, identifier: str, manufacturerId: bytes, rawdata: bytes):
        """
        Set Advertisement data
        """

        advertisementCommand = self.BTMgmt_path + ' add-adv -d ' + self._CreateTelegramForBTMgmmt(manufacturerId, rawdata) + ' --general-discov 1' + ' &> /dev/null'
        try:
            self._advertisementTable_thread_Lock.acquire(blocking=True)
            self._advertisementTable[identifier] = advertisementCommand
        finally:
            self._advertisementTable_thread_Lock.release()

        timeSlot = self._CalcTimeSlot()
        self._Advertise(advertisementCommand, timeSlot)

        if(not self._ad_thread_Run):
            self._ad_thread = threading.Thread(target=self._publish)
            self._ad_thread.daemon = True
            self._ad_thread.start()
            self._ad_thread_Run = True

        if (self._tracer is not None):
            self._tracer.TraceInfo('AdvertiserBTMgmnt.AdvertisementSet')

        return

    def _publish(self):
        if (self._tracer is not None):
            self._tracer.TraceInfo('AdvertiserBTMgmnt._publish')

        while(self._ad_thread_Run):
            try:
                try:
                    self._advertisementTable_thread_Lock.acquire(blocking=True)
                    copy_of_advertisementTable = self._advertisementTable.copy()
                finally:
                    self._advertisementTable_thread_Lock.release()
                
                timeSlot = self._CalcTimeSlot()

                for key, advertisementCommand in copy_of_advertisementTable.items():
                    # stop publishing?
                    if(not self._ad_thread_Run):
                        return

                    self._Advertise(advertisementCommand, timeSlot)
            except:
                pass
    def _CalcTimeSlot(self) -> float:
        # We want to repeat each command 
        repetitionsPerSecond = 4
        # timeSlot = 1 second / repetitionsPerSecond / len(self._advertisementTable)
        timeSlot = 1 / repetitionsPerSecond / max(1, len(self._advertisementTable))
        return timeSlot

    def _Advertise(self, advertisementCommand: str, timeSlot: float):
        try:
            self._ad_thread_Lock.acquire(blocking=True)
            timeStart = time.time()    

            if (self._lastSetAdvertisementCommand != advertisementCommand):
                self._lastSetAdvertisementCommand = advertisementCommand

                subprocess.run(advertisementCommand, shell=True, executable="/bin/bash")

                if(not self._isInitialized):
                    self._isInitialized = True

            timeEnd = time.time()    
            timeDelta = timeEnd - timeStart
            timeSlotRemain = max(0.001, timeSlot - timeDelta)

            # stop publishing?
            if(self._ad_thread_Run):
                time.sleep(timeSlotRemain)
        finally:
            self._ad_thread_Lock.release()

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
