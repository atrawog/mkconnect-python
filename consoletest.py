#!/usr/bin/python

# to run:  python -i consoletest.py

try:
  from MouldKing.MouldKingCrypt import MouldKingCrypt
  from MouldKing.MouldKing_6 import MouldKing_6
except ImportError:
  from MouldKingCrypt import MouldKingCrypt
  from MouldKing_6 import MouldKing_6

import subprocess
import platform
import time

hcitool_path = '/usr/bin/hcitool'
hub0 = MouldKing_6(0)
hub1 = MouldKing_6(1)
hub2 = MouldKing_6(2)

def _getChannelId(channel):
    switch={
    'A': 0,
    'B': 1,
    'C': 2,
    'D': 3,
    'E': 4,
    'F': 5,
    }
    return switch.get(channel,"")

def _getHubId(deviceId):
    if deviceId == 0:
        return hub0
    elif deviceId == 1:
        return hub1
    elif deviceId == 2:
        return hub2
    else:
        raise Exception("deviceId 0..2")

def mkbtstop():
    """
    stop bluetooth advertising
    """
    hcitool_args1 = hcitool_path + ' -i hci0 cmd 0x08 0x000a 00' + ' &> /dev/null'

    if platform.system() == 'Linux':
        subprocess.run(hcitool_args1, shell=True, executable="/bin/bash")
    elif platform.system() == 'Windows':
        print('Connect command :')
        print(hcitool_args1)
    else:
        print('Unsupported OS')

    return

def mkconnect():
    """
    send the bluetooth connect telegram to switch the MouldKing hubs in bluetooth mode
    press the button on the hub(s) and the flashing of status led should switch from blue-green to blue
    """
    hub = _getHubId(0)
    rawdata = hub.Connect()
    hcitool_args1 = hcitool_path + ' -i hci0 cmd 08 0008 ' + MouldKingCrypt.CreateTelegramForHCITool(MouldKing_6.ManufacturerID, rawdata) + ' &> /dev/null'
    hcitool_args2 = hcitool_path + ' -i hci0 cmd 0x08 0x0006 A0 00 A0 00 03 00 00 00 00 00 00 00 00 07 00' + ' &> /dev/null'
    hcitool_args3 = hcitool_path + ' -i hci0 cmd 0x08 0x000a 01' + ' &> /dev/null'

    if platform.system() == 'Linux':
        subprocess.run(hcitool_args1, shell=True, executable="/bin/bash")
        subprocess.run(hcitool_args2, shell=True, executable="/bin/bash")
        subprocess.run(hcitool_args3, shell=True, executable="/bin/bash")
    elif platform.system() == 'Windows':
        print('Connect command :')
        print(hcitool_args1)
        print(hcitool_args2)
        print(hcitool_args3)
    else:
        print('Unsupported OS')

    return

def mkstop(deviceId=0):
    hub = _getHubId(deviceId)
    rawdata = hub.Stop()
    hcitool_args = hcitool_path + ' -i hci0 cmd 08 0008 ' + MouldKingCrypt.CreateTelegramForHCITool(MouldKing_6.ManufacturerID, rawdata) + ' &> /dev/null'

    if platform.system() == 'Linux':
        subprocess.run(hcitool_args, shell=True, executable="/bin/bash")
    elif platform.system() == 'Windows':
        print('Control command selected:')
        print(hcitool_args)
    else:
        print('Unsupported OS')

    return        

def mkcontrol(deviceId=0, channel=0, powerAndDirection=1):
    hub = _getHubId(deviceId)
    rawdata = hub.SetChannel(channel, powerAndDirection)
    hcitool_args = hcitool_path + ' -i hci0 cmd 08 0008 ' + MouldKingCrypt.CreateTelegramForHCITool(MouldKing_6.ManufacturerID, rawdata) + ' &> /dev/null'

    if platform.system() == 'Linux':
        subprocess.run(hcitool_args, shell=True, executable="/bin/bash")
    elif platform.system() == 'Windows':
        print('Control command selected:')
        print(hcitool_args)
    else:
        print('Unsupported OS')

    return

print("\nReady to execute commands\n")
print("stop bluetooth advertising: mkbtstop()\n")
print("For connecting: mkconnect(hubId) ex: mkconnect(0) or mkconnect(1) for the second hub\n")
print(" Available commands: mkconnect(hubId)\n mkstop(hubId)\n mkcontrol(deviceId, channel, powerAndDirection)\n")
print("ex: mkcontrol(0, 0, 0.5) ; mkcontrol(0, 'B', -1)\n the minus sign - indicate reverse motor direction\n")
