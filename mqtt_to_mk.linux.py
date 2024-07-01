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

    import asyncio
    import aiomqtt
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

async def messages(client):  # Respond to incoming messages
    async for topic, msg, retained in client.queue:
        try:
            topic_str = topic.decode()
            msg_str = msg.decode()

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


async def up(client):  # Respond to connectivity being (re)established
    while True:
        await client.up.wait()  # Wait on an Event
        client.up.clear()
        await client.subscribe('mk/#', 1)  # renew subscriptions
        print('up')


async def main():
    async with aiomqtt.Client("192.168.0.131") as client:
        await client.subscribe("'mk/#'")
        async for message in client.messages:
            if message.topic.matches('mk/hub'):
                print("A:", message.payload)

asyncio.run(main())
