#!/bin/bash
export PX4_HOME_LAT=19.133701 # Latitude of the home position
export PX4_HOME_LON=72.912971 # Longitude of the home position
export PX4_HOME_ALT=0         # Altitude of the home position
make px4_sitl gazebo    # To launch fixed wing plane in gazebo
