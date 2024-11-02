import xbmcaddon
import os

ADDON_ID = xbmcaddon.Addon().getAddonInfo('id')
PATH = xbmcaddon.Addon().getAddonInfo('path')
ART = os.path.join(PATH, 'resources', 'media')
autointall='Yes'
buildfile ='https://raw.githubusercontent.com/apoyotech/luc_kodi.wizard/refs/heads/main/resources/texts/builds.xml'
notify_url  = 'http://'
excludes  = [addon_id, 'plugin.program.luc_kodi.wizard']
