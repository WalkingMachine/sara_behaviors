# sara_behaviors
This repo contains all sara-specific states and behaviors.

# Steps to run
## LU4R Semantic recognition
To allow semantic recognition, run the [lu4r semantic analyser](https://drive.google.com/file/d/0BwncD7Fw45HYd3JfZEIyQ0FSMU0/view)
with this command:
```sh
java -Xmx1G -jar lu4r-server-0.2.1.jar simple amr en 9001
```
## Sara_say
Launch the [wm_tts](https://github.com/WalkingMachine/wm_tts) launchfile using this command:
```sh
roslaunch wm_tts wm_tts_EN.launch
```
