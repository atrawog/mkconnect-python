__author__ = "J0EK3R"
__version__ = "0.1"

import sys

sys.path.append("Tracer") 
from Tracer.Tracer import Tracer

sys.path.append("Advertiser") 
from Advertiser.Advertiser import Advertiser

try:
    from gi.repository import GLib, GObject  # python3
except ImportError:
    import gobject as GObject  # python2

import dbus
import dbus.exceptions
import dbus.mainloop.glib
import dbus.service
import time
import threading

dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

BLUEZ_SERVICE_NAME = 'org.bluez'
DBUS_OM_IFACE = 'org.freedesktop.DBus.ObjectManager'
DBUS_PROP_IFACE = 'org.freedesktop.DBus.Properties'
LE_ADVERTISING_MANAGER_IFACE = 'org.bluez.LEAdvertisingManager1'
LE_ADVERTISEMENT_IFACE = 'org.bluez.LEAdvertisement1'

class InvalidArgsException(dbus.exceptions.DBusException):
    _dbus_error_name = 'org.freedesktop.DBus.Error.InvalidArgs'


class NotSupportedException(dbus.exceptions.DBusException):
    _dbus_error_name = 'org.bluez.Error.NotSupported'


class NotPermittedException(dbus.exceptions.DBusException):
    _dbus_error_name = 'org.bluez.Error.NotPermitted'


class InvalidValueLengthException(dbus.exceptions.DBusException):
    _dbus_error_name = 'org.bluez.Error.InvalidValueLength'


class FailedException(dbus.exceptions.DBusException):
    _dbus_error_name = 'org.bluez.Error.Failed'

class Advertisement(dbus.service.Object):
    PATH_BASE = '/org/bluez/example/advertisement'

    def __init__(self, bus, identifier: str, advertising_type):
        self.path = self.PATH_BASE + identifier
        self.bus = bus
        self.ad_type = advertising_type
        self.service_uuids = None
        self.manufacturer_data = None
        self.solicit_uuids = None
        self.service_data = None
        self.local_name = None
        self.include_tx_power = False
        self.discoverable = False
        self.data = None
        dbus.service.Object.__init__(self, bus, self.path)

    def get_properties(self):
        properties = dict()
        properties['Type'] = self.ad_type

        if self.service_uuids is not None:
            properties['ServiceUUIDs'] = dbus.Array(self.service_uuids,
                                                    signature='s')
        if self.solicit_uuids is not None:
            properties['SolicitUUIDs'] = dbus.Array(self.solicit_uuids,
                                                    signature='s')
        if self.manufacturer_data is not None:
            properties['ManufacturerData'] = dbus.Dictionary(
                self.manufacturer_data, signature='qv')
        if self.service_data is not None:
            properties['ServiceData'] = dbus.Dictionary(self.service_data,
                                                        signature='sv')
        if self.local_name is not None:
            properties['LocalName'] = dbus.String(self.local_name)
        if self.include_tx_power:
            properties['Includes'] = dbus.Array(["tx-power"], signature='s')

        if self.discoverable is True:
            properties['Discoverable'] = dbus.Boolean(True)

        if self.data is not None:
            properties['Data'] = dbus.Dictionary(
                self.data, signature='yv')
        return {LE_ADVERTISEMENT_IFACE: properties}

    def get_path(self):
        return dbus.ObjectPath(self.path)

    def add_service_uuid(self, uuid):
        if not self.service_uuids:
            self.service_uuids = []
        self.service_uuids.append(uuid)

    def add_solicit_uuid(self, uuid):
        if not self.solicit_uuids:
            self.solicit_uuids = []
        self.solicit_uuids.append(uuid)

    def add_manufacturer_data(self, manuf_code, data):
        if not self.manufacturer_data:
            self.manufacturer_data = dbus.Dictionary({}, signature='qv')
        self.manufacturer_data[manuf_code] = dbus.Array(data, signature='y')

    def add_service_data(self, uuid, data):
        if not self.service_data:
            self.service_data = dbus.Dictionary({}, signature='sv')
        self.service_data[uuid] = dbus.Array(data, signature='y')

    def add_local_name(self, name):
        if not self.local_name:
            self.local_name = ""
        self.local_name = dbus.String(name)

    def add_data(self, ad_type, data):
        if not self.data:
            self.data = dbus.Dictionary({}, signature='yv')
        self.data[ad_type] = dbus.Array(data, signature='y')

    @dbus.service.method(DBUS_PROP_IFACE,
                        in_signature='s',
                        out_signature='a{sv}')
    def GetAll(self, interface):
        print('GetAll')
        if interface != LE_ADVERTISEMENT_IFACE:
            raise InvalidArgsException()
        print('returning props')
        return self.get_properties()[LE_ADVERTISEMENT_IFACE]

    @dbus.service.method(LE_ADVERTISEMENT_IFACE,
                        in_signature='',
                        out_signature='')
    def Release(self):
        print('%s: Released!' % self.path)

class AdvertiserBluez(Advertiser) :
    """
    AdvertiserBluez
    """

    class TestAdvertisement(Advertisement):

        def __init__(self, bus, identifier: str, manufacturerId, manufacturer_data: bytearray):
            Advertisement.__init__(self, bus, identifier, 'peripheral')
            # Advertisement.__init__(self, bus, index, 'broadcast')
            self.discoverable = True
            # self.add_service_uuid('180D')
            # self.add_service_uuid('180F')
            # self.add_manufacturer_data(0xfff0, [0x00, 0x01, 0x02, 0x03])
            # self.add_manufacturer_data(0xfff0, [0x6D, 0xB6, 0x43, 0xCF, 0x7E, 0x8F, 0x47, 0x11, 
            #                                     0x88, 0x66, 0x59, 
            #                                     0x38, 0xD1, 0x7A, 0xAA, 
            #                                     0x26, 
            #                                     0x49, 0x5E, 
            #                                     0x13, 0x14, 0x15, 0x16, 0x17, 0x18])
            self.add_manufacturer_data(int.from_bytes(manufacturerId), manufacturer_data)
            #self.add_service_data('9999', [0x00, 0x01, 0x02, 0x03, 0x04])
            self.add_local_name('Advertisement_' + identifier)
            # self.include_tx_power = True
            #self.add_data(0x26, [0x01, 0x01, 0x00])
            # self.add_data(0xff, [0x6D, 0xB6, 0x43, 0xCF, 0x7E, 0x8F, 0x47, 0x11, 
            #                                       0x88, 0x66, 0x59, 
            #                                       0x38, 0xD1, 0x7A, 0xAA, 
            #                                       0x26, 
            #                                       0x49, 0x5E, 
            #                                       0x13, 0x14, 0x15, 0x16, 0x17, 0x18])

            self.mainloop = GLib.MainLoop()
            self._ad_thread = None

        def _publish(self):
            self.mainloop.run()

        def Start(self):
            """Start GLib event loop"""
            self._ad_thread = threading.Thread(target=self._publish)
            self._ad_thread.daemon = True
            self._ad_thread.start()

        def Stop(self):
            """Stop GLib event loop"""
            self.mainloop.quit()

        def Release(self):  # pylint: disable=invalid-name
            """
            This method gets called when the service daemon
            removes the Advertisement. A client can use it to do
            cleanup tasks. There is no need to call
            UnregisterAdvertisement because when this method gets
            called it has already been unregistered.
            :return:
            """
            pass

    def __init__(self):
        """
        initializes the object and defines the fields
        """

        super().__init__()

        self._mainloop = GObject.MainLoop()

        self._bus = dbus.SystemBus()
        self._adapter = AdvertiserBluez._find_adapter(self._bus)
        
        adapter_props = dbus.Interface(self._bus.get_object(BLUEZ_SERVICE_NAME, self._adapter), DBUS_PROP_IFACE)
        adapter_props.Set("org.bluez.Adapter1", "Powered", dbus.Boolean(1))

        self._ad_manager = dbus.Interface(self._bus.get_object(BLUEZ_SERVICE_NAME, self._adapter), LE_ADVERTISING_MANAGER_IFACE)
        self._advertisementTable = dict()
        return

    def _find_adapter(bus):
        remote_om = dbus.Interface(bus.get_object(BLUEZ_SERVICE_NAME, '/'), DBUS_OM_IFACE)
        objects = remote_om.GetManagedObjects()

        for o, props in objects.items():
            if (LE_ADVERTISING_MANAGER_IFACE in props):
                return o

        return None
    
    def register_ad_cb(self):
        print('Advertisement registered')


    def register_ad_error_cb(self, error):
        print('Failed to register advertisement: ' + str(error))
        self._mainloop.quit()


    def AdvertisementStop(self):
        """
        stop bluetooth advertising

        """

        for advertisement in self._advertisementTable.values():
            advertisement.Stop()
            try:
                self._ad_manager.UnregisterAdvertisement(advertisement)
            except:
                pass
            try:
                dbus.service.Object.remove_from_connection(advertisement)
            except:
                pass

        # todo

        if (self._tracer is not None):
            pass

        return

    def AdvertisementSet(self, identifier: str, manufacturerId: bytes, rawdata: bytes):
        """
        Set Advertisement data
        """

        advertisement = self._advertisementTable.get(identifier)
        if(advertisement == None):
            advertisement = AdvertiserBluez.TestAdvertisement(self._bus, identifier, manufacturerId, rawdata)
            advertisement.Start()
            self._advertisementTable[identifier] = advertisement

        try:
            self._ad_manager.UnregisterAdvertisement(advertisement)
        except:
            pass

        self._ad_manager.RegisterAdvertisement(advertisement.get_path(), {},
                                        reply_handler=self.register_ad_cb,
                                        error_handler=self.register_ad_error_cb)

        if (self._tracer is not None):
            pass

        return
    

