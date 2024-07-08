import asyncio
import logging
import sys

# create and setup logger
logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO)

print('Script: mqtt_to_mk.linux.py')
print('Platform: ' + sys.platform)

# set ip-adress of mqtt broker
mqttbrockerip = '192.168.0.131'

sys.path.append("Advertiser") 
if (sys.platform == 'linux'):
    # uncomment to choose advertiser
    #from Advertiser.AdvertiserHCITool import AdvertiserHCITool as Advertiser
    #from Advertiser.AdvertiserBTMgmt import AdvertiserBTMgmt as Advertiser
    from Advertiser.AdvertiserBTSocket import AdvertiserBTSocket as Advertiser

    from contextlib import AsyncExitStack, asynccontextmanager
    from random import randrange
    from asyncio_mqtt import Client, MqttError    

    # Connect to the MQTT broker
    def createClient():
        return Client(mqttbrockerip)
   
    pass
else:
    raise Exception('unsupported platform')

sys.path.append("MouldKing") 
from MouldKing.MouldKing import MouldKing

# instantiate Advertiser
advertiser = Advertiser()

# save pre-instantiated objects in local variables
hub0 = MouldKing.Module6_0.Device0
hub1 = MouldKing.Module6_0.Device1
hub2 = MouldKing.Module6_0.Device2

hub3 = MouldKing.Module4_0.Device0
hub4 = MouldKing.Module4_0.Device1
hub5 = MouldKing.Module4_0.Device2

# array of all hubs
hubs = [hub0, hub1, hub2, hub3, hub4, hub5]


async def publish_hubs(mqtt_Client) -> None:
    """ for all hubs publish current state and channel values with the given mqtt-client

    :param mqtt_Client: mqtt_Client
    :return: returns nothing
    """
    hubId: int = 0
    for hub in hubs:
        await publish_hub_state(mqtt_Client, hub, hubId)

        hubId += 1


async def publish_hub_state(mqtt_Client, hub, hubId: int) -> None:
    """ publish current state and channel values of the given hub with the given mqtt-client

    :param mqtt_Client: mqtt_Client
    :param hub: hub
    :param hubId: id of the hub
    :return: returns nothing
    """
    await mqtt_Client.publish(f'mk/hub{hubId}/AdvertisementIdentifier', hub.get_advertisement_identifier(), qos = 1)
    await mqtt_Client.publish(f'mk/hub{hubId}/connect', str((int(hub.get_is_connected()))), qos = 1)

    for channelId in range(hub.get_number_of_channels()):
        await mqtt_Client.publish(f'mk/hub{hubId}/channel{channelId}', str(hub.get_channel(channelId)), qos = 1)


async def process_mqtt_message(mqtt_client, topic_str: str, msg_str: str) -> None:
    """ process the incomming mqtt messages

    :param mqtt_Client: mqtt_Client
    :param topic_str: topic string
    :param msg_str: message string
    :return: returns nothing
    """
    try:
        if(topic_str.startswith('mk/hub')):
            # extract hubId from message
            hubId = int(topic_str[6])

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
                    await publish_hub_state(mqtt_client, hub, hubId)

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
                # update state
                # await publish_hub_state(mqtt_client, hub, hubId)
    except:
        pass


async def process_mqtt_messages(mqtt_client, messages) -> None:
    """ process all incoming messages

    :param mqtt_client: mqtt_client
    :param messages: list of messages to process
    :return: returns nothing
    """
    async for message in messages:
        await process_mqtt_message(mqtt_client, message.topic, message.payload.decode())


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


async def connect_mqtt():
    # We 💛 context managers. Let's create a stack to help
    # us manage them.
    async with AsyncExitStack() as stack:
        # Keep track of the asyncio tasks that we create, so that
        # we can cancel them on exit
        tasks = set()
        stack.push_async_callback(cancel_tasks, tasks)

        # Connect to the MQTT broker
        client = createClient()
        await stack.enter_async_context(client)

        # You can create any number of topic filters
        topic_filters = (
            "mk/#",
            #"floors/rooftop/#"
            # 👉 Try to add more filters!
        )

        for topic_filter in topic_filters:
            # Log all messages that matches the filter
            manager = client.filtered_messages(topic_filter)
            messages = await stack.enter_async_context(manager)
            task = asyncio.create_task(process_mqtt_messages(client, messages))
            tasks.add(task)

        # Subscribe to topic(s)
        # 🤔 Note that we subscribe *after* starting the message
        # loggers. Otherwise, we may miss retained messages.
        await client.subscribe("mk/#")

        task = asyncio.create_task(publish_hubs(client))
        tasks.add(task)

        # Wait for everything to complete (or fail due to, e.g., network
        # errors)
        await asyncio.gather(*tasks)


async def main():
    # set advertiser to all hubs
    await MouldKing.set_advertiser(advertiser)

    # Run the connect_mqtt indefinitely.
    # Reconnect automatically if the connection is lost.
    reconnect_interval = 3  # [seconds]
    while True:
        try:
            await connect_mqtt()
        except MqttError as error:
            print(f'Error "{error}". Reconnecting in {reconnect_interval} seconds.')
        finally:
            await asyncio.sleep(reconnect_interval)


if __name__ == "__main__":
    asyncio.run(main())
