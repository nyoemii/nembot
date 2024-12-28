# :3

~~(anything < python 3.12 breaks i do not know why... it's the GSI library tho :3)~~

no this doesn't read memory it's not a cheat, i'm just using fucking [schizo methods](https://github.com/Pandaptable/CS-dotfiles/tree/main/selfbot/ticks) of sending console commands (exec_async with `n` getting executed every 50 ticks that is aliased to `exec selfbot`)

## Setup
1. `uv install`
2. `cp config_default.py config.py`
3. edit config
4. setup CFG folder
	- add the selfbot folder from [this](https://github.com/Pandaptable/CS-dotfiles) repo into your cfg folder
	- add `alias n "exec selfbot.cfg"` into your autoexec (or whatever you named the file at the root of your cfg directory)
	- add `exec "selfbot/setup.cfg"` into your autoexec (in main menu, it needs `sv_cheats 1` so it will break otherwise)
	- add `gamestate_integration_GSI.cfg` to the root of your cfg folder and use the same auth token you set in config
5. download the [steamworks SDK](https://partner.steamgames.com/downloads/list) dll for version 1.61'
6. put `steam_api64.dll` and `steam_api64.lib` in the root of the repo
7. `uv run main.py`
8. :trollface:

### credits for fish (other than webfishing)
[More Fishing](https://github.com/reallymako/MoreFishingWEBFISHING)

[Fishing Expanded](https://github.com/coolbot100s/FishingExpanded)

[InsaniquariumWEB](https://github.com/MonkeyMan1242/InsaniquariumWEB)

[Webfishing101](https://github.com/Mudkipster/Webfishing101)

[WebValley](https://thunderstore.io/c/webfishing/p/Junohno/WebValley/)

[SuperMarioWeb](https://github.com/MonkeyMan1242/SuperMarioWEB)

[Webnautica](https://github.com/SecondEgg101/Webnautica)

[PortalFish](https://thunderstore.io/c/webfishing/p/Amma/PortalFish/)

[CatchThemAll](https://thunderstore.io/c/webfishing/p/hostileonion/CatchThemAll/)

