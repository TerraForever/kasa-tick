from api.hs110 import HS110


def run():
    plug = HS110("192.168.0.214")
    print(plug.get_info())
    print(plug.get_name())
    print(plug.get_power())
    print(plug.get_stats())


run()
