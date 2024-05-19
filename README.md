# mkconnect-python
...some little code to connect to MouldKing bluetooth bricks

At the moment we only are able to generate the rawdata-bytearrays to be advertised over bluetooth - no bluetooth functionality yet.

Just look in [main.py](https://github.com/J0EK3R/mkconnect-python/blob/main/main.py) for the current usage...

Current output in [micropython-pi-pico-simulator](https://wokwi.com/projects/new/micropython-pi-pico)
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
