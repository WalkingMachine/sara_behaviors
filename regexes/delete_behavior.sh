#!/usr/bin/env bash

DEPFILE="regexes/graphs/dependenceGraph.plantuml"

# If the behavior exist
if [ -d "behaviors/behavior_$1" ]
then

    # If the file is in the deppendency file
    if [[ 0 = $(grep -c "$1" "$DEPFILE") ]]
    then

        echo "deleting: behaviors/behavior_$1"
        rm -rf behaviors/behavior_$1

        echo "deleting: flexbe_behaviors/behaviors/behavior_$1.xml"
        rm -rf flexbe_behaviors/behaviors/behavior_$1.xml

        echo "deleting: behavior_$1 from package.xml"
        sed -i "/$1/d" flexbe_behaviors/package.xml

    else

        echo "behavior_$1 is still in use"
        grep "$1" "$DEPFILE"

    fi
else

    echo "behavior_$1 does not exist"

fi