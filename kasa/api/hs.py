from api.kasa import Kasa


class HS(Kasa):

    def __init__(self , *args, **kwargs):
        Kasa.__init__(self, *args, **kwargs)
        self.info : str = None

    def __str__(self):
        return self.get_name()

    def __repr__(self):
        return str(self)

    def get_name(self):
        return self.get_info(cache=True)['alias']

    def get_info(self, cache=False):
        if cache and self.info:
            return self.info
        self.info = self._send_command('system', 'get_sysinfo')
        return self.info
