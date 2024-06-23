""" Dummy Advertiser
"""

import sys
import logging
sys.path.append("Advertiser") 
from Advertiser.Advertiser import Advertiser


__author__ = "J0EK3R"
__version__ = "0.1"


logger = logging.getLogger(__name__)


class AdvertiserDummy(Advertiser) :
    """ Dummy Advertiser
    """

    def __init__(self):
        """ initializes the object and defines the fields
        """
        super().__init__()

        logger.debug("AdvertiserDummy.__init__")

        return


    async def advertisement_stop(self) -> None:
        """ stop bluetooth advertising

        :return: returns nothing
        """
        logger.debug("AdvertiserDummy.advertisement_stop")

        return


    def set_advertisement_data(self, advertisementIdentifier: str, manufacturerId: bytes, rawdata: bytes) -> None:
        """ Set Advertisement data

        :param advertisementIdentifier:  advertisementIdentifier
        :param manufacturerId: manufacturerId
        :param rawdata: rawdata
        :return: returns nothing
        """
        logger.debug("AdvertiserDummy.AdvertisementDataSet")

        return
