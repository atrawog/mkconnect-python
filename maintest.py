#!/usr/bin/python

import sys
import time
import logging

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

# instantiate Advertiser
advertiser = Advertiser()

# Set Advertiser for all MouldKing Hubs
MouldKing.SetAdvertiser(advertiser)

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

hub0.Connect()
#hub1.Connect()
#hub2.Connect()
time.sleep(5)

#print("rawdata: " + ' '.join(f'{x:02x}' for x in rawdata))

#crypted = MouldKingCrypt.Crypt(rawdata) # get crypted data from rawdata
#print("crypted: " + ' '.join(f'{x:02x}' for x in crypted))

############################################################################
# get uncrypted stop-telegram as bytearray
title = "stop-telegram"
print("\n" + title)

rawdata = hub0.Stop()
#rawdata = hub1.Stop()
#rawdata = hub2.Stop()
time.sleep(1)

#print("rawdata: " + ' '.join(f'{x:02x}' for x in rawdata))

#crypted = MouldKingCrypt.Crypt(rawdata) # get crypted data from rawdata
#print("crypted: " + ' '.join(f'{x:02x}' for x in crypted))

############################################################################
# get uncrypted telegram with channel 1 (indexer 0) fullspeed forwards
title = "C1: fullspeed forwards"
print("\n" + title)

rawdata = hub0.SetChannel(0, 1)
time.sleep(1)

#print("rawdata: " + ' '.join(f'{x:02x}' for x in rawdata))

#crypted = MouldKingCrypt.Crypt(rawdata) # get crypted data from rawdata
#print("crypted: " + ' '.join(f'{x:02x}' for x in crypted))

############################################################################
# get uncrypted telegram with channel 1 (indexer 0) halfspeed forwards
title = "C1: halfspeed forwards"
print("\n" + title)

rawdata = hub0.SetChannel(0, 0.5)
time.sleep(1)

#print("rawdata: " + ' '.join(f'{x:02x}' for x in rawdata))

#crypted = MouldKingCrypt.Crypt(rawdata) # get crypted data from rawdata
#print("crypted: " + ' '.join(f'{x:02x}' for x in crypted))

############################################################################
# get uncrypted telegram with channel 1 (indexer 0) fullspeed forwards
title = "C1: fullspeed forwards"
print("\n" + title)

#rawdata = hub1.SetChannel(0, 1)
#time.sleep(2)

#print("rawdata: " + ' '.join(f'{x:02x}' for x in rawdata))

#crypted = MouldKingCrypt.Crypt(rawdata) # get crypted data from rawdata
#print("crypted: " + ' '.join(f'{x:02x}' for x in crypted))

############################################################################
# get uncrypted telegram with channel 1 (indexer 0) halfspeed backwards
title = "C1: halfspeed backwards"
print("\n" + title)

rawdata = hub0.SetChannel(0, -0.5)
time.sleep(1)

#print("rawdata: " + ' '.join(f'{x:02x}' for x in rawdata))

#crypted = MouldKingCrypt.Crypt(rawdata) # get crypted data from rawdata
#print("crypted: " + ' '.join(f'{x:02x}' for x in crypted))

############################################################################
# get uncrypted telegram with channel 1 (indexer 0) halfspeed backwards
title = "C2: halfspeed backwards"
print("\n" + title)

rawdata = hub0.SetChannel(1, -0.5)
time.sleep(1)

#print("rawdata: " + ' '.join(f'{x:02x}' for x in rawdata))

#crypted = MouldKingCrypt.Crypt(rawdata) # get crypted data from rawdata
#print("crypted: " + ' '.join(f'{x:02x}' for x in crypted))

############################################################################
# disconnect from advertiser
title = "Disconnect from advertiser"
print("\n" + title)

hub0.Disconnect()
#hub1.Disconnect()
#hub2.Disconnect()
time.sleep(1)

############################################################################
# stop Advertisement
title = "Advertisement stop"
print("\n" + title)
advertiser.AdvertisementStop()
time.sleep(1)
