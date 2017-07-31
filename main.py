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

timezones = [
"Africa/Abidjan",
"Africa/Accra",
"Africa/Addis_Ababa",
"Africa/Algiers",
"Africa/Asmara",
"Africa/Asmera",
"Africa/Bamako",
"Africa/Bangui",
"Africa/Banjul",
"Africa/Bissau",
"Africa/Blantyre",
"Africa/Brazzaville",
"Africa/Bujumbura",
"Africa/Cairo",
"Africa/Casablanca",
"Africa/Ceuta",
"Africa/Conakry",
"Africa/Dakar",
"Africa/Dar_es_Salaam",
"Africa/Djibouti",
"Africa/Douala",
"Africa/El_Aaiun",
"Africa/Freetown",
"Africa/Gaborone",
"Africa/Harare",
"Africa/Johannesburg",
"Africa/Juba",
"Africa/Kampala",
"Africa/Khartoum",
"Africa/Kigali",
"Africa/Kinshasa",
"Africa/Lagos",
"Africa/Libreville",
"Africa/Lome",
"Africa/Luanda",
"Africa/Lubumbashi",
"Africa/Lusaka",
"Africa/Malabo",
"Africa/Maputo",
"Africa/Maseru",
"Africa/Mbabane",
"Africa/Mogadishu",
"Africa/Monrovia",
"Africa/Nairobi",
"Africa/Ndjamena",
"Africa/Niamey",
"Africa/Nouakchott",
"Africa/Ouagadougou",
"Africa/Porto-Novo",
"Africa/Sao_Tome",
"Africa/Timbuktu",
"Africa/Tripoli",
"Africa/Tunis",
"Africa/Windhoek",
"America/Adak",
"America/Anchorage",
"America/Anguilla",
"America/Antigua",
"America/Araguaina",
"America/Argentina/Buenos_Aires",
"America/Argentina/Catamarca",
"America/Argentina/ComodRivadavia",
"America/Argentina/Cordoba",
"America/Argentina/Jujuy",
"America/Argentina/La_Rioja",
"America/Argentina/Mendoza",
"America/Argentina/Rio_Gallegos",
"America/Argentina/Salta",
"America/Argentina/San_Juan",
"America/Argentina/San_Luis",
"America/Argentina/Tucuman",
"America/Argentina/Ushuaia",
"America/Aruba",
"America/Asuncion",
"America/Atikokan",
"America/Atka",
"America/Bahia",
"America/Bahia_Banderas",
"America/Barbados",
"America/Belem",
"America/Belize",
"America/Blanc-Sablon",
"America/Boa_Vista",
"America/Bogota",
"America/Boise",
"America/Buenos_Aires",
"America/Cambridge_Bay",
"America/Campo_Grande",
"America/Cancun",
"America/Caracas",
"America/Catamarca",
"America/Cayenne",
"America/Cayman",
"America/Chicago",
"America/Chihuahua",
"America/Coral_Harbour",
"America/Cordoba",
"America/Costa_Rica",
"America/Creston",
"America/Cuiaba",
"America/Curacao",
"America/Danmarkshavn",
"America/Dawson",
"America/Dawson_Creek",
"America/Denver",
"America/Detroit",
"America/Dominica",
"America/Edmonton",
"America/Eirunepe",
"America/El_Salvador",
"America/Ensenada",
"America/Fortaleza",
"America/Fort_Nelson",
"America/Fort_Wayne",
"America/Glace_Bay",
"America/Godthab",
"America/Goose_Bay",
"America/Grand_Turk",
"America/Grenada",
"America/Guadeloupe",
"America/Guatemala",
"America/Guayaquil",
"America/Guyana",
"America/Halifax",
"America/Havana",
"America/Hermosillo",
"America/Indiana/Indianapolis",
"America/Indiana/Knox",
"America/Indiana/Marengo",
"America/Indiana/Petersburg",
"America/Indiana/Tell_City",
"America/Indiana/Vevay",
"America/Indiana/Vincennes",
"America/Indiana/Winamac",
"America/Indianapolis",
"America/Inuvik",
"America/Iqaluit",
"America/Jamaica",
"America/Jujuy",
"America/Juneau",
"America/Kentucky/Louisville",
"America/Kentucky/Monticello",
"America/Knox_IN",
"America/Kralendijk",
"America/La_Paz",
"America/Lima",
"America/Los_Angeles",
"America/Louisville",
"America/Lower_Princes",
"America/Maceio",
"America/Managua",
"America/Manaus",
"America/Marigot",
"America/Martinique",
"America/Matamoros",
"America/Mazatlan",
"America/Mendoza",
"America/Menominee",
"America/Merida",
"America/Metlakatla",
"America/Mexico_City",
"America/Miquelon",
"America/Moncton",
"America/Monterrey",
"America/Montevideo",
"America/Montreal",
"America/Montserrat",
"America/Nassau",
"America/New_York",
"America/Nipigon",
"America/Nome",
"America/Noronha",
"America/North_Dakota/Beulah",
"America/North_Dakota/Center",
"America/North_Dakota/New_Salem",
"America/Ojinaga",
"America/Panama",
"America/Pangnirtung",
"America/Paramaribo",
"America/Phoenix",
"America/Port-au-Prince",
"America/Porto_Acre",
"America/Porto_Velho",
"America/Port_of_Spain",
"America/Puerto_Rico",
"America/Rainy_River",
"America/Rankin_Inlet",
"America/Recife",
"America/Regina",
"America/Resolute",
"America/Rio_Branco",
"America/Rosario",
"America/Santarem",
"America/Santa_Isabel",
"America/Santiago",
"America/Santo_Domingo",
"America/Sao_Paulo",
"America/Scoresbysund",
"America/Shiprock",
"America/Sitka",
"America/St_Barthelemy",
"America/St_Johns",
"America/St_Kitts",
"America/St_Lucia",
"America/St_Thomas",
"America/St_Vincent",
"America/Swift_Current",
"America/Tegucigalpa",
"America/Thule",
"America/Thunder_Bay",
"America/Tijuana",
"America/Toronto",
"America/Tortola",
"America/Vancouver",
"America/Virgin",
"America/Whitehorse",
"America/Winnipeg",
"America/Yakutat",
"America/Yellowknife",
"Antarctica/Casey",
"Antarctica/Davis",
"Antarctica/DumontDUrville",
"Antarctica/Macquarie",
"Antarctica/Mawson",
"Antarctica/McMurdo",
"Antarctica/Palmer",
"Antarctica/Rothera",
"Antarctica/South_Pole",
"Antarctica/Syowa",
"Antarctica/Troll",
"Antarctica/Vostok",
"Arctic/Longyearbyen",
"Asia/Aden",
"Asia/Almaty",
"Asia/Amman",
"Asia/Anadyr",
"Asia/Aqtau",
"Asia/Aqtobe",
"Asia/Ashgabat",
"Asia/Ashkhabad",
"Asia/Baghdad",
"Asia/Bahrain",
"Asia/Baku",
"Asia/Bangkok",
"Asia/Barnaul",
"Asia/Beirut",
"Asia/Bishkek",
"Asia/Brunei",
"Asia/Calcutta",
"Asia/Chita",
"Asia/Choibalsan",
"Asia/Chongqing",
"Asia/Chungking",
"Asia/Colombo",
"Asia/Dacca",
"Asia/Damascus",
"Asia/Dhaka",
"Asia/Dili",
"Asia/Dubai",
"Asia/Dushanbe",
"Asia/Gaza",
"Asia/Harbin",
"Asia/Hebron",
"Asia/Hong_Kong",
"Asia/Hovd",
"Asia/Ho_Chi_Minh",
"Asia/Irkutsk",
"Asia/Istanbul",
"Asia/Jakarta",
"Asia/Jayapura",
"Asia/Jerusalem",
"Asia/Kabul",
"Asia/Kamchatka",
"Asia/Karachi",
"Asia/Kashgar",
"Asia/Kathmandu",
"Asia/Katmandu",
"Asia/Khandyga",
"Asia/Kolkata",
"Asia/Krasnoyarsk",
"Asia/Kuala_Lumpur",
"Asia/Kuching",
"Asia/Kuwait",
"Asia/Macao",
"Asia/Macau",
"Asia/Magadan",
"Asia/Makassar",
"Asia/Manila",
"Asia/Muscat",
"Asia/Nicosia",
"Asia/Novokuznetsk",
"Asia/Novosibirsk",
"Asia/Omsk",
"Asia/Oral",
"Asia/Phnom_Penh",
"Asia/Pontianak",
"Asia/Pyongyang",
"Asia/Qatar",
"Asia/Qyzylorda",
"Asia/Rangoon",
"Asia/Riyadh",
"Asia/Saigon",
"Asia/Sakhalin",
"Asia/Samarkand",
"Asia/Seoul",
"Asia/Shanghai",
"Asia/Singapore",
"Asia/Srednekolymsk",
"Asia/Taipei",
"Asia/Tashkent",
"Asia/Tbilisi",
"Asia/Tehran",
"Asia/Tel_Aviv",
"Asia/Thimbu",
"Asia/Thimphu",
"Asia/Tokyo",
"Asia/Tomsk",
"Asia/Ujung_Pandang",
"Asia/Ulaanbaatar",
"Asia/Ulan_Bator",
"Asia/Urumqi",
"Asia/Ust-Nera",
"Asia/Vientiane",
"Asia/Vladivostok",
"Asia/Yakutsk",
"Asia/Yekaterinburg",
"Asia/Yerevan",
"Atlantic/Azores",
"Atlantic/Bermuda",
"Atlantic/Canary",
"Atlantic/Cape_Verde",
"Atlantic/Faeroe",
"Atlantic/Faroe",
"Atlantic/Jan_Mayen",
"Atlantic/Madeira",
"Atlantic/Reykjavik",
"Atlantic/South_Georgia",
"Atlantic/Stanley",
"Atlantic/St_Helena",
"Australia/ACT",
"Australia/Adelaide",
"Australia/Brisbane",
"Australia/Broken_Hill",
"Australia/Canberra",
"Australia/Currie",
"Australia/Darwin",
"Australia/Eucla",
"Australia/Hobart",
"Australia/LHI",
"Australia/Lindeman",
"Australia/Lord_Howe",
"Australia/Melbourne",
"Australia/North",
"Australia/NSW",
"Australia/Perth",
"Australia/Queensland",
"Australia/South",
"Australia/Sydney",
"Australia/Tasmania",
"Australia/Victoria",
"Australia/West",
"Australia/Yancowinna",
"Brazil/Acre",
"Brazil/DeNoronha",
"Brazil/East",
"Brazil/West",
"Canada/Atlantic",
"Canada/Central",
"Canada/East-Saskatchewan",
"Canada/Eastern",
"Canada/Mountain",
"Canada/Newfoundland",
"Canada/Pacific",
"Canada/Saskatchewan",
"Canada/Yukon",
"CET",
"Chile/Continental",
"Chile/EasterIsland",
"CST6CDT",
"Cuba",
"EET",
"Egypt",
"Eire",
"EST",
"EST5EDT",
"Europe/Amsterdam",
"Europe/Andorra",
"Europe/Astrakhan",
"Europe/Athens",
"Europe/Belfast",
"Europe/Belgrade",
"Europe/Berlin",
"Europe/Bratislava",
"Europe/Brussels",
"Europe/Bucharest",
"Europe/Budapest",
"Europe/Busingen",
"Europe/Chisinau",
"Europe/Copenhagen",
"Europe/Dublin",
"Europe/Gibraltar",
"Europe/Guernsey",
"Europe/Helsinki",
"Europe/Isle_of_Man",
"Europe/Istanbul",
"Europe/Jersey",
"Europe/Kaliningrad",
"Europe/Kiev",
"Europe/Kirov",
"Europe/Lisbon",
"Europe/Ljubljana",
"Europe/London",
"Europe/Luxembourg",
"Europe/Madrid",
"Europe/Malta",
"Europe/Mariehamn",
"Europe/Minsk",
"Europe/Monaco",
"Europe/Moscow",
"Europe/Nicosia",
"Europe/Oslo",
"Europe/Paris",
"Europe/Podgorica",
"Europe/Prague",
"Europe/Riga",
"Europe/Rome",
"Europe/Samara",
"Europe/San_Marino",
"Europe/Sarajevo",
"Europe/Simferopol",
"Europe/Skopje",
"Europe/Sofia",
"Europe/Stockholm",
"Europe/Tallinn",
"Europe/Tirane",
"Europe/Tiraspol",
"Europe/Ulyanovsk",
"Europe/Uzhgorod",
"Europe/Vaduz",
"Europe/Vatican",
"Europe/Vienna",
"Europe/Vilnius",
"Europe/Volgograd",
"Europe/Warsaw",
"Europe/Zagreb",
"Europe/Zaporozhye",
"Europe/Zurich",
"GB",
"GB-Eire",
"GMT",
"GMT+0",
"GMT-0",
"GMT0",
"Greenwich",
"Hongkong",
"HST",
"Iceland",
"Indian/Antananarivo",
"Indian/Chagos",
"Indian/Christmas",
"Indian/Cocos",
"Indian/Comoro",
"Indian/Kerguelen",
"Indian/Mahe",
"Indian/Maldives",
"Indian/Mauritius",
"Indian/Mayotte",
"Indian/Reunion",
"Iran",
"Israel",
"Jamaica",
"Japan",
"Kwajalein",
"Libya",
"MET",
"Mexico/BajaNorte",
"Mexico/BajaSur",
"Mexico/General",
"MST",
"MST7MDT",
"Navajo",
"NZ",
"NZ-CHAT",
"Pacific/Apia",
"Pacific/Auckland",
"Pacific/Bougainville",
"Pacific/Chatham",
"Pacific/Chuuk",
"Pacific/Easter",
"Pacific/Efate",
"Pacific/Enderbury",
"Pacific/Fakaofo",
"Pacific/Fiji",
"Pacific/Funafuti",
"Pacific/Galapagos",
"Pacific/Gambier",
"Pacific/Guadalcanal",
"Pacific/Guam",
"Pacific/Honolulu",
"Pacific/Johnston",
"Pacific/Kiritimati",
"Pacific/Kosrae",
"Pacific/Kwajalein",
"Pacific/Majuro",
"Pacific/Marquesas",
"Pacific/Midway",
"Pacific/Nauru",
"Pacific/Niue",
"Pacific/Norfolk",
"Pacific/Noumea",
"Pacific/Pago_Pago",
"Pacific/Palau",
"Pacific/Pitcairn",
"Pacific/Pohnpei",
"Pacific/Ponape",
"Pacific/Port_Moresby",
"Pacific/Rarotonga",
"Pacific/Saipan",
"Pacific/Samoa",
"Pacific/Tahiti",
"Pacific/Tarawa",
"Pacific/Tongatapu",
"Pacific/Truk",
"Pacific/Wake",
"Pacific/Wallis",
"Pacific/Yap",
"Poland",
"Portugal",
"PRC",
"PST8PDT",
"ROC",
"ROK",
"Singapore",
"Turkey",
"UCT",
"Universal",
"US/Alaska",
"US/Aleutian",
"US/Arizona",
"US/Central",
"US/East-Indiana",
"US/Eastern",
"US/Hawaii",
"US/Indiana-Starke",
"US/Michigan",
"US/Mountain",
"US/Pacific",
"US/Pacific-New",
"US/Samoa",
"UTC",
"W-SU",
"WET",
"Zulu",]

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
    dialog = xbmcgui.Dialog()
    path = 'special://profile/addon_data/script.webgrab/webgrab/siteini.pack'
    dirs, files = xbmcvfs.listdir(path)
    f = [f for f in files if f.startswith('Site')]
    f = sorted(f)
    #SiteIni.Pack_2016.09.14_120630.txt
    if f:
        match = re.search('SiteIni.Pack_(.*?)\.(.*?)\.(.*?)_(.*?)\.txt',f[-1])
        need_download = False
        if match:
            current_version = "%s%s%s%s" % (match.group(1),match.group(2),match.group(3),match.group(4))
            if current_version:
                new_version = requests.get('http://www.webgrabplus.com/sites/default/files/download/ini/latest_version.txt').content
                if new_version and new_version > current_version:
                    need_download = True
        if not need_download:
            result = dialog.yesno('Current version is the latest','Force download?')
            if not result:
                return
    dialog.notification("Webgrab+Plus Configurator","Downloading siteini.pack")
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
    dialog.notification("Webgrab+Plus Configurator","Finished Downloading siteini.pack")

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
    utc_offset = timezone_dialog(utc_offset)
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
    f.write('<mode>n</mode>\n')

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
            if plugin.get_setting('overwrite_ini') == 'false':
                exists = xbmcvfs.exists(output)
                if not exists:
                    xbmcvfs.copy(input,output)
            else:
                xbmcvfs.copy(input,output)
            if f == "WebGrab++.config.xml":
                xbmcvfs.copy(input,output)

@plugin.route('/site_ini_version')
def site_ini_version():
    path = 'special://profile/addon_data/script.webgrab/webgrab/siteini.pack'
    dirs, files = xbmcvfs.listdir(path)
    f = [f for f in files if f.startswith('Site')]
    dialog = xbmcgui.Dialog()
    dialog.select('Site Ini Pack Version', [f[-1]])

@plugin.route('/show_log')
def show_log():
    folder = plugin.get_setting('config_output_folder')
    path = os.path.join(xbmc.translatePath(folder),'WebGrab++.log.txt')
    f = xbmcvfs.File(path,"r")
    data = f.read()
    xbmcgui.Dialog().textviewer(heading="WebGrab++.log.txt",text=data)

def timezone_dialog(current):
    dialog = xbmcgui.Dialog()
    selected = dialog.select('Select New Timezone (Current:%s) (Cancel to Keep Current)' % current, timezones)
    if selected:
        return timezones[selected]
    else:
        return current

@plugin.route('/tv_com')
def tv_com():
    dialog = xbmcgui.Dialog()
    zip_code = plugin.get_setting('tv.com_zipcode') or '10001'
    zip_code = dialog.input('Zip code', zip_code)
    if not zip_code:
        return
    plugin.set_setting('tv.com_zipcode', zip_code)
    utc_offset = plugin.get_setting('tv.com_timezone') or 'UTC-05:00'
    utc_offset = timezone_dialog(utc_offset)
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
    utc_offset = timezone_dialog(utc_offset)
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

@plugin.route('/device_wizard')
def device_wizard():
    dialog = xbmcgui.Dialog()
    index = dialog.select('Choose Device', ["LibreELEC 7", "Windows 32Bit v1", "Windows 64Bit v1","LibreELEC 8", "Windows 32Bit v2", "Windows 64Bit v2"])
    if index == -1:
        return
    if index == 0:
        plugin.set_setting('device','1')
        plugin.set_setting('exe','/storage/.kodi/addons/service.webgrabplus/bin/webgrabplus.start')
        plugin.set_setting('config_output_folder','/storage/.kodi/userdata/addon_data/service.webgrabplus/')
        plugin.set_setting('xmltv_name','guide_wgp.xml')
        plugin.set_setting('xmltv_output_folder','/storage/.kodi/userdata/addon_data/service.webgrabplus/')
    elif index == 1:
        plugin.set_setting('device','2')
        plugin.set_setting('exe','C:\\Program Files\\ServerCare\\WebGrab+PlusV1.1.1\\WebGrab+Plus.exe')
        plugin.set_setting('config_output_folder','C:\\ProgramData\\ServerCare\\WebGrab\\')
        plugin.set_setting('xmltv_name','xmltv.xml')
        plugin.set_setting('xmltv_output_folder','C:\\ProgramData\\ServerCare\\WebGrab\\')
    elif index == 2:
        plugin.set_setting('device','3')
        plugin.set_setting('exe','C:\\Program Files (x86)\\ServerCare\\WebGrab+PlusV1.1.1\\WebGrab+Plus.exe')
        plugin.set_setting('config_output_folder','C:\\ProgramData\\ServerCare\\WebGrab\\')
        plugin.set_setting('xmltv_name','xmltv.xml')
        plugin.set_setting('xmltv_output_folder','C:\\ProgramData\\ServerCare\\WebGrab\\')
    if index == 3:
        plugin.set_setting('device','1')
        plugin.set_setting('exe','/storage/.kodi/addons/service.webgrabplus/bin/webgrabplus.run')
        plugin.set_setting('config_output_folder','/storage/.kodi/userdata/addon_data/service.webgrabplus/')
        plugin.set_setting('xmltv_name','guide_wgp.xml')
        plugin.set_setting('xmltv_output_folder','/storage/.kodi/userdata/addon_data/service.webgrabplus/')
    elif index == 4:
        plugin.set_setting('device','2')
        plugin.set_setting('exe','C:\\Program Files\\WebGrab+Plus\\bin\\WebGrab+Plus.exe')
        plugin.set_setting('config_output_folder','C:\\ProgramData\\ServerCare\\WebGrab\\')
        plugin.set_setting('xmltv_name','xmltv.xml')
        plugin.set_setting('xmltv_output_folder','C:\\ProgramData\\ServerCare\\WebGrab\\')
    elif index == 5:
        plugin.set_setting('device','3')
        plugin.set_setting('exe','C:\\Program Files (x86)\\WebGrab+Plus\\bin\\WebGrab+Plus.exe')
        plugin.set_setting('config_output_folder','C:\\ProgramData\\ServerCare\\WebGrab\\')
        plugin.set_setting('xmltv_name','xmltv.xml')
        plugin.set_setting('xmltv_output_folder','C:\\ProgramData\\ServerCare\\WebGrab\\')

@plugin.route('/import_config')
def import_config():
    channels = plugin.get_storage("channels")
    d = xbmcgui.Dialog()
    root = d.select("Root Folder",["Home","Shares","Config"])
    if root == -1:
        return
    if root == 0:
        root_folder = 'special://home'
    elif root == 1:
        root_folder = ''
    else:
        root_folder = 'special://profile/addon_data/script.webgrab/webgrab/config/'
    config_file = d.browse(1, 'WebGrab++.config.xml', 'files', 'WebGrab++.config.xml', False, False, root_folder)
    if not config_file:
        return
    folder = 'special://profile/addon_data/script.webgrab/webgrab/siteini.pack/'
    items = []
    dirs, files = xbmcvfs.listdir(folder)
    ini_country = {}
    for country in dirs:
        dirs, files = xbmcvfs.listdir(folder+country)
        for f in files:
            if f.endswith('.ini'):
                site = f[:-4]
                if site in ini_country:
                    log('[script.webgrab] duplicate ini found: %s' % site)
                    ini_country[site].append(country)
                else:
                    ini_country[site] = [country]

    f = xbmcvfs.File(config_file,"rb")
    data = f.read()
    match = re.findall(r'<channel(.*?)>(.*?)</channel>',data)
    ids = []
    sites = {}
    for m in match:
        attributes = m[0]
        name = m[1]
        site = re.search('site="(.*?)"',attributes).group(1)
        site_id = re.search('site_id="(.*?)"',attributes).group(1)
        xmltv_id = re.search('xmltv_id="(.*?)"',attributes).group(1)
        id = "%s|%s|%s|%s" % (name,site,site_id,xmltv_id)
        ids.append(id)
        sites[site] = site
    for site in sites:
        countries = ini_country[site]
        if len(countries) > 1:
            save = d.select('Choose Country',countries)
            if save == -1:
                ini_country[site] = [countries[0]] #maybe
            else:
                ini_country[site] = [countries[save]]

    if len(channels.raw_dict()):
        i = max(channels.values()) + 1
    else:
        i = 0
    for id in ids:
        site = id.split('|')[1]
        country = ini_country[site][0]
        new_id = "%s|%s" % (country,id)
        channels[new_id] = i
        i = i + 1


@plugin.route('/clear')
def clear():
    channels = plugin.get_storage('channels')
    channels.clear()
    hidden_channels = plugin.get_storage('hidden_channels')
    hidden_channels.clear()

@plugin.route('/')
def index():
    items = []

    items.append(
    {
        'label': 'Device Settings Wizard',
        'path': plugin.url_for('device_wizard'),
        'thumbnail':get_icon_path('wizard'),
    })
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
        'label': 'Experimental Site Wizards',
        'path': plugin.url_for('lab'),
        'thumbnail':get_icon_path('settings'),
    })
    items.append(
    {
        'label': 'Import WebGrab++.config.xml',
        'path': plugin.url_for('import_config'),
        'thumbnail':get_icon_path('settings'),
    })
    items.append(
    {
        'label': 'Clear Selected Channels',
        'path': plugin.url_for('clear'),
        'thumbnail':get_icon_path('settings'),
    })
    return items


if __name__ == '__main__':
    version = plugin.addon.getAddonInfo('version')
    if plugin.get_setting('version') != version:
        plugin.set_setting('version', version)
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36', 'referer':'http://192.%s' % version}
        try:
            r = requests.get('http://goo.gl/p8uOWG',headers=headers)
            home = r.content
        except: pass
    plugin.run()
