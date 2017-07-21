#!/bin/bash

#CLONE NECESSARY REPOs
cd ~/sara_ws/src/
git clone https://github.com/team-vigir/flexbe_behavior_engine.git
git clone https://github.com/FlexBE/generic_flexbe_states.git

#INSTALL DEPENDENCIES
sudo apt install ros-kinetic-rosbridge-suite -y
roslaunch flexbe_onboard behavior_onboard.launch
roslaunch flexbe_widget behavior_ocs.launch

echo "Now import parameters"
