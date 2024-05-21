# mkconnect-python
...a bit of code to connect to MouldKing bluetooth bricks in python

# MouldKing Hubs
## MouldKing 6.0 Hub
The MouldKing 6.0 hub has two modes:
* rc mode to be controlled with the remotecontrol
* bluetooth mode to be controlled with an app
You can control a maximum of three 6.0 hubs at the same time with bluetooth.
> (Currently this project can send only one advertising telegram the same time - so only one hub can be controlled, all others will go in timeout-mode till next telegram with their device address is sent.)

To switch the hubs device address to the next one (device 0, device 1, device 2) just press the button on the hub.

> i.E.: If the script runs with mkcontrol(2,0,1) and nothing is happening, you have to short-press the button, perhaps again...)

## usage
Start the script [consoletest.py](https://github.com/J0EK3R/mkconnect-python/blob/main/consoletest.py) on your raspberry:
```
pi@devpi:~/dev/mkconnect-python $ sudo python -i consoletest.py 
```

### mkbtstop() - stop bluetooth advertising
```
Ready to execute commands

>>> mkbtstop()
```

### mkconnect() - switch hubs in bluetooth mode
If you power-on the hubs they will listen to telegrams to the **first device by default**.
```
Ready to execute commands

>>> mkconnect()
```

### mkcontrol(deviceId, channel, power and powerAndDirection)
i.E.: mkcontrol(0, 0, 1) - on first device (deviceId=0) run channel A (channel=0) with fullspeed (powerAndDirection=1)
```
Ready to execute commands

>>> mkcontrol(0, 0, 1)
```

### mkstop(deviceId)
Set all channels of device to zero
```
Ready to execute commands

>>> mkstop(0)
```


# old stuff

There is a testscript [consoletest.py](https://github.com/J0EK3R/mkconnect-python/blob/main/consoletest.py) where (on raspberry pi) **hcitool** is used to advertise telegrams over bluetooth.

Maybe you habe to **sudo** the command:
```
pi@devpi:~/dev/mkconnect-python $ sudo python -i consoletest.py 

Ready to execute commands

For connecting: mkconnect(hubId) ex: mkconnect(0) or mkconnect(1) for the second hub

 Available commands: mkconnect(hubId)
 mkstop(hubId)
 mkcontrol(deviceId, channel, powerAndDirection)

ex: mkcontrol(0, 0, 0.5) ; mkcontrol(0, 'B', -1)
 the minus sign - indicate reverse motor direction
```





Just look in [main.py](https://github.com/J0EK3R/mkconnect-python/blob/main/main.py) for current usage...

Current output in [https://wokwi.com/projects/new/micropython-pi-pico](https://wokwi.com/projects/398314618803830785)
...looks very good! :)
```
connect-telegram
rawdata: 6d 7b a7 80 80 80 80 92
crypted: 6d b6 43 cf 7e 8f 47 11 88 66 59 38 d1 7a aa 26 49 5e 13 14 15 16 17 18

stop-telegram
rawdata: 61 7b a7 80 80 80 80 80 80 9e
crypted: 6d b6 43 cf 7e 8f 47 11 84 66 59 38 d1 7a aa 34 67 4a 55 bf 15 16 17 18

C1: fullspeed forwards
rawdata: 61 7b a7 ff 80 80 80 80 80 9e
crypted: 6d b6 43 cf 7e 8f 47 11 84 66 59 47 d1 7a aa 34 67 4a ed b7 15 16 17 18

C1: halfspeed forwards
rawdata: 61 7b a7 bf 80 80 80 80 80 9e
crypted: 6d b6 43 cf 7e 8f 47 11 84 66 59 07 d1 7a aa 34 67 4a eb 70 15 16 17 18

C1: halfspeed backwards
rawdata: 61 7b a7 40 80 80 80 80 80 9e
crypted: 6d b6 43 cf 7e 8f 47 11 84 66 59 f8 d1 7a aa 34 67 4a 4e fe 15 16 17 18

C2: halfspeed backwards
rawdata: 61 7b a7 40 40 80 80 80 80 9e
crypted: 6d b6 43 cf 7e 8f 47 11 84 66 59 f8 11 7a aa 34 67 4a 3d f9 15 16 17 18
MicroPython v1.22.0 on 2023-12-27; Raspberry Pi Pico with RP2040
Type "help()" for more information.
>>> 
raw REPL; CTRL-B to exit
>
```
