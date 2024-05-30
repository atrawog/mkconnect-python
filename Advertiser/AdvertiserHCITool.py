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

class AdvertiserHCITool(Advertiser) :
    """
    baseclass
    """

    HCITool_path = '/usr/bin/hcitool'

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

    def AdvertisementStop(self):
        """
        stop bluetooth advertising
        """

        self._ad_thread_Run = False
        if(self._ad_thread is not None):
            self._ad_thread.join()
            self._ad_thread = None
            self._isInitialized = False

        hcitool_args_0x08_0x000a = self.HCITool_path + ' -i hci0 cmd 0x08 0x000a 00' + ' &> /dev/null'

        subprocess.run(hcitool_args_0x08_0x000a, shell=True, executable="/bin/bash")

        if (self._tracer is not None):
            self._tracer.TraceInfo('AdvertiserHCITool.AdvertisementStop')
            self._tracer.TraceInfo(hcitool_args_0x08_0x000a)

        return

    def AdvertisementSet(self, identifier: str, manufacturerId: bytes, rawdata: bytes):
        """
        Set Advertisement data
        """

        advertisement = self.HCITool_path + ' -i hci0 cmd 0x08 0x0008 ' + self._CreateTelegramForHCITool(manufacturerId, rawdata)
        self._ad_thread_Lock.acquire(blocking=True)
        self._advertisementTable[identifier] = advertisement
        self._ad_thread_Lock.release()

        if(not self._ad_thread_Run):
            self._ad_thread = threading.Thread(target=self._publish)
            self._ad_thread.daemon = True
            self._ad_thread.start()
            self._ad_thread_Run = True

        if (self._tracer is not None):
            self._tracer.TraceInfo('AdvertiserHCITool.AdvertisementSet')

        return

    def _publish(self):
        if (self._tracer is not None):
            self._tracer.TraceInfo('AdvertiserHCITool._publish')

        while(self._ad_thread_Run):
            try:
                self._ad_thread_Lock.acquire(blocking=True)
                advertisementValues = self._advertisementTable.copy()
                self._ad_thread_Lock.release()

                for advertisement in advertisementValues.values():
                    if(not self._ad_thread_Run):
                        return
                        
                    subprocess.run(advertisement + ' &> /dev/null', shell=True, executable="/bin/bash")

                    # if (self._tracer is not None):
                    #     self._tracer.TraceInfo(str(advertisement))

                    if(not self._isInitialized):
                        hcitool_args_0x08_0x0006 = self.HCITool_path + ' -i hci0 cmd 0x08 0x0006 A0 00 A0 00 03 00 00 00 00 00 00 00 00 07 00'
                        hcitool_args_0x08_0x000a = self.HCITool_path + ' -i hci0 cmd 0x08 0x000a 01'

                        subprocess.run(hcitool_args_0x08_0x0006 + ' &> /dev/null', shell=True, executable="/bin/bash")
                        subprocess.run(hcitool_args_0x08_0x000a + ' &> /dev/null', shell=True, executable="/bin/bash")

                        if (self._tracer is not None):
                            self._tracer.TraceInfo(str(hcitool_args_0x08_0x0006))
                            self._tracer.TraceInfo(str(hcitool_args_0x08_0x000a))
                        
                        self._isInitialized = True

                    time.sleep(0.05)
            except:
                pass

    def _CreateTelegramForHCITool(self, manufacturerId: bytes, rawDataArray: bytes):
        """
        Create input data for hcitool 
        """
        rawDataArrayLen = len(rawDataArray)
        
        resultArray = bytearray(8 + rawDataArrayLen)
        resultArray[0] = rawDataArrayLen + 7 # len
        resultArray[1] = 0x02                 # flags
        resultArray[2] = 0x01
        resultArray[3] = 0x02
        resultArray[4] = rawDataArrayLen + 3 # len
        resultArray[5] = 0xFF                # type manufacturer specific
        resultArray[6] = manufacturerId[1]   # companyId
        resultArray[7] = manufacturerId[0]   # companyId
        for index in range(rawDataArrayLen):
            resultArray[index + 8] = rawDataArray[index]

        return ' '.join(f'{x:02x}' for x in resultArray)
