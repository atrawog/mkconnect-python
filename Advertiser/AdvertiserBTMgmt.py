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
        self._advertisementTable = dict()

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

    def AdvertisementSet_(self, identifier: str, manufacturerId: bytes, rawdata: bytes):
        """
        Set Advertisement data
        """

        self._ad_thread_Lock.acquire(blocking=True)
        advertisementNumber = self._advertisementTable.get(identifier)
        if(advertisementNumber is None):
            advertisementNumber = len(self._advertisementTable) + 1
            self._advertisementTable[identifier] = advertisementNumber
        self._ad_thread_Lock.release()

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

    def AdvertisementSet(self, identifier: str, manufacturerId: bytes, rawdata: bytes):
        """
        Set Advertisement data
        """

        advertisementCommand = self.BTMgmt_path + ' add-adv -d ' + self._CreateTelegramForBTMgmmt(manufacturerId, rawdata) + ' --general-discov 1'
        self._ad_thread_Lock.acquire(blocking=True)
        self._advertisementTable[identifier] = advertisementCommand
        self._ad_thread_Lock.release()

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

        lastSetAdvertisementCommand = None

        while(self._ad_thread_Run):
            try:
                self._ad_thread_Lock.acquire(blocking=True)
                copy_of_advertisementTable = self._advertisementTable.copy()
                self._ad_thread_Lock.release()
                
                # We want to repeat each command 
                repetitionsPerSecond = 4
                # timeSlot = 1 second / repetitionsPerSecond / len(copy_of_advertisementTable)
                timeSlot = 1 / repetitionsPerSecond / max(1, len(copy_of_advertisementTable))

                for key, advertisementCommand in copy_of_advertisementTable.items():
                    # stop publishing?
                    if(not self._ad_thread_Run):
                        return

                    timeStart = time.time()    

                    if (lastSetAdvertisementCommand != advertisementCommand):
                        subprocess.run(advertisementCommand + ' &> /dev/null', shell=True, executable="/bin/bash")
                        lastSetAdvertisementCommand = advertisementCommand

                        if(not self._isInitialized):
                            # hcitool_args_0x08_0x0006 = self.HCITool_path + ' -i hci0 cmd 0x08 0x0006 A0 00 A0 00 03 00 00 00 00 00 00 00 00 07 00'
                            # hcitool_args_0x08_0x000a = self.HCITool_path + ' -i hci0 cmd 0x08 0x000a 01'

                            # subprocess.run(hcitool_args_0x08_0x0006 + ' &> /dev/null', shell=True, executable="/bin/bash")
                            # subprocess.run(hcitool_args_0x08_0x000a + ' &> /dev/null', shell=True, executable="/bin/bash")

                            # if (self._tracer is not None):
                            #     self._tracer.TraceInfo(str(hcitool_args_0x08_0x0006))
                            #     self._tracer.TraceInfo(str(hcitool_args_0x08_0x000a))
                            #     self._tracer.TraceInfo()
                            
                            self._isInitialized = True

                    timeEnd = time.time()    
                    timeDelta = timeEnd - timeStart
                    timeSlotRemain = max(0.001, timeSlot - timeDelta)

                    # if (self._tracer is not None):
                    #     self._tracer.TraceInfo(str(timeSlotRemain) + " " + str(key) + ": " + str(advertisement))
                        
                    # if (self._tracer is not None):
                    #     self._tracer.TraceInfo(str(timeSlotRemain))

                    time.sleep(timeSlotRemain)
            except:
                pass

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
