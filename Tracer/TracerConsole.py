__author__ = "J0EK3R"
__version__ = "0.1"

import sys

sys.path.append("Tracer") 
from Tracer.Tracer import Tracer

class TracerConsole(Tracer) :
    """
    baseclass
    """

    def __init__(self):
        """
        initializes the object and defines the fields
        """

        super().__init__()


    def TraceInfo(self, value: str=""):
        """
        prints out
        """
        print(value)

