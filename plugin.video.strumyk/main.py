import sys
from urllib.parse import parse_qsl, urlencode

import xbmcgui
import xbmcplugin

HANDLE = int(sys.argv[1])
BASE = sys.argv[0]

SPORTS = (
    ("Piłka nożna", "football"),
    ("Koszykówka", "basketball"),
    ("Siatkówka", "volleyball"),
    ("Tenis", "tennis"),
    ("Sporty motorowe", "motorsport"),
    ("Sporty walki", "combat"),
    ("Hokej", "hockey"),
    ("Inne sporty", "other"),
)


def plugin_url(**params):
    return BASE + "?" + urlencode(params)


def add_folder(label, action, **params):
    item = xbmcgui.ListItem(label=label)
    item.setProperty("IsPlayable", "false")
    xbmcplugin.addDirectoryItem(HANDLE, plugin_url(action=action, **params), item, True)


def add_playable(label, url):
    item = xbmcgui.ListItem(label=label)
    item.setProperty("IsPlayable", "true")
    item.setPath(url)
    xbmcplugin.addDirectoryItem(HANDLE, plugin_url(action="play", url=url, label=label), item, False)


def home():
    xbmcplugin.setPluginCategory(HANDLE, "Strumyk / Strims24")
    add_folder("Kategorie sportowe", "categories")
    add_folder("Legalne / własne streamy", "streams")
    add_folder("Strumyk — strona źródłowa", "site_strumyk")
    add_folder("Strims24 — strona źródłowa", "site_strims24")
    xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=False)


def categories():
    xbmcplugin.setPluginCategory(HANDLE, "Kategorie sportowe")
    for label, category in SPORTS:
        add_folder(label, "category", category=category)
    xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=False)


def category(category):
    names = dict(SPORTS)
    title = next((label for label, key in SPORTS if key == category), category)
    url = xbmcplugin.getSetting(f"url_{category}")
    label = xbmcplugin.getSetting(f"label_{category}") or title

    xbmcplugin.setPluginCategory(HANDLE, title)
    if url.strip():
        add_playable(label.strip(), url.strip())
    else:
        xbmcgui.Dialog().ok(
            title,
            "Brak skonfigurowanego legalnego/licencjonowanego streamu dla tej kategorii.\n\n"
            "Dodaj URL HLS (.m3u8) lub DASH (.mpd) w ustawieniach dodatku."
        )
    xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=False)


def source_page(title, url):
    item = xbmcgui.ListItem(label=title)
    item.setProperty("IsPlayable", "false")
    item.setPath(url)
    xbmcplugin.addDirectoryItem(HANDLE, url, item, False)
    xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=False)


def streams():
    xbmcgui.Dialog().ok(
        "Strumyk / Strims24",
        "Dodaj legalne/licencjonowane URL-e HLS/DASH w ustawieniach dodatku."
    )
    xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=False)


def play(url, label):
    item = xbmcgui.ListItem(label=label)
    item.setPath(url)
    xbmcplugin.setResolvedUrl(HANDLE, True, item)


def route():
    params = dict(parse_qsl(sys.argv[2][1:] if len(sys.argv) > 2 else ""))
    action = params.get("action")
    if not action:
        home()
    elif action == "categories":
        categories()
    elif action == "category":
        category(params.get("category", "other"))
    elif action == "play":
        play(params.get("url", ""), params.get("label", "Stream"))
    elif action == "site_strumyk":
        source_page("Otwórz Strumyk", "https://strumyk.pk/")
    elif action == "site_strims24":
        source_page("Otwórz Strims24", "https://strims24.st/")
    elif action == "streams":
        streams()
    else:
        xbmcplugin.endOfDirectory(HANDLE, succeeded=False)


if __name__ == "__main__":
    route()
