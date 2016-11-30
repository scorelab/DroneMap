#Created by Imal thiunuwan using Intellij Idea

class Callback_Methods(object):

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
	selfvehicle.add_attribute_listener('attitude', attitude_callback)

	print " Wait 2s so callback invoked before observer removed"
	time.sleep(2)

	print " Remove Vehicle.attitude observer" 

	# Remove observer added with `add_attribute_listener()` specifying the attribute and callback function
	self.vehicle.remove_attribute_listener('attitude', attitude_callback)


	# Add mode attribute callback using decorator (callbacks added this way cannot be removed).
	print "\nAdd `mode` attribute callback/observer using decorator" 
	@self.vehicle.on_attribute('mode')   

	def decorated_mode_callback(self, attr_name, value):
    	# `attr_name` is the observed attribute (used if callback is used for multiple attributes)
    	# `attr_name` - the observed attribute (used if callback is used for multiple attributes)
    	# `value` is the updated attribute value.
    	print " CALLBACK: Mode changed to", value

	print " Set mode=STABILIZE (currently: %s) and wait for callback" % vehicle.mode.name 
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
