# sara_behaviors
Ce repo contient tout les states et bahaviors spécifiques à sara.

### Installation
- Installer flexbe

### Dependances
Ce paquet a de nombreuses dépendances. En voicis quelques unes.
- [lu4r semantic analyser](https://drive.google.com/file/d/0BwncD7Fw45HYd3JfZEIyQ0FSMU0/view)
- [wm_tts](https://github.com/WalkingMachine/wm_tts)
- [sara_navigation](https://github.com/WalkingMachine/sara_navigation)


# FLEXBE,

C'est l'engine de nos state machines. C'est une interface graphique qui permet d'assembler des states pour tracer des behaviors comme on veut. Ça    marche en python et on peut ajouter nos propres states personnalisé selon nos besoins. L'engine produit du code smack.

### Installation :
- sudo ./install.sh
- Insaller chrome ou chromium
- Importer l'app flexbe_behavior_engine/FlexBE.crx vers le menu des extention du navigateur. (drag and drop)
- Importer les paramètres json fournis ici dans settings en utilisant l'app

### Pour lancer
Le serveur flexbe:
```sh
    roslaunch flexbe_onboard behavior_onboard.launch
```
L'interface graphique:
```sh
    roslaunch flexbe_widget behavior_ocs.launch
```
Une behavior en particulié sans l'interface
```sh
rosrun flexbe_widget be_launcher -b 'Example Behavior'
```
### liens utiles
- [Le site de flexbe](http://philserver.bplaced.net/fbe/index.php)
- [Les tutoriels de flexbe](http://wiki.ros.org/flexbe/Tutorials)
