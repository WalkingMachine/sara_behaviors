#!/usr/bin/env bash
if [ $# -lt 2 ]
then
    manifestPath="$HOME/sara_ws/src/sara_behaviors/sara_flexbe_behaviors/manifest/"
    behaviorPath="$HOME/sara_ws/src/sara_behaviors/sara_flexbe_behaviors/src/sara_flexbe_behaviors/"
else
    manifestPath=$2"/"
    behaviorPath=$3"/"
fi
name=$( head -1  $1| sed 's/\(.*\)/\L\1/');
echo $manifestPath$name".xml"
echo $behaviorPath$name"_sm.py"
gawk -f genManifest.awk $1 > $manifestPath$name".xml"
lineCount=$(sed '/^\s*#$/d;/^\s*$/d' $1 | wc -l);
gawk -f generatePyFile_lastPass.awk -v lineCount=$lineCount $1 > $behaviorPath$name"_sm.py"
