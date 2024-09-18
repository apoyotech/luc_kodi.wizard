import xbmc
import xbmcgui
import xbmcaddon
import json
import base64
import xml.etree.ElementTree as ET
from .maintenance import clear_packages, clear_thumbnails, create_ThumbsFolder
from uservar import buildfile
from .addonvar import setting, setting_set, addon_name, isBase64, headers, dialog, local_string, addon_id

current_build = setting('buildname')
try:
	current_version = float(setting('buildversion')) 
except:
	current_version = 0.0

class Startup:
	
	def check_updates(self):
	   	if current_build == 'No hay build instalada':
	   		if dialog.yesno(addon_name, 'No hay ninguna build instalada.\n¿Desea instalar una build ahora?') is True:
	   			xbmc.executebuiltin(f'ActivateWindow(10001, "plugin://{addon_id}/?mode=1",return)')
	   		else:
	   			return
	   	response = self.get_page(buildfile)
	   	version = 0.0
	   	try:
	   		builds = json.loads(response)['builds']
	   		for build in builds:
	   				if build.get('name') == current_build:
	   					version = float(build.get('version'))
	   					break
	   	except:
	   		builds = ET.fromstring(response)
	   		for tag in builds.findall('build'):
	   				if tag.find('name').text == current_build:
	   					version = float(tag.find('version').text)
	   					break
	   	if version > current_version:
	   		if xbmcgui.Dialog().yesno(addon_name, local_string(30047) + ' ' + current_build +' ' + local_string(30048) + '\n' + local_string(30049) + ' ' + str(current_version) + '\n' + local_string(30050) + ' ' + str(version) + '\n' + local_string(30051)) is True:
	   			xbmc.executebuiltin(f'ActivateWindow(10001, "plugin://{addon_id}/?mode=1",return)')
	   		else:
	   			return
	   	else:
	   		return

	def file_check(self, bfile):
		if isBase64(bfile):
			return base64.b64decode(bfile).decode('utf8')
		else:
			return bfile
			
	def get_page(self, url):
	   	from urllib.request import Request,urlopen
	   	req = Request(self.file_check(url), headers = headers)
	   	return urlopen(req).read()

	def run_startup(self):
		if setting('autoclearpackages')=='true':
			xbmc.sleep(2000)
			clear_packages()
		if xbmc.getCondVisibility('System.HasAddon(plugin.video.palantir2)'):
			xbmc.executebuiltin('ActivateWindow(plugin.video.palantir2)')
			xbmc.executebuiltin('ReplaceWindow(plugin.video.palantir2)')
			xbmc.sleep(1000)
		if xbmc.getCondVisibility('System.HasAddon(plugin.video.winner)'):
			xbmc.executebuiltin('ActivateWindow(plugin.video.winner)')
			xbmc.executebuiltin('ReplaceWindow(plugin.video.winner)')
			xbmc.sleep(10000)
		if xbmc.getCondVisibility('System.HasAddon(plugin.googledrive)'):
			if dialog.yesno(current_build, '\n [B]¿Desea que actualice la videoteca?\n Pulse SI[/B] y actualizaré la videoteca para usted.\n Para evitar fallos no interactúe por el menú.\n [B]Espere por el mensaje de confirmación, gracias.[/B]', nolabel=local_string(30032), yeslabel=local_string(30067)) is True:
				xbmc.executebuiltin('UpdateLibrary(video)')
				xbmc.sleep(20000)
				xbmc.executebuiltin('CleanLibrary(video)')
				xbmc.sleep(7000)
				xbmc.executebuiltin('UpdateLibrary(video)')
				xbmc.sleep(7000)
				xbmc.executebuiltin('ReloadSkin()')
				dialog.ok(current_build, '\n \n [B]Videoteca Actualizada.[/B]\n Disfrute del nuevo contenido.')
			else:
				return
		if xbmc.getCondVisibility('System.HasAddon(script.module.clouddrive.common)'):
			xbmc.executebuiltin('!System.HasAddon(resource.images.studios.white)>InstallAddon(resource.images.studios.white)')
			xbmc.executebuiltin('!System.HasAddon(resource.images.moviecountryicons.maps)>InstallAddon(resource.images.moviecountryicons.maps)')
			xbmc.sleep(1000)

		if not setting('firstrunSave')=='true':
			xbmc.sleep(2000)
			self.check_updates()
		
		if setting('firstrun') == 'true':
			from resources.lib.modules import addons_enable
			addons_enable.enable_addons()
		setting_set('firstrun', 'false')