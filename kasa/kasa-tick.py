#!/usr/bin/env python3
import argparse

from telegraf import HttpClient  # https://github.com/paksu/pytelegraf

from api.home import Home


class KasaTick:
    def __init__(self, domain, home, reset=False):
        self.home_name = home
        self.home_file = 'dat/{}.json'.format(home)
        self.domain = domain
        self.reset = reset
        self.home = None
        self.tick = None

    def run(self):
        # Connect to home and tick
        self._connect_home()
        self._connect_tick()

        # Send data
        self._do_tick_tack()

    def _connect_home(self):
        # Create home
        self.home = Home(domain=self.domain)

        # Load saved home
        if not self.reset:
            try:
                print('Loading home: {}'.format(self.home_file))
                self.home.load(cache=self.home_file)
            except FileNotFoundError:
                pass

        # Discover home
        if not self.home.get_all_items():
            print('Saved home not found, discovering devices on {}'.format(self.domain))
            self.home.discover()
            print('Discovered {} devices'.format(len(self.home.get_all_items())))
            self.home.save(cache=self.home_file)
            print('Saved home info: {}'.format(self.home_file))

    def _connect_tick(self):
        self.tick = HttpClient(host='localhost', port=8186)

    def _do_tick_tack(self):
        # Get HS110 plugs
        plugs = self.home.get_items('HS110')
        home_power = 0

        # Iterate over plugs
        print('Querying {} HS110 plugs'.format(len(plugs)))
        for plug in plugs:
            try:
                # Get plug info
                name = plug.get_name()
                power = plug.get_power()
                home_power += power
                sanitized = name.replace(' ', '_').lower()
                print('{}: {} W'.format(name, power))

                # Send to TICK
                self.tick.metric(sanitized, {'power': power})

            except Exception as ex:
                # Catch such that we can continue handling the other plugs
                print('Warning: exception while handling plug {}: {}'.format(plug.get_host(), ex))

        # Send summed power to TICK
        print('{}: {} W'.format(self.home_name, home_power))
        self.tick.metric(self.home_name, home_power)


# Args
parser = argparse.ArgumentParser(description='''Queries locally discovered HS110 smart plugs for the current power usage. Pushes the power and summed power over all plugs to the TICK stack platform.
The name of the metric in the TICK stack is the name of smart plug (in lower case and spaces replaced by underscores: e.g. Internet Power -> internet_power).''')
parser.add_argument('--domain', help='Domain to discover', default='192.168.0.1/24')
parser.add_argument('--home', help='Name of your home', default='home')
parser.add_argument('--reset', help='Rediscover devices', action='store_true')
args = parser.parse_args()

kasa = KasaTick(args.domain, args.home, reset=args.reset)
kasa.run()