#-*- coding: UTF-8 -*-

""" pyJeedom v0.2
	https://github.com/KiboOst/pyJeedom

	Requirements:

	Réglages → Système → Configuration / API : Accès API JSONRPC : Activé, IP Blanche, localhost
	Python 2 / Python 3

	#https://jeedom.github.io/core/fr_FR/jsonrpc_api
"""

import sys,os
import json

if sys.version_info[0] == 2:
	import urllib2
	requestUrl = urllib2
	quoteurl = urllib2.quote
else:
	import urllib.request, urllib.parse
	requestUrl = urllib.request
	quoteurl = urllib.parse.quote

try:
	reload(sys)
	sys.setdefaultencoding('utf-8')
except:
	pass

#import locale

class jeedom():
	def __init__(self, adrss, apiKey):
		self.adrss = adrss + '/core/api/jeeApi.php?request='
		self.apiKey = apiKey
		self.config = self._config(self)
		self.plugin = self._plugin(self)
		self.jeeObject = self._jeeObject(self)
		self.summary = self._summary(self)
		self.datastore = self._datastore(self)
		self.eqLogic = self._eqLogic(self)
		self.cmd = self._cmd(self)
		self.scenario = self._scenario(self)
		self.log = self._log(self)
		self.message = self._message(self)
		self.interact = self._interact(self)
		self.update = self._update(self)
		self.network = self._network(self)

		#self.language = self.config.byKey('language')
		#locale.setlocale(locale.LC_ALL, self.language+'.utf8')
	#
	def ping(self):
		_params = {"method":"ping"}
		return self.callJeedom(_params)
	#
	def version(self):
		_params = {"method":"version"}
		return self.callJeedom(_params)
	#
	def isOk(self):
		_params = {"method":"jeedom::isOk"}
		return self.callJeedom(_params)
	#
	def halt(self):
		_params = {"method":"jeedom::halt"}
		return self.callJeedom(_params)
	#
	def reboot(self):
		_params = {"method":"jeedom::reboot"}
		return self.callJeedom(_params)
	#
	def update(self):
		_params = {"method":"jeedom::update"}
		return self.callJeedom(_params)
	#
	def backup(self):
		_params = {"method":"jeedom::backup"}
		return self.callJeedom(_params)
	#
	def datetime(self):
		_params = {"method":"datetime"}
		return self.callJeedom(_params)
	#
	def getUsbMapping(self, name=None, gpio=None):
		_params = {"jeedom::getUsbMapping"}
		_params['params'] = {}
		_params['params']['name'] = name
		_params['params']['gpio'] = gpio
		return self.callJeedom(_params)
	#

	class _config:
		def __init__(self, parent):
			self.jeedom = parent
		#
		def byKey(self, key='', plugin=None, default=''):
			if plugin is None: plugin = 'core'
			_params = {"method":"config::byKey"}
			_params['params'] = {}
			_params['params']['key'] = key
			_params['params']['plugin'] = plugin
			_params['params']['default'] = default
			return self.jeedom.callJeedom(_params)
		#
		def save(self, key='', value='', plugin=None):
			if plugin is None: plugin = 'core'
			_params = {"method":"config::save"}
			_params['params'] = {}
			_params['params']['key'] = key
			_params['params']['value'] = value
			_params['params']['plugin'] = plugin
			return self.jeedom.callJeedom(_params)
	#
	class _plugin:
		def __init__(self, parent):
			self.jeedom = parent
		#
		def listPlugin(self, activateOnly=False, orderByCaterogy=False):
			_params = {"method":"plugin::listPlugin"}
			_params['params'] = {}
			if activateOnly: _params['params']['activateOnly'] = 1
			if orderByCaterogy: _params['params']['orderByCaterogy'] = 1
			return self.jeedom.callJeedom(_params)
		#
		def byId(self, id=None):
			allPlugins = self.listPlugin()
			for plugin in allPlugins:
				if plugin['id'] == id:
					return plugin
			return {"error": {"message": "%s introuvable"%__class__.__name__}}
		#
		def install(self, plugin_id=None, logicalId=None):
			_params = {"method":"plugin::install"}
			_params['params'] = {}
			if plugin_id: _params['params']['plugin_id'] = plugin_id
			if logicalId: _params['params']['logicalId'] = logicalId
			return self.jeedom.callJeedom(_params)
		#
		def remove(self, plugin_id=None, logicalId=None):
			_params = {"method":"plugin::remove"}
			_params['params'] = {}
			if plugin_id: _params['params']['plugin_id'] = plugin_id
			if logicalId: _params['params']['logicalId'] = logicalId
			return self.jeedom.callJeedom(_params)
		#
		def dependancyInfo(self, plugin_id=None):
			_params = {"method":"plugin::dependancyInfo"}
			_params['params'] = {}
			_params['params']['plugin_id'] = plugin_id
			return self.jeedom.callJeedom(_params)
		#
		def dependancyInstall(self, plugin_id=None):
			_params = {"method":"plugin::dependancyInstall"}
			_params['params'] = {}
			_params['params']['plugin_id'] = plugin_id
			return self.jeedom.callJeedom(_params)
		#
		def deamonInfo(self, plugin_id=None):
			_params = {"method":"plugin::deamonInfo"}
			_params['params'] = {}
			_params['params']['plugin_id'] = plugin_id
			return self.jeedom.callJeedom(_params)
		#
		def deamonStart(self, plugin_id=None, debug=None, forceRestart=None):
			_params = {"method":"plugin::deamonStart"}
			_params['params'] = {}
			_params['params']['plugin_id'] = plugin_id
			if debug: _params['params']['debug'] = 1
			if forceRestart: _params['params']['forceRestart'] = 1
			return self.jeedom.callJeedom(_params)
		#
		def deamonStop(self, plugin_id=None):
			_params = {"method":"plugin::deamonStop"}
			_params['params'] = {}
			_params['params']['plugin_id'] = plugin_id
			return self.jeedom.callJeedom(_params)
		#
		def deamonChangeAutoMode(self, plugin_id=None):
			_params = {"method":"plugin::deamonChangeAutoMode"}
			_params['params'] = {}
			_params['params']['plugin_id'] = plugin_id
			return self.jeedom.callJeedom(_params)
		#
	#
	class _jeeObject:
		def __init__(self, parent):
			self.jeedom = parent
		#
		def byName(self, _name=None):
			result = self.all()
			if 'error' in result: return result
			for item in result:
				if _name == item['name']:
					return item
			return {"error": {"message": "%s introuvable"%__class__.__name__}}
		#
		def all(self):
			_params = {"method":"jeeObject::all"}
			return self.jeedom.callJeedom(_params)
		#
		def byId(self, id=None):
			_params = {"method":"jeeObject::byId"}
			_params['params'] = {}
			_params['params']['id'] = id
			return self.jeedom.callJeedom(_params)
		#
		def full(self):
			_params = {"method":"jeeObject::full"}
			return self.jeedom.callJeedom(_params)
		#
		def fullById(self):
			_params = {"method":"jeeObject::fullById"}
			_params = {"method":"jeeObject::byId"}
			_params['params'] = {}
			_params['params']['id'] = id
			return self.jeedom.callJeedom(_params)
		#
		def save(self, id=None):
			_params = {"method":"jeeObject::save"}
			_params['params'] = {}
			_params['params']['id'] = id
			return self.jeedom.callJeedom(_params)
		#
	#
	class _summary:
		def __init__(self, parent):
			self.jeedom = parent
		#
		def main(self):
			_params = {"method":"summary::global"}
			return self.jeedom.callJeedom(_params)
		#
		def byId(self, id=None, key=None, raw=None):
			_params = {"method":"jeeObject::byId"}
			_params['params'] = {}
			_params['params']['id'] = id
			if key: _params['params']['key'] = key
			if raw: _params['params']['raw'] = raw
			return self.jeedom.callJeedom(_params)
		#
	#
	class _datastore:
		def __init__(self, parent):
			self.jeedom = parent
		#
		def byTypeLinkIdKey(self, type=None, linkId=None, key=None):
			_params = {"method":"datastore::byTypeLinkIdKey"}
			_params['params'] = {}
			if type: _params['params']['type'] = type
			if linkId: _params['params']['linkId'] = linkId
			if key: _params['params']['key'] = key
			return self.jeedom.callJeedom(_params)
		#
		def save(self, type=None, linkId=None, key=None, value=''):
			_params = {"method":"datastore::save"}
			_params['params'] = {}
			_params['params']['type'] = type
			_params['params']['linkId'] = linkId
			_params['params']['key'] = key
			_params['params']['value'] = value
			return self.jeedom.callJeedom(_params)
		#
	#
	class _eqLogic:
		def __init__(self, parent):
			self.jeedom = parent
		#
		def byName(self, _name=None):
			result = self.all()
			if 'error' in result: return result
			for item in result:
				if _name == item['name']:
					return item
			return {"error": {"message": "%s introuvable"%__class__.__name__}}
		#
		def byHumanName(self, _humanName=''):
			allObjects = self.jeedom.jeeObject.all()
			objectsList = {}
			for obj in allObjects:
				objectsList[obj['id']] = obj['name']

			allEqlogics = self.all()
			for item in allEqlogics:
				object_name = objectsList[item['object_id']] if item['object_id'] != None else 'Aucun'
				humanName = '[%s][%s]'%(object_name, item['name'])
				if _humanName == humanName:
					return item
			return {"error": {"message": "%s introuvable"%__class__.__name__}}
		#
		def all(self):
			_params = {"method":"eqLogic::all"}
			return self.jeedom.callJeedom(_params)
		#
		def byType(self, type=None):
			_params = {"method":"eqLogic::byType"}
			_params['params'] = {}
			_params['params']['type'] = type
			return self.jeedom.callJeedom(_params)
		#
		def byObjectId(self, object_id=None):
			_params = {"method":"eqLogic::byObjectId"}
			_params['params'] = {}
			_params['params']['object_id'] = object_id
			return self.jeedom.callJeedom(_params)
		#
		def byId(self, id=None):
			_params = {"method":"eqLogic::byId"}
			_params['params'] = {}
			_params['params']['id'] = id
			return self.jeedom.callJeedom(_params)
		#
		def fullById(self, id=None):
			_params = {"method":"eqLogic::fullById"}
			_params['params'] = {}
			_params['params']['id'] = id
			return self.jeedom.callJeedom(_params)
		#
		def save(self, eqType_name=None, id=None, cmd=None):
			_params = {"method":"eqLogic::save"}
			_params['params'] = {}
			_params['params']['eqType_name'] = eqType_name
			if id: _params['params']['id'] = id
			if cmd: _params['params']['cmd'] = cmd
			return self.jeedom.callJeedom(_params)
		#
		def byTypeAndId(self, eqType=None, id=None):
			_params = {"method":"eqLogic::byTypeAndId"}
			_params['params'] = {}
			_params['params']['id'] = id
			_params['params']['cmd'] = cmd
			return self.jeedom.callJeedom(_params)
		#
	#
	class _cmd:
		def __init__(self, parent):
			self.jeedom = parent
		#
		def byName(self, _name=None):
			result = self.all()
			if 'error' in result: return result
			for item in result:
				if _name == item['name']:
					return item
			return {"error": {"message": "%s introuvable"%__class__.__name__}}
		#
		def byHumanName(self, _humanName=''):
			allObjects = self.jeedom.jeeObject.all()
			objectsList = {}
			for obj in allObjects:
				objectsList[obj['id']] = obj['name']

			allEqlogics = self.jeedom.eqLogic.all()
			allCmds = self.all()
			for item in allCmds:
				object_name = ''
				for eq in allEqlogics:
					if eq['id'] == item['eqLogic_id']:
						eqlogic_name = eq['name']
						object_name = objectsList[eq['object_id']] if eq['object_id'] != None else 'Aucun'
						break

				humanName = '[%s][%s][%s]'%(object_name, eqlogic_name, item['name'])
				if _humanName == humanName:
					return item
			return {"error": {"message": "%s introuvable"%__class__.__name__}}
		#
		def all(self):
			_params = {"method":"cmd::all"}
			return self.jeedom.callJeedom(_params)
		#
		def byEqLogicId(self, eqLogic_id=None):
			_params = {"method":"cmd::byEqLogicId"}
			_params['params'] = {}
			_params['params']['eqLogic_id'] = eqLogic_id
			return self.jeedom.callJeedom(_params)
		#
		def byId(self, id=None):
			_params = {"method":"cmd::byId"}
			_params['params'] = {}
			_params['params']['id'] = id
			return self.jeedom.callJeedom(_params)
		#
		def execCmd(self, id=None):
			_params = {"method":"cmd::execCmd"}
			_params['params'] = {}
			_params['params']['id'] = id
			return self.jeedom.callJeedom(_params)
		#
		def getStatistique(self, id=None):
			_params = {"method":"cmd::getStatistique"}
			_params['params'] = {}
			_params['params']['id'] = id
			return self.jeedom.callJeedom(_params)
		#
		def getTendance(self, id=None):
			_params = {"method":"cmd::getTendance"}
			_params['params'] = {}
			_params['params']['id'] = id
			return self.jeedom.callJeedom(_params)
		#
		def getHistory(self, id=None):
			_params = {"method":"cmd::getHistory"}
			_params['params'] = {}
			_params['params']['id'] = id
			return self.jeedom.callJeedom(_params)
		#
		def save(self, eqType_name=None, id=None):
			_params = {"method":"cmd::save"}
			_params['params'] = {}
			_params['params']['eqType_name'] = eqType_name
			if id: _params['params']['id'] = id
			return self.jeedom.callJeedom(_params)
		#
		def event(self, id=None, value=None, datetime=None):
			_params = {"method":"cmd::event"}
			_params['params'] = {}
			_params['params']['id'] = id
			_params['params']['value'] = value
			if datetime: _params['params']['datetime'] = datetime
			return self.jeedom.callJeedom(_params)
		#
	#
	class _scenario:
		def __init__(self, parent):
			self.jeedom = parent
		#
		def byName(self, _name=None):
			result = self.all()
			if 'error' in result: return result
			for item in result:
				if _name == item['name']:
					return item
			return {"error": {"message": "%s introuvable"%__class__.__name__}}
		#
		def byHumanName(self, _humanName=''):
			allObjects = self.jeedom.jeeObject.all()
			objectsList = {}
			for obj in allObjects:
				objectsList[obj['id']] = obj['name']

			allScenarios = self.all()
			for item in allScenarios:
				object_name = objectsList[item['object_id']] if item['object_id'] != None else 'Aucun'
				group = item['group'] if item['group'] != '' else 'Aucun'
				humanName = '[%s][%s][%s]'%(object_name, group, item['name'])
				if _humanName == humanName:
					return item
			return {"error": {"message": "%s introuvable"%__class__.__name__}}
		#
		def all(self):
			_params = {"method":"scenario::all"}
			return self.jeedom.callJeedom(_params)
		#
		def byId(self, id=None):
			_params = {"method":"scenario::byId"}
			_params['params'] = {}
			_params['params']['id'] = id
			return self.jeedom.callJeedom(_params)
		#
		def changeState(self, id=None, state=None):
			_params = {"method":"scenario::changeState"}
			_params['params'] = {}
			_params['params']['id'] = id
			_params['params']['state'] = state
			return self.jeedom.callJeedom(_params)
		#
		def export(self, id=None):
			_params = {"method":"scenario::export"}
			_params['params'] = {}
			_params['params']['id'] = id
			return self.jeedom.callJeedom(_params)
		#
		def doImport(self, id=None, humanName=None, doImport=None):
			_params = {"method":"scenario::import"}
			_params['params'] = {}
			_params['params']['id'] = id
			_params['params']['import'] = doImport
			if humanName: _params['params']['humanName'] = humanName
			return self.jeedom.callJeedom(_params)
		#
	#
	class _log:
		def __init__(self, parent):
			self.jeedom = parent
		#
		def get(self, log=None, start=0, nbLine=10):
			_params = {"method":"log::get"}
			_params['params'] = {}
			_params['params']['log'] = log
			_params['params']['start'] = start
			_params['params']['nbLine'] = nbLine
			return self.jeedom.callJeedom(_params)
		#
		def list(self, filtre=None):
			_params = {"method":"log::list"}
			_params['params'] = {}
			if filtre: _params['params']['filtre'] = filtre
			return self.jeedom.callJeedom(_params)
		#
		def empty(self, log=None):
			_params = {"method":"log::empty"}
			_params['params'] = {}
			_params['params']['log'] = log
			return self.jeedom.callJeedom(_params)
		#
		def remove(self, log=None):
			_params = {"method":"log::remove"}
			_params['params'] = {}
			_params['params']['log'] = log
			return self.jeedom.callJeedom(_params)
		#
	#
	class _message:
		def __init__(self, parent):
			self.jeedom = parent
		#
		def all(self):
			_params = {"method":"message::all"}
			return self.jeedom.callJeedom(_params)
		#
		def removeAll(self):
			_params = {"method":"message::removeAll"}
			return self.jeedom.callJeedom(_params)
		#
	#
	class _interact:
		def __init__(self, parent):
			self.jeedom = parent
		#
		def tryToReply(self):
			_params = {"method":"interact::tryToReply"}
			return self.jeedom.callJeedom(_params)
		#
		def all(self):
			_params = {"method":"interactQuery::all"}
			return self.jeedom.callJeedom(_params)
		#
	#
	class _update:
		def __init__(self, parent):
			self.jeedom = parent
		#
		def all(self):
			_params = {"method":"update::all"}
			return self.jeedom.callJeedom(_params)
		#
		def nbNeedUpdate(self):
			_params = {"method":"update::nbNeedUpdate"}
			return self.jeedom.callJeedom(_params)
		#
		def update(self):
			_params = {"method":"update::update"}
			return self.jeedom.callJeedom(_params)
		#
		def checkUpdate(self):
			_params = {"method":"update::checkUpdate"}
			return self.jeedom.callJeedom(_params)
		#
		def doUpdate(self, plugin_id=None, logicalId=None):
			_params = {"method":"update::doUpdate"}
			_params['params'] = {}
			if plugin_id: _params['params']['plugin_id'] = plugin_id
			if logicalId: _params['params']['logicalId'] = logicalId
			return self.jeedom.callJeedom(_params)
		#
	#
	class _network:
		def __init__(self, parent):
			self.jeedom = parent
		#
		def restartDns(self):
			_params = {"method":"network::restartDns"}
			return self.jeedom.callJeedom(_params)
		#
		def stopDns(self):
			_params = {"method":"network::stopDns"}
			return self.jeedom.callJeedom(_params)
		#
		def dnsRun(self):
			_params = {"method":"network::dnsRun"}
			return self.jeedom.callJeedom(_params)
		#
	#



	#__jeeApi caller__
	def callJeedom(self, _params=''):
		if not 'params' in _params:
			_params['params'] = {}
		_params['params']['apikey'] = self.apiKey
		_params['jsonrpc'] = "2.0"
		data = json.dumps(_params)
		url = self.adrss + quoteurl(data)
		response = requestUrl.urlopen(url).read()
		try:
			result = json.loads(response)
			if 'error' in result: return result
			return result['result']
		except Exception as e:
			return {"error":e}
	#
	def callJeedomByType(self, _params=''):
		pass
	#
#
