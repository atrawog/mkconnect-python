#!/usr/bin/python

# to run: sudo python -i consoletest.py

print('consoletest')

import sys
import time

sys.path.append("Tracer") 
from Tracer.Tracer import Tracer
from Tracer.TracerConsole import TracerConsole

sys.path.append("Advertiser") 
# uncomment to choose advertiser
if (sys.platform == 'linux'):
    #from Advertiser.AdvertiserHCITool import AdvertiserHCITool as Advertiser
    from Advertiser.AdvertiserBTMgmt import AdvertiserBTMgmt as Advertiser
    #from Advertiser.AdvertiserBluez import AdvertiserBluez as Advertiser      # don't work yet
    #from Advertiser.AdvertiserDBus import AdvertiserDBus as Advertiser        # don't work yet
    pass
elif (sys.platform == 'rp2'):
    #from Advertiser.AdvertiserMicroPython import AdvertiserMicroPython as Advertiser
    pass
else:
    raise Exception('unsupported platform')

sys.path.append("MouldKing") 
from MouldKing.MouldKing import MouldKing

# instantiate Tracer
tracer = TracerConsole()

# instantiate Advertiser
advertiser = Advertiser()
advertiser.SetTracer(tracer)

# Set Tracer for all MouldKing Hubs
MouldKing.SetTracer(tracer)
MouldKing.SetAdvertiser(advertiser)

# save pre-instantiated objects in local variables
hub0 = MouldKing.Module6_0.Device0
hub1 = MouldKing.Module6_0.Device1
hub2 = MouldKing.Module6_0.Device2

hub3 = MouldKing.Module4_0.Device0
hub4 = MouldKing.Module4_0.Device1
hub5 = MouldKing.Module4_0.Device2

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
    # MK6
    if deviceId == 0:
        return hub0
    elif deviceId == 1:
        return hub1
    elif deviceId == 2:
        return hub2
    # MK4
    elif deviceId == 3:
        return hub3
    elif deviceId == 4:
        return hub4
    elif deviceId == 5:
        return hub5
    else:
        raise Exception("deviceId 0..5")

def _automate(deviceId: int, channel: int):
    userinput = input("\nDo you want to test channel "+ str(channel) +" ? enter y/n\n")

    if (userinput != str("y")):
        return

    tracer.TraceInfo("HUB: "+  str(deviceId) +", FORWARD : Power ramp up from 0 to 100% on channel :" + str(channel))
    for percent in range(0, 110, 10):
        tracer.TraceInfo("Power : " + str(percent) + "%")
        mkcontrol(deviceId,channel, percent/100)
        time.sleep(1)

    mkstop(deviceId)

    tracer.TraceInfo("HUB: "+  str(deviceId) +", REVERSE: Power ramp up from 0 to 100% on channel :" + str(channel))
    for percent in range(-0, -110, -10):
        tracer.TraceInfo("Power : " + str(percent) + "%")
        mkcontrol(deviceId,channel,percent/100)
        time.sleep(1)

    mkstop(deviceId)

def mkbtstop():
    """
    stop bluetooth advertising
    """
    advertiser.AdvertisementStop()
    # hcitool_args1 = hcitool_path + ' -i hci0 cmd 0x08 0x000a 00' + ' &> /dev/null'

    # if platform.system() == 'Linux':
    #     subprocess.run(hcitool_args1, shell=True, executable="/bin/bash")
    # elif platform.system() == 'Windows':
    #     print('Connect command :')
    #     print(hcitool_args1)
    # else:
    #     print('Unsupported OS')

    return

def mkconnect(deviceId: int=0):
    """
    send the bluetooth connect telegram to switch the MouldKing hubs in bluetooth mode
    press the button on the hub(s) and the flashing of status led should switch from blue-green to blue
    """
    hub = _getHubId(deviceId)
    rawdata = hub.Connect()
    return

def mkstop(deviceId: int=0):
    hub = _getHubId(deviceId)
    rawdata = hub.Stop()
    return        

def mkcontrol(deviceId: int=0, channel: int=0, powerAndDirection: float=0):
    hub = _getHubId(deviceId)
    rawdata = hub.SubDevice_SetChannel(channel, powerAndDirection)
    return

def test_hub(hubId: int=0):
    tracer.TraceInfo("HUB "+ str(hubId) +" connecting")
    mkconnect()
    time.sleep(1)

    for index in range(6):
        _automate(hubId, index) # start channel 0 = A
        tracer.TraceInfo("Channel change requested")
        time.sleep(1)

def help():
    tracer.TraceInfo("Available commands:")
    tracer.TraceInfo(" help()                                                    : print available commands")
    tracer.TraceInfo(" hints()                                                   : print hints and examples")
    tracer.TraceInfo(" mkconnect()                                               : Initiate hub control by sending bluetooth connect telegram")
    tracer.TraceInfo(" mkstop(hubId)                                             : Stop ALL motors")
    tracer.TraceInfo(" mkcontrol(hubId, channel, powerAndDirection)              : Control a specific hub, channel, power and motor direction")
    tracer.TraceInfo(" test_hub(hubId)                                           : run automated tests on each channels")
    tracer.TraceInfo(" mkbtstop()                                                : stop bluetooth advertising")

def hints():
    tracer.TraceInfo("HINTS:")
    tracer.TraceInfo("If run on windows, commands are shown but not executed (hcitool dependency)")
    tracer.TraceInfo()
    tracer.TraceInfo("For connecting:")
    tracer.TraceInfo(" Switch MK6.0 Hubs on - led is flashing green/blue")
    tracer.TraceInfo(" mkconnect() to send the bluetooth connect telegram. All hubs switch to bluetooth mode")
    tracer.TraceInfo(" by short-pressing the button on MK6.0 Hubs you can choose the hubId")
    tracer.TraceInfo("  hubId=0 - one Led flash")
    tracer.TraceInfo("  hubId=1 - two Led flashs")
    tracer.TraceInfo("  hubId=2 - three Led flashs")
    tracer.TraceInfo()
    tracer.TraceInfo("ex: test_hub(0), mkcontrol(0, 0, 0.5); mkcontrol(0, 1, -1, True)")
    tracer.TraceInfo(" the minus sign - indicate reverse motor direction")

##################################################################
# Entry point when script is started by python -i consoletest.py
help()
tracer.TraceInfo()
hints()

tracer.TraceInfo()
tracer.TraceInfo("Ready to execute commands\n")
