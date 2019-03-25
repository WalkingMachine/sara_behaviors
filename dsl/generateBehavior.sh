#!/usr/bin/env bash
if [ $# -lt 2 ]
then
    manifestPath="$HOME/sara_ws/src/sara_behaviors/sara_flexbe_behaviors/manifest/"
    behaviorPath="$HOME/sara_ws/src/sara_behaviors/sara_flexbe_behaviors/src/sara_flexbe_behaviors/"
else
    manifestPath=$2"/"
    behaviorPath=$3"/"
fi
echo $manifestPath$(head -1  $1| sed 's/\(.*\)/\L\1/').xml
echo $behaviorPath$(head -1  $1| sed 's/\(.*\)/\L\1/')_sm.py
gawk -f genManifest.awk $1 > $manifestPath$(head -1  $1| sed 's/\(.*\)/\L\1/').xml
lineCount=$(wc -l $1 | awk '{print $1}')
gawk -f generatePyFile_lastPass.awk -v lineCount=$lineCount $1 > $behaviorPath$(head -1  $1| sed 's/\(.*\)/\L\1/')_sm.py
