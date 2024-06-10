__author__ = "J0EK3R"
__version__ = "0.1"

import sys

sys.path.append("Tracer") 
from Tracer.Tracer import Tracer

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

        return

    def AdvertisementStop(self) -> None:
        """
        stop bluetooth advertising

        """

        return

    def AdvertisementDataSet(self, identifier: str, manufacturerId: bytes, rawdata: bytes) -> None:
        """
        Set Advertisement data
        """
        return
