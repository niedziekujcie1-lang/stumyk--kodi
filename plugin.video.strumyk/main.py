import sys
from urllib.parse import parse_qsl, urlencode, urlparse

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

SOURCE_SITES = (
    ("Strumyk", "https://strumyk.pk/"),
    ("Strims24", "https://strims24.st/"),
)

# Oficjalne polskojęzyczne źródła. Dostępność konkretnej transmisji może się zmieniać
# zależnie od praw do wydarzenia i aktualnego programu nadawcy.
# Pozycje YouTube korzystają z oficjalnego dodatku YouTube dla Kodi.
LEGAL_PL_SOURCES = (
    ("TVP Sport — transmisje na żywo", "https://sport.tvp.pl/", "web"),
    ("TVP VOD — Sport", "https://vod.tvp.pl/sport", "web"),
    ("Łączy nas piłka TV — PZPN (YouTube LIVE)", "plugin://plugin.video.youtube/channel/UCcz1Tizq8IFdEguy3smvnhA/live/", "plugin"),
    ("ORLEN Basket Liga — YouTube LIVE", "plugin://plugin.video.youtube/user/WWWPLKPL/live/", "plugin"),
    ("Polski Związek Piłki Siatkowej", "https://www.pzps.pl/pl/", "web"),
    ("Polsat Sport", "https://www.polsatsport.pl/", "web"),
)


def plugin_url(**params):
    return BASE + "?" + urlencode(params)


def stream_kind(url):
    try:
        path = urlparse(url).path.lower()
    except ValueError:
        path = url.lower()
    if path.endswith((".m3u8", ".m3u")):
        return "hls"
    if path.endswith(".mpd"):
        return "dash"
    return "direct"


def prepare_player_item(label, url):
    item = xbmcgui.ListItem(label=label or "Stream")
    item.setProperty("IsPlayable", "true")
    item.setProperty("VideoPlayer", "true")

    kind = stream_kind(url)
    if kind in ("hls", "dash"):
        item.setProperty("inputstream", "inputstream.adaptive")
        item.setContentLookup(False)
        if kind == "hls":
            item.setMimeType("application/vnd.apple.mpegurl")
        else:
            item.setMimeType("application/dash+xml")

    item.setPath(url)
    return item


def add_folder(label, action, **params):
    item = xbmcgui.ListItem(label=label)
    item.setProperty("IsPlayable", "false")
    xbmcplugin.addDirectoryItem(HANDLE, plugin_url(action=action, **params), item, True)


def add_playable(label, url):
    clean_url = url.strip()
    item = prepare_player_item(label, clean_url)
    xbmcplugin.addDirectoryItem(
        HANDLE,
        plugin_url(action="play", url=clean_url, label=label),
        item,
        False,
    )


def home():
    xbmcplugin.setPluginCategory(HANDLE, "Strumyk / Strims24")
    xbmcplugin.setContent(HANDLE, "videos")
    add_folder("Kategorie sportowe", "categories")
    add_folder("Legalne / własne streamy", "streams")
    add_folder("Legalne transmisje PL", "legal_pl")
    add_folder("Źródła", "sources")
    xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=False)


def categories():
    xbmcplugin.setPluginCategory(HANDLE, "Kategorie sportowe")
    for label, category in SPORTS:
        add_folder(label, "category", category=category)
    xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=False)


def category(category):
    title = next((label for label, key in SPORTS if key == category), "Inne sporty")
    url = xbmcplugin.getSetting(HANDLE, f"url_{category}").strip()
    label = xbmcplugin.getSetting(HANDLE, f"label_{category}").strip() or title

    xbmcplugin.setPluginCategory(HANDLE, title)
    xbmcplugin.setContent(HANDLE, "videos")
    if url:
        add_playable(label, url)
    else:
        xbmcgui.Dialog().ok(
            title,
            "Brak skonfigurowanego legalnego/licencjonowanego streamu dla tej kategorii.\n\n"
            "Otwórz Ustawienia dodatku i wpisz bezpośredni URL HLS (.m3u8) lub DASH (.mpd)."
        )
    xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=False)


def legal_pl():
    xbmcplugin.setPluginCategory(HANDLE, "Legalne transmisje PL")
    xbmcplugin.setContent(HANDLE, "videos")
    for title, url, kind in LEGAL_PL_SOURCES:
        item = xbmcgui.ListItem(label=title)
        item.setInfo("video", {"title": title, "plot": url})
        if kind == "plugin":
            # Oficjalny dodatek YouTube obsługuje listy LIVE w Kodi.
            item.setProperty("IsPlayable", "true")
            item.setPath(url)
            target = url
        else:
            item.setProperty("IsPlayable", "false")
            target = plugin_url(action="info", url=url, label=title)
        xbmcplugin.addDirectoryItem(HANDLE, target, item, False)
    xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=False)


def source_page(title, url):
    item = xbmcgui.ListItem(label=title)
    item.setProperty("IsPlayable", "false")
    item.setInfo("video", {"title": title, "plot": url})
    item.setPath(url)
    xbmcplugin.addDirectoryItem(
        HANDLE,
        plugin_url(action="info", url=url, label=title),
        item,
        False,
    )


def sources():
    xbmcplugin.setPluginCategory(HANDLE, "Źródła")
    for title, url in SOURCE_SITES:
        source_page(title, url)
    xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=False)


def streams():
    xbmcgui.Dialog().ok(
        "Strumyk / Strims24",
        "Źródła bezpośrednie są przeznaczone wyłącznie do legalnych/licencjonowanych streamów.\n\n"
        "Skonfiguruj je w Ustawieniach dodatku, wybierając kategorię sportową i wpisując URL HLS/DASH.\n\n"
        "Po zapisaniu otwórz kategorię i wybierz pozycję streamu — Kodi uruchomi wbudowany odtwarzacz wideo."
    )
    xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=False)


def play(url, label):
    clean_url = url.strip()
    if not clean_url:
        xbmcgui.Dialog().notification(
            "Strumyk / Strims24",
            "Brak adresu streamu.",
            xbmcgui.NOTIFICATION_ERROR,
        )
        xbmcplugin.setResolvedUrl(HANDLE, False, xbmcgui.ListItem())
        return

    item = prepare_player_item(label, clean_url)
    xbmcplugin.setResolvedUrl(HANDLE, True, item)


def show_info(label, url):
    xbmcgui.Dialog().ok(label or "Źródło", url or "")
    xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=False)


def route():
    query = sys.argv[2][1:] if len(sys.argv) > 2 and sys.argv[2].startswith("?") else ""
    params = dict(parse_qsl(query, keep_blank_values=True))
    action = params.get("action")

    if not action:
        home()
    elif action == "categories":
        categories()
    elif action == "category":
        category(params.get("category", "other"))
    elif action == "legal_pl":
        legal_pl()
    elif action == "play":
        play(params.get("url", ""), params.get("label", "Stream"))
    elif action == "sources":
        sources()
    elif action == "site_strumyk":
        source_page("Strumyk", SOURCE_SITES[0][1])
    elif action == "site_strims24":
        source_page("Strims24", SOURCE_SITES[1][1])
    elif action == "streams":
        streams()
    elif action == "info":
        show_info(params.get("label", "Źródło"), params.get("url", ""))
    else:
        xbmcplugin.endOfDirectory(HANDLE, succeeded=False)


if __name__ == "__main__":
    route()
