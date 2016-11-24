import ConfigParser as cp
import json

config = cp.RawConfigParser()
config.read('./config/config.cfg')

drone_id = json.loads(config.get("drone","d_id"))
simulation = config.getboolean("drone", "simulation")
grounded = config.getboolean("drone", "grounded")
connection_list = json.loads(config.get("drone", "connection_list"))




