__author__ = "J0EK3R"
__version__ = "0.1"

class AdvertisingDevice :
    """
    baseclass
    """
    
    def __init__(self):
        """
        initializes the object and defines the fields
        """

        self._advertiser = None

    def SetAdvertiser(self, advertiser):
        self._advertiser = advertiser


