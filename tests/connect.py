from pymavlink import mavutil
import argparse
import time
parser = argparse.ArgumentParser()
parser.add_argument('--connect', default='127.0.0.1:14550')
args = parser.parse_args()

print ('Connecting to vehicle on: %s' % args.connect)
the_connection = mavutil.mavlink_connection(args.connect)

the_connection.wait_heartbeat()
print("Heartbeat from system (system %u component %u)" %
      (the_connection.target_system, the_connection.target_component))

while 1:
      # msg = the_connection.recv_match(type='ATTITUDE', blocking=True)
      # pos = the_connection.recv_match(type='GLOBAL_POSITION_INT', blocking=True)

      # distance to next waypoint
      
      the_connection.mav.command_long_encode(
		0, 0,
		mavutil.mavlink.MAV_CMD_REQUEST_MESSAGE,
		0,
		30,
		0,
		0,
		0,
		0,0, 0)
      #msg = the_connection.recv_match(type='MAV',blocking=True)
      data = the_connection.messages.keys()
      system = the_connection.recv_match(type='ATTITUDE', blocking=True)
      # print(data)
      
      the_connection.mav.send(mavutil.mavlink.MAVLink_set_position_target_local_ned_message(10, the_connection.target_system,
                        the_connection.target_component, mavutil.mavlink.MAV_FRAME_BODY_OFFSET_NED , int(0b100111100111), 0, 0, 0, 0.2, 0, 0, 0, 0, 0, 0.8, 0))
      
      time.sleep(1)
      pos = the_connection.recv_match(type='GPS_RAW_INT', blocking=True)
      # print(system.yaw)
      print(pos)
      # data = the_connection.messages['HOME']
      time.sleep(2)