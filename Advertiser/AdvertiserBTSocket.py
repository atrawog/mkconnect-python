__author__ = "J0EK3R"
__version__ = "0.1"

import sys
import enum
import threading
import time
import logging

logger = logging.getLogger(__name__)

from btsocket import btmgmt_socket
from btsocket import btmgmt_protocol

sys.path.append("Advertiser") 
from IAdvertisingDevice import IAdvertisingDevice
from Advertiser.Advertiser import Advertiser


class AdvertiserBTSocket(Advertiser) :
    """
    baseclass
    """

    class Flags(enum.IntEnum):
        CONNECTABLE = enum.auto()
        GENERAL_DISCOVERABLE = enum.auto()
        LIMITED_DISCOVERABLE = enum.auto()
        FLAGS_IN_ADV_DATA = enum.auto()
        TX_IN_ADV_DATA = enum.auto()
        APPEARANCE_IN_ADV_DATA = enum.auto()
        LOCAL_NAME_IN_ADV_DATA = enum.auto()
        PHY_LE_1M = enum.auto()
        PHY_LE_2M = enum.auto()
        PHY_LE_CODED = enum.auto()

    # Number of repetitions per second
    _RepetitionsPerSecond = 4

    def __init__(self):
        """
        initializes the object and defines the member fields
        """
        super().__init__() # call baseclass

        logger.debug("AdvertiserBTSocket.__init__")

        self._advertisement_thread_Run = False
        self._advertisement_thread = None
        self._advertisement_thread_Lock = threading.Lock()

        # Table
        # * key: AdvertisementIdentifier
        # * value: advertisement-command for the call of btmgmt tool
        self._advertisementTable_thread_Lock = threading.Lock()
        self._advertisementTable = dict()
        
        self._lastSetAdvertisementCommand = None

        self.sock = btmgmt_socket.open()

        return


    def TryRegisterAdvertisingDevice(self, advertisingDevice: IAdvertisingDevice) -> bool:
        """
        try to register the given AdvertisingDevice
        * returns True if the AdvertisingDevice was registered successfully
        * returns False if the AdvertisingDevice wasn't registered successfully (because it still was registered)
        """
        result = super().TryRegisterAdvertisingDevice(advertisingDevice)

        logger.debug("AdvertiserBTSocket.TryRegisterAdvertisingDevice")

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

        logger.debug("AdvertiserBTSocket.TryUnregisterAdvertisingDevice")

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

        logger.debug("AdvertiserBTSocket.AdvertisementStop")

        # stop publishing thread
        self._advertisement_thread_Run = False
        if(self._advertisement_thread is not None):
            self._advertisement_thread.join()
            self._advertisement_thread = None

        advertisementCommand = AdvertiserBTSocket._create_rm_advert_command(1)
        self.sock.send(advertisementCommand)

        #     logger.debug(f"AdvertiserBTMgmnt.AdvertisementStop")

        return


    def _RegisterAdvertisementIdentifier(self, advertisementIdentifier: str) -> None:
        """
        Register AdvertisementIdentifier
        """

        logger.debug("AdvertiserBTSocket._RegisterAdvertisementIdentifier")

        try:
            self._advertisementTable_thread_Lock.acquire(blocking=True)

            if(not advertisementIdentifier in self._advertisementTable):
                self._advertisementTable[advertisementIdentifier] = None
        finally:
            self._advertisementTable_thread_Lock.release()

        return


    def _UnregisterAdvertisementIdentifier(self, advertisementIdentifier: str) -> None:
        """
        Unregister AdvertisementIdentifier
        """
        logger.debug("AdvertiserBTSocket._UnregisterAdvertisementIdentifier")

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

    def _RemoveAdvertisementIdentifier(self, advertisementIdentifier: str) -> None:
        """
        Remove AdvertisementIdentifier
        """
        logger.debug("AdvertiserBTSocket._RemoveAdvertisementIdentifier")

        try:
            self._advertisementTable_thread_Lock.acquire(blocking=True)

            if(advertisementIdentifier in self._advertisementTable):
                self._advertisementTable.pop(advertisementIdentifier)
            
        finally:
            self._advertisementTable_thread_Lock.release()

        if(len(self._advertisementTable) == 0):
            self.AdvertisementStop()

        return

    def AdvertisementDataSet(self, advertisementIdentifier: str, manufacturerId: bytes, rawdata: bytes) -> None:
        """
        Set Advertisement data
        """
        logger.debug("AdvertiserBTSocket.AdvertisementDataSet")

        try:
            self._advertisementTable_thread_Lock.acquire(blocking=True)
            
            # only registered AdvertisementIdentifier are handled
            if(advertisementIdentifier in self._advertisementTable):
                # advertisementCommand = self._BTMgmt_path + ' add-adv -d ' + self._CreateTelegramForBTMgmmt(manufacturerId, rawdata) + ' --general-discov 1' + ' &> /dev/null'
                advertisingData = self._CreateAdvertisingDataString(manufacturerId, rawdata)

                advertisementCommand = AdvertiserBTSocket._create_add_advert_command(
                    instance_id=1,
                    flags=AdvertiserBTSocket.Flags.GENERAL_DISCOVERABLE,
                    duration=0x00,  # zero means use default
                    timeout=0x00,  # zero means use default
                    #adv_data='1bfff0ff6DB643CF7E8F471188665938D17AAA26495E131415161718',
                    adv_data=advertisingData,
                    scan_rsp='',                    
                )
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

        logger.debug('AdvertiserBTMgmnt.AdvertisementSet')

        return


    def _publish(self) -> None:
        """
        publishing loop
        """
        logger.debug("AdvertiserBTSocket._publish")

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


    def _Advertise(self, advertisementCommand: str, timeSlot: float) -> None:
        """
        calls the btmgmt tool as subprocess
        """
        logger.debug("AdvertiserBTSocket._publish")

        try:
            self._advertisement_thread_Lock.acquire(blocking=True)
            timeStart = time.time()    

            if (self._lastSetAdvertisementCommand != advertisementCommand):
                self._lastSetAdvertisementCommand = advertisementCommand

                # self.loop.call_soon(self.sock.send, advertisementCommand)
                self.sock.send(advertisementCommand)

            timeEnd = time.time()    
            timeDelta = timeEnd - timeStart
            timeSlotRemain = max(0.001, timeSlot - timeDelta)

            # stop publishing?
            if(self._advertisement_thread_Run):
                time.sleep(timeSlotRemain)
        finally:
            self._advertisement_thread_Lock.release()

        return

    def _CreateAdvertisingDataString(self, manufacturerId: bytes, rawDataArray: bytes) -> str:
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

    @staticmethod
    def _little_bytes(value, size_of):
        return int(value).to_bytes(size_of, byteorder='little')

    @staticmethod
    def _create_add_advert_command(instance_id, flags, duration, timeout, adv_data, scan_rsp):
        """ Add Advertising Command

        Command Code:		0x003e
        Controller Index:	<controller id>
        Command Parameters:	Instance (1 Octet)
                    Flags (4 Octets)
                    Duration (2 Octets)
                    Timeout (2 Octets)
                    Adv_Data_Len (1 Octet)
                    Scan_Rsp_Len (1 Octet)
                    Adv_Data (0-255 Octets)
                    Scan_Rsp (0-255 Octets)
        Return Parameters:	Instance (1 Octet)

        This command is used to configure an advertising instance that
        can be used to switch a Bluetooth Low Energy controller into
        advertising mode.

        Added advertising information with this command will not be visible
        immediately if advertising is enabled via the Set Advertising
        command. The usage of the Set Advertising command takes precedence
        over this command. Instance information is stored and will be
        advertised once advertising via Set Advertising has been disabled.

        The Instance identifier is a value between 1 and the number of
        supported instances. The value 0 is reserved.

        With the Flags value the type of advertising is controlled and
        the following flags are defined:

            0	Switch into Connectable mode
            1	Advertise as Discoverable
            2	Advertise as Limited Discoverable
            3	Add Flags field to Adv_Data
            4	Add TX Power field to Adv_Data
            5	Add Appearance field to Scan_Rsp
            6	Add Local Name in Scan_Rsp
            7	Secondary Channel with LE 1M
            8	Secondary Channel with LE 2M
            9	Secondary Channel with LE Coded

        When the connectable flag is set, then the controller will use
        undirected connectable advertising. The value of the connectable
        setting can be overwritten this way. This is useful to switch a
        controller into connectable mode only for LE operation. This is
        similar to the mode 0x02 from the Set Advertising command.

        When the connectable flag is not set, then the controller will
        use advertising based on the connectable setting. When using
        non-connectable or scannable advertising, the controller will
        be programmed with a non-resolvable random address. When the
        system is connectable, then the identity address or resolvable
        private address will be used.

        Using the connectable flag is useful for peripheral mode support
        where BR/EDR (and/or LE) is controlled by Add Device. This allows
        making the peripheral connectable without having to interfere
        with the global connectable setting.

        If Scan_Rsp_Len is zero and connectable flag is not set and
        the global connectable setting is off, then non-connectable
        advertising is used. If Scan_Rsp_Len is larger than zero and
        connectable flag is not set and the global advertising is off,
        then scannable advertising is used. This small difference is
        supported to provide less air traffic for devices implementing
        broadcaster role.

        Secondary channel flags can be used to advertise in secondary
        channel with the corresponding PHYs. These flag bits are mutually
        exclusive and setting multiple will result in Invalid Parameter
        error. Choosing either LE 1M or LE 2M will result in using
        extended advertising on the primary channel with LE 1M and the
        respectively LE 1M or LE 2M on the secondary channel. Choosing
        LE Coded will result in using extended advertising on the primary
        and secondary channels with LE Coded. Choosing none of these flags
        will result in legacy advertising.

        The Duration parameter configures the length of an Instance. The
        value is in seconds.

        A value of 0 indicates a default value is chosen for the
        Duration. The default is 2 seconds.

        If only one advertising Instance has been added, then the Duration
        value will be ignored. It only applies for the case where multiple
        Instances are configured. In that case every Instance will be
        available for the Duration time and after that it switches to
        the next one. This is a simple round-robin based approach.

        The Timeout parameter configures the life-time of an Instance. In
        case the value 0 is used it indicates no expiration time. If a
        timeout value is provided, then the advertising Instance will be
        automatically removed when the timeout passes. The value for the
        timeout is in seconds. Powering down a controller will invalidate
        all advertising Instances and it is not possible to add a new
        Instance with a timeout when the controller is powered down.

        When a Timeout is provided, then the Duration subtracts from
        the actual Timeout value of that Instance. For example an Instance
        with Timeout of 5 and Duration of 2 will be scheduled exactly 3
        times, twice with 2 seconds and once with one second. Other
        Instances have no influence on the Timeout.

        Re-adding an already existing instance (i.e. issuing the Add
        Advertising command with an Instance identifier of an existing
        instance) will update that instance's configuration.

        An instance being added or changed while another instance is
        being advertised will not be visible immediately but only when
        the new/changed instance is being scheduled by the round robin
        advertising algorithm.

        Changes to an instance that is currently being advertised will
        cancel that instance and switch to the next instance. The changes
        will be visible the next time the instance is scheduled for
        advertising. In case a single instance is active, this means
        that changes will be visible right away.

        A pre-requisite is that LE is already enabled, otherwise this
        command will return a "rejected" response.

        This command can be used when the controller is not powered and
        all settings will be programmed once powered.

        This command generates a Command Complete event on success or a
        Command Status event on failure.

        Possible errors:	Failed
                    Rejected
                    Not Supported
                    Invalid Parameters
                    Invalid Index
        """
        cmd = AdvertiserBTSocket._little_bytes(0x003e, 2)
        ctrl_idx = AdvertiserBTSocket._little_bytes(0x00, 2)
        instance = AdvertiserBTSocket._little_bytes(instance_id, 1)  # (1 Octet)
        flags = AdvertiserBTSocket._little_bytes(flags, 4)  # (4 Octets)
        duration = AdvertiserBTSocket._little_bytes(duration, 2)  # (2 Octets)
        timeout = AdvertiserBTSocket._little_bytes(timeout, 2)  # (2 Octets)
        adv_data = bytes.fromhex(adv_data)  # (0-255 Octets)
        adv_data_len = AdvertiserBTSocket._little_bytes(len(adv_data), 1)  # (1 Octet)
        scan_rsp = bytes.fromhex(scan_rsp)  # (0-255 Octets)
        scan_rsp_len = AdvertiserBTSocket._little_bytes(len(scan_rsp), 1)  # (1 Octet)
        params = instance + flags + duration + timeout + adv_data_len + scan_rsp_len + adv_data + scan_rsp
        param_len = AdvertiserBTSocket._little_bytes(len(params), 2)

        return cmd + ctrl_idx + param_len + params

    @staticmethod
    def _create_rm_advert_command(instance_id):
        """ Remove Advertising Command
    
        Command Code:		0x003f
        Controller Index:	<controller id>
        Command Parameters:	Instance (1 Octet)
        Return Parameters:	Instance (1 Octet)

        This command is used to remove an advertising instance that
        can be used to switch a Bluetooth Low Energy controller into
        advertising mode.

        When the Instance parameter is zero, then all previously added
        advertising Instances will be removed.

        Removing advertising information with this command will not be
        visible as long as advertising is enabled via the Set Advertising
        command. The usage of the Set Advertising command takes precedence
        over this command. Changes to Instance information are stored and
        will be advertised once advertising via Set Advertising has been
        disabled.

        Removing an instance while it is being advertised will immediately
        cancel the instance, even when it has been advertised less then its
        configured Timeout or Duration.

        This command can be used when the controller is not powered and
        all settings will be programmed once powered.

        This command generates a Command Complete event on success or
        a Command Status event on failure.

        Possible errors:	Invalid Parameters
                    Invalid Index
        """

        cmd = AdvertiserBTSocket._little_bytes(0x003f, 2)
        ctrl_idx = AdvertiserBTSocket._little_bytes(0x00, 2)
        instance = AdvertiserBTSocket._little_bytes(instance_id, 1)  # (1 Octet)
        params = instance
        param_len = AdvertiserBTSocket._little_bytes(len(params), 2)

        return cmd + ctrl_idx + param_len + params