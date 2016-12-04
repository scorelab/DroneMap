import ConfigParser as cp
import json
import time
from dronekit import connect, VehicleMode
import sys
import pymongo


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
    # print "   Supports MISSION_FLOAT message type: %s" % vehicle.capabilities.mission_float
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


def vehicle_state_json_builder(vehicle, configs):
    data = {
        'drone_id': configs.get('drone', 'drone_id'),
        'timestamp': vehicle._master.timestamp,
        'air_speed': vehicle.airspeed,
        'is_armable': vehicle.is_armable,
        'autopilot_type': vehicle._autopilot_type,
        'flightmode': vehicle._flightmode,
        'groundspeed': vehicle._groundspeed,
        'heading': vehicle.heading,
        'home_location': vehicle._home_location,
        'last_heartbeat': vehicle._last_heartbeat,
        'location': {
            'alt': vehicle._location._alt,
            'down': vehicle._location._down,
            'east': vehicle._location._east,
            'north': vehicle._location._north,
            'relative_alt': vehicle._location._relative_alt,
            'lat': vehicle._location._lat,
            'log': vehicle._location._lon
        },
        'location_global': {
            'alt': vehicle._location.global_frame.alt,
            'lat': vehicle._location.global_frame.lat,
            'log': vehicle._location.global_frame.lon
        },
        'location_global_relative': {
            'alt': vehicle._location.global_relative_frame.alt,
            'lat': vehicle._location.global_relative_frame.lat,
            'log': vehicle._location.global_relative_frame.lon
        },
        'location_local': {
            'down': vehicle._location.local_frame.down,
            'east': vehicle._location.local_frame.east,
            'north': vehicle._location.local_frame.north
        },
        'attitude': {
            'pitch': vehicle._pitch,
            'pitch_speed': vehicle._pitchspeed,
            'roll': vehicle._roll,
            'roll_speed': vehicle._rollspeed,
            'yaw': vehicle._yaw,
            'yaw_speed': vehicle._yawspeed
        },
        'battery': {
            'battery_current': vehicle.battery.current,
            'battery_level': vehicle.battery.level,
            'battery_voltage': vehicle.battery.voltage
        },
        'gps': {
            'eph': vehicle.gps_0.eph,
            'epv': vehicle.gps_0.epv,
            'fix_type': vehicle.gps_0.fix_type,
            'satellites_visible': vehicle.gps_0.satellites_visible
        },
        'groundspeed': vehicle._groundspeed,
        'last_heartbeat': vehicle.last_heartbeat,
        'velocity': vehicle.velocity,
    }

    print data
    return data


def connect_to_db(uri):
    client = pymongo.MongoClient(uri)
    db = client.get_default_database()
    return db


def insert(db, documentName, dataArray):
    document = db[documentName]
    val = document.insert(dataArray)
    if (val):
        print("Successed!")
    else:
        print("Something went wrong.")


def read(db):
    try:
        # data_column = db.dronemap_collections.find()
        data_column = db.dronemap_collections.find({}).sort([
            ("timestamp", pymongo.DESCENDING)
        ]).limit(1)
        for d in data_column:
            return d
    except Exception, e:
        print str(e)


if __name__ == "__main__":
    # Load configurations
    configs = config_loader()

    # Connect to vehicle
    # vehicle = connect_vehicle(configs)

    # Print vehicle status
    # count = 0
    # while(count < 2):
    #
    #     # print_vehicle_state(vehicle, configs)
    #
    #     # Build the vehicle state json
    #     json_data = vehicle_state_json_builder(vehicle, configs)
    #
    #     # Connect to remote DB
    #     db = connect_to_db(configs.get('db', 'db_connection'))
    #
    #     #Insert data to remote DB
    #     insert(db, 'dronemap_collections', json_data)
    #
    #     # count = count +1
    #
    #     time.sleep(float(configs.get('drone', 'data_collection_frequency')))

    # Read data from remote DB
    db = connect_to_db(configs.get('db', 'db_connection'))
    data = read(db)
    print(data)

    # Close the connection
    # vehicle.close()
