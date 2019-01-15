#!/usr/bin/env python3
from datetime import datetime
from typing import List

from telegraf import HttpClient  # https://github.com/paksu/pytelegraf

from api.home import Home
from api.hs110 import HS110


class KasaTick:
    def __init__(self, home='home', domain='192.168.0.0/24'):
        self.home = home
        self.home_file = 'dat/{}.json'.format(home)
        self.domain = domain
        self._home = None
        self._tick = None

    def run(self):
        # Connect to home and tick
        self._connect_home()
        self._connect_tick()

        # Send data
        self._do_tick_tack()

    def _connect_home(self):
        # Create home and load devices
        self._home = Home(domain=self.domain)
        try:
            print('Loading home: {}'.format(datetime.now()))
            self._home.load(cache=self.home_file)
        except FileNotFoundError:
            print('Saved home not found, discovering devices on {}'.format(self.domain))
            self._home.discover()
            print('Discovered {} devices'.format(len(self._home.get_all_items())))
            self._home.save(cache=self.home_file)
            print('Saved home info')

    def _connect_tick(self):
        self._tick = HttpClient(host='localhost', port=8186)

    def _do_tick_tack(self):
        # Get HS110 plugs
        plugs = self._home.get_items('HS110')
        home_power = 0

        # Iterate over plugs
        for plug in plugs:
            # Get plug info
            name = plug.get_name()
            power = plug.get_power()
            home_power += power
            sanitized = name.replace(' ', '_').lower()
            # https://github.com/paksu/pytelegraf
            print(sanitized, power)

            # Send to TICK
            self._tick.metric(sanitized, {'power': power})

        # Send summed power to TICK
        print(self.home, home_power)
        self._tick.metric(self.home, home_power)


kasa = KasaTick()
kasa.run()