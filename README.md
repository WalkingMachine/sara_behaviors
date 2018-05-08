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
- `./install.sh`
- Insaller chrome ou chromium
- Importer l'app flexbe_behavior_engine/FlexBE.crx vers le menu des extention du navigateur. (drag and drop)
- Parametrer l'application depuis le widget ajouté à **Chrome**:
![alt text](https://raw.githubusercontent.com/WalkingMachine/sara_behaviors/feature/installation_documentation/config_FlexBe.png "Logo Title Text 1")

1. Importer les paramètres json fournis ici dans settings en utilisant l'app: `/settings/flexbe_config.json`
2. Ajouter les dossiers necessaires contenant les states
    - `~/sara_ws/src/sara_behaviors/sara_flexbe_states/src/sara_flexbe_states`
    - `~/sara_ws/src/generic_flexbe_states`
    - `~/sara_ws/src/flexbe_behavior_engine/flexbe_states`
3. Ajouter les dossiers necessaires contenant les behaviors de SARA
    - `~/sara_ws/src/sara_behaviors/behaviors`
4. Ajouter les dossiers necessaires contenant les behaviors flexbe de SARA
    - `~/sara_ws/src/sara_behaviors/flexbe_behaviors/behaviors`

- Compiler le workspace: `cd ~/sara_ws/ && catkin_make`

- Tester les commandes de la section [#Pour lancer](Pour lancer)

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
