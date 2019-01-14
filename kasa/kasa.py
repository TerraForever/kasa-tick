#!/usr/bin/env python3
from datetime import datetime

from api.home import Home
from api.hs110 import HS110


def run():
    # Create home and load devices
    domain = '192.168.0.0/24'
    home = Home(domain=domain)
    try:
        print('Loading home: {}'.format(datetime.now()))
        home.load()
    except FileNotFoundError:
        print('Saved home not found, discovering devices on {}'.format(domain))
        home.discover()
        print('Discovered {} devices'.format(len(home.get_all_items())))
        home.save()
        print('Saved home info')

    # List
    print('Devices')
    print(home.get_dict())

    print(home.get_items('HS100'))
    print(home.get_all_items())

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
