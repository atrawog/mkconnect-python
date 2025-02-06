import pydbus
from time import sleep
from gi.repository import GObject

# Setup of device specific values
dev_id = 'DE:82:35:E7:43:BE'
btn_a_uuid = 'E95DDA90-251D-470A-A062-FA1922DFA9A8'
temp_period_uuid = 'E95D1B25-251D-470A-A062-FA1922DFA9A8'
temp_value_uuid = 'E95D9250-251D-470A-A062-FA1922DFA9A8'

# DBus object paths
bluez_service = 'org.bluez'
adapter_path = '/org/bluez/hci0'
device_path = f"{adapter_path}/dev_{dev_id.replace(':', '_')}"

# setup dbus
bus = pydbus.SystemBus()
mngr = bus.get(bluez_service, '/')
adapter = bus.get(bluez_service, adapter_path) 
device = bus.get(bluez_service, device_path)

# Access adapter properties
print(adapter.Name)
print(adapter.Powered)
print(adapter.Address)

# Commands and properties from the DBus API
print(dir(adapter))
print(dir(device))

# Assume device has been paired already so can use connect
device.Connect()
