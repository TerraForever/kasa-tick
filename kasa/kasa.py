#!/usr/bin/env python3
import argparse
from datetime import datetime

from api.home import Home


def run():
    # Args
    parser = argparse.ArgumentParser(description='''Demonstrates a basic API to interact with TP-Link smart plugs.
    These plugs can be automatically discovered on the local network and persisted across invocations of the script.''')
    parser.add_argument('--domain', help='Domain to discover', default='192.168.0.1/24')
    parser.add_argument('--home', help='Location of the save home file', default='dat/home.json')
    parser.add_argument('--reset', help='Rediscover devices', action='store_true')
    args = parser.parse_args()

    # Create home
    home = Home(domain=args.domain)

    # Load saved home
    if not args.reset:
        try:
            print('Loading home: {}'.format(args.home))
            home.load(cache=args.home)
        except FileNotFoundError:
            pass

    # Discover home
    if not home.get_all_items():
        print('Saved home not found, discovering devices on {}'.format(args.domain))
        home.discover()
        print('Discovered {} devices'.format(len(home.get_all_items())))
        home.save(cache=args.home)
        print('Saved home info: {}'.format(args.home))

    # List
    print('Devices available: {}'.format(len(home.get_all_items())))
    print(home.get_dict())

    # Loop over HS100 plugs
    for plug in home.get_items('HS100'):
        print('***')
        print(plug.get_name())
        print(plug.get_info())
        print('***')

    # Loop over HS100 plugs
    for plug in home.get_items('HS110'):
        print('***')
        print(plug.get_name())
        print(plug.get_info())
        print(plug.get_realtime())
        print(plug.get_power())
        print(plug.get_stats())
        print('***')


run()
