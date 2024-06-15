import sys
import time

if (sys.platform == 'rp2'):
    import _thread as thread
else:
    import threading as thread

class Test:

    def __init__(self):
        """
        initializes the object and defines the member fields
        """
        print("Test.init:")
        self._advertisement_thread = None
        self._advertisement_thread_Lock = thread.allocate_lock()
        self._advertisement_thread_Run = False
        return

    def start(self) -> None:
        print("Test.start:")
        if(not self._advertisement_thread_Run):
            self._advertisement_thread_Run = True
            self._advertisement_thread = thread.start_new_thread(self._publish, ())

        time.sleep(2)
        return

    def _publish(self) -> None:
        """
        publishing loop
        """

        print('AdvertiserMicroPython._publish: started ' + str(self._advertisement_thread_Run))

        # loop while field is True
        while(self._advertisement_thread_Run):
            print('AdvertiserMicroPython._publish: started')