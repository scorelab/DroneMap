from dronekit import connect, VehicleMode
import time
import argparse
from dbconnection import dbConnection

class Vehicle(object):


	def __init__(self,version,gimbal):
		self.version = version
		self.gimbal = gimbal

	def __name__ == '__main__': 	

		parser = argparse.ArgumentParser(description='Print out vehicle state information. Connects to SITL on local PC by default.')
		parser.add_argument('--connect', 
                   help="vehicle connection target string. If not specified, SITL automatically started and used.")
		args = parser.parse_args()

		connection_string = args.connect
		sitl = None

		#Start SITL if no connection string specified
		if not connection_string:
    		import dronekit_sitl
    		sitl = dronekit_sitl.start_default()
    		connection_string = sitl.connection_string()


	def connect_vehicle(self):
		# Connect to the Vehicle. 
		# Set `wait_ready=True` to ensure default attributes are populated before `connect()` returns.

		print "\nConnecting to vehicle on: %s" % connection_string
		self.vehicle = connect(connection_string, wait_ready=True)

		self.vehicle.wait_ready('autopilot_version')

	
	# Get Vehicle Home location - will be `None` until first set by autopilot
	
	def get_Vehicle_Home_Location(self):
		while not self.vehicle.home_location:
    		cmds = self.vehicle.commands
    		cmds.download()
    		cmds.wait_ready()
    		if not self.vehicle.home_location:
        		print " Waiting for home location ..."

        # We have a home location, so print it! 
        print "\n Home location: %s" % self.vehicle.home_location		
		

	def set_Vehicle_Home_Location(self):
		print "\nSet new home location"
		# Home location must be within 50km of EKF home location (or setting will fail silently)
		# In this case, just set value to current location with an easily recognisable altitude (222)
		my_location_alt = self.vehicle.location.global_frame
		my_location_alt.alt = 222.0
		self.vehicle.home_location = my_location_alt
		print " New Home Location (from attribute - altitude should be 222): %s" % self.vehicle.home_location

		#Confirm current value on vehicle by re-downloading commands

		cmds = self.vehicle.commands
		cmds.download()
		cmds.wait_ready()
		print " New Home Location (from vehicle - altitude should be 222): %s" % self.vehicle.home_location

		print "\nSet Vehicle.mode = GUIDED (currently: %s)" % self.vehicle.mode.name 
		selfvehicle.mode = VehicleMode("GUIDED")
		while not self.vehicle.mode.name=='GUIDED':  #Wait until mode has changed
    	print " Waiting for mode change ..."
    	time.sleep(1)


    def check_Armability(self):

    	while not self.vehicle.is_armable:
    		print " Waiting for vehicle to initialise..."
    		time.sleep(1)
    # If required, you can provide additional information about initialisation
    # using `vehicle.gps_0.fix_type` and `vehicle.mode.name`.
    
		print "\nSet Vehicle.armed=True (currently: %s)" % self.vehicle.armed 
		self.vehicle.armed = True
		while not self.vehicle.armed:
    		print " Waiting for arming..."
    		time.sleep(1)
		print " Vehicle is armed: %s" % self.vehicle.armed 


		# Add and remove and attribute callbacks

		#Define callback for `vehicle.attitude` observer

		last_attitude_cache = None

	def attitude_callback(self, attr_name, value):
    	# `attr_name` - the observed attribute (used if callback is used for multiple attributes)
    	# `self` - the associated vehicle object (used if a callback is different for multiple vehicles)
    	# `value` is the updated attribute value.
    	global last_attitude_cache
    	# Only publish when value changes
    	if value!=last_attitude_cache:
        	print " CALLBACK: Attitude changed to", value
        	last_attitude_cache=value

	print "\nAdd `attitude` attribute callback/observer on `vehicle`"     
	self.vehicle.add_attribute_listener('attitude', attitude_callback)

	print " Wait 2s so callback invoked before observer removed"
	time.sleep(2)

	print " Remove Vehicle.attitude observer" 

	# Remove observer added with `add_attribute_listener()` specifying the attribute and callback function
	self.vehicle.remove_attribute_listener('attitude', attitude_callback)


	# Add mode attribute callback using decorator (callbacks added this way cannot be removed).
	print "\nAdd `mode` attribute callback/observer using decorator" 
	@vehicle.on_attribute('mode')   

	def decorated_mode_callback(self, attr_name, value):
    # `attr_name` is the observed attribute (used if callback is used for multiple attributes)
    # `attr_name` - the observed attribute (used if callback is used for multiple attributes)
    # `value` is the updated attribute value.
    	print " CALLBACK: Mode changed to", value

	print " Set mode=STABILIZE (currently: %s) and wait for callback" % self.vehicle.mode.name 
	self.vehicle.mode = VehicleMode("STABILIZE")

	print " Wait 2s so callback invoked before moving to next example"
	time.sleep(2)

	print "\n Attempt to remove observer added with `on_attribute` decorator (should fail)" 
	try:
    	self.vehicle.remove_attribute_listener('mode', decorated_mode_callback)
	except:
    	print " Exception: Cannot remove observer added using decorator"



	# Demonstrate getting callback on any attribute change
	def wildcard_callback(self, attr_name, value):
    	print " CALLBACK: (%s): %s" % (attr_name,value)

	print "\nAdd attribute callback detecting ANY attribute change"     
	self.vehicle.add_attribute_listener('*', wildcard_callback)


	print " Wait 1s so callback invoked before observer removed"
	time.sleep(1)

	print " Remove Vehicle attribute observer"    
# Remove observer added with `add_attribute_listener()`
	self.vehicle.remove_attribute_listener('*', wildcard_callback)
    


# Get/Set Vehicle Parameters
	def set_parameters(self):
		print "\nRead and write parameters"
		print " Read vehicle param 'THR_MIN': %s" % self.vehicle.parameters['THR_MIN']

		print " Write vehicle param 'THR_MIN' : 10"
		self.vehicle.parameters['THR_MIN']=10
		print " Read new value of param 'THR_MIN': %s" % self.vehicle.parameters['THR_MIN']


		print "\nPrint all parameters (iterate `vehicle.parameters`):"
		for key, value in self.vehicle.parameters.iteritems():
	    	print " Key:%s Value:%s" % (key,value)
	    

		print "\nCreate parameter observer using decorator"
	# Parameter string is case-insensitive
	# Value is cached (listeners are only updated on change)
	# Observer added using decorator can't be removed.
	 
		@vehicle.parameters.on_attribute('THR_MIN')


	def decorated_thr_min_callback(self, attr_name, value):
	    print " PARAMETER CALLBACK: %s changed to: %s" % (attr_name, value)


	print "Write vehicle param 'THR_MIN' : 20 (and wait for callback)"
	self.vehicle.parameters['THR_MIN']=20
	for x in range(1,5):
	    #Callbacks may not be updated for a few seconds
	    if self.vehicle.parameters['THR_MIN']==20:
	        break
	    time.sleep(1)


	#Callback function for "any" parameter
	print "\nCreate (removable) observer for any parameter using wildcard string"


	def any_parameter_callback(self, attr_name, value):
	    print " ANY PARAMETER CALLBACK: %s changed to: %s" % (attr_name, value)

	#Add observer for the vehicle's any/all parameters parameter (defined using wildcard string ``'*'``)
	self.vehicle.parameters.add_attribute_listener('*', any_parameter_callback)     
	print " Change THR_MID and THR_MIN parameters (and wait for callback)"    
	self.vehicle.parameters['THR_MID']=400  
	self.vehicle.parameters['THR_MIN']=30


	## Reset variables to sensible values.
	def reset_vehicle_attributes(self):
		print "\nReset vehicle attributes/parameters and exit"
		self.vehicle.mode = VehicleMode("STABILIZE")
		self.vehicle.armed = False
		self.vehicle.parameters['THR_MIN']=130
		self.vehicle.parameters['THR_MID']=500


	#Close vehicle object before exiting script
	def close_vehicle(self):
		print "\nClose vehicle object"
		self.vehicle.close()

	# Shut down simulator if it was started.
	def shutdown_simulator(self):
		if sitl is not None:
	    	sitl.stop()

	print("Completed")




