import os
import shutil
import sqlite3
import xbmc
import xbmcgui
from .skinSwitch import swapSkins
from .save_data import save_backup, save_restore
from .utils import log
from .addonvar import currSkin, user_path, thumbs_f, db_path, addon_name, textures_db, advancedsettings_folder, advancedsettings_xml, dialog, dp, xbmcPath, EXCLUDES, packages, setting_set, addon_icon, local_string, current_build, setting


def purge_db(db):
	if os.path.exists(db):
		try:
			conn = sqlite3.connect(db)
			cur = conn.cursor()
		except Exception as e:
			xbmc.log("DB Connection Error: %s" % str(e), xbmc.LOGDEBUG)
			return False
	else: 
		xbmc.log('%s not found.' % db, xbmc.LOGINFO)
		return False
	cur.execute("SELECT name FROM sqlite_master WHERE type = 'table'")
	for table in cur.fetchall():
		if table[0] == 'version': 
			xbmc.log('Data from table `%s` skipped.' % table[0], xbmc.LOGDEBUG)
		else:
			try:
				cur.execute("DELETE FROM %s" % table[0])
				conn.commit()
				xbmc.log('Data from table `%s` cleared.' % table[0], xbmc.LOGDEBUG)
			except Exception as e:
				xbmc.log("DB Remove Table `%s` Error: %s" % (table[0], str(e)), xbmc.LOGERROR)
	conn.close()
	xbmc.log('%s DB Purging Complete.' % db, xbmc.LOGINFO)

def clear_thumbnails():
	try:
		if os.path.exists(os.path.join(user_path, 'Thumbnails')):
			shutil.rmtree(os.path.join(user_path, 'Thumbnails'))
	except Exception as e:
    		xbmc.log('Failed to delete %s. Reason: %s' % (os.path.join(user_path, 'Thumbnails'), e), xbmc.LOGINFO)
    		return
	try:
		if os.path.exists(os.path.join(db_path, 'Textures13.db')):
			os.unlink(os.path.join(db_path, 'Textures13.db'))
	except:
		purge_db(textures_db)
	create_ThumbsFolder()
	xbmc.sleep(7000)
	xbmcgui.Dialog().notification(addon_name, local_string(30037), addon_icon, 5000)  # Thumbnails Folder Created
	os._exit(1)
	
def create_ThumbsFolder():
		if not os.path.exists(thumbs_f):
				os.makedirs(os.path.join(thumbs_f, '0'))
		if not os.path.exists('1'):
				os.makedirs(os.path.join(thumbs_f, '1'))
		if not os.path.exists('2'):
				os.makedirs(os.path.join(thumbs_f, '2'))
		if not os.path.exists('3'):
				os.makedirs(os.path.join(thumbs_f, '3'))
		if not os.path.exists('4'):
				os.makedirs(os.path.join(thumbs_f, '4'))
		if not os.path.exists('5'):
				os.makedirs(os.path.join(thumbs_f, '5'))
		if not os.path.exists('6'):
				os.makedirs(os.path.join(thumbs_f, '6'))
		if not os.path.exists('7'):
				os.makedirs(os.path.join(thumbs_f, '7'))
		if not os.path.exists('8'):
				os.makedirs(os.path.join(thumbs_f, '8'))
		if not os.path.exists('9'):
				os.makedirs(os.path.join(thumbs_f, '9'))
		if not os.path.exists('a'):
				os.makedirs(os.path.join(thumbs_f, 'a'))
		if not os.path.exists('b'):
				os.makedirs(os.path.join(thumbs_f, 'b'))
		if not os.path.exists('c'):
				os.makedirs(os.path.join(thumbs_f, 'c'))
		if not os.path.exists('d'):
				os.makedirs(os.path.join(thumbs_f, 'd'))
		if not os.path.exists('e'):
				os.makedirs(os.path.join(thumbs_f, 'e'))
		if not os.path.exists('f'):
				os.makedirs(os.path.join(thumbs_f, 'f'))
		if not os.path.exists('Video'):
				os.makedirs(os.path.join(thumbs_f, 'Video'))
		xbmc.sleep(1000)
		xbmcgui.Dialog().notification(addon_name, 'Eliminadas imágenes y creada carpeta Thumbsnail', addon_icon, 5000)  # Thumbnails Folder Created

def advanced_settings():
	selection = xbmcgui.Dialog().select(local_string(30038), ['1GB (Firestick Lite, MiTV, Agile TV,...)','2GB (Firestick 4K, MiBox, KM7, KM2,...)','3GB o más (nVidia Shield Pro, Mecool KM9, KM3, KM1, KM6,...)','+4GB (Mini PC, Rpi 4b, PC,...)','ROM (Usa el almacenamiento libre del dispositivo)',local_string(30039)])  # Select Ram Size, Delete
	if selection==0:
		xml = os.path.join(advancedsettings_folder, 'less1.xml')
	elif selection==1:
		xml = os.path.join(advancedsettings_folder, '1plus.xml')
	elif selection==2:
		xml = os.path.join(advancedsettings_folder, 'firetv.xml')
	elif selection==3:
		xml = os.path.join(advancedsettings_folder, '2plus.xml')
	elif selection==4:
		xml = os.path.join(advancedsettings_folder,'shield.xml')
	elif selection==5:
		if os.path.exists(advancedsettings_xml):
			os.unlink(advancedsettings_xml)
		xbmc.sleep(1000)
		dialog.ok(addon_name, local_string(30040))  # Advanced Settings Deleted
		os._exit(1)
	else:
		return
	if os.path.exists(advancedsettings_xml):
		os.unlink(advancedsettings_xml)
	shutil.copyfile(xml, advancedsettings_xml)
	xbmc.sleep(1000)
	dialog.ok(addon_name, local_string(30041))  # Advanced Settings Set
	os._exit(1)

def fresh_start(standalone=False):
	yesFresh = dialog.yesno(local_string(30012), local_string(30042), nolabel=local_string(30032), yeslabel=local_string(30067))  # Are you sure?
	if yesFresh:
		if not currSkin() in ['skin.estuary']:
			swapSkins('skin.estuary')
			x = 0
			xbmc.sleep(100)
			while not xbmc.getCondVisibility("Window.isVisible(yesnodialog)") and x < 150:
				x += 1
				xbmc.sleep(100)
				xbmc.executebuiltin('SendAction(Select)')
			if xbmc.getCondVisibility("Window.isVisible(yesnodialog)"):
				xbmc.executebuiltin('SendClick(11)')
			else: 
				xbmc.log('Fresh Install: Skin Swap Timed Out!', xbmc.LOGINFO)
				return False
			xbmc.sleep(100)
		if not currSkin() in ['skin.estuary']:
			xbmc.log('Fresh Install: Skin Swap failed.', xbmc.LOGINFO)
			return
		if standalone is True:
			save_backup()
			
		dp.create(addon_name, local_string(30043))  # Deleting files and folders...
		xbmc.sleep(100)
		dp.update(30, local_string(30043))
		xbmc.sleep(100)
		for root, dirs, files in os.walk(xbmcPath, topdown=True):
			dirs[:] = [d for d in dirs if d not in EXCLUDES]
			for name in files:
				if name not in EXCLUDES:
					log('name', name)
					try:
						os.remove(os.path.join(root, name))
					except:
						xbmc.log('Unable to delete ' + name, xbmc.LOGINFO)
		dp.update(60, local_string(30043))
		xbmc.sleep(100)	
		for root, dirs, files in os.walk(xbmcPath,topdown=True):
			dirs[:] = [d for d in dirs if d not in EXCLUDES]
			for name in dirs:
				if name not in ['addons', 'userdata', 'Database', 'addon_data', 'backups', 'temp']:
					try:
						shutil.rmtree(os.path.join(root,name),ignore_errors=True, onerror=None)
					except:
						xbmc.log('Unable to delete ' + name, xbmc.LOGINFO)
		dp.update(60, local_string(30043))
		xbmc.sleep(100)
		if not os.path.exists(packages):
			os.mkdir(packages)
		dp.update(100, local_string(30044))  # Done Deleting Files
		xbmc.sleep(1000)
		if standalone is True:
			save_restore()
			setting_set('firstrun', 'true')
			setting_set('buildname', 'No Build Installed')
			setting_set('buildversion', '0')
			dialog.ok(addon_name, local_string(30045))  # Fresh Start Complete
			os._exit(1)
	else:
		return

def clear_packages():
    file_count = len([name for name in os.listdir(packages)])
    for filename in os.listdir(packages):
    	file_path = os.path.join(packages, filename)
    	try:
    	       if os.path.isfile(file_path) or os.path.islink(file_path):
    	       	os.unlink(file_path)
    	       elif os.path.isdir(file_path):
    	       	shutil.rmtree(file_path)
    	except Exception as e:
    		xbmc.log('Failed to delete %s. Reason: %s' % (file_path, e), xbmc.LOGINFO)
    xbmcgui.Dialog().notification(addon_name, str(file_count)+' ' + local_string(30046), addon_icon, 5000, sound=False)  # Packages Cleared