from subprocess import call
from xbmcswift2 import Plugin
import StringIO
import os
import re
import requests
import sys
import xbmc,xbmcaddon,xbmcvfs,xbmcgui,xbmcplugin
import zipfile
import operator

plugin = Plugin()

def log(v):
    xbmc.log(repr(v))


def get_icon_path(icon_name):
    addon_path = xbmcaddon.Addon().getAddonInfo("path")
    return os.path.join(addon_path, 'resources', 'img', icon_name+".png")

def remove_formatting(label):
    label = re.sub(r"\[/?[BI]\]",'',label)
    label = re.sub(r"\[/?COLOR.*?\]",'',label)
    return label

@plugin.route('/download_ini_pack')
def download_ini_pack():
    folder = 'special://profile/addon_data/script.webgrab/webgrab'
    file = 'special://profile/addon_data/script.webgrab/SiteIniPack_current.zip'
    xbmcvfs.mkdirs(folder)
    url = 'http://www.webgrabplus.com/sites/default/files/download/ini/SiteIniPack_current.zip'
    r = requests.get(url,stream=True)
    f = xbmcvfs.File(file, 'wb')
    chunk_size = 1024
    for chunk in r.iter_content(chunk_size):
        f.write(chunk)
    f.close()
    try:
        zip = zipfile.ZipFile(xbmc.translatePath(file))
        z = zip.extractall(xbmc.translatePath(folder))
    except:
        return

@plugin.route('/toggle/<country>/<site>/<site_id>/<xmltv_id>/<name>')
def toggle(country,site,site_id,xmltv_id,name):
    channels = plugin.get_storage('channels')
    id = "%s|%s|%s|%s|%s" % (country,name,site,site_id,xmltv_id)
    if id in channels:
        del(channels[id])
    else:
        channels[id] = -1
    xbmc.executebuiltin('Container.Refresh')

@plugin.route('/provider/<country>/<provider>')
def provider(country,provider):
    channels = plugin.get_storage('channels')
    folder = 'special://profile/addon_data/script.webgrab/webgrab/siteini.pack/%s' % country
    channel_file = "%s/%s.channels.xml" % (folder,provider)
    items = []
    f = xbmcvfs.File(channel_file,"rb")
    data = f.read()
    match = re.findall(r'<channel update="i" site="(.*?)" site_id="(.*?)" xmltv_id="(.*?)">(.*?)</channel>',data)
    for (site,site_id,xmltv_id,name) in match:
        id = "%s|%s|%s|%s|%s" % (country,name,site,site_id,xmltv_id)
        if id in channels:
            label = "[COLOR yellow]%s[/COLOR]" % name
        else:
            label = name
        items.append(
        {
            'label': label,
            'path': plugin.url_for('toggle',country=country,site=site,site_id=site_id,xmltv_id=xmltv_id,name=name),
            'thumbnail':get_icon_path('settings'),
        })
    sorted_items = sorted(items, key=lambda item: remove_formatting(item['label']))
    return sorted_items

@plugin.route('/country/<country>')
def country(country):
    this_country = country
    channels = plugin.get_storage('channels')
    sites = {}
    for c in channels:
        (country,name,site,site_id,xmltv_id) = c.split("|")
        sites[site] = site
    folder = 'special://profile/addon_data/script.webgrab/webgrab/siteini.pack/%s' % this_country
    items = []
    dirs, files = xbmcvfs.listdir(folder)
    files = [f for f in files if f.endswith('channels.xml')]
    for f in sorted(files):
        provider = f[:-13]
        if provider in sites:
            label = "[COLOR yellow]%s[/COLOR]" % provider
        else:
            label = provider
        items.append(
        {
            'label': label,
            'path': plugin.url_for('provider', country=this_country, provider=provider),
            'thumbnail':get_icon_path('settings'),
        })
    return items

@plugin.route('/countries')
def countries():
    channels = plugin.get_storage('channels')
    countries = {}
    for c in channels:
        (country,name,site,site_id,xmltv_id) = c.split("|")
        countries[country] = country
    folder = 'special://profile/addon_data/script.webgrab/webgrab/siteini.pack'
    items = []
    dirs, files = xbmcvfs.listdir(folder)
    for dir in dirs:
        if dir in countries:
            label = "[COLOR yellow]%s[/COLOR]" % dir
        else:
            label = dir
        items.append(
        {
            'label': label,
            'path': plugin.url_for('country', country=dir),
            'thumbnail':get_icon_path('settings'),
        })
    sorted_items = sorted(items, key=lambda item: remove_formatting(item['label']))
    return items

@plugin.route('/rename_id/<id>')
def rename_id(id):
    channels = plugin.get_storage('channels')
    channel = channels[id]
    (country,name,site,site_id,xmltv_id) = id.split("|")
    dialog = xbmcgui.Dialog()
    xmltv_id = dialog.input('New xmltv id', xmltv_id, type=xbmcgui.INPUT_ALPHANUM)
    if xmltv_id:
        del(channels[id])
        id = "%s|%s|%s|%s|%s" % (country,name,site,site_id,xmltv_id)
        channels[id] = channel
        xbmc.executebuiltin('Container.Refresh')

@plugin.route('/rename_channel/<id>')
def rename_channel(id):
    channels = plugin.get_storage('channels')
    channel = channels[id]
    (country,name,site,site_id,xmltv_id) = id.split("|")
    dialog = xbmcgui.Dialog()
    name = dialog.input('New Channel Name', name, type=xbmcgui.INPUT_ALPHANUM)
    if name:
        del(channels[id])
        id = "%s|%s|%s|%s|%s" % (country,name,site,site_id,xmltv_id)
        channels[id] = channel
        xbmc.executebuiltin('Container.Refresh')

@plugin.route('/sort_channels')
def sort_channels():
    dialog = xbmcgui.Dialog()
    how = ['Country','Name','Provider','site id','xmltv id']
    index = dialog.select('New xmltv id', how)
    if index == -1:
        return
    channels = plugin.get_storage('channels')
    channel_list = []
    for c in channels:
        order = channels[c]
        (country,name,site,site_id,xmltv_id) = c.split("|")
        channel_list.append((country,name,site,site_id,xmltv_id,order))
    sorted_channels = sorted(channel_list, key=lambda c: c[index]) #TODO how
    i = 0
    for (country,name,site,site_id,xmltv_id,order) in sorted_channels:
        id = "%s|%s|%s|%s|%s" % (country,name,site,site_id,xmltv_id)
        channels[id] = i
        i = i + 1
    xbmc.executebuiltin('Container.Refresh')

@plugin.route('/move_channel/<id>')
def move_channel(id):
    channels = plugin.get_storage('channels')
    channel_list = []
    for c in channels:
        order = channels[c]
        (country,name,site,site_id,xmltv_id) = c.split("|")
        channel_list.append((country,name,site,site_id,xmltv_id,order))
    sorted_channels = sorted(channel_list, key=lambda c: c[5])
    sorted_channels_names = ["%s - [COLOR yellow]%s[/COLOR] - %s (%s) [%s]" % (c[0],c[1],c[2],c[3],c[4]) for c in sorted_channels]
    length = len(sorted_channels_names)
    dialog = xbmcgui.Dialog()

    index = dialog.select('Move Before?', sorted_channels_names)
    if index == -1:
        return

    this_channel = channels[id]
    order = channels[id]
    (country,name,site,site_id,xmltv_id) = id.split("|")
    oldindex = sorted_channels.index((country,name,site,site_id,xmltv_id,order))
    sorted_channels.insert(index, sorted_channels.pop(oldindex))
    channels.clear()

    i = 0
    for (country,name,site,site_id,xmltv_id,order) in sorted_channels:
        id = "%s|%s|%s|%s|%s" % (country,name,site,site_id,xmltv_id)
        channels[id] = i
        i = i + 1

    xbmc.executebuiltin('Container.Refresh')

@plugin.route('/channels')
def channels():
    channels = plugin.get_storage('channels')
    items = []
    sorted_ids = sorted(channels.items(), key=operator.itemgetter(1))
    for (id,order) in sorted_ids:
        (country,name,site,site_id,xmltv_id) = id.split("|")
        label = "%s - [COLOR yellow]%s[/COLOR] - %s (%s) [%s]" % (country,name,site,site_id,xmltv_id)
        context_items = []
        context_items.append(('Move', 'XBMC.RunPlugin(%s)' % (plugin.url_for('move_channel', id=id))))
        context_items.append(('Rename Channel', 'XBMC.RunPlugin(%s)' % (plugin.url_for('rename_channel', id=id))))
        context_items.append(('Rename xmltv id', 'XBMC.RunPlugin(%s)' % (plugin.url_for('rename_id', id=id))))
        context_items.append(('Sort', 'XBMC.RunPlugin(%s)' % (plugin.url_for('sort_channels'))))
        items.append(
        {
            'label': label,
            'path': plugin.url_for('toggle',country=country,site=site,site_id=site_id,xmltv_id=xmltv_id,name=name),
            'thumbnail':get_icon_path('settings'),
            'context_menu': context_items,
        })
    return items

@plugin.route('/write_config')
def write_config():
    folder = 'special://profile/addon_data/script.webgrab/webgrab/config'
    file = '%s/%s' % (folder,'WebGrab++.config.xml')
    xbmcvfs.mkdirs(folder)
    f = xbmcvfs.File(file, 'wb')
    channels = plugin.get_storage('channels')
    f.write('<settings>\n')
    xmltv_output_folder = plugin.get_setting('xmltv_output_folder')
    xmltv_name = plugin.get_setting('xmltv_name')
    if not xmltv_name:
        xmltv_name = "xmltv.xml"
    if xmltv_output_folder:
        xmltv = "%s%s" % (xmltv_output_folder,xmltv_name)
    else:
        xmltv = 'special://profile/addon_data/script.webgrab/webgrab/%s' % xmltv_name
    f.write('<filename>%s</filename>\n' % xbmc.translatePath(xmltv))
    sorted_ids = sorted(channels.items(), key=operator.itemgetter(1))
    for (id,order) in sorted_ids:
        (country,name,site,site_id,xmltv_id) = id.split("|")
        xml = '<channel update="i" site="%s" site_id="%s" xmltv_id="%s">%s</channel>' % (site,site_id,xmltv_id,name)
        str = "%s\n" % xml
        f.write(str)
    f.write('</settings>\n')
    f.close()
    inis = {}
    for c in channels:
        (country,name,site,site_id,xmltv_id) = c.split("|")
        inis[site] = country #TODO deal with duplicates
    for ini in inis:
        country = inis[ini]
        src = 'special://profile/addon_data/script.webgrab/webgrab/siteini.pack/%s/%s.ini' % (country,ini)
        dst = 'special://profile/addon_data/script.webgrab/webgrab/config/%s.ini' % ini
        xbmcvfs.copy(src,dst)

@plugin.route('/run_webgrab')
def run_webgrab():
    exe = plugin.get_setting('exe')
    path = xbmc.translatePath('special://profile/addon_data/script.webgrab/webgrab/config')
    status = call([exe,path],shell=False)
    return

@plugin.route('/copy_config')
def copy_config():
    output_folder = plugin.get_setting('config_output_folder')
    input_folder = 'special://profile/addon_data/script.webgrab/webgrab/config/'
    if output_folder:
        dirs, files = xbmcvfs.listdir(input_folder)
        for f in files:
            input = "%s%s" % (input_folder,f)
            output = "%s%s" % (output_folder,f)
            xbmcvfs.copy(input,output)



@plugin.route('/')
def index():
    items = []
    items.append(
    {
        'label': 'Download Site Pack',
        'path': plugin.url_for('download_ini_pack'),
        'thumbnail':get_icon_path('settings'),
    })
    items.append(
    {
        'label': 'Countries',
        'path': plugin.url_for('countries'),
        'thumbnail':get_icon_path('settings'),
    })
    items.append(
    {
        'label': 'Channels',
        'path': plugin.url_for('channels'),
        'thumbnail':get_icon_path('settings'),
    })
    items.append(
    {
        'label': 'Write Config File',
        'path': plugin.url_for('write_config'),
        'thumbnail':get_icon_path('settings'),
    })
    items.append(
    {
        'label': 'Run Webgrab',
        'path': plugin.url_for('run_webgrab'),
        'thumbnail':get_icon_path('settings'),
    })
    items.append(
    {
        'label': 'Copy Config to Output Folder',
        'path': plugin.url_for('copy_config'),
        'thumbnail':get_icon_path('settings'),
    })
    return items


if __name__ == '__main__':
    plugin.run()
