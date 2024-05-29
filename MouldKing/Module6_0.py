__author__ = "J0EK3R"
__version__ = "0.1"

import sys

sys.path.append("Tracer") 
from Tracer.Tracer import Tracer

sys.path.append("Advertiser") 
from Advertiser.Advertiser import Advertiser

sys.path.append("MouldKing") 
from MouldKing.MouldKing_6 import MouldKing_6

class Module6_0 :
    """
    abstract class to store the static objects
    """

    Device0 = MouldKing_6(0)
    """
    MouldKing Hub 6.0 with address 1
    """

    Device1 = MouldKing_6(1)
    """
    MouldKing Hub 6.0 with address 2
    """

    Device2 = MouldKing_6(2)
    """
    MouldKing Hub 6.0 with address 3
    """

    @staticmethod
    def SetAdvertiser(advertiser: Advertiser) -> Advertiser:
        """
        Set Advertiser for all MouldKing 6.0 Hubs
        """

        Module6_0.Device0.SetAdvertiser(advertiser)
        Module6_0.Device1.SetAdvertiser(advertiser)
        Module6_0.Device2.SetAdvertiser(advertiser)
        return advertiser

    @staticmethod
    def SetTracer(tracer: Tracer) -> Tracer:
        """
        Set Tracer for all MouldKing 6.0 Hubs
        """

        Module6_0.Device0.SetTracer(tracer)
        Module6_0.Device1.SetTracer(tracer)
        Module6_0.Device2.SetTracer(tracer)
        return tracer
