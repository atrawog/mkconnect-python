#!/usr/bin/python

print('testmain')

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
#hub0 = MouldKing.Module6_0.Device0
hub1 = MouldKing.Module6_0.Device1
hub2 = MouldKing.Module6_0.Device2

hub0 = MouldKing.Module4_0.Device0
#hub1 = MouldKing.Module4_0.Device0
#hub2 = MouldKing.Module4_0.Device2

############################################################################
# get uncrypted connect-telegram as bytearray
title = "connect-telegram"
tracer.TraceInfo("\n" + title)

rawdata = hub0.Connect()
rawdata = hub0.Disconnect()
time.sleep(5)


rawdata = hub0.Connect()
rawdata = hub1.Connect()
rawdata = hub2.Connect()
time.sleep(5)

#tracer.TraceInfo("rawdata: " + ' '.join(f'{x:02x}' for x in rawdata))

#crypted = MouldKingCrypt.Crypt(rawdata) # get crypted data from rawdata
#tracer.TraceInfo("crypted: " + ' '.join(f'{x:02x}' for x in crypted))

############################################################################
# get uncrypted stop-telegram as bytearray
title = "stop-telegram"
tracer.TraceInfo("\n" + title)

rawdata = hub0.Stop()
rawdata = hub1.Stop()
time.sleep(1)

#tracer.TraceInfo("rawdata: " + ' '.join(f'{x:02x}' for x in rawdata))

#crypted = MouldKingCrypt.Crypt(rawdata) # get crypted data from rawdata
#tracer.TraceInfo("crypted: " + ' '.join(f'{x:02x}' for x in crypted))

############################################################################
# get uncrypted telegram with channel 1 (indexer 0) fullspeed forwards
title = "C1: fullspeed forwards"
tracer.TraceInfo("\n" + title)

rawdata = hub0.SetChannel(0, 1)
time.sleep(1)

#tracer.TraceInfo("rawdata: " + ' '.join(f'{x:02x}' for x in rawdata))

#crypted = MouldKingCrypt.Crypt(rawdata) # get crypted data from rawdata
#tracer.TraceInfo("crypted: " + ' '.join(f'{x:02x}' for x in crypted))

############################################################################
# get uncrypted telegram with channel 1 (indexer 0) halfspeed forwards
title = "C1: halfspeed forwards"
tracer.TraceInfo("\n" + title)

rawdata = hub0.SetChannel(0, 0.5)
time.sleep(1)

#tracer.TraceInfo("rawdata: " + ' '.join(f'{x:02x}' for x in rawdata))

#crypted = MouldKingCrypt.Crypt(rawdata) # get crypted data from rawdata
#tracer.TraceInfo("crypted: " + ' '.join(f'{x:02x}' for x in crypted))

############################################################################
# get uncrypted telegram with channel 1 (indexer 0) fullspeed forwards
title = "C1: fullspeed forwards"
tracer.TraceInfo("\n" + title)

rawdata = hub1.SetChannel(0, 1)
time.sleep(2)

#tracer.TraceInfo("rawdata: " + ' '.join(f'{x:02x}' for x in rawdata))

#crypted = MouldKingCrypt.Crypt(rawdata) # get crypted data from rawdata
#tracer.TraceInfo("crypted: " + ' '.join(f'{x:02x}' for x in crypted))

############################################################################
# get uncrypted telegram with channel 1 (indexer 0) halfspeed backwards
title = "C1: halfspeed backwards"
tracer.TraceInfo("\n" + title)

rawdata = hub0.SetChannel(0, -0.5)
time.sleep(1)

#tracer.TraceInfo("rawdata: " + ' '.join(f'{x:02x}' for x in rawdata))

#crypted = MouldKingCrypt.Crypt(rawdata) # get crypted data from rawdata
#tracer.TraceInfo("crypted: " + ' '.join(f'{x:02x}' for x in crypted))

############################################################################
# get uncrypted telegram with channel 1 (indexer 0) halfspeed backwards
title = "C2: halfspeed backwards"
tracer.TraceInfo("\n" + title)

rawdata = hub0.SetChannel(1, -0.5)
time.sleep(1)

#tracer.TraceInfo("rawdata: " + ' '.join(f'{x:02x}' for x in rawdata))

#crypted = MouldKingCrypt.Crypt(rawdata) # get crypted data from rawdata
#tracer.TraceInfo("crypted: " + ' '.join(f'{x:02x}' for x in crypted))

############################################################################
# disconnect from advertiser
title = "Disconnect from advertiser"
tracer.TraceInfo("\n" + title)

rawdata = hub0.Disconnect()
rawdata = hub1.Disconnect()
rawdata = hub2.Disconnect()
time.sleep(1)

############################################################################
# stop Advertisement
title = "Advertisement stop"
tracer.TraceInfo("\n" + title)
advertiser.AdvertisementStop()
time.sleep(1)
