#Created by Imal thiunuwan using Intellij Idea

import ConfigParser as cp
import json

config = cp.RawConfigParser()
config.read('./config/config.cfg')

drone_id = json.loads(config.get("drone","d_id"))
print "Drone ID :",drone_id
simulation = config.getboolean("drone", "simulation")
print "Simulation status :",simulation
grounded = config.getboolean("drone", "grounded")
print "Grounded :",grounded
connection_list = json.loads(config.get("drone", "connection_list"))
print "Connection list :",connection_list



