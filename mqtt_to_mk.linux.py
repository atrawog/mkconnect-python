# This example connects to a mqtt-broker and publishes the states of all hubs.
# Each hub creates an own topic containing sub-topics for 'connect' and each 'channel'.
# By modifying the topics 'connect' and 'channel' i.e. with a mqtt-client you can control
# the hubs and set the values of the hub's channels.
#
# This example uses asyncio-mqtt (https://pypi.org/project/asyncio-mqtt/) wich has to be
# installed first.


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

# create and setup logger
logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO)

print('Script: mqtt_to_mk.linux.py')
print('Platform: ' + sys.platform)

sys.path.append("MouldKing") 
from MouldKing.MouldKing import MouldKing

sys.path.append("Advertiser")
from Advertiser.IAdvertisingDevice import IAdvertisingDevice

if (sys.platform == 'linux'):
    # uncomment to choose advertiser
    # from Advertiser.AdvertiserHCITool import AdvertiserHCITool as Advertiser      # worsest choice
    # from Advertiser.AdvertiserBTMgmt import AdvertiserBTMgmt as Advertiser        # should work
    from Advertiser.AdvertiserBTSocket import AdvertiserBTSocket as Advertiser      # best choice

    from contextlib import AsyncExitStack, asynccontextmanager
    from asyncio_mqtt import Client, MqttError    

    # funkction to create MQTT-client
    def mqtt_create_client():
        logger.info('Creating MQTT-Client')
        return Client(mqtt_brocker_ip)


    def bt_create_advertiser():
        logger.info('Creating Bluetooth-Advertiser')
        return Advertiser()


    async def mqtt_connect(mqtt_client):
        # We 💛 context managers. Let's create a stack to help
        # us manage them.
        async with AsyncExitStack() as stack:
            # Keep track of the asyncio tasks that we create, so that
            # we can cancel them on exit
            tasks = set()
            stack.push_async_callback(cancel_tasks, tasks)

            # Connect to the MQTT broker
            await stack.enter_async_context(mqtt_client)

            # You can create any number of topic filters
            topic_filters = (
                mqtt_topic_base + "/#",
                #"floors/rooftop/#"
                # 👉 Try to add more filters!
            )

            for topic_filter in topic_filters:
                # Log all messages that matches the filter
                manager = mqtt_client.filtered_messages(topic_filter)
                messages = await stack.enter_async_context(manager)
                task = asyncio.create_task(mqtt_process_messages(mqtt_client, messages))
                tasks.add(task)

            # Subscribe to topic(s)
            # 🤔 Note that we subscribe *after* starting the message
            # loggers. Otherwise, we may miss retained messages.
            await mqtt_client.subscribe(mqtt_topic_base + "/#")

            task = asyncio.create_task(mqtt_publish_hubs(mqtt_client))
            tasks.add(task)

            # Wait for everything to complete (or fail due to, e.g., network
            # errors)
            await asyncio.gather(*tasks)


    async def mqtt_loop(mqtt_client):  # Respond to connectivity being (re)established
        logger.info('Created task mqtt_loop')

        # Run the connect_mqtt indefinitely.
        # Reconnect automatically if the connection is lost.
        while True:
            try:
                await mqtt_connect(mqtt_client)
            except MqttError as error:
                logger.info(f'Error "{error}". Reconnecting in {mqtt_reconnect_interval} seconds.')
            finally:
                await asyncio.sleep(mqtt_reconnect_interval)

    async def mqtt_stop(mqtt_client):
        pass

    pass

else:
    raise Exception('unsupported platform')

######################################################
# globals

# save pre-instantiated objects in global variables
hub0 = MouldKing.Module6_0.Device0
hub1 = MouldKing.Module6_0.Device1
hub2 = MouldKing.Module6_0.Device2

hub3 = MouldKing.Module4_0.Device0
hub4 = MouldKing.Module4_0.Device1
hub5 = MouldKing.Module4_0.Device2

# array of all hubs
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


async def mqtt_process_messages(mqtt_client, messages) -> None:
    """ process all incoming messages

    :param mqtt_client: mqtt_client
    :param messages: list of messages to process
    :return: returns nothing
    """
    async for message in messages:
        await mqtt_process_message(mqtt_client, message.topic, message.payload.decode())


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


async def cancel_tasks(tasks) -> None:
    """ cancel each task in given list

    :param tasks: list of tasks to cancel
    :return: returns nothing
    """
    for task in tasks:
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass


async def main():
    try:
        # instantiate Advertiser
        advertiser = bt_create_advertiser()
        await MouldKing.set_advertiser(advertiser)

        # instantiate MQTT-Client
        mqtt_client = mqtt_create_client()

        # run mqtt-loop
        asyncio.create_task(mqtt_loop(mqtt_client))

        # main-loop
        while True:
            await asyncio.sleep(5)

    finally:
        await advertiser.advertisement_stop()
        await mqtt_stop(mqtt_client)


if __name__ == "__main__":
    asyncio.run(main())
