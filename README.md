
# pyJeedom

Module python pour Jeedom.

Utilisation dans des scripts python dans Jeedom, ou depuis l’extérieur (même réseau ou pas)

## Requirements
- Une installation Jeedom fonctionnelle !
- Activer l'API Json dans : Réglages → Système → Configuration / API : Accès API JSONRPC : Activé, IP Blanche, localhost.
- Python 2 ou 3 installé.

## Installation
- Copier le fichier `[pyJeedom.py](https://github.com/KiboOst/pyJeedom/blob/master/pyJeedom.py "pyJeedom.py")` Sur votre Jeedom ou une autre machine.
- Importer le module dans un script Python.

## Documentation
- Vous pouvez vous référer à la documentation de l'API JSONRPC : [jsonrpc_api](https://jeedom.github.io/core/fr_FR/jsonrpc_api)

### Changements
Certains noms de fonctions sont réservés en Python :
##### summary::global
Utilisez `jeedom.summary.main()`

##### scenario::import
Utilisez `jeedom.scenario.doImport()`

### Additions
##### `jeedom.eqLogic.byName('string')`
##### `jeedom.cmd.byName('string')`
##### `jeedom.scenario.byName('string')`
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

#Variables:
jeedom.datastore.save('scenario', -1, 'maVariable', 'pyJeedom rocks')
var = jeedom.datastore.byTypeLinkIdKey('scenario', -1, 'maVariable')
if 'value' in var:
	print(var['value'])
else:
	print('Unfound variable')
```

Appel et passage de paramètres depuis un bloc CODE :
Ici, on écrit les tags du scénarios dans un fichier json, puis on appelle le script python.
```php
$tags = $scenario->getTags();
$data = array();
foreach ($tags as $key => $value) {
  $key = str_replace('#', '', $key);
  $data[$key] = $value;
}
$fp = fopen('/var/www/html/kiboost/data.json', 'w');
fwrite($fp, json_encode($data));
fclose($fp);

$result = shell_exec('python /var/www/html/kiboost/doStuff.py');
$tags['#result#'] = $result;
$scenario->setTags($tags);
```
/var/www/html/kiboost/doStuff.py :
```python
#-*- coding: UTF-8 -*-
import sys,os
import json
f = open(r'/var/www/html/kiboost/data.json', "r")
data = f.read()
f.close()
data = json.loads(data)

#do stuff here

#send result to scenario:
print('something stuffy')
```
Vous pouvez ensuite utiliser **tag(result)**, ou une variable enregistrer par le votre script python ou autre, dans la suite de votre scénario.

## Changelog

##### 09/01/2020
- Création et parution !

### ToDo
- byHumanName sur les eqLogic, scenario, cmd, jeeObject etc

