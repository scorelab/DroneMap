from dronekit import connect, VehicleMode
import time
import argparse
#import config
#from dbconnection import dbConnection
#import callback_methods

class Vehicle():

    def __init__(self,version,gimbal):
        self.version = version
        self.gimbal = gimbal

    def main(self):

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


    def connect_vehicle(self, connection_string=None):
        # Connect to the Vehicle.
        # Set `wait_ready=True` to ensure default attributes are populated before `connect()` returns.

        print ("\nConnecting to vehicle on: %s" % connection_string)
        self.vehicle = connect(connection_string, wait_ready=True)

        self.vehicle.wait_ready('autopilot_version')


    # Get Vehicle Home location - will be `None` until first set by autopilot

    def get_Vehicle_Home_Location(self):
        while not self.vehicle.home_location:
            cmds = self.vehicle.commands
            cmds.download()
            cmds.wait_ready()
            if not self.vehicle.home_location:
                print (" Waiting for home location ...")

            # We have a home location, so print it!
            print ("\n Home location: %s" % self.vehicle.home_location)


    def set_Vehicle_Home_Location(self):
        print ("\nSet new home location")
        # Home location must be within 50km of EKF home location (or setting will fail silently)
        # In this case, just set value to current location with an easily recognisable altitude (222)
        my_location_alt = self.vehicle.location.global_frame
        my_location_alt.alt = 222.0
        self.vehicle.home_location = my_location_alt
        print (" New Home Location (from attribute - altitude should be 222): %s" % self.vehicle.home_location)

        #Confirm current value on vehicle by re-downloading commands

        cmds = self.vehicle.commands
        cmds.download()
        cmds.wait_ready()
        print (" New Home Location (from vehicle - altitude should be 222): %s" % self.vehicle.home_location)

        print ("\nSet Vehicle.mode = GUIDED (currently: %s)" % self.vehicle.mode.name)
        self.vehicle.mode = VehicleMode("GUIDED")
        while not self.vehicle.mode.name=='GUIDED':  #Wait until mode has changed
                print (" Waiting for mode change ...")
                time.sleep(1)


    def check_Armability(self):

        while not self.vehicle.is_armable:
            print (" Waiting for vehicle to initialise...")
            time.sleep(1)
        # If required, you can provide additional information about initialisation
        # using `vehicle.gps_0.fix_type` and `vehicle.mode.name`.
   
        print ("\nSet Vehicle.armed=True (currently: %s)" % self.vehicle.armed)
        self.vehicle.armed = True
        while not self.vehicle.armed:
            print (" Waiting for arming...")
            time.sleep(1)
        print (" Vehicle is armed: %s" % self.vehicle.armed)


        # Add and remove and attribute callbacks

        #Define callback for `vehicle.attitude` observer

        last_attitude_cache = None

        # Get/Set Vehicle Parameters
    def set_parameters(self):
        print ("\nRead and write parameters")
        print (" Read vehicle param 'THR_MIN': %s" % self.vehicle.parameters['THR_MIN'])

        print (" Write vehicle param 'THR_MIN' : 10")
        self.vehicle.parameters['THR_MIN']=10
        print (" Read new value of param 'THR_MIN': %s" % self.vehicle.parameters['THR_MIN'])


        print ("\nPrint all parameters (iterate `vehicle.parameters`)")
        for key, value in self.vehicle.parameters.iteritems():
                print (" Key:%s Value:%s" % (key,value))


        print ("\nCreate parameter observer using decorator")
        # Parameter string is case-insensitive
        # Value is cached (listeners are only updated on change)
        # Observer added using decorator can't be removed.

        @vehicle.parameters.on_attribute('THR_MIN')

    # Reset variables to sensible values
        def reset_vehicle_attributes(self):
            print ("\nReset vehicle attributes/parameters and exit")
            self.vehicle.mode = VehicleMode("STABILIZE")
            self.vehicle.armed = False
            self.vehicle.parameters['THR_MIN']=130
            self.vehicle.parameters['THR_MID']=500


    #Close vehicle object before exiting script
        def close_vehicle(self):
            print ("\nClose vehicle object")
            self.vehicle.close()

    # Shut down simulator if it was started.
    def shutdown_simulator(self):
        if sitl is not None:
            sitl.stop()

    #completion
    print("Completed")




