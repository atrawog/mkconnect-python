__author__ = "J0EK3R"
__version__ = "0.1"

import sys

sys.path.append("Tracer") 
from Tracer.Tracer import Tracer

sys.path.append("Advertiser") 
from Advertiser.Advertiser import Advertiser

import subprocess
import platform

class AdvertiserHCITool(Advertiser) :
    """
    baseclass
    """

    def __init__(self):
        """
        initializes the object and defines the fields
        """

        super().__init__()
        self._hcitool_path = '/usr/bin/hcitool'

    def BlueToothStop(tracer: Tracer=None):
        """
        stop bluetooth advertising
        """
        pass

    def AdvertismentStop(self, tracer: Tracer=None):
        """
        stop bluetooth advertising
        """
        hcitool_args1 = self._hcitool_path + ' -i hci0 cmd 0x08 0x000a 00' + ' &> /dev/null'

        if platform.system() == 'Linux':
            subprocess.run(hcitool_args1, shell=True, executable="/bin/bash")

        if (tracer != None):
            tracer.TraceInfo('Connect command :')
            tracer.TraceInfo(hcitool_args1)

        return

    def AdvertisementStart(self, identifier: str, manufacturerId: bytes, rawdata: bytes, tracer: Tracer=None):
        """
        send the bluetooth connect telegram to switch the MouldKing hubs in bluetooth mode
        press the button on the hub(s) and the flashing of status led should switch from blue-green to blue
        """
        hcitool_args1 = self._hcitool_path + ' -i hci0 cmd 0x08 0x0008 ' + self._CreateTelegramForHCITool(manufacturerId, rawdata)
        hcitool_args2 = self._hcitool_path + ' -i hci0 cmd 0x08 0x0006 A0 00 A0 00 03 00 00 00 00 00 00 00 00 07 00'
        hcitool_args3 = self._hcitool_path + ' -i hci0 cmd 0x08 0x000a 01'

        if platform.system() == 'Linux':
            subprocess.run(hcitool_args1 + ' &> /dev/null', shell=True, executable="/bin/bash")
            subprocess.run(hcitool_args2 + ' &> /dev/null', shell=True, executable="/bin/bash")
            subprocess.run(hcitool_args3 + ' &> /dev/null', shell=True, executable="/bin/bash")

        if (tracer != None):
            tracer.TraceInfo(str(hcitool_args1))
            tracer.TraceInfo(str(hcitool_args2))
            tracer.TraceInfo(str(hcitool_args3))

        return

    def AdvertisementSet(self, identifier: str, manufacturerId: bytes, rawdata: bytes, tracer: Tracer=None):
        """
        Set Advertisment data
        """
        hcitool_args = self._hcitool_path + ' -i hci0 cmd 0x08 0x0008 ' + self._CreateTelegramForHCITool(manufacturerId, rawdata)

        if platform.system() == 'Linux':
            subprocess.run(hcitool_args + ' &> /dev/null', shell=True, executable="/bin/bash")

        if (tracer != None):
            tracer.TraceInfo(str(hcitool_args) + '\n')

        return

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
