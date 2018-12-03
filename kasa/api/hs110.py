from api.hs import HS


class HS110(HS):

    def get_realtime(self):
        return self._send_command('emeter', 'get_realtime')

    def get_power(self) -> float:
        # Returns current power in W
        return self.get_realtime()['power_mw'] / 1000.0

    def get_self_power(self) -> float:
        info = self.get_realtime()['power_mw']
        return info['voltage_mv'] * info['current_ma'] / 1000000.0 - info['power_mw']

    # Get Daily Statistic for given Month
    # {"emeter":{"get_daystat":{"month":1,"year":2016}}}
    def get_stats(self):
        return self._send_command('emeter', 'get_daystat', {'month': 11, 'year': 2018})
