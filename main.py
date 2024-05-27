#!/usr/bin/python

# import hack for micro-python-simulator with flat filesystem
try:
  from Tracer.Tracer import Tracer
  from Tracer.TracerConsole import TracerConsole
  from MouldKing.MouldKing import MouldKing
  from MouldKing.Module6_0 import Module6_0
  from MouldKing.MouldKingCrypt import MouldKingCrypt
  from MouldKing.MouldKing_6 import MouldKing_6
  from Advertiser.AdvertiserHCITool import AdvertiserHCITool
except ImportError:
  from Tracer import Tracer
  from TracerConsole import TracerConsole
  from MouldKing import MouldKing
  from Module6_0 import Module6_0
  from MouldKingCrypt import MouldKingCrypt
  from MouldKing_6 import MouldKing_6
  from AdvertiserHCITool import AdvertiserHCITool

# instantiate Advertiser
tracer = TracerConsole()

# instantiate Advertiser
advertiser = AdvertiserHCITool()

# Set Tracer for all MouldKing 6.0 Hubs
MouldKing.Module6_0.SetTracer(tracer)

# Set Advertiser for all MouldKing 6.0 Hubs
MouldKing.Module6_0.SetAdvertiser(advertiser)

# save pre-instantiated objects in local variables
mk6_0 = MouldKing.Module6_0.Device0
mk6_1 = MouldKing.Module6_0.Device1
mk6_2 = MouldKing.Module6_0.Device2

############################################################################
# get uncrypted connect-telegram as bytearray
title = "connect-telegram"
rawdata = mk6_0.Connect()

print("\n" + title)
print("rawdata: " + ' '.join(f'{x:02x}' for x in rawdata))

crypted = MouldKingCrypt.Crypt(rawdata) # get crypted data from rawdata
print("crypted: " + ' '.join(f'{x:02x}' for x in crypted))

############################################################################
# get uncrypted stop-telegram as bytearray
title = "stop-telegram"
rawdata = mk6_0.Stop()

print("\n" + title)
print("rawdata: " + ' '.join(f'{x:02x}' for x in rawdata))

crypted = MouldKingCrypt.Crypt(rawdata) # get crypted data from rawdata
print("crypted: " + ' '.join(f'{x:02x}' for x in crypted))

############################################################################
# get uncrypted telegram with channel 1 (indexer 0) fullspeed forwards
title = "C1: fullspeed forwards"
rawdata = mk6_0.SetChannel(0, 1)

print("\n" + title)
print("rawdata: " + ' '.join(f'{x:02x}' for x in rawdata))

crypted = MouldKingCrypt.Crypt(rawdata) # get crypted data from rawdata
print("crypted: " + ' '.join(f'{x:02x}' for x in crypted))

############################################################################
# get uncrypted telegram with channel 1 (indexer 0) halfspeed forwards
title = "C1: halfspeed forwards"
print("\n" + title)

rawdata = mk6_0.SetChannel(0, 0.5)
print("rawdata: " + ' '.join(f'{x:02x}' for x in rawdata))

crypted = MouldKingCrypt.Crypt(rawdata) # get crypted data from rawdata
print("crypted: " + ' '.join(f'{x:02x}' for x in crypted))

############################################################################
# get uncrypted telegram with channel 1 (indexer 0) halfspeed backwards
title = "C1: halfspeed backwards"
print("\n" + title)

rawdata = mk6_0.SetChannel(0, -0.5)
print("rawdata: " + ' '.join(f'{x:02x}' for x in rawdata))

crypted = MouldKingCrypt.Crypt(rawdata) # get crypted data from rawdata
print("crypted: " + ' '.join(f'{x:02x}' for x in crypted))

############################################################################
# get uncrypted telegram with channel 1 (indexer 0) halfspeed backwards
title = "C2: halfspeed backwards"
print("\n" + title)

rawdata = mk6_0.SetChannel(1, -0.5)
print("rawdata: " + ' '.join(f'{x:02x}' for x in rawdata))

crypted = MouldKingCrypt.Crypt(rawdata) # get crypted data from rawdata
print("crypted: " + ' '.join(f'{x:02x}' for x in crypted))

############################################################################
# stop Advertisment
title = "Advertisement stop"
print("\n" + title)
advertiser.AdvertismentStop(tracer)

#subprocess.call(["sudo", "hciconfig hci0 up"])
#subprocess.call(["sudo", "hciconfig hci0 leadv 3"])
# subprocess.call(["hcitool", "-i hci0 cmd 08 0008 25 02 01 02 1b ff f0 ff 6D B6 43 CF 7E 8F 47 11 88 66 59 38 D1 7A AA 26 49 5E 13 14 15 16 17 18"])

#print(command)
#subprocess.call(["sudo", "hcitool -i hci0 cmd 08 0008 " + command])

# result = mk6_0.SetChannel(0, 1)
# print(' '.join(f'{x:02x}' for x in result))

# result = mk6_0.SetChannel(0, 10)
# print(' '.join(f'{x:02x}' for x in result))

# result = mk6_0.SetChannel(0, -1)
# print(' '.join(f'{x:02x}' for x in result))

