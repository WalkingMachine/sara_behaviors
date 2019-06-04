# sara_behaviors
Ce repo contient tout les states et bahaviors spécifiques à sara.

### Installation
- [Installer flexbe](http://philserver.bplaced.net/fbe/download.php)
#### Warning:
La version actuelle de flexbe est incompatible avec notre projet. Installer ce fix en attendant un fix officiel.
```
cd flexbe_app
git remote set-url origin git@github.com:ffriese/flexbe_app.git
OU
git remote set-url origin https://github.com/ffriese/flexbe_app.git
git fetch
git checkout 2afa637417c10fdbc9216113f2aac8b80800ab94
```

### Dependances
Ce paquet a de nombreuses dépendances. En voicis quelques unes.
- [sara_msgs](https://github.com/WalkingMachine/sara_msgs)
- [wm_tts](https://github.com/WalkingMachine/wm_tts)
- [sara_navigation](https://github.com/WalkingMachine/sara_navigation)
- [vizbox](https://github.com/WalkingMachine/vizbox)
- [wm_nlu](https://github.com/WalkingMachine/wm_nlu)
- [wm_direction_to_point](https://github.com/WalkingMachine/wm_direction_to_point)

### Pour lancer
Flexbe au complet avec le GUI et le serveur:
```sh
roslaunch flexbe_app flexbe_full.launch
```
Le serveur flexbe seulement:
```sh
roslaunch flexbe_onboard behavior_onboard.launch
```
Le flexbe app seulement:
```sh
roslaunch flexbe_app flexbe_ocs.launch
```
Une behavior en particulié sans le GUI
```sh
rosrun flexbe_widget be_launcher -b 'Example Behavior'
```
Des alias pour simplifier l'utilisation sont disponnibles dans [settings standards de WM](https://github.com/WalkingMachine/settings)

### liens utiles
- [Le site de flexbe](http://philserver.bplaced.net/fbe/index.php)
- [Les tutoriels de flexbe](http://wiki.ros.org/flexbe/Tutorials)
