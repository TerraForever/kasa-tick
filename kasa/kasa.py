from api.discovery import Discovery
from api.hs110 import HS110


def run():
    discovery = Discovery(domain='192.168.0.0/24')
    #discovery.discover()
    discovery.load()
    print(discovery.get_items('HS100'))
    print(discovery.get_all_items())

    plug = HS110("192.168.0.214")
    print(plug.get_info())
    print(plug.get_name())
    print(plug.get_realtime())
    print(plug.get_power())
    print(plug.get_stats())

    plug = HS110("192.168.0.213")
    print(plug.get_info())
    print(plug.get_name())
    print(plug.get_realtime())
    print(plug.get_power())
    print(plug.get_stats())


run()
