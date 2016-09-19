from subprocess import Popen
from xbmcswift2 import Plugin
import StringIO
import os
import re
import requests
import sys
import xbmc,xbmcaddon,xbmcvfs,xbmcgui,xbmcplugin
import zipfile
import operator
import HTMLParser

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

@plugin.route('/toggle_hide/<country>/<site>/<site_id>/<xmltv_id>/<name>')
def toggle_hide(country,site,site_id,xmltv_id,name):
    channels = plugin.get_storage('hidden_channels')
    id = "%s|%s|%s|%s|%s" % (country,name,site,site_id,xmltv_id)
    if id in channels:
        del(channels[id])
    else:
        channels[id] = -1
    xbmc.executebuiltin('Container.Refresh')

@plugin.route('/toggle/<country>/<site>/<site_id>/<xmltv_id>/<name>')
def toggle(country,site,site_id,xmltv_id,name):
    channels = plugin.get_storage('channels')
    id = "%s|%s|%s|%s|%s" % (country,name,site,site_id,xmltv_id)
    if id in channels:
        del(channels[id])
    else:
        channels[id] = -1
    xbmc.executebuiltin('Container.Refresh')

@plugin.route('/edit_timezone/<country>/<site>')
def edit_timezone(country,site):
    ini_name = 'special://profile/addon_data/script.webgrab/webgrab/siteini.pack/%s/%s.ini' % (country,site)
    setting = '%s.timezone' % site
    site_offset = plugin.get_setting(setting)
    f = xbmcvfs.File(ini_name,"rb")
    data = f.read()
    f.close()
    match = re.search(r'timezone=(.*?)\|',data)
    default_utc_offset = match.group(1)
    utc_offset = site_offset or default_utc_offset
    dialog = xbmcgui.Dialog()
    utc_offset = dialog.input('Enter UTC Offset (cancel to reset)', utc_offset)
    if not utc_offset:
        plugin.set_setting(setting, default_utc_offset)
    else:
        plugin.set_setting(setting, utc_offset)


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

@plugin.route('/quick_add/<country>/<provider>')
def quick_add(country,provider):
    channels = plugin.get_storage('channels')
    folder = 'special://profile/addon_data/script.webgrab/webgrab/siteini.pack/%s' % country
    channel_file = "%s/%s.channels.xml" % (folder,provider)
    items = []
    f = xbmcvfs.File(channel_file,"rb")
    data = f.read()
    match = re.findall(r'<channel update="i" site="(.*?)" site_id="(.*?)" xmltv_id="(.*?)">(.*?)</channel>',data)

    ids = []
    for (site,site_id,xmltv_id,name) in match:
        id = "%s|%s|%s|%s|%s" % (country,name,site,site_id,xmltv_id)
        ids.append((country,name,site,site_id,xmltv_id))

    ids = sorted(ids, key=lambda c: c[1])
    names = []
    for (country,name,site,site_id,xmltv_id) in ids:
        id = "%s|%s|%s|%s|%s" % (country,name,site,site_id,xmltv_id)
        if id in channels:
            label = "[COLOR yellow]%s[/COLOR]" % name
        else:
            label = name
        names.append(label)
    dialog = xbmcgui.Dialog()
    index = dialog.multiselect('Add to Channels', names)
    if not index:
        return
    if index == -1:
        return
    for i in index:
        (country,name,site,site_id,xmltv_id) = ids[i]
        id = "%s|%s|%s|%s|%s" % (country,name,site,site_id,xmltv_id)
        channels[id] = -1

@plugin.route('/quick_remove/<country>/<provider>')
def quick_remove(country,provider):
    channels = plugin.get_storage('channels')
    folder = 'special://profile/addon_data/script.webgrab/webgrab/siteini.pack/%s' % country
    channel_file = "%s/%s.channels.xml" % (folder,provider)
    items = []
    f = xbmcvfs.File(channel_file,"rb")
    data = f.read()
    match = re.findall(r'<channel update="i" site="(.*?)" site_id="(.*?)" xmltv_id="(.*?)">(.*?)</channel>',data)

    ids = []
    for (site,site_id,xmltv_id,name) in match:
        id = "%s|%s|%s|%s|%s" % (country,name,site,site_id,xmltv_id)
        if id in channels:
            ids.append((country,name,site,site_id,xmltv_id))

    ids = sorted(ids, key=lambda c: c[1])
    names = [i[1] for i in ids]
    dialog = xbmcgui.Dialog()
    index = dialog.multiselect('Add to Channels', names)
    if not index:
        return
    if index == -1:
        return
    for i in index:
        (country,name,site,site_id,xmltv_id) = ids[i]
        id = "%s|%s|%s|%s|%s" % (country,name,site,site_id,xmltv_id)
        del(channels[id])


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
        context_items = []
        context_items.append(('Timezone Edit', 'XBMC.RunPlugin(%s)' % (plugin.url_for('edit_timezone',country=this_country,site=provider))))
        context_items.append(('Quick Add Channels', 'XBMC.RunPlugin(%s)' % (plugin.url_for('quick_add',country=this_country,provider=provider))))
        context_items.append(('Quick Remove Channels', 'XBMC.RunPlugin(%s)' % (plugin.url_for('quick_remove',country=this_country,provider=provider))))
        items.append(
        {
            'label': label,
            'path': plugin.url_for('provider', country=this_country, provider=provider),
            'thumbnail':get_icon_path('settings'),
            'context_menu': context_items,
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
    return sorted_items

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
    second_index = 1
    if index == 1:
        second_index = 0
    sorted_channels = sorted(channel_list, key=lambda c: (c[index],c[second_index]))
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
    if oldindex < index:
        index = index - 1
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
    hidden_channels = plugin.get_storage('hidden_channels')
    items = []
    sorted_ids = sorted(channels.items(), key=operator.itemgetter(1))
    for (id,order) in sorted_ids:
        (country,name,site,site_id,xmltv_id) = id.split("|")
        if id in hidden_channels:
            label = "%s - [COLOR grey]%s[/COLOR] - %s (%s) [%s]" % (country,name,site,site_id,xmltv_id)
        else:
            label = "%s - [COLOR yellow]%s[/COLOR] - %s (%s) [%s]" % (country,name,site,site_id,xmltv_id)
        context_items = []
        context_items.append(('Sort Channels', 'XBMC.RunPlugin(%s)' % (plugin.url_for('sort_channels'))))
        context_items.append(('Move Channel', 'XBMC.RunPlugin(%s)' % (plugin.url_for('move_channel', id=id))))
        context_items.append(('Rename Channel', 'XBMC.RunPlugin(%s)' % (plugin.url_for('rename_channel', id=id))))
        context_items.append(('Rename xmltv id', 'XBMC.RunPlugin(%s)' % (plugin.url_for('rename_id', id=id))))
        context_items.append(('Delete Channel', 'XBMC.RunPlugin(%s)' % (plugin.url_for('toggle',country=country,site=site,site_id=site_id,xmltv_id=xmltv_id,name=name))))
        items.append(
        {
            'label': label,
            'path': plugin.url_for('toggle_hide',country=country,site=site,site_id=site_id,xmltv_id=xmltv_id,name=name),
            'thumbnail':get_icon_path('settings'),
            'context_menu': context_items,
        })
    return items

@plugin.route('/write_and_copy_config')
def write_and_copy_config():
    write_config()
    copy_config()

@plugin.route('/write_config')
def write_config():
    folder = 'special://profile/addon_data/script.webgrab/webgrab/config'
    file = '%s/%s' % (folder,'WebGrab++.config.xml')
    xbmcvfs.mkdirs(folder)
    xbmcvfs.copy(file, file+'.last')
    f = xbmcvfs.File(file, 'wb')
    channels = plugin.get_storage('channels')
    hidden_channels = plugin.get_storage('hidden_channels')
    f.write('<settings>\n')
    xmltv_output_folder = plugin.get_setting('xmltv_output_folder')
    xmltv_name = plugin.get_setting('xmltv_name')
    if not xmltv_name:
        xmltv_name = "xmltv.xml"
    if xmltv_output_folder:
        xmltv = "%s%s" % (xmltv_output_folder,xmltv_name)
    else:
        xmltv = 'special://profile/addon_data/script.webgrab/webgrab/%s' % xmltv_name
    timespan = plugin.get_setting('timespan')
    if not timespan:
        timespan = "1"
    timespan = int(timespan) - 1
    f.write('<timespan>%d</timespan>\n' % timespan)

    update = plugin.get_setting('update')
    if not update:
        update = "0"
    updates = ['','i','l','s','f']
    f.write('<update>%s</update>\n' % updates[int(update)])

    proxy = plugin.get_setting('proxy')
    if proxy:
        proxy_user = plugin.get_setting('proxy_user')
        proxy_password = plugin.get_setting('proxy_password')
        f.write('<proxy password="%s" user="%s">%s</proxy>\n' % (proxy_password,proxy_user,proxy))

    mdb = plugin.get_setting('mdb')
    if mdb == "true":
        mdb_grab = plugin.get_setting('mdb_grab')
        mdb_run = plugin.get_setting('mdb_run')
        f.write('<postprocess run="%s" grab="%s">mdb</postprocess>\n' % (mdb_run,mdb_grab))

    rex = plugin.get_setting('rex')
    if rex == "true":
        rex_grab = plugin.get_setting('rex_grab')
        rex_run = plugin.get_setting('rex_run')
        f.write('<postprocess run="%s" grab="%s">rex</postprocess>\n' % (rex_run,rex_grab))

    user_agent = plugin.get_setting('user_agent')
    if user_agent:
        f.write('<user-agent>%s</user-agent>\n' % (user_agent))


    f.write('<filename>%s</filename>\n' % xbmc.translatePath(xmltv))
    sorted_ids = sorted(channels.items(), key=operator.itemgetter(1))
    for (id,order) in sorted_ids:
        (country,name,site,site_id,xmltv_id) = id.split("|")
        xml = '<channel update="i" site="%s" site_id="%s" xmltv_id="%s">%s</channel>' % (site,site_id,xmltv_id,name)
        str = "%s\n" % xml
        if id not in hidden_channels:
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
        setting = '%s.timezone' % ini
        site_offset = plugin.get_setting(setting)
        if site_offset:
            f = xbmcvfs.File(src,"rb")
            data = f.read()
            f.close()
            data = re.sub(r'timezone=.*?\|','timezone=%s|' % site_offset,data)
            f = xbmcvfs.File(src,"wb")
            f.write(data)
            f.close()
        xbmcvfs.copy(src,dst)

@plugin.route('/run_webgrab')
def run_webgrab():
    xbmc.executebuiltin('XBMC.RunScript(special://home/addons/script.webgrab/run.py)')

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

@plugin.route('/site_ini_version')
def site_ini_version():
    path = 'special://profile/addon_data/script.webgrab/webgrab/siteini.pack'
    dirs, files = xbmcvfs.listdir(path)
    f = [f for f in files if f.startswith('Site')]
    dialog = xbmcgui.Dialog()
    dialog.select('Site Ini Pack Version', f)

@plugin.route('/show_log')
def show_log():
    folder = plugin.get_setting('config_output_folder')
    path = os.path.join(xbmc.translatePath(folder),'WebGrab++.log.txt')
    f = xbmcvfs.File(path,"r")
    data = f.read()
    xbmcgui.Dialog().textviewer(heading="WebGrab++.log.txt",text=data)

@plugin.route('/tv_com')
def tv_com():
    dialog = xbmcgui.Dialog()
    zip_code = plugin.get_setting('tv.com_zipcode') or '10001'
    zip_code = dialog.input('Zip code', zip_code)
    if not zip_code:
        return
    plugin.set_setting('tv.com_zipcode', zip_code)
    utc_offset = plugin.get_setting('tv.com_timezone') or 'UTC-05:00'
    utc_offset = dialog.input('Enter UTC Offset (Cancel for Default UTC)', utc_offset)
    if not utc_offset:
        utc_offset = "UTC"
    plugin.set_setting('tv.com_timezone', utc_offset)
    s = requests.Session()
    r = s.get("http://www.tv.com/listings/")
    csrftoken = r.cookies['csrftoken']
    r = s.get("http://www.tv.com/listings/settings_refresh/%s" % zip_code)
    data = r.content
    match = re.findall(r'<option value=\\"(.*?)\\" data-provider=\\"(.*?)\\" data-provider_type=\\"(.*?)\\">\\r\\n(.*?)\\',data,flags=(re.DOTALL | re.MULTILINE))
    labels = []
    providers = []
    for (id,provider,type,name) in match:
        label = '(%s) %s' % (type,name)
        providers.append((id,provider,type,name,label))
    providers = sorted(providers, key=lambda c: (c[2],c[3]))
    labels = [p[4] for p in providers]
    index = dialog.select('Choose Provider', labels)
    if index == -1:
        return
    headend = providers[index][0]
    data={
        "csrfmiddlewaretoken":csrftoken,
        "zip":zip_code,
        "headend":headend,
        "Submit":"Submitting..."
    }
    r = s.post("http://www.tv.com/listings/",data=data)
    cookies = r.cookies

    f = xbmcvfs.File('special://profile/addon_data/script.webgrab/webgrab/siteini.pack/USA/tv.com.cookies.txt',"wb")
    f.write('# Cookies for domains related to tv.com.\n')
    f.write('# This content may be pasted into a cookies.txt file and used by wget\n')
    f.write('# Example:  wget -x --load-cookies cookies.txt http://www.tv.com/listings/\n')
    f.write('#\n')
    for c in cookies:
        line = "%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (
            c.domain,
            str.upper(str(c.domain_specified)),
            c.path,
            str.upper(str(c.secure)),
            int(c.expires or 0),
            c.name,
            c.value,
        )
        f.write(line)
    f.close()
    xbmcvfs.copy('special://profile/addon_data/script.webgrab/webgrab/siteini.pack/USA/tv.com.cookies.txt',
    'special://profile/addon_data/script.webgrab/webgrab/config/tv.com.cookies.txt')

    data = r.content
    match = re.findall(r'<a href="/listings/station/(.*?)".*?title="(.*?)".*?>(.*?)<',data,flags=(re.DOTALL | re.MULTILINE))
    labels = []
    channels = list(set(match))
    channels = sorted(channels, key=lambda c: (c[1],c[0]))
    channels = [(c[0], re.sub('&','&amp;',c[1]),c[2]) for c in channels]

    f = xbmcvfs.File('special://profile/addon_data/script.webgrab/webgrab/siteini.pack/USA/tv.com.channels.xml',"wb")
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    f.write('<site generator-info-name="WebGrab+Plus/w MDB &amp; REX Postprocess -- version V1.56.6 -- Jan van Straaten" site="tv.com">\n')
    f.write('<channels>\n')
    for c in channels:
        id = c[0]
        station = c[2]
        station =  station
        name = "%s (%s)" % (c[1], c[2])
        xmltv = name
        f.write('<channel update="i" site="tv.com" site_id="%s" xmltv_id="%s">%s</channel>\n' % (id,xmltv,name))
    f.write('</channels>\n')
    f.write('</site>\n')
    f.close()

    f = xbmcvfs.File('special://profile/addon_data/script.webgrab/webgrab/siteini.pack/USA/tv.com.ini',"rb")
    data = f.read()
    f.close()
    data = re.sub(r'timezone=.*?\|','timezone=%s|' % utc_offset,data)
    f = xbmcvfs.File('special://profile/addon_data/script.webgrab/webgrab/siteini.pack/USA/tv.com.ini',"wb")
    f.write(data)
    f.close()

    names = ["%s (%s) [%s]" % (c[1], c[2], c[0])  for c in channels]
    index = dialog.multiselect('Add to Channels', names)
    if not index:
        return
    if index == -1:
        return

    channel_storage = plugin.get_storage('channels')
    for i in index:
        c = channels[i]
        country = "USA"
        name = "%s (%s)" % (c[1],c[2])
        site = "tv.com"
        xmltv_id = name
        site_id = c[0]
        id = "%s|%s|%s|%s|%s" % (country,name,site,site_id,xmltv_id)
        if id in channel_storage:
            pass
        else:
            channel_storage[id] = -1

@plugin.route('/directv_com')
def directv_com():
    dialog = xbmcgui.Dialog()
    zip_code = plugin.get_setting('directv.com_zipcode') or '10001'
    zip_code = dialog.input('Zip code', zip_code)
    if not zip_code:
        return
    plugin.set_setting('directv.com_zipcode', zip_code)
    utc_offset = plugin.get_setting('directv.com_timezone') or 'UTC-05:00'
    utc_offset = dialog.input('Enter UTC Offset (Cancel for Default UTC)', utc_offset)
    if not utc_offset:
        utc_offset = "UTC"
    plugin.set_setting('directv.com_timezone', utc_offset)
    s = requests.Session()
    r = s.get("https://www.directv.com/modal/zipcode")

    r = s.get("https://www.directv.com/json/zipcode/%s" % zip_code)

    cookies = s.cookies
    r = s.get("https://www.directv.com/guide")

    f = xbmcvfs.File('special://profile/addon_data/script.webgrab/webgrab/siteini.pack/Networks/directv.com.cookies.txt',"wb")
    f.write('# Cookies for domains related to directv.com.\n')
    f.write('# This content may be pasted into a cookies.txt file and used by wget\n')
    f.write('# Example:  wget -x --load-cookies cookies.txt http://www.directv.com/guide/\n')
    f.write('#\n')
    for c in cookies:
        line = "%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (
            c.domain,
            str.upper(str(c.domain_specified)),
            c.path,
            str.upper(str(c.secure)),
            int(c.expires or 0),
            c.name,
            c.value,
        )
        f.write(line)
    f.close()
    xbmcvfs.copy('special://profile/addon_data/script.webgrab/webgrab/siteini.pack/Networks/directv.com.cookies.txt',
    'special://profile/addon_data/script.webgrab/webgrab/config/directv.com.cookies.txt')


    data = r.content
    match = re.findall(r'"chName":"(.*?)".*?"chNum":(.*?),.*?"chCall":"(.*?)"',data,flags=(re.DOTALL | re.MULTILINE))
    labels = []
    channels = list(set(match))
    channels = sorted(channels, key=lambda c: (c[0],c[2]))
    channels = [(re.sub('&','&amp;',c[0]),c[1],re.sub('&','&amp;',c[2])) for c in channels]

    f = xbmcvfs.File('special://profile/addon_data/script.webgrab/webgrab/siteini.pack/Networks/directv.com.channels.xml',"wb")
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    f.write('<site generator-info-name="WebGrab+Plus/w MDB &amp; REX Postprocess -- version V1.56.6 -- Jan van Straaten" site="directv.com">\n')
    f.write('<channels>\n')
    for c in channels:
        id = c[1]
        station = c[2]
        station =  station
        name = "%s (%s)" % (c[0], c[2])
        xmltv = name
        f.write('<channel update="i" site="directv.com" site_id="%s" xmltv_id="%s">%s</channel>\n' % (id,xmltv,name))
    f.write('</channels>\n')
    f.write('</site>\n')
    f.close()

    f = xbmcvfs.File('special://profile/addon_data/script.webgrab/webgrab/siteini.pack/Networks/directv.com.ini',"rb")
    data = f.read()
    f.close()
    data = re.sub(r'timezone=.*?\|','timezone=%s|' % utc_offset,data)
    f = xbmcvfs.File('special://profile/addon_data/script.webgrab/webgrab/siteini.pack/Networks/directv.com.ini',"wb")
    f.write(data)
    f.close()

    names = ["%s (%s) [%s]" % (c[0], c[2], c[1])  for c in channels]
    index = dialog.multiselect('Add to Channels', names)
    if not index:
        return
    if index == -1:
        return

    channel_storage = plugin.get_storage('channels')
    for i in index:
        c = channels[i]
        country = "Networks"
        name = "%s (%s)" % (c[0],c[2])
        site = "directv.com"
        xmltv_id = name
        site_id = c[1]
        id = "%s|%s|%s|%s|%s" % (country,name,site,site_id,xmltv_id)
        if id in channel_storage:
            pass
        else:
            channel_storage[id] = -1

@plugin.route('/lab')
def lab():
    items = []
    items.append(
    {
        'label': 'tv.com',
        'path': plugin.url_for('tv_com'),
        'thumbnail':get_icon_path('settings'),
    })
    items.append(
    {
        'label': 'directv.com',
        'path': plugin.url_for('directv_com'),
        'thumbnail':get_icon_path('settings'),
    })
    return items


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
        'label': 'Selected Channels',
        'path': plugin.url_for('channels'),
        'thumbnail':get_icon_path('settings'),
    })
    items.append(
    {
        'label': 'Output Config Files',
        'path': plugin.url_for('write_and_copy_config'),
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
        'label': 'Show Webgrab+Plus Log',
        'path': plugin.url_for('show_log'),
        'thumbnail':get_icon_path('settings'),
    })
    items.append(
    {
        'label': 'Show Site Ini Version',
        'path': plugin.url_for('site_ini_version'),
        'thumbnail':get_icon_path('settings'),
    })
    items.append(
    {
        'label': 'Lab',
        'path': plugin.url_for('lab'),
        'thumbnail':get_icon_path('settings'),
    })
    return items


if __name__ == '__main__':
    plugin.run()
