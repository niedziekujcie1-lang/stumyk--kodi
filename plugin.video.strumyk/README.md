# plugin.video.strumyk

Kodi 21 Omega starter framework.

## Current behavior
- One Kodi add-on containing entries for Strumyk and Strims24.
- A separate area for user-owned/licensed direct HLS/DASH streams.
- No DRM bypass, authentication bypass, paywall bypass, or extraction of protected/unlicensed streams.

## Installation
1. Zip the `plugin.video.strumyk` directory itself.
2. Kodi → Add-ons → Install from zip file.
3. Enable the add-on.

## Development
Kodi plugins use `xbmcplugin.addDirectoryItem()` for directory entries and
`xbmcplugin.setResolvedUrl()` when a plugin resolves a playable URL.
