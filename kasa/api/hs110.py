from api.hs import HS


class HS110(HS):

    def get_power(self):
        return self._send_command('emeter', 'get_realtime')

    # Get Daily Statistic for given Month
    # {"emeter":{"get_daystat":{"month":1,"year":2016}}}
    def get_stats(self):
        return self._send_command('emeter', 'get_daystat', {'month': 11, 'year': 2018, 'day': 25})
