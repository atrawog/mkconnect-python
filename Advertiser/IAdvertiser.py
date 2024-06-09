__author__ = "J0EK3R"
__version__ = "0.1"

class IAdvertiser :
    """
    (kind of) interface for Advertiser
    This Type mustn't import any AdvertisingDevice stuff!
    To prevent cyclic imports caused by imports of Advertiser <--> AdvertisingDevice.
    """