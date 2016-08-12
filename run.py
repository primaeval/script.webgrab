from subprocess import call
import xbmcaddon,xbmcgui

dialog = xbmcgui.Dialog()


ADDON = xbmcaddon.Addon(id='script.webgrab')
try: LIBRE = xbmcaddon.Addon(id='service.webgrabplus')
except: LIBRE = ''
exe = ADDON.getSetting('exe')
path = ADDON.getSetting('config_output_folder')
dialog.notification("Webgrab+Plus Configurator","Starting")
if LIBRE:
    status = call([exe])
else:
    status = call([exe,path])
if status != 0:
    message = "Error %s" % status
else:
    message ="Finished"
dialog.notification("Webgrab+Plus Configurator",message)

