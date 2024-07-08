""" (kind of interface) for AdvertisingDevice
This Type mustn't import any Advertiser stuff!
To prevent cyclic imports caused by imports of Advertiser <--> AdvertisingDevice.
"""

__author__ = "J0EK3R"
__version__ = "0.1"


class IAdvertisingDevice :
    """ (kind of interface) for AdvertisingDevice
    This Type mustn't import any Advertiser stuff!
    To prevent cyclic imports caused by imports of Advertiser <--> AdvertisingDevice.
    """


    def get_typename(self) -> str:
        """ Returns the typename of the device.
        This Methode has to be overridden by the implementation of the AdvertisingDevice!

        :return: returns a string containing the typename
        """
        raise NotImplementedError # override this methode


    def get_advertisement_identifier(self) -> str:
        """ Returns the AdvertisementIdentifier to differentiate the Advertising-Data.
        The AdvertisementIdentifier is used to register the Advertising-Data object.
        This Methode has to be overridden by the implementation of the AdvertisingDevice!

        Some AdvertisingDevices like MouldKing 4.0 Hub use only one Advertising telegram for all 
        (three possible) devices. So each AdvertisingDevices returns the same AdvertisementIdentifier

        :return: returns the AdvertisementIdentifier
        """
        raise NotImplementedError # override this methode


    def get_number_of_channels(self) -> int:
        """ Returns the number of channels.
        This Methode has to be overridden by the implementation of the AdvertisingDevice!

        :return: returns the number of channels
        """
        raise NotImplementedError # override this methode


    def get_is_connected(self) -> bool:
        """ Returns true if device is connected.
        This Methode has to be overridden by the implementation of the AdvertisingDevice!

        :return: returns true if device is connected
        """
        raise NotImplementedError # override this methode


    async def connect(self) -> None:
        """ connects the device to the advertiser

        :return: returns nothing
        """
        raise NotImplementedError # override this methode


    async def disconnect(self) -> None:
        """ disconnects the device from the advertiser

        :return: returns nothing
        """
        raise NotImplementedError # override this methode


    async def stop(self) -> bytes:
        """ stops the device by setting the internal stored values of all channels to zero and return the telegram

        :return: returns the generated rawdata
        """
        raise NotImplementedError # override this methode
    

    async def set_channel(self, channelId: int, value: float) -> bytes:
        """ set internal stored value of channel with channelId to value and return the telegram

        :param channelId: identifier for the channel
        :param value: value to set for the channel
        :return: returns the generated rawdata
        """
        raise NotImplementedError # override this methode


    def get_channel(self, channelId: int) -> float:
        """ get internal stored value of channel with channelId

        :param channelId: identifier for the channel
        :param value: value to set for the channel
        :return: returns the internal stored value
        """
        raise NotImplementedError # override this methode
