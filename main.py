import ConfigParser as cp
import json
from dronekit import connect, VehicleMode


def config_loader():
    configs = cp.RawConfigParser()
    configs.read('./config/config.cfg')
    return configs
    # print config.get('drone', 'drone_id')


def connect_vehicle(configs):
    # Connect to the Vehicle.
    # Set `wait_ready=True` to ensure default attributes are populated before `connect()` returns.

    connection_string = configs.get('drone', 'connection')
    simulation = configs.get('drone', 'simulation')

    sitl = None

    # Start SITL if no connection string specified
    if simulation == 'TRUE':
        import dronekit_sitl
        sitl = dronekit_sitl.start_default()
        connection_string = sitl.connection_string()

    print ("\nConnecting to vehicle on: %s" % connection_string)
    return connect(connection_string, wait_ready=True)


def print_vehicle_state(vehicle, configs):
    # Get all vehicle attributes (state)
    print "\nGet all vehicle attribute values:"
    print " Autopilot Firmware version: %s" % vehicle.version
    print "   Major version number: %s" % vehicle.version.major
    print "   Minor version number: %s" % vehicle.version.minor
    print "   Patch version number: %s" % vehicle.version.patch
    print "   Release type: %s" % vehicle.version.release_type()
    print "   Release version: %s" % vehicle.version.release_version()
    print "   Stable release?: %s" % vehicle.version.is_stable()
    print " Autopilot capabilities"
    print "   Supports MISSION_FLOAT message type: %s" % vehicle.capabilities.mission_float
    print "   Supports PARAM_FLOAT message type: %s" % vehicle.capabilities.param_float
    print "   Supports MISSION_INT message type: %s" % vehicle.capabilities.mission_int
    print "   Supports COMMAND_INT message type: %s" % vehicle.capabilities.command_int
    print "   Supports PARAM_UNION message type: %s" % vehicle.capabilities.param_union
    print "   Supports ftp for file transfers: %s" % vehicle.capabilities.ftp
    print "   Supports commanding attitude offboard: %s" % vehicle.capabilities.set_attitude_target
    print "   Supports commanding position and velocity targets in local NED frame: %s" % vehicle.capabilities.set_attitude_target_local_ned
    print "   Supports set position + velocity targets in global scaled integers: %s" % vehicle.capabilities.set_altitude_target_global_int
    print "   Supports terrain protocol / data handling: %s" % vehicle.capabilities.terrain
    print "   Supports direct actuator control: %s" % vehicle.capabilities.set_actuator_target
    print "   Supports the flight termination command: %s" % vehicle.capabilities.flight_termination
    print "   Supports mission_float message type: %s" % vehicle.capabilities.mission_float
    print "   Supports onboard compass calibration: %s" % vehicle.capabilities.compass_calibration
    print " Global Location: %s" % vehicle.location.global_frame
    print " Global Location (relative altitude): %s" % vehicle.location.global_relative_frame
    print " Local Location: %s" % vehicle.location.local_frame
    print " Attitude: %s" % vehicle.attitude
    print " Velocity: %s" % vehicle.velocity
    print " GPS: %s" % vehicle.gps_0
    print " Gimbal status: %s" % vehicle.gimbal
    print " Battery: %s" % vehicle.battery
    print " EKF OK?: %s" % vehicle.ekf_ok
    print " Last Heartbeat: %s" % vehicle.last_heartbeat
    print " Rangefinder: %s" % vehicle.rangefinder
    print " Rangefinder distance: %s" % vehicle.rangefinder.distance
    print " Rangefinder voltage: %s" % vehicle.rangefinder.voltage
    print " Heading: %s" % vehicle.heading
    print " Is Armable?: %s" % vehicle.is_armable
    print " System status: %s" % vehicle.system_status.state
    print " Groundspeed: %s" % vehicle.groundspeed  # settable
    print " Airspeed: %s" % vehicle.airspeed  # settable
    print " Mode: %s" % vehicle.mode.name  # settable
    print " Armed: %s" % vehicle.armed  # settable

def vehicle_state_json_builder(vehicle):
    data = {}
    data['vehicleId'] = config.get('drone', 'drone_id')
    data['vehicle_version'] = vehicle.version
    data['vehicle_version_major'] = vehicle.version.major
    data['vehicle_version_minor'] = vehicle.version.minor
    data['vehicle_version_patch'] = vehicle.version.patch
    data['vehicle_version_release_type'] = vehicle.version.release_type()
    data['vehicle_version_release_version'] = vehicle.version.release_version()
    data['vehicle_version_release_is_stable'] = vehicle.version.is_stable()
    data['vehicle_capabilities_mission_float'] = vehicle.capabilities.mission_float
    data['vehicle_capabilities_param_float'] = vehicle.capabilities.param_float
    data['vehicle_capabilities_mission_int'] = vehicle.capabilities.mission_int
    data['vehicle_capabilities_command_int'] = vehicle.capabilities.command_int
    data['vehicle_capabilities_param_union'] = vehicle.capabilities.param_union
    data['vehicle_capabilities_ftp'] = vehicle.capabilities.ftp
    data['vehicle_capabilities_set_attitude_target'] = vehicle.capabilities.set_attitude_target
    data['vehicle_capabilities_set_attitude_target_local_ned'] = vehicle.capabilities.set_attitude_target
    data['vehicle_capabilities_set_attitude_target_global_int'] = vehicle.capabilities.set_altitude_target_global_int
    data['vehicle_capabilities_terrain'] = vehicle.capabilities.terrain
    data['vehicle_capabilities_set_actuator_target'] = vehicle.capabilities.set_actuator_target
    data['vehicle_capabilities_flight_termination'] = vehicle.capabilities.flight_termination
    data['vehicle_capabilities_mission_float'] = vehicle.capabilities.mission_float
    data['vehicle_capabilities_compass_calibration'] = vehicle.capabilities.compass_calibration
    data['vehicle_global_location'] = vehicle.location.global_frame
    data['vehicle_global_location_relative_altitude'] = vehicle.location.global_relative_frame
    data['vehicle_local_location'] = vehicle.location.local_frame
    data['vehicle_attitude'] = vehicle.attitude
    data['vehicle_velocity'] = vehicle.velocity
    data['vehicle_gps'] = vehicle.gps_0
    data['vehicle_gimbal_status'] = vehicle.gimbal
    data['vehicle_battery'] = vehicle.battery
    data['vehicle_ekf_ok'] = vehicle.ekf_ok
    data['vehicle_last_heartbeat'] = vehicle.last_heartbeat
    data['vehicle_rangefinder'] = vehicle.rangefinder
    data['vehicle_rangefinder_distance'] = vehicle.rangefinder.distance
    data['vehicle_rangefinder_voltage'] = vehicle.rangefinder.voltage
    data['vehicle_heading'] = vehicle.heading
    data['vehicle_is_armable'] = vehicle.is_armable
    data['vehicle_system_status_state'] = vehicle.system_status.state
    data['vehicle_groundspeed'] = vehicle.groundspeed
    data['vehicle_airspeed'] = vehicle.airspeed
    data['vehicle_mode'] = vehicle.mode.name
    data['vehicle_armed'] = vehicle.armed

    return json.dumps(data)


if __name__ == "__main__":
    # Load configurations
    configs = config_loader()

    # Connect to vehicle
    vehicle = connect_vehicle(configs)

    # Print vehicle status
    count = 0
    while (count < 9):
        print_vehicle_state(vehicle, configs)
        json_data = vehicle_state_json_builder(vehicle, configs)
        import time
        time.sleep(5)

    # Close the connection
    vehicle.close()