#!/usr/bin/python

# to run:  python -i consoletest.py

try:
  from MouldKing.MouldKing import MouldKing
  from Advertiser.AdvertiserHCITool import AdvertiserHCITool
except ImportError:
  from MouldKing import MouldKing
  from AdvertiserHCITool import AdvertiserHCITool

import time
import numpy as np

# instantiate Advertiser
advertiser = AdvertiserHCITool()

# Set Advertiser for all MouldKing Hubs 6.0
MouldKing.Module6_0.SetAdvertiser(advertiser)

# save pre-instantiated objects in local variables
hub0 = MouldKing.Module6_0.Device0
hub1 = MouldKing.Module6_0.Device1
hub2 = MouldKing.Module6_0.Device2

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

def _automate(deviceId: int, channel: int):
    userinput = input("\nDo you want to test channel "+ str(channel) +" ? enter y/n\n")

    if (userinput != str("y")):
        return

    print("HUB: "+  str(deviceId) +", FORWARD : Power ramp up from 0 to 100% on channel :" + str(channel))
    for i in np.arange(0, 1.1, 0.1):
        print("Power : " + str(i))
        mkcontrol(deviceId,channel,i)
        time.sleep(1)

    mkstop(deviceId)

    print("HUB: "+  str(deviceId) +", REVERSE: Power ramp up from 0 to 100% on channel :" + str(channel))
    for i in np.arange(-0, -1.1, -0.1):
        print("Power : " + str(i) + "\n")
        mkcontrol(deviceId,channel,i)
        time.sleep(1)

    mkstop(deviceId)

def mkbtstop():
    """
    stop bluetooth advertising
    """
    advertiser.AdvertismentStop()
    # hcitool_args1 = hcitool_path + ' -i hci0 cmd 0x08 0x000a 00' + ' &> /dev/null'

    # if platform.system() == 'Linux':
    #     subprocess.run(hcitool_args1, shell=True, executable="/bin/bash")
    # elif platform.system() == 'Windows':
    #     print('Connect command :')
    #     print(hcitool_args1)
    # else:
    #     print('Unsupported OS')

    return

def mkconnect(debug: bool=False):
    """
    send the bluetooth connect telegram to switch the MouldKing hubs in bluetooth mode
    press the button on the hub(s) and the flashing of status led should switch from blue-green to blue
    """
    hub = _getHubId(0)
    rawdata = hub.Connect()
    return

def mkstop(deviceId: int=0, debug: bool=False):
    hub = _getHubId(deviceId)
    rawdata = hub.Stop()
    return        

def mkcontrol(deviceId: int=0, channel: int=0, powerAndDirection: float=1, debug: bool=False):
    hub = _getHubId(deviceId)
    rawdata = hub.SetChannel(channel, powerAndDirection)
    return

def test_hub(hubId: int=0):
    print("HUB "+ str(hubId) +" connecting")
    mkconnect(hubId)
    time.sleep(1)

    for index in range(6):
        _automate(hubId, index) # start channel 0 = A
        print("Channel change requested")
        time.sleep(1)

def help():
    print("Available commands:")
    print(" help()                                                    : print available commands")
    print(" hints()                                                   : print hints and examples")
    print(" mkconnect(debug=False)                                    : Initiate hub control by sending bluetooth connect telegram")
    print(" mkstop(hubId, debug=False)                                : Stop ALL motors")
    print(" mkcontrol(hubId, channel, powerAndDirection, debug=False) : Control a specific hub, channel, power and motor direction")
    print(" test_hub(hubId)                                           : run automated tests on each channels")
    print(" mkbtstop()                                                : stop bluetooth advertising")

def hints():
    print("HINTS:")
    print("If run on windows, commands are shown but not executed (hcitool dependency)")
    print()
    print("For connecting:")
    print(" Switch MK6.0 Hubs on - led is flashing green/blue")
    print(" mkconnect() to send the bluetooth connect telegram. All hubs switch to bluetooth mode")
    print(" by short-pressing the button on MK6.0 Hubs you can choose the hubId")
    print("  hubId=0 - one Led flash")
    print("  hubId=1 - two Led flashs")
    print("  hubId=2 - three Led flashs")
    print()
    print("ex: test_hub(0), mkcontrol(0, 0, 0.5); mkcontrol(0, 1, -1, True)")
    print(" the minus sign - indicate reverse motor direction")

##################################################################
# Entry point when script is started by python -i consoletest.py
help()
print()
hints()

print()
print("Ready to execute commands\n")
