#!/usr/bin/python

import subprocess
from MouldKingCrypt import MouldKingCrypt
from MouldKing_6 import MouldKing_6

subprocess.call(["sudo", "hciconfig hci0 up"])
subprocess.call(["sudo", "hciconfig hci0 leadv 3"])
# subprocess.call(["hcitool", "-i hci0 cmd 08 0008 25 02 01 02 1b ff f0 ff 6D B6 43 CF 7E 8F 47 11 88 66 59 38 D1 7A AA 26 49 5E 13 14 15 16 17 18"])

mk6_0 = MouldKing_6(0)
mk6_1 = MouldKing_6(1)
mk6_2 = MouldKing_6(2)
#mk6_3 = MouldKing_6(3)

result = mk6_0.Connect()
command = MouldKingCrypt.CreateTelegramForHCITool(MouldKing_6.ManufacturerID, result)
print(command)
subprocess.call(["sudo", "hcitool -i hci0 cmd 08 0008 " + command])

# result = mk6_0.SetChannel(0, 1)
# print(' '.join(f'{x:02x}' for x in result))

# result = mk6_0.SetChannel(0, 10)
# print(' '.join(f'{x:02x}' for x in result))

# result = mk6_0.SetChannel(0, -1)
# print(' '.join(f'{x:02x}' for x in result))

