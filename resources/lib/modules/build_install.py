import os
import xbmc
from .downloader import Downloader
from zipfile import ZipFile
from .save_data import save_backup,save_restore
from .maintenance import fresh_start
from .addonvar import dp, dialog, zippath, addon_name, home, setting_set, local_string

def main(name, name2, version, url):
	yesInstall = dialog.yesno(name, local_string(30028), nolabel=local_string(30029), yeslabel=local_string(30030))  # Ready to install, Cancel, Continue
	if yesInstall:
	    save_backup()
	    yesFresh = dialog.yesno(local_string(30012), local_string(30031), nolabel=local_string(30032), yeslabel=local_string(30067))  # Fresh Start?
	    if yesFresh:
	    	fresh_start()
	    build_install(name, name2, version, url)
	else:
		return

def build_install(name, name2, version, url):
	if os.path.exists(zippath):
		os.unlink(zippath)
	d = Downloader(url)
	if 'dropbox' in url:
		if not xbmc.getCondVisibility('System.HasAddon(script.module.requests)'):
			xbmc.executebuiltin('InstallAddon(script.module.requests)')
			dialog.ok(name, local_string(30033))  # Installing Requests
			return
		d.download_build(name, zippath, meth='requests')
	else:
		d.download_build(name, zippath, meth='urllib')
	if os.path.exists(zippath):
		dp.create(addon_name, local_string(30034))  # Extracting files
		dp.update(66, local_string(30034))
		zf = ZipFile(zippath)
		zf.extractall(path = home)
		dp.update(100, local_string(30035))  # Done Extracting
		zf.close()
		os.unlink(zippath)
		save_restore()
		setting_set('buildname', name2)
		setting_set('buildversion', version)
		setting_set('firstrun', 'true')
		dialog.ok(addon_name, local_string(30036))  # Install Complete
		os._exit(1)
	else:
		return