#!/usr/bin/python

import sys
import time
import logging
import asyncio

# set logging
logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO)

print('Script: main.py')
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

async def main():
    # instantiate Advertiser
    advertiser = Advertiser()

    # Set Advertiser for all MouldKing Hubs
    await MouldKing.SetAdvertiser(advertiser)

    # save pre-instantiated objects in local variables
    hub0 = MouldKing.Module6_0.Device0
    hub1 = MouldKing.Module6_0.Device1
    #hub2 = MouldKing.Module6_0.Device2

    #hub0 = MouldKing.Module4_0.Device0
    #hub1 = MouldKing.Module4_0.Device1
    hub2 = MouldKing.Module4_0.Device0


    ############################################################################
    # get uncrypted connect-telegram as bytearray
    title = "connect-telegram"
    print("\n" + title)

    await hub0.Connect()
    await hub1.Connect()
    await hub2.Connect()
    time.sleep(5)

    #print("rawdata: " + ' '.join(f'{x:02x}' for x in rawdata))

    #crypted = MouldKingCrypt.Crypt(rawdata) # get crypted data from rawdata
    #print("crypted: " + ' '.join(f'{x:02x}' for x in crypted))

    ############################################################################
    # get uncrypted telegram with channel 1 (indexer 0) fullspeed forwards
    title = "C1: fullspeed forwards"
    print("\n" + title)

    rawdata = await hub0.SetChannel(0, 1)
    rawdata = await hub1.SetChannel(0, 1)
    rawdata = await hub2.SetChannel(0, 1)
    rawdata = await hub2.SetChannel(1, 1)
    await asyncio.sleep(1)

    #print("rawdata: " + ' '.join(f'{x:02x}' for x in rawdata))

    #crypted = MouldKingCrypt.Crypt(rawdata) # get crypted data from rawdata
    #print("crypted: " + ' '.join(f'{x:02x}' for x in crypted))

    ############################################################################
    # get uncrypted telegram with channel 1 (indexer 0) halfspeed forwards
    title = "C1: halfspeed forwards"
    print("\n" + title)

    rawdata = await hub1.SetChannel(1, 1)
    await asyncio.sleep(1)

    #print("rawdata: " + ' '.join(f'{x:02x}' for x in rawdata))

    #crypted = MouldKingCrypt.Crypt(rawdata) # get crypted data from rawdata
    #print("crypted: " + ' '.join(f'{x:02x}' for x in crypted))

    ############################################################################
    # get uncrypted telegram with channel 1 (indexer 0) fullspeed forwards
    title = "C1: fullspeed forwards"
    print("\n" + title)

    rawdata = await hub2.SetChannel(0, 1)
    await asyncio.sleep(1)

    #print("rawdata: " + ' '.join(f'{x:02x}' for x in rawdata))

    #crypted = MouldKingCrypt.Crypt(rawdata) # get crypted data from rawdata
    #print("crypted: " + ' '.join(f'{x:02x}' for x in crypted))

    ############################################################################
    # get uncrypted telegram with channel 1 (indexer 0) halfspeed backwards
    title = "C1: halfspeed backwards"
    print("\n" + title)

    rawdata = await hub1.SetChannel(1, -0.5)
    await asyncio.sleep(1)

    #print("rawdata: " + ' '.join(f'{x:02x}' for x in rawdata))

    #crypted = MouldKingCrypt.Crypt(rawdata) # get crypted data from rawdata
    #print("crypted: " + ' '.join(f'{x:02x}' for x in crypted))

    ############################################################################
    # get uncrypted telegram with channel 1 (indexer 0) halfspeed backwards
    title = "C2: halfspeed backwards"
    print("\n" + title)

    rawdata = await hub1.SetChannel(1, -0.5)
    await asyncio.sleep(1)

    #print("rawdata: " + ' '.join(f'{x:02x}' for x in rawdata))

    #crypted = MouldKingCrypt.Crypt(rawdata) # get crypted data from rawdata
    #print("crypted: " + ' '.join(f'{x:02x}' for x in crypted))

    ############################################################################
    # disconnect from advertiser
    title = "Disconnect from advertiser"
    print("\n" + title)

    await hub0.Disconnect()
    await hub1.Disconnect()
    await hub2.Disconnect()
    await asyncio.sleep(1)

    ############################################################################
    # stop Advertisement
    title = "Advertisement stop"
    print("\n" + title)
    await advertiser.AdvertisementStop()
    await asyncio.sleep(1)

if __name__ == "__main__":
    
    asyncio.run(main())

