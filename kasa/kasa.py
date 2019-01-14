#!/usr/bin/env python3
from datetime import datetime

from api.home import Home
from api.hs100 import HS100
from api.hs110 import HS110


def run(domain='192.168.0.0/24'):
    # Create home and load devices
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

    # Loop over HS100 plugs
    plug : HS100
    for plug in home.get_items('HS100'):
        print(plug.get_info())
        print(plug.get_name())

    # Loop over HS100 plugs
    plug : HS110
    for plug in home.get_items('HS110'):
        print(plug.get_info())
        print(plug.get_name())
        print(plug.get_realtime())
        print(plug.get_power())
        print(plug.get_stats())


run()
