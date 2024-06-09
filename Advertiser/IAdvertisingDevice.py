__author__ = "J0EK3R"
__version__ = "0.1"

class IAdvertisingDevice :
    """
    (kind of interface) for AdvertisingDevice
    This Type mustn't import any Advertiser stuff!
    To prevent cyclic imports caused by imports of Advertiser <--> AdvertisingDevice.
    """

    def GetAdvertisementIdentifier(self) -> str:
        """
        Returns the AdvertisementIdentifier to differentiate the Advertising-Data.
        The AdvertisementIdentifier is used to register the Advertising-Data object.
        This Methode has to be overridden by the implementation of the AdvertisingDevice!

        Some AdvertisingDevices like MouldKing 4.0 Hub use only one Advertising telegram for all 
        (three possible) devices. So each AdvertisingDevices returns the same AdvertisementIdentifier
        """
        raise NotImplementedError # override this methode

