from api.kasa import Kasa


class HS(Kasa):

    def get_name(self):
        return self.get_info()['alias']

    def get_info(self):
        return self._send_command('system', 'get_sysinfo')
