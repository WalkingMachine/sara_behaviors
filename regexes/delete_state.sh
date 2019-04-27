#!/usr/bin/env bash

DEPFILE="regexes/graphs/dependenceGraph.plantuml"
STATE=$1


gawk -f regexes/generateDependenciesGraph.gawk  sara_flexbe_behaviors/src/sara_flexbe_behaviors/*.py  > /dev/null && sort -u regexes/graphs/dependenceGraph.plantuml > /dev/null

STATE2=$(echo $STATE | tr -d _)

OCCURENCE="$(grep -ci "$STATE2 -> " "$DEPFILE")"
echo $OCCURENCE

# If the behavior exist
if [ -f "sara_flexbe_states/src/sara_flexbe_states/$STATE.py" ]
then

    # If the file is in the deppendency file
    if [[ 0 = $OCCURENCE ]]
    then

        echo "deleting sara_flexbe_states/src/sara_flexbe_states/$STATE.py"
        rm -rf deleting sara_flexbe_states/src/sara_flexbe_states/$STATE.py

    else

        echo "The state \"$STATE\" is still in use"
        grep -i "$STATE2 -> " "$DEPFILE"

    fi
else

    echo "The state \"$STATE\" does not exist."

fi