import sys
import json
import xbmc
import xbmcplugin
from .utils import add_dir
from .parser import Parser
from .dropbox import DownloadFile
from uservar import buildfile
from .addonvar import addon_icon, addon_fanart, local_string, build_file

handle = int(sys.argv[1])

def main_menu():
	xbmcplugin.setPluginCategory(handle, 'Main Menu')
	
	add_dir(local_string(30010),'',1,addon_icon,addon_fanart,local_string(30001),isFolder=True)  # Build Menu
	
	add_dir(local_string(30011),'',5,addon_icon,addon_fanart,local_string(30002),isFolder=True)  # Maintenance
	
	add_dir(local_string(30015),'',9,addon_icon,addon_fanart,local_string(30016),isFolder=False)  # Settings

def build_menu():
    xbmc.executebuiltin('Dialog.Close(busydialog)')
    xbmcplugin.setPluginCategory(handle, local_string(30010))
    if buildfile.startswith('https://github.com/taoxtrece/plugin.program.taoxwizard19/releases/download/build/solovod19.zip'):
    	DownloadFile(buildfile, build_file)
    	try:
    		builds = json.load(open(build_file,'r')).get('builds')
    	except:
    		xml = Parser(build_file)
    		builds = json.loads(xml.get_list2())['builds']
    elif not buildfile.endswith('.xml') and not buildfile.endswith('.json'):
    	add_dir(local_string(30017),'','',addon_icon,addon_fanart,local_string(30017),isFolder=False)  # Invalid Build URL
    	return
    else:
    	p = Parser(buildfile)
    	builds = json.loads(p.get_list())['builds']
    
    for build in builds:
    	name = (build.get('name', local_string(30018)))  # Unknown Name
    	version = (build.get('version', '0.0'))
    	url = (build.get('url', ''))
    	icon = (build.get('icon', addon_icon))
    	fanart = (build.get('fanart', addon_fanart))
    	description = (build.get('description', local_string(30019)))  # No Description Available.
    	preview = (build.get('preview',None))
    	
    	if url.endswith('.xml') or url.endswith('.json'):
    		add_dir(name,url,1,icon,fanart,description,name2=name,version=version,isFolder=True)
    	add_dir(name + ' ' + local_string(30020) + ' ' + version,url,3,icon,fanart,description,name2=name,version=version,isFolder=False)  # Version
    	if preview is not None:
    		add_dir(local_string(30021) + ' ' + name + ' ' + local_string(30020) + ' ' + version,preview,2,icon,fanart,description,name2=name,version=version,isFolder=False)  # Video Preview

def submenu_maintenance():
	xbmcplugin.setPluginCategory(handle, local_string(30022))  # Maintenance
	add_dir(local_string(30023),'',6,addon_icon,addon_fanart,local_string(30005),isFolder=False)  # Clear Packages
	add_dir(local_string(30024),'',7,addon_icon,addon_fanart,local_string(30008),isFolder=False)  # Clear Thumbnails
	add_dir(local_string(30025),'',8,addon_icon,addon_fanart,local_string(30009),isFolder=False)  # Advanced Settings
	add_dir(local_string(30064),'',11,addon_icon,addon_fanart,local_string(30064), isFolder=False)  # Edit Whitelist
	add_dir('Backup/Restaurar','',12,addon_icon,addon_fanart,'Backup and Restore')  # Backup Build
	add_dir('Forzar Cierre','', 18, addon_icon,addon_fanart,'Force Close Kodi')

def backup_restore():
	add_dir('Backup Build','',13,addon_icon,addon_fanart,'Backup Build', isFolder=False)  # Backup Build
	add_dir('Restaurar Backup','',14, addon_icon,addon_fanart,'Restore Backup')  # Restore Backup
	add_dir('Cambiar localización del backup','',16,addon_icon,addon_fanart,'Change the location where backups will be stored and accessed.', isFolder=False)  # Backup Location
	add_dir('Resetear la localización del backup','',17,addon_icon,addon_fanart,'Set the backup location to its default.', isFolder=False)  # Reset Backup Location

def authorize_menu():
    xbmcplugin.setPluginCategory(handle, local_string(30027))  # Authorize Services
    p = Parser(authorize)
    builds = json.loads(p.get_list())['items']
    for build in builds:
    	name = (build.get('name', 'Unknown'))
    	url = (build.get('url', ''))
    	icon = (build.get('icon', addon_icon))
    	fanart = (build.get('fanart', addon_fanart))
    	add_dir(name,url,2,icon,fanart,name,name2=name,version='' ,isFolder=False)