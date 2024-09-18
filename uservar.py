import xbmcaddon
addon_id = xbmcaddon.Addon().getAddonInfo('id')

'''#####-----Build File-----#####'''
buildfile = 'https://raw.githubusercontent.com/taoxtrece/plugin.program.taoxwizard19/main/builds.json'

'''#####-----Excludes-----#####'''
excludes  = [addon_id, 'packages', 'Addons33.db', 'kodi.log', 'script.module.certifi', 'script.module.chardet', 'script.module.idna', 'script.module.requests', 'script.module.urllib3', 'backups']