# settings
mqtt_brocker_ip = '192.168.0.131' # set ip-adress of mqtt broker
mqtt_reconnect_interval = 3  # [seconds]

mqtt_topic_base = 'mouldking'
mqtt_topic_hub_base = mqtt_topic_base + '/hub'
mqtt_topic_hub = mqtt_topic_hub_base + '{hubId:}'
mqtt_topic_info = mqtt_topic_hub + '/info'
mqtt_topic_advertisementIdentifier = mqtt_topic_info + '/advertisementIdentifier'
mqtt_topic_type = mqtt_topic_info + '/typename'
mqtt_topic_connect = mqtt_topic_hub + '/connect'
mqtt_topic_channel = mqtt_topic_hub + '/channel{channelId:}'

# imports
import asyncio
import logging
import sys

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO)

print('Script: mqtt_to_mk.py')
print('Platform: ' + sys.platform)

sys.path.append("Advertiser") 
from Advertiser.IAdvertisingDevice import IAdvertisingDevice

if (sys.platform == 'linux'):
    # uncomment to choose advertiser
    #from Advertiser.AdvertiserHCITool import AdvertiserHCITool as Advertiser
    #from Advertiser.AdvertiserBTMgmt import AdvertiserBTMgmt as Advertiser
    from Advertiser.AdvertiserBTSocket import AdvertiserBTSocket as Advertiser
    
    pass

elif (sys.platform == 'rp2'):
    from Advertiser.AdvertiserMicroPython import AdvertiserMicroPython as Advertiser

    from lib.mqtt_as import MQTTClient, config

    # function to create MQTT-client
    def mqtt_create_Client():
        logger.info('Creating MQTT-Client')
        # Local configuration
        # config['ssid'] = enter ssid
        # config['wifi_pw'] = enter password
        config['ssid'] = enter ssid
        config['wifi_pw'] = enter password
        config['server'] = mqtt_brocker_ip
        config["queue_len"] = 1  # Use event interface with default queue size

        #MQTTClient.DEBUG = True  # Optional: print diagnostic messages
        return MQTTClient(config)
    
    def createAdvertiser():
        logger.info('Creating Bluetooth-Advertiser')
        return Advertiser()

    pass

elif (sys.platform == 'win32'):
    from Advertiser.AdvertiserDummy import AdvertiserDummy as Advertiser

    # function to create MQTT-client
    def mqtt_create_Client():
        return None

    def createAdvertiser():
        return Advertiser()
    
    pass
else:
    raise Exception('unsupported platform')

sys.path.append("MouldKing") 
from MouldKing.MouldKing import MouldKing

# save pre-instantiated objects in local variables
hub0 = MouldKing.Module6_0.Device0
hub1 = MouldKing.Module6_0.Device1
hub2 = MouldKing.Module6_0.Device2

hub3 = MouldKing.Module4_0.Device0
hub4 = MouldKing.Module4_0.Device1
hub5 = MouldKing.Module4_0.Device2

hubs = [hub0, hub1, hub2, hub3, hub4, hub5]


async def mqtt_publish_hubs(mqtt_Client) -> None:
    """ for all hubs publish current state and channel values with the given mqtt-client

    :param mqtt_Client: mqtt_Client
    :return: returns nothing
    """
    hubId: int = 0
    for hub in hubs:
        await mqtt_publish_hub_state(mqtt_Client, hub, hubId)

        hubId += 1


async def mqtt_publish_hub_state(mqtt_Client, hub: IAdvertisingDevice, hubId: int) -> None:
    """ publish current state and channel values of the given hub with the given mqtt-client

    :param mqtt_Client: mqtt_Client
    :param hub: hub
    :param hubId: id of the hub
    :return: returns nothing
    """
    # info:
    await mqtt_Client.publish(mqtt_topic_type.format(hubId = hubId), hub.get_typename())
    await mqtt_Client.publish(mqtt_topic_advertisementIdentifier.format(hubId = hubId), hub.get_advertisement_identifier())

    # command
    await mqtt_Client.publish(mqtt_topic_connect.format(hubId = hubId), str((int(hub.get_is_connected()))))

    for channelId in range(hub.get_number_of_channels()):
        await mqtt_Client.publish(mqtt_topic_channel.format(hubId = hubId, channelId = channelId), str(hub.get_channel(channelId)))


async def mqtt_process_messages(mqtt_client):  # Respond to incoming messages
    logger.info('Created task mqtt_process_messages')

    async for topic, msg, retained in mqtt_client.queue:
        try:
            topic_str = topic.decode()
            msg_str = msg.decode()

            logger.info(topic_str)

            await mqtt_process_message(mqtt_client, topic_str, msg_str)
        except:
            pass


async def mqtt_process_message(mqtt_client, topic_str: str, msg_str: str) -> None:
    """ process the incomming mqtt messages

    :param mqtt_Client: mqtt_Client
    :param topic_str: topic string
    :param msg_str: message string
    :return: returns nothing
    """
    try:
        if(topic_str.startswith(mqtt_topic_hub_base)):
            # extract hubId from message
            hubId = int(topic_str[len(mqtt_topic_hub_base)])

            if(hubId < 0 or hubId >= len(hubs)):
                return
            
            # take hub from array
            hub = hubs[hubId]

            # command 'connect'
            if('connect' in topic_str):
                mqttValue = bool(msg_str == '1')
                currentValue: bool = hub.get_is_connected()

                # only set on changed value
                if(mqttValue == currentValue):
                    return
                
                if(mqttValue):
                    await hub.connect()
                else:
                    await hub.disconnect()
                    # update state
                    # on disconnect all channel values are set to 0
                    await mqtt_publish_hub_state(mqtt_client, hub, hubId)

            # command 'channel'
            elif('channel' in topic_str):
                channelStartIndex = topic_str.index('channel') + len('channel')
                channelId = int(topic_str[channelStartIndex :])
                
                if(channelId < 0 or channelId >= hub.get_number_of_channels()):
                    return

                mqttValue = float(msg_str)
                currentValue = hub.get_channel(channelId)

                # only set on changed value
                if(mqttValue == currentValue):
                    return
                
                await hub.set_channel(channelId, mqttValue)

            # unhandled command
            else:
                pass

    except:
        pass


async def mqtt_loop(mqtt_client):  # Respond to connectivity being (re)established
    logger.info('Created task mqtt_loop')

    for coroutine in (mqtt_process_messages, mqtt_publish_hubs):
        asyncio.create_task(coroutine(mqtt_client))

    while True:
        await mqtt_client.up.wait()  # Wait on an Event
        mqtt_client.up.clear()
        await mqtt_client.subscribe(mqtt_topic_base + '/#', 1)  # renew subscriptions


async def main():
    try:
        # instantiate Advertiser
        advertiser = createAdvertiser()
        await MouldKing.set_advertiser(advertiser)

        mqtt_client = mqtt_create_Client()
        await mqtt_client.connect()
        logger.info('MQTT-Client connected')

        # run mqtt-loop
        asyncio.create_task(mqtt_loop(mqtt_client))

        # main-loop
        while True:
            await asyncio.sleep(5)

    finally:
        advertiser.advertisement_stop()
        mqtt_client.close()  # Prevent LmacRxBlk:1 errors


if __name__ == "__main__":
    asyncio.run(main())
