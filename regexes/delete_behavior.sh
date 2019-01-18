#!/usr/bin/env bash

DEPFILE="regexes/graphs/dependenceGraph.plantuml"

gawk -f regexes/generateDependenciesGraph.gawk  behaviors/behavior_action_*/src/behavior_*/*.py  > /dev/null && sort -u regexes/graphs/dependenceGraph.plantuml > /dev/null


OCCURENCE="$(grep -ci "$1 -> " "$DEPFILE")"
echo $OCCURENCE

# If the behavior exist
if [ -d "behaviors/behavior_$1" ]
then

    # If the file is in the deppendency file
    if [[ 0 = $OCCURENCE ]]
    then

        echo "deleting: behaviors/behavior_$1"
        rm -rf behaviors/behavior_$1

        echo "deleting: flexbe_behaviors/behaviors/behavior_$1.xml"
        rm -rf flexbe_behaviors/behaviors/behavior_$1.xml

        echo "deleting: behavior_$1 from package.xml"
        sed -i "/$1/d" flexbe_behaviors/package.xml

        echo "$1 deleting: behavior_$1 from package.xml"

    else

        echo "behavior_$1 is still in use"
        grep "$1 => " "$DEPFILE"

    fi
else

    echo "behavior_$1 does not exist"

fi