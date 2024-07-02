import asyncio
import logging
import sys

logger = logging.getLogger(__name__)

logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO)

print('Script: mqtt_to_mk.py')
print('Platform: ' + sys.platform)

client = None

sys.path.append("Advertiser") 
# uncomment to choose advertiser
if (sys.platform == 'linux'):
    #from Advertiser.AdvertiserHCITool import AdvertiserHCITool as Advertiser
    #from Advertiser.AdvertiserBTMgmt import AdvertiserBTMgmt as Advertiser
    from Advertiser.AdvertiserBTSocket import AdvertiserBTSocket as Advertiser

    from contextlib import AsyncExitStack, asynccontextmanager
    from random import randrange
    from asyncio_mqtt import Client, MqttError    
    pass
elif (sys.platform == 'rp2'):
    from Advertiser.AdvertiserMicroPython import AdvertiserMicroPython as Advertiser

    from lib.mqtt_as import MQTTClient, config

    # Local configuration
    config['ssid'] = ''
    config['wifi_pw'] = 'enter password'
    config['server'] = '192.168.0.131'
    config["queue_len"] = 1  # Use event interface with default queue size

    #MQTTClient.DEBUG = True  # Optional: print diagnostic messages
    client = MQTTClient(config)

    pass
elif (sys.platform == 'win32'):
    from Advertiser.AdvertiserDummy import AdvertiserDummy as Advertiser
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

hubs = [hub0, hub1, hub2, hub3, hub4, hub5]

async def process(topic_str: str, msg_str: str):
    try:
        if(topic_str.startswith('mk/hub')):
            hubId = int(topic_str[6])

            if(hubId < 0 or hubId >= len(hubs)):
                return
            
            hub = hubs[hubId]

            if('connect' in topic_str):
                if(msg_str == '1'):
                    await hub.connect()
                else:
                    await hub.disconnect()

            elif('channel' in topic_str):
                channelStartIndex = topic_str.index('channel') + len('channel')
                channelId = int(topic_str[channelStartIndex :])
                
                # print(f'channelStartIndex: {channelStartIndex} channelId: {channelId}')

                if(channelId >= 0 and channelId < hub.get_number_of_channels()):
                    await hub.set_channel(channelId, float(msg_str))
    except:
        pass

async def messages(client):  # Respond to incoming messages
    async for topic, msg, retained in client.queue:
        try:
            topic_str = topic.decode()
            msg_str = msg.decode()

            await process(topic_str, msg_str)

        except:
            pass


async def up(client):  # Respond to connectivity being (re)established
    while True:
        await client.up.wait()  # Wait on an Event
        client.up.clear()
        await client.subscribe('mk/#', 1)  # renew subscriptions
        print('up')


async def advanced_example():
    # We 💛 context managers. Let's create a stack to help
    # us manage them.
    async with AsyncExitStack() as stack:
        # Keep track of the asyncio tasks that we create, so that
        # we can cancel them on exit
        tasks = set()
        stack.push_async_callback(cancel_tasks, tasks)

        # Connect to the MQTT broker
        client = Client("192.168.0.131")
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
            task = asyncio.create_task(process_messages(messages))
            tasks.add(task)

        # Messages that doesn't match a filter will get logged here
        messages = await stack.enter_async_context(client.unfiltered_messages())
        task = asyncio.create_task(log_messages(messages, "[unfiltered] {}"))
        tasks.add(task)

        # Subscribe to topic(s)
        # 🤔 Note that we subscribe *after* starting the message
        # loggers. Otherwise, we may miss retained messages.
        await client.subscribe("mk/#")

        # Publish a random value to each of these topics
        topics = (
            "floors/basement/humidity",
            "floors/rooftop/humidity",
            "floors/rooftop/illuminance",
            # 👉 Try to add more topics!
        )
#        task = asyncio.create_task(post_to_topics(client, topics))
#        tasks.add(task)

        task = asyncio.create_task(post_init(client))
        tasks.add(task)

        # Wait for everything to complete (or fail due to, e.g., network
        # errors)
        await asyncio.gather(*tasks)

async def post_init(client):
    # init topics
    hubId = 0
    for hub in hubs:
        await client.publish(f'mk/hub{hubId}/AdvertisementIdentifier', hub.get_advertisement_identifier(), qos = 1)
        await client.publish(f'mk/hub{hubId}/connect', '{}'.format(0), qos = 1)

        for channelId in range(hub.get_number_of_channels()):
            await client.publish(f'mk/hub{hubId}/channel{channelId}', '{}'.format(0), qos = 1)

        hubId += 1

    await MouldKing.set_advertiser(advertiser)


async def post_to_topics(client, topics):
    while True:
        for topic in topics:
            message = randrange(100)
            print(f'[topic="{topic}"] Publishing message={message}')
            await client.publish(topic, message, qos=1)
            await asyncio.sleep(2)

async def log_messages(messages, template):
    async for message in messages:
        print(template.format(message.payload.decode()))
#        await process(message.topic, message.payload.decode())

async def process_messages(messages):
    async for message in messages:
        await process(message.topic, message.payload.decode())


async def cancel_tasks(tasks):
    for task in tasks:
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass

async def main():

    # Run the advanced_example indefinitely. Reconnect automatically
    # if the connection is lost.
    reconnect_interval = 3  # [seconds]
    while True:
        try:
            await advanced_example()
        except MqttError as error:
            print(f'Error "{error}". Reconnecting in {reconnect_interval} seconds.')
        finally:
            await asyncio.sleep(reconnect_interval)


asyncio.run(main())
