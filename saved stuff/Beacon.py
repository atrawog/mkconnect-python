import threading
import pydbus
from gi.repository import GLib


class Beacon1:
    """
    <node>
        <interface name='org.bluez.LEAdvertisement1'>
            <method name='Release'>
                <annotation name="org.freedesktop.DBus.Method.NoReply" value="true"/>
            </method>
            <annotation name="org.freedesktop.DBus.Properties.PropertiesChanged" value="const"/>
            <property name="Type" type="s" access="read"/>
            <property name="ServiceUUIDs" type="as" access="read"/>
            <property name="ServiceData" type="a{sv}" access="read"/>
            <property name="IncludeTxPower" type="b" access="read"/>
            <property name="ManufacturerData" type="a{qv}" access="read"/>
            <property name="SolicitUUIDs" type="as" access="read"/>
        </interface>
    </node>
    """
    LE_ADVERTISEMENT_IFACE = 'org.bluez.LEAdvertisement1'

    def Release(self):
        pass

    @property
    def Type(self):
        return 'peripheral'
        # return 'broadcast'
    
    @property
    def ServiceUUIDs(self):
        return []

    @property
    def ServiceData(self):
        return {}

    @property
    def IncludeTxPower(self):
        return True

    @property
    def Discoverable(self):
        return True

    @property
    def ManufacturerData(self):
        # return {0x004c: pydbus.Variant('ay', [0x02, 0x15, 0xE2, 0xC5, 0x6D, 0xB5, 0xDF, 0xFB,
        #                                       0x48, 0xD2, 0xB0, 0x60, 0xD0, 0xF5, 0xA7, 0x10,
        #                                       0x96, 0xE0, 0x00, 0x01, 0x00, 0x02, 0x0c])}
        return {0xfff0: pydbus.Variant('ay', [0x6D, 0xB6, 0x43, 0xCF, 0x7E, 0x8F, 0x47, 0x11, 
                                              0x88, 0x66, 0x59, 
                                              0x38, 0xD1, 0x7A, 0xAA, 
                                              0x26, 
                                              0x49, 0x5E, 
                                              0x13, 0x14, 0x15, 0x16, 0x17, 0x18])}


    @property
    def SolicitUUIDs(self):
        return []

class Beacon2:
    """
    <node>
        <interface name='org.bluez.LEAdvertisement1'>
            <method name='Release'>
                <annotation name="org.freedesktop.DBus.Method.NoReply" value="true"/>
            </method>
            <annotation name="org.freedesktop.DBus.Properties.PropertiesChanged" value="const"/>
            <property name="Type" type="s" access="read"/>
            <property name="ServiceUUIDs" type="as" access="read"/>
            <property name="ServiceData" type="a{sv}" access="read"/>
            <property name="IncludeTxPower" type="b" access="read"/>
            <property name="ManufacturerData" type="a{qv}" access="read"/>
            <property name="SolicitUUIDs" type="as" access="read"/>
        </interface>
    </node>
    """
    LE_ADVERTISEMENT_IFACE = 'org.bluez.LEAdvertisement1'

    def Release(self):
        pass

    @property
    def Type(self):
        return 'broadcast'
    
    @property
    def ServiceUUIDs(self):
        return []

    @property
    def ServiceData(self):
        return {}

    @property
    def IncludeTxPower(self):
        return False

    @property
    def ManufacturerData(self):
        # return {0x004c: pydbus.Variant('ay', [0x02, 0x15, 0xE2, 0xC5, 0x6D, 0xB5, 0xDF, 0xFB,
        #                                       0x48, 0xD2, 0xB0, 0x60, 0xD0, 0xF5, 0xA7, 0x10,
        #                                       0x96, 0xE0, 0x00, 0x01, 0x00, 0x02, 0x0c])}
        return {0xfff0: pydbus.Variant('ay', [0x6D, 0xB6, 0x43, 0xCF, 0x7E, 0x8F, 0x47, 0x11, 
                                              0x88, 0x66, 0x59])}


    @property
    def SolicitUUIDs(self):
        return []
    
class Beacon3:
    """
    <node>
        <interface name='org.bluez.LEAdvertisement1'>
            <method name='Release'>
                <annotation name="org.freedesktop.DBus.Method.NoReply" value="true"/>
            </method>
            <annotation name="org.freedesktop.DBus.Properties.PropertiesChanged" value="const"/>
            <property name="Type" type="s" access="read"/>
            <property name="ServiceUUIDs" type="as" access="read"/>
            <property name="ServiceData" type="a{sv}" access="read"/>
            <property name="IncludeTxPower" type="b" access="read"/>
            <property name="ManufacturerData" type="a{qv}" access="read"/>
            <property name="SolicitUUIDs" type="as" access="read"/>
        </interface>
    </node>
    """
    LE_ADVERTISEMENT_IFACE = 'org.bluez.LEAdvertisement1'

    def Release(self):
        pass

    @property
    def Type(self):
        return 'peripheral'
        # return 'broadcast'
    
    @property
    def ServiceUUIDs(self):
        return []

    @property
    def ServiceData(self):
        return {}

    @property
    def Data(self):
        return {}

    @property
    def IncludeTxPower(self):
        return False

    @property
    def ManufacturerData(self):
        # return {0x004c: pydbus.Variant('ay', [0x02, 0x15, 0xE2, 0xC5, 0x6D, 0xB5, 0xDF, 0xFB,
        #                                       0x48, 0xD2, 0xB0, 0x60, 0xD0, 0xF5, 0xA7, 0x10,
        #                                       0x96, 0xE0, 0x00, 0x01, 0x00, 0x02, 0x0c])}
        return {0xfff0: pydbus.Variant('ay', [0x6D, 0xB6, 0x43, 0xCF])}


    @property
    def SolicitUUIDs(self):
        return []

class LEAdvertisement:
    def __init__(self, object_path, beacon):
        bus = pydbus.SystemBus()
        reg1 = bus.register_object(object_path, beacon, None)

class LEAdvertisingManager:
    def __init__(self, object_path):
        lea_iface = 'org.bluez.LEAdvertisingManager1'
        bus = pydbus.SystemBus()
        ad_manager = bus.get('org.bluez', '/org/bluez/hci0')[lea_iface]
        ad_manager.RegisterAdvertisement(object_path, {})
        print('Registered Ad')


def publish_now():
    print('Publishing Ad')
    aloop = GLib.MainLoop()
    aloop.run()

def thread_function(path, beacon):
    print('Starting thread ' + path)
    LEAdvertisement(path, beacon)
    publish_now()
    print('thread finished ' + path)

#https://github.com/hadess/bluez/blob/master/doc/advertising-api.txt
#https://pydbus.readthedocs.io/en/latest/legacydocs/tutorial.html
#https://git.kernel.org/pub/scm/bluetooth/bluez.git/tree/test/example-advertisement
#https://stackoverflow.com/questions/63661259/how-to-have-2-advertisements-in-blebluetooth-low-energy
#https://stackoverflow.com/questions/75819464/how-to-send-a-python-dbus-advertising-packet-with-flags
#https://github.com/kevincar/bless/blob/master/bless/backends/bluezdbus/dbus/advertisement.py
#https://ukbaz.github.io/howto/python_gio_3.html
if __name__ == '__main__':
    #app_path1 = '/org/bluez/example/advertisement0098'
    app_path1 = '/org/bluez/first'
    #app_path2 = '/org/bluez/example/advertisement0099'
    app_path2 = '/org/bluez/second'

    beacon1 = Beacon1()
    beacon2 = Beacon2()
    beacon3 = Beacon3()

    x1 = threading.Thread(target=thread_function, args=[app_path1, beacon1], daemon=True)
    x1.start()

    x2 = threading.Thread(target=thread_function, args=[app_path2, beacon2], daemon=True)
    x2.start()

    LEAdvertisingManager(app_path1)
    # LEAdvertisingManager(app_path2)

    # lea_iface = 'org.bluez.LEAdvertisingManager1'
    # bus = pydbus.SystemBus()
    # ad_manager = bus.get('org.bluez', '/org/bluez/hci0')[lea_iface]
    # ad_manager.UnregisterAdvertisement(app_path1)

    # reg1 = bus.unregister_object(app_path1, None)


    loop = GLib.MainLoop()
    try:
        loop.run()
    except KeyboardInterrupt:
        print("\nStopping ...")
        loop.quit()