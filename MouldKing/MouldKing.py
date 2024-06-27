__author__ = "J0EK3R"
__version__ = "0.1"

import sys
import logging

logger = logging.getLogger(__name__)

sys.path.append("Advertiser") 
from Advertiser.Advertiser import Advertiser

sys.path.append("MouldKing") 
from MouldKing.MouldKing_Hub_4 import MouldKing_Hub_4
from MouldKing.MouldKing_Hub_6 import MouldKing_Hub_6

class MouldKing :
    """
    abstract class to store the static objects
    """

    class Module4_0 :
        """
        abstract class to store the static objects
        """

        Device0 = MouldKing_Hub_4(0)
        """
        MouldKing Hub 4.0 with address 1
        """

        Device1 = MouldKing_Hub_4(1)
        """
        MouldKing Hub 4.0 with address 2
        """

        Device2 = MouldKing_Hub_4(2)
        """
        MouldKing Hub 4.0 with address 3
        """

        @staticmethod
        async def set_advertiser(advertiser: Advertiser) -> Advertiser:
            """
            Set Advertiser for all MouldKing 4.0 Hubs
            """

            # MouldKing_4_Hubs is the same instance for all MouldKing_4_Hub-Instances
            await MouldKing.Module4_0.Device0._MouldKing_4_Hubs.set_advertiser(advertiser)
            # MouldKing.Module4_0.Device1.MouldKing_4_Hubs.set_advertiser(advertiser)
            # MouldKing.Module4_0.Device2.MouldKing_4_Hubs.set_advertiser(advertiser)
            return advertiser


    class Module6_0 :
        """
        abstract class to store the static objects
        """

        Device0 = MouldKing_Hub_6(0)
        """
        MouldKing Hub 6.0 with address 1
        """

        Device1 = MouldKing_Hub_6(1)
        """
        MouldKing Hub 6.0 with address 2
        """

        Device2 = MouldKing_Hub_6(2)
        """
        MouldKing Hub 6.0 with address 3
        """

        @staticmethod
        async def set_advertiser(advertiser: Advertiser) -> Advertiser:
            """
            Set Advertiser for all MouldKing 6.0 Hubs
            """

            await MouldKing.Module6_0.Device0.set_advertiser(advertiser)
            await MouldKing.Module6_0.Device1.set_advertiser(advertiser)
            await MouldKing.Module6_0.Device2.set_advertiser(advertiser)
            return advertiser


    @staticmethod
    async def set_advertiser(advertiser: Advertiser) -> Advertiser:
        """
        Set Advertiser for all MouldKing 4.0 Hubs
        """

        # MouldKing_4_Hubs is the same instance for all MouldKing_4_Hub-Instances
        await MouldKing.Module4_0.set_advertiser(advertiser)
        await MouldKing.Module6_0.set_advertiser(advertiser)
        return advertiser
