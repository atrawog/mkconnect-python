# install aiorepl-lib first!
# to install in VSCode use command "micropico-device-wifi.focus" of VSCode-extension MicroPico
# connect to WiFi and install package "aiorepl"

import asyncio
import aiorepl
import logging
import sys

logger = logging.getLogger(__name__)

logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO)

print('Script: consoletest.py')
print('Platform: ' + sys.platform)

sys.path.append("Advertiser") 
# uncomment to choose advertiser
if (sys.platform == 'linux'):
    #from Advertiser.AdvertiserHCITool import AdvertiserHCITool as Advertiser
    #from Advertiser.AdvertiserBTMgmt import AdvertiserBTMgmt as Advertiser
    from Advertiser.AdvertiserBTSocket import AdvertiserBTSocket as Advertiser
    pass
elif (sys.platform == 'rp2'):
    from Advertiser.AdvertiserMicroPython import AdvertiserMicroPython as Advertiser
    pass
elif (sys.platform == 'win32'):
    from Advertiser.AdvertiserDummy import AdvertiserDummy as Advertiser
else:
    raise Exception('unsupported platform')

sys.path.append("MouldKing") 
from MouldKing.MouldKing import MouldKing

# instantiate Advertiser
advertiser = Advertiser()

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

async def _automate(deviceId: int, channel: int):
    #userinput = input("\nDo you want to test channel "+ str(channel) +" ? enter y/n\n")

    #if (userinput != str("y")):
    #   return

    print("HUB: "+  str(deviceId) +", FORWARD : Power ramp up from 0 to 100% on channel :" + str(channel))
    for percent in range(0, 110, 10):
        print("Power : " + str(percent) + "%")
        await mkcontrol(deviceId,channel, percent/100)
        await asyncio.sleep(1)

    await mkstop(deviceId)

    print("HUB: "+  str(deviceId) +", REVERSE: Power ramp up from 0 to 100% on channel :" + str(channel))
    for percent in range(-0, -110, -10):
        print("Power : " + str(percent) + "%")
        await mkcontrol(deviceId,channel,percent/100)
        await asyncio.sleep(1)

    await mkstop(deviceId)

async def mkbtstop():
    """
    stop bluetooth advertising
    """
    await advertiser.AdvertisementStop()
    # hcitool_args1 = hcitool_path + ' -i hci0 cmd 0x08 0x000a 00' + ' &> /dev/null'

    # if platform.system() == 'Linux':
    #     subprocess.run(hcitool_args1, shell=True, executable="/bin/bash")
    # elif platform.system() == 'Windows':
    #     print('Connect command :')
    #     print(hcitool_args1)
    # else:
    #     print('Unsupported OS')

    return

async def mkconnect(deviceId: int=0):
    """
    send the bluetooth connect telegram to switch the MouldKing hubs in bluetooth mode
    press the button on the hub(s) and the flashing of status led should switch from blue-green to blue
    """
    hub = _getHubId(deviceId)
    rawdata = await hub.Connect()
    return

async def mkstop(deviceId: int=0):
    hub = _getHubId(deviceId)
    rawdata = await hub.Stop()
    return        

async def mkcontrol(deviceId: int=0, channel: int=0, powerAndDirection: float=0):
    hub = _getHubId(deviceId)
    rawdata = await hub.SetChannel(channel, powerAndDirection)
    return

async def test_hub(hubId: int=0):
    print("HUB "+ str(hubId) +" connecting")
    await mkconnect()
    await asyncio.sleep(1)

    for index in range(6):
        await _automate(hubId, index) # start channel 0 = A
        print("Channel change requested")
        await asyncio.sleep(1)

def help():
    print("Available commands:")
    print(" help()                                                    : print available commands")
    print(" hints()                                                   : print hints and examples")
    print(" mkconnect()                                               : Initiate hub control by sending bluetooth connect telegram")
    print(" mkstop(hubId)                                             : Stop ALL motors")
    print(" mkcontrol(hubId, channel, powerAndDirection)              : Control a specific hub, channel, power and motor direction")
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

state = 20
t1Task: asyncio.Task | None = None
replTask: asyncio.Task | None = None
mainTask: asyncio.Task | None = None

def exit():
    print("exit demo")
    state = 0
    if(t1Task is not None):
        t1Task.cancel()
    if(replTask is not None):
        replTask.cancel()
    if(mainTask is not None):
        mainTask.cancel()

async def task1():
    # Set Advertiser for all MouldKing Hubs
    await MouldKing.SetAdvertiser(advertiser)

    help()
    print()
    hints()

    print()
    print("Ready to execute commands\n")

    while state:
        #print("task 1")
        await asyncio.sleep(0.5)
    print("done")

async def main():
    print("Starting tasks...")

    # Start other program tasks.
    t1Task = asyncio.create_task(task1())

    # Start the aiorepl task.
    repl = asyncio.create_task(aiorepl.task())

    await asyncio.gather(t1Task, repl)

mainTask = asyncio.run(main())
print("Exited aioREPL")
