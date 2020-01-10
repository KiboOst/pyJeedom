# pyJeedom

Module python pour Jeedom.

Utilisation dans des scripts python dans Jeedom, ou depuis l’extérieur (même réseau ou pas).

## Requirements
- Une installation Jeedom fonctionnelle !
- Activer l'API Json:
Réglages → Système → Configuration / API :
Accès API JSONRPC : Activé, IP Blanche ou localhost.
- Python 2 ou 3 installé.

## Installation
- Copier le fichier [pyJeedom.py](https://github.com/KiboOst/pyJeedom/blob/master/pyJeedom.py "pyJeedom.py") sur votre Jeedom, ou une autre machine ayant Python.
- Importer le module dans un script Python.

## Documentation
- Vous pouvez vous référer à la documentation de l'API JSONRPC : [jsonrpc_api](https://jeedom.github.io/core/fr_FR/jsonrpc_api)

### Changements
Certains noms de fonctions sont réservés en Python :
##### summary::global
> Utilisez `jeedom.summary.main()`

##### scenario::import
> Utilisez `jeedom.scenario.doImport()`

### Additions
##### `jeedom.eqLogic.byName('string')`
##### `jeedom.eqLogic.byHumanName('string')`
##### `jeedom.cmd.byName('string')`
##### `jeedom.cmd.byHumanName('string')`
##### `jeedom.scenario.byName('string')`
##### `jeedom.scenario.byHumanName('string')`
##### `jeedom.jeeObject.byName('string')`

## Utilisation
Voici un exemple avec le module copié sur Jeedom, dans le répertoire */var/www/html/kiboost/*
Vous trouverez la clé API dans Réglages → Système → Configuration / API : Clé API

```python
#-*- coding: UTF-8 -*-

import sys
sys.path.append(r'/var/www/html/kiboost/')
from pyJeedom import jeedom

adrss = 'http://192.168.1.10'
apiKey = 'xxxmyxapixkeyxxx'
jeedom = jeedom(adrss, apiKey)
#Your Jeedom name:
value = jeedom.config.byKey('name')
print(value)
#Some Jeedom infos:
print(jeedom.datetime())
print(jeedom.version())
print(jeedom.isOk())

#Message center:
msgs = jeedom.message.all()
print(msgs)

#Get eqLogic by humanName:
eq = jeedom.eqLogic.byHumanName('[Maison][Journal]')
print(eq)

#Get cmd by humanName:
cmd = jeedom.cmd.byHumanName('[Salon][Ampli][Power]')
print(cmd)

#Variables:
jeedom.datastore.save('scenario', -1, 'maVariable', 'pyJeedom rocks')
var = jeedom.datastore.byTypeLinkIdKey('scenario', -1, 'maVariable')
if 'value' in var:
	print(var['value'])
else:
	print('Unfound variable')

#Get scenario by humanName:
sc = jeedom.scenario.byHumanName('[Maison][rhasspy][rhasspy_Skills]')
print(sc)

#Disable a scenario:
sc = jeedom.scenario.byName('testPython')
jeedom.scenario.changeState(sc['id'], 'disable')
#Run it:
jeedom.scenario.changeState(sc['id'], 'run')

#Get plugins list:
plugins = jeedom.plugin.listPlugin()
print(plugins)

#Get a plugin by id:
plugin = jeedom.plugin.byId('jeerhasspy')
print(plugin['changelog'])

#Get all its eqLogics:
pluginEqlogics = jeedom.eqLogic.byType('jeerhasspy')
print(pluginEqlogics)
```

Exemple depuis un scénario, bloc CODE:
On passe en paramètre les tags du scénario au script python, puis on récupère le résultat.
```php
$tags = $scenario->getTags();
$arg = escapeshellarg(json_encode($tags));
$tags['#result#'] = shell_exec("python /var/www/html/kiboost/doStuff.py ".$arg);
$scenario->setTags($tags);
```
En Python (/var/www/html/kiboost/doStuff.py) :
```python
#-*- coding: UTF-8 -*-

import sys
import json
sys.path.append(r'/var/www/html/kiboost/')
from pyJeedom import jeedom

if __name__ == "__main__":
	data = None
	if len(sys.argv) > 1:
		data = json.loads(sys.argv[1])

	adrss = 'http://192.168.1.10'
	apiKey = 'xxxmyxapixkeyxxx'
	jeedom = jeedom(adrss, apiKey)

	#do stuff here
	#

	#send result to scenario:
	print('something stuffy')
```
Vous pouvez ensuite utiliser **tag(result)**, ou une variable enregistrée par votre script python par exemple, dans la suite de votre scénario.

## Changelog

##### 10/01/2020
- New : `jeedom.eqLogic.byHumanName('string')`
- New : `jeedom.cmd.byHumanName('string')`
- New : `jeedom.scenario.byHumanName('string')`

##### 09/01/2020
- Création et parution !



