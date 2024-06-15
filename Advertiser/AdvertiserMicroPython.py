__author__ = "J0EK3R"
__version__ = "0.1"

import sys
import time

if (sys.platform == 'rp2'):
    import _thread as thread
else:
    import threading as thread

sys.path.append("Tracer") 
from Tracer.Tracer import Tracer

sys.path.append("Advertiser") 
from IAdvertisingDevice import IAdvertisingDevice
from Advertiser.Advertiser import Advertiser

try:
    import bluetooth
except ImportError as err:
    print("AdvertiserMicroPython: " + str(err))

class AdvertiserMicroPython(Advertiser) :
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

        # Activate bluetooth
        try:
            self.ble = bluetooth.BLE()
            self.ble.active(True)
        except Exception as exception:
            self.ble = None
            print("AdvertiserMicroPython.init: " + str(exception))

        self._advertisement_thread_Run = False
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

        # stop publishing thread
        self._advertisement_thread_Run = False
        if(self._advertisement_thread is not None):
            self._advertisement_thread.join()
            self._advertisement_thread = None

        if(self.ble is not None):
            self.ble.gap_advertise(None)

            if (self._tracer is not None):
                self._tracer.TraceInfo("AdvertiserMicroPython.AdvertisementStop")
        else:
            if (self._tracer is not None):
                self._tracer.TraceInfo("AdvertiserMicroPython.AdvertisementStop: self.ble is None")

        if (self._tracer is not None):
            pass

        return


    def _RegisterAdvertisementIdentifier(self, advertisementIdentifier: str) -> None:
        """
        Register AdvertisementIdentifier
        """

        try:
            self._advertisementTable_thread_Lock.acquire()

            if(not advertisementIdentifier in self._advertisementTable):
                self._advertisementTable[advertisementIdentifier] = None

                if (self._tracer is not None):
                    self._tracer.TraceInfo("AdvertiserMicroPython._RegisterAdvertisementIdentifier: " + advertisementIdentifier)
            else:
                if (self._tracer is not None):
                    self._tracer.TraceInfo("AdvertiserMicroPython._RegisterAdvertisementIdentifier: " + advertisementIdentifier + " exists")

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

                if (self._tracer is not None):
                    self._tracer.TraceInfo("AdvertiserMicroPython._UnregisterAdvertisementIdentifier: " + advertisementIdentifier)

            else:
                if (self._tracer is not None):
                    self._tracer.TraceInfo("AdvertiserMicroPython._UnregisterAdvertisementIdentifier: " + advertisementIdentifier + " not exists")

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
            
                if (self._tracer is not None):
                    self._tracer.TraceInfo("AdvertiserMicroPython._RemoveAdvertisementIdentifier: " + advertisementIdentifier)

            else:
                if (self._tracer is not None):
                    self._tracer.TraceInfo("AdvertiserMicroPython._RemoveAdvertisementIdentifier: " + advertisementIdentifier + " not exists")

        finally:
            self._advertisementTable_thread_Lock.release()

        if(len(self._advertisementTable) == 0):
            self.AdvertisementStop()

        return
    

    def AdvertisementDataSet(self, advertisementIdentifier: str, manufacturerId: bytes, rawdata: bytes) -> None:
        """
        Set Advertisement data
        """
        # data = self._CreateTelegramForPicoW(manufacturerId, rawdata)

        # if(self.ble is not None):
        #     self.ble.gap_advertise(100, data)

        #     if (self._tracer is not None):
        #         self._tracer.TraceInfo("AdvertisementSet")
        # else:
        #     if (self._tracer is not None):
        #         self._tracer.TraceInfo("self.ble is None")

        try:
            self._advertisementTable_thread_Lock.acquire()
            
            # only registered AdvertisementIdentifier are handled
            if(advertisementIdentifier in self._advertisementTable):
                advertisementCommand = self._CreateTelegramForPicoW(manufacturerId, rawdata)
                self._advertisementTable[advertisementIdentifier] = advertisementCommand

                if (self._tracer is not None):
                    self._tracer.TraceInfo("AdvertiserMicroPython.AdvertisementDataSet: " + advertisementIdentifier + " changed")

                # for quick change handle immediately
                timeSlot = self._CalcTimeSlot()
                self._Advertise(advertisementCommand, timeSlot)
            else:
                if (self._tracer is not None):
                    self._tracer.TraceInfo("AdvertiserMicroPython.AdvertisementDataSet: " + advertisementIdentifier + " not registered")
        finally:
            self._advertisementTable_thread_Lock.release()

        # start publish thread if necessary
        if(not self._advertisement_thread_Run):
            self._advertisement_thread_Run = True
            self._advertisement_thread = thread.start_new_thread(self._publish, ())
            # self._advertisement_thread.daemon = True
            # self._advertisement_thread.start()

        return


    def _publish(self) -> None:
        """
        publishing loop
        """

        if (self._tracer is not None):
            self._tracer.TraceInfo('AdvertiserMicroPython._publish: started a')
            self._tracer.TraceInfo('AdvertiserMicroPython._publish: started ' + str(self._advertisement_thread_Run))

        # loop while field is True
        while(self._advertisement_thread_Run):
            if (self._tracer is not None):
                self._tracer.TraceInfo('AdvertiserMicroPython._publish: started')
            try:
                try:
                    if (self._tracer is not None):
                        self._tracer.TraceInfo('AdvertiserMicroPython._publish: acquire before')

                    self._advertisementTable_thread_Lock.acquire()

                    if (self._tracer is not None):
                        self._tracer.TraceInfo('AdvertiserMicroPython._publish: acquire after')

                    # make a copy of the table to release the lock as quick as possible
                    copy_of_advertisementTable = self._advertisementTable.copy()

                    if (self._tracer is not None):
                        self._tracer.TraceInfo('AdvertiserMicroPython._publish: copy')

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

            if (self._tracer is not None):
                self._tracer.TraceInfo('AdvertiserMicroPython._publishLoop')

        if (self._tracer is not None):
            self._tracer.TraceInfo('AdvertiserMicroPython._publish: exit')


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

            if (self._tracer is not None):
                self._tracer.TraceInfo('AdvertiserMicroPython._Advertise: try')

            if (self._lastSetAdvertisementCommand != advertisementCommand):
                self._lastSetAdvertisementCommand = advertisementCommand

                if(self.ble is not None):
                    if (self._tracer is not None):
                        self._tracer.TraceInfo('AdvertiserMicroPython._Advertise: before')

                    self.ble.gap_advertise(100, advertisementCommand)

                    if (self._tracer is not None):
                        self._tracer.TraceInfo('AdvertiserMicroPython._Advertise: after')
                else:
                    if (self._tracer is not None):
                        self._tracer.TraceInfo('AdvertiserMicroPython._Advertise: else')

            timeEnd = time.time()    
            timeDelta = timeEnd - timeStart
            timeSlotRemain = max(0.001, timeSlot - timeDelta)

            # stop publishing?
            if(self._advertisement_thread_Run):
                if (self._tracer is not None):
                    self._tracer.TraceInfo('AdvertiserMicroPython._Advertise: sleep: ' + str(timeSlotRemain))
                time.sleep(timeSlotRemain)
        finally:
            self._advertisement_thread_Lock.release()

            if (self._tracer is not None):
                self._tracer.TraceInfo('AdvertiserMicroPython._Advertise: finally')
        return
    

    def _CreateTelegramForPicoW(self, manufacturerId: bytes, rawDataArray: bytes) -> bytes:
        """
        Create input data for bluetooth lib for Pico W 
        """
        rawDataArrayLen = len(rawDataArray)

        btdata = bytearray(2 + rawDataArrayLen)
        btdata[0] = manufacturerId[0]
        btdata[1] = manufacturerId[1]
        for index in range(rawDataArrayLen):
            btdata[index + 2] = rawDataArray[index]

        btcrypteddata = bytearray(b'\x02\x01\x02') + bytearray((len(btdata) + 1, 0xFF)) + btdata

        return bytes(btcrypteddata)

