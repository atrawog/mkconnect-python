__author__ = "J0EK3R"
__version__ = "0.1"

import sys

sys.path.append("Tracer") 
from Tracer.Tracer import Tracer

sys.path.append("Advertiser") 
from Advertiser.Advertiser import Advertiser

sys.path.append("MouldKing") 
from MouldKing.MouldKing_4_Hub import MouldKing_4_Hub
from MouldKing.MouldKing_6_Hub import MouldKing_6_Hub

class MouldKing :
    """
    abstract class to store the static objects
    """

    class Module4_0 :
        """
        abstract class to store the static objects
        """

        Device0 = MouldKing_4_Hub(0)
        """
        MouldKing Hub 4.0 with address 1
        """

        Device1 = MouldKing_4_Hub(1)
        """
        MouldKing Hub 4.0 with address 2
        """

        Device2 = MouldKing_4_Hub(2)
        """
        MouldKing Hub 4.0 with address 3
        """

        @staticmethod
        def SetAdvertiser(advertiser: Advertiser) -> Advertiser:
            """
            Set Advertiser for all MouldKing 4.0 Hubs
            """

            # MouldKing_4_Hubs is the same instance for all MouldKing_4_Hub-Instances
            MouldKing.Module4_0.Device0.MouldKing_4_Hubs.SetAdvertiser(advertiser)
            # MouldKing.Module4_0.Device1.MouldKing_4_Hubs.SetAdvertiser(advertiser)
            # MouldKing.Module4_0.Device2.MouldKing_4_Hubs.SetAdvertiser(advertiser)
            return advertiser

        @staticmethod
        def SetTracer(tracer: Tracer) -> Tracer:
            """
            Set Tracer for all MouldKing 4.0 Hubs
            """

            MouldKing.Module4_0.Device0.SetTracer(tracer)
            MouldKing.Module4_0.Device1.SetTracer(tracer)
            MouldKing.Module4_0.Device2.SetTracer(tracer)
            return tracer

    class Module6_0 :
        """
        abstract class to store the static objects
        """

        Device0 = MouldKing_6_Hub(0)
        """
        MouldKing Hub 6.0 with address 1
        """

        Device1 = MouldKing_6_Hub(1)
        """
        MouldKing Hub 6.0 with address 2
        """

        Device2 = MouldKing_6_Hub(2)
        """
        MouldKing Hub 6.0 with address 3
        """

        @staticmethod
        def SetAdvertiser(advertiser: Advertiser) -> Advertiser:
            """
            Set Advertiser for all MouldKing 6.0 Hubs
            """

            MouldKing.Module6_0.Device0.SetAdvertiser(advertiser)
            MouldKing.Module6_0.Device1.SetAdvertiser(advertiser)
            MouldKing.Module6_0.Device2.SetAdvertiser(advertiser)
            return advertiser

        @staticmethod
        def SetTracer(tracer: Tracer) -> Tracer:
            """
            Set Tracer for all MouldKing 6.0 Hubs
            """

            MouldKing.Module6_0.Device0.SetTracer(tracer)
            MouldKing.Module6_0.Device1.SetTracer(tracer)
            MouldKing.Module6_0.Device2.SetTracer(tracer)
            return tracer
    
    @staticmethod
    def SetAdvertiser(advertiser: Advertiser) -> Advertiser:
        """
        Set Advertiser for all MouldKing 4.0 Hubs
        """

        # MouldKing_4_Hubs is the same instance for all MouldKing_4_Hub-Instances
        MouldKing.Module4_0.SetAdvertiser(advertiser)
        MouldKing.Module6_0.SetAdvertiser(advertiser)
        return advertiser

    @staticmethod
    def SetTracer(tracer: Tracer) -> Tracer:
        """
        Set Tracer for all MouldKing 4.0 Hubs
        """

        MouldKing.Module4_0.SetTracer(tracer)
        MouldKing.Module6_0.SetTracer(tracer)
        return tracer
