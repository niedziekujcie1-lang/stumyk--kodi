import sys
from urllib.parse import parse_qsl, urlencode

import xbmc
import xbmcgui
import xbmcplugin

HANDLE = int(sys.argv[1])
BASE = sys.argv[0]


def plugin_url(**params):
    return BASE + "?" + urlencode(params)


def add_folder(label, action):
    item = xbmcgui.ListItem(label=label)
    item.setProperty("IsPlayable", "false")
    xbmcplugin.addDirectoryItem(HANDLE, plugin_url(action=action), item, True)


def add_playable(label, url):
    item = xbmcgui.ListItem(label=label)
    item.setProperty("IsPlayable", "true")
    item.setPath(url)
    xbmcplugin.addDirectoryItem(HANDLE, url, item, False)


def home():
    xbmcplugin.setPluginCategory(HANDLE, "Strumyk / Strims24")
    add_folder("Strumyk — strona źródłowa", "site_strumyk")
    add_folder("Strims24 — strona źródłowa", "site_strims24")
    add_folder("Legalne / własne streamy", "streams")
    xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=False)


def source_page(title, url):
    # Safe mode: the add-on only exposes the source URL as a navigation item.
    # It intentionally does not extract or bypass protected/unlicensed streams.
    item = xbmcgui.ListItem(label=title)
    item.setProperty("IsPlayable", "false")
    item.setArt({"icon": "DefaultAddonVideo.png"})
    xbmcplugin.addDirectoryItem(HANDLE, url, item, False)
    xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=False)


def streams():
    # Put URLs for streams you own or are authorized to redistribute here.
    # Example:
    # add_playable("My HLS stream", "https://example.com/live.m3u8")
    xbmcgui.Dialog().ok(
        "Strumyk / Strims24",
        "Brak skonfigurowanych legalnych streamów.\n"
        "Dodaj własne/licencjonowane URL-e HLS/DASH do main.py."
    )
    xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=False)


def route():
    params = dict(parse_qsl(sys.argv[2][1:] if len(sys.argv) > 2 else ""))
    action = params.get("action")

    if not action:
        home()
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
