__author__ = "J0EK3R"
__version__ = "0.1"

import sys
import logging

logger = logging.getLogger(__name__)

sys.path.append("Advertiser") 
from Advertiser.Advertiser import Advertiser


class AdvertiserDummy(Advertiser) :
    """
    Dummy Advertiser
    """

    def __init__(self):
        """
        initializes the object and defines the fields
        """
        super().__init__()

        logger.debug("AdvertiserDummy.__init__")

        return


    def AdvertisementStop(self) -> None:
        """
        stop bluetooth advertising

        """
        logger.debug("AdvertiserDummy.AdvertisementStop")

        return


    def AdvertisementDataSet(self, identifier: str, manufacturerId: bytes, rawdata: bytes) -> None:
        """
        Set Advertisement data
        """
        logger.debug("AdvertiserDummy.AdvertisementDataSet")

        return
