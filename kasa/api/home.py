import json
from json import JSONEncoder
from typing import List, Dict

import nmap

from api.hs100 import HS100
from api.hs import HS
from api.hs110 import HS110
from api.kasa import Kasa

MODELS = {'HS': HS, 'HS100': HS100, 'HS110': HS110}


class Home:
    def __init__(self, domain='192.168.0.0/24', port=9999, progs=('/mnt/c/Program Files (x86)/Nmap/nmap.exe', 'nmap')):
        self.domain = domain
        self.port = port
        self.progs = progs
        self.hs = {}

    def reset(self):
        self.hs = {}

    def get_all_items(self) -> List[Kasa]:
        return [item for items in self.hs.values() for item in items]

    def get_items(self, model) -> List[Kasa]:
        if model in self.hs:
            return self.hs[model]
        return []

    def get_dict(self) -> Dict[str, List[Kasa]]:
        return self.hs

    def load(self, cache='home.json'):
        # Load file
        with open(cache, 'rb') as fp:
            raw = fp.read()
        data = str(raw, 'utf-8')

        # Parse JSON
        map = json.loads(data)

        # Iterate of the data
        for model, items in map.items():
            if model in MODELS:
                clazz : Kasa.__class__ = MODELS[model]
                self.hs[model] = [clazz(host) for name, host in items]

    def save(self, cache='home.json'):
        # JSON encode
        encoder = Home.CustomEncoder()
        data = encoder.encode(self.hs)

        # Write to file
        with open(cache, 'wb') as fp:
            fp.write(bytes(data, 'utf-8'))

    def discover(self):
        # Scan domain
        nm = nmap.PortScanner(nmap_search_path=self.progs)
        print('Scanning {}:{}'.format(self.domain, self.port))
        nm.scan(hosts=self.domain, ports=str(self.port), sudo=False, arguments='-sT' )

        # Iterate over results
        for host in nm.all_hosts():
            scan : nmap.PortScannerHostDict = nm[host]
            if scan.has_tcp(self.port):
                # Generic HS on Kasa port
                print('Discovered {}'.format(host))
                hs = HS(host)
                try:
                    # Attempt to communicate with the plug
                    print('Getting info from {}'.format(host))
                    info = hs.get_info()
                    print('Successfully discovered: {} - {}'.format(info['alias'], host))

                    # Detect model
                    model = info['model']
                    if 'HS100' in model:
                        self.hs.setdefault('HS100', []).append(HS100(host))
                    elif 'HS110' in model:
                        self.hs.setdefault('HS110', []).append(HS110(host))
                    else:
                        self.hs.setdefault('HS', []).append(hs)

                except (ConnectionError, BlockingIOError):
                    continue

    class CustomEncoder(JSONEncoder):
        def default(self, o):
            if isinstance(o, HS):
                return o.get_name(), o.get_host()
            return JSONEncoder.default(self, o)