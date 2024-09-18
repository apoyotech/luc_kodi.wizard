import xbmc
import xbmcplugin
import xbmcaddon
import sys
import os
from .params import Params
from .utils import play_video
from .menus import main_menu, build_menu, submenu_maintenance, authorize_menu, backup_restore
from .build_install import main
from .maintenance import fresh_start, clear_packages, clear_thumbnails, advanced_settings
from .whitelist import get_whitelist
from .addonvar import addon
from .backup_restore import backup_build, restore_menu, restore_build, get_backup_folder, reset_backup_folder

handle = int(sys.argv[1])

def router(paramstring):
    p = Params(paramstring)
    xbmc.log(str(p.get_params()),xbmc.LOGDEBUG)
    
    name = p.get_name()
    name2 = p.get_name2()
    version = p.get_version()
    url = p.get_url()
    mode = p.get_mode()
    icon = p.get_icon()
    fanart = p.get_fanart()
    description = p.get_description()
    
    xbmcplugin.setContent(handle, 'files')

    if mode is None:
    	main_menu()
    
    elif mode == 1:
    	build_menu()
    
    elif mode == 2:
    	play_video(name, url, icon, description)
    
    elif mode == 3:
    	main(name, name2, version, url)
    
    elif mode == 4:
    	fresh_start(standalone=True)
    
    elif mode == 5:
    	submenu_maintenance()
    
    elif mode == 6:
    	clear_packages()
    
    elif mode == 7:
    	clear_thumbnails()
    
    elif mode == 8:
    	advanced_settings()
    
    elif mode == 9:
    	addon.openSettings()
    
    elif mode == 10:
    	authorize_menu()
    
    elif mode == 11:
    	get_whitelist()
    
    elif mode == 12:
    	backup_restore()
    
    elif mode == 13:
    	backup_build()
    
    elif mode == 14:
    	restore_menu()
    
    elif mode == 15:
    	restore_build(url)
    
    elif mode == 16:
    	get_backup_folder()
    
    elif mode == 17:
    	reset_backup_folder()
    
    elif mode == 18:
    	os._exit(1)
		
    xbmcplugin.endOfDirectory(handle)