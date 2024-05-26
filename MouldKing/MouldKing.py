__author__ = "J0EK3R"
__version__ = "0.1"

import abc

# import hack for micro-python-simulator with flat filesystem
try:
    from MouldKing.Module6_0 import Module6_0
except ImportError:
    from Module6_0 import Module6_0

class MouldKing :
    """
    abstract class to store the static objects
    """

    Module6_0 = Module6_0()


