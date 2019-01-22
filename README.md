# sara_behaviors
Ce repo contient tout les states et bahaviors spécifiques à sara.

### Installation
- [Installer flexbe](http://philserver.bplaced.net/fbe/download.php)

### Dependances
Ce paquet a de nombreuses dépendances. En voicis quelques unes.
- [sara_msgs](https://github.com/WalkingMachine/sara_msgs)
- [wm_tts](https://github.com/WalkingMachine/wm_tts)
- [sara_navigation](https://github.com/WalkingMachine/sara_navigation)


### Pour lancer
Le serveur flexbe:
```sh
roslaunch flexbe_onboard behavior_onboard.launch
```
Le flexbe app:
```sh
roslaunch flexbe_app flexbe_full.launch
```
Ou si vous utilisez les [settings standards de WM](https://github.com/WalkingMachine/settings)
```sh
FLEXBE
FLEXBEWIDGET
```
Une behavior en particulié sans l'interface
```sh
rosrun flexbe_widget be_launcher -b 'Example Behavior'
```
### liens utiles
- [Le site de flexbe](http://philserver.bplaced.net/fbe/index.php)
- [Les tutoriels de flexbe](http://wiki.ros.org/flexbe/Tutorials)