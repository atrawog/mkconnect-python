#!/usr/bin/python

import subprocess
from MouldKing.MouldKingCrypt import MouldKingCrypt
from MouldKing.MouldKing_6 import MouldKing_6

# instantiate MouldKing_6-objects
mk6_0 = MouldKing_6(0)
mk6_1 = MouldKing_6(1)
mk6_2 = MouldKing_6(2)
#mk6_3 = MouldKing_6(3) # only 0..2 allowed - exception will be thrown

# get uncrypted connect-telegram as bytearray
title = "connect-telegram"
rawdata = mk6_0.Connect()

print("\n" + title)
print("rawdata: " + ' '.join(f'{x:02x}' for x in rawdata))

crypted = MouldKingCrypt.Crypt(rawdata) # get crypted data from rawdata
print("crypted: " + ' '.join(f'{x:02x}' for x in crypted))

# get uncrypted stop-telegram as bytearray
title = "stop-telegram"
rawdata = mk6_0.Stop()

print("\n" + title)
print("rawdata: " + ' '.join(f'{x:02x}' for x in rawdata))

crypted = MouldKingCrypt.Crypt(rawdata) # get crypted data from rawdata
print("crypted: " + ' '.join(f'{x:02x}' for x in crypted))

# get uncrypted telegram with channel 1 (indexer 0) fullspeed forwards
title = "C1: fullspeed forwards"
rawdata = mk6_0.SetChannel(0, 1)

print("\n" + title)
print("rawdata: " + ' '.join(f'{x:02x}' for x in rawdata))

crypted = MouldKingCrypt.Crypt(rawdata) # get crypted data from rawdata
print("crypted: " + ' '.join(f'{x:02x}' for x in crypted))

# get uncrypted telegram with channel 1 (indexer 0) halfspeed forwards
title = "C1: halfspeed forwards"
print("\n" + title)

rawdata = mk6_0.SetChannel(0, 0.5)
print("rawdata: " + ' '.join(f'{x:02x}' for x in rawdata))

crypted = MouldKingCrypt.Crypt(rawdata) # get crypted data from rawdata
print("crypted: " + ' '.join(f'{x:02x}' for x in crypted))

# get uncrypted telegram with channel 1 (indexer 0) halfspeed backwards
title = "C1: halfspeed backwards"
print("\n" + title)

rawdata = mk6_0.SetChannel(0, -0.5)
print("rawdata: " + ' '.join(f'{x:02x}' for x in rawdata))

crypted = MouldKingCrypt.Crypt(rawdata) # get crypted data from rawdata
print("crypted: " + ' '.join(f'{x:02x}' for x in crypted))

# get uncrypted telegram with channel 1 (indexer 0) halfspeed backwards
title = "C2: halfspeed backwards"
print("\n" + title)

rawdata = mk6_0.SetChannel(1, -0.5)
print("rawdata: " + ' '.join(f'{x:02x}' for x in rawdata))

crypted = MouldKingCrypt.Crypt(rawdata) # get crypted data from rawdata
print("crypted: " + ' '.join(f'{x:02x}' for x in crypted))

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

