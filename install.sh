#!/bin/bash

#CLONE NECESSARY REPOs
cd ..
git clone https://github.com/team-vigir/flexbe_behavior_engine.git
git clone https://github.com/FlexBE/generic_flexbe_states.git

sudo apt install ros-kinetic-rosbridge-suite -y

echo "Now import parameters"
