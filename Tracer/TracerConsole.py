__author__ = "J0EK3R"
__version__ = "0.1"

# import hack for micro-python-simulator with flat filesystem
try:
    from Tracer.Tracer import Tracer
except ImportError:
    from Tracer import Tracer

class TracerConsole(Tracer) :
    """
    baseclass
    """

    def __init__(self):
        """
        initializes the object and defines the fields
        """

        super().__init__()


    def TraceInfo(value: str):
        """
        prints out
        """
        print(value)

