__author__ = "J0EK3R"
__version__ = "0.1"

# import hack for micro-python-simulator with flat filesystem
try:
    from Advertiser.AdvertiserBase import AdvertiserBase
except ImportError:
    from Advertiser import AdvertiserBase

class AdvertisingDevice :
    """
    baseclass
    """
    
    def __init__(self):
        """
        initializes the object and defines the fields
        """

        self._advertiser = None

    def SetAdvertiser(self, advertiser: AdvertiserBase):
        self._advertiser = advertiser


