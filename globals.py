import win32gui

from config import GAME, GSI_TOKEN
from gsi.server import GSIServer
from util.signal import EventSignal

BANNED_LIST = [
	76561198055654571,
	76561198162871889,
	76561198398160009,
	76561198189637015,
]


COMMAND_LIST = [
	"!i",
	"!switchhands",
	"!flash",
	"!fish",
	"!〈͜͡˒",
	"!info",
	"!location",
	"!fact",
	"!drop",
	"!help",
	"!commands",
	"!cmds",
	"!balance",
	"!bal",
	"!money",
	"!steamid",
	"!heartrate",
	"!hr",
]


# List of strings to filter out of console output (if the line contains anything in this then it'll be filtered)
PRE_FILTER = [
	"[InputSystem]",
	"[InputService]",
	"[NetSteamConn]",
	"[Networking]",
	"[Host]",
	"[VProf]",
	"[Client]",
	"[EngineServiceManager]",
	"[CL CommandQueue]",
	"[SplitScreen]",
	"[RenderSystem]",
	"[Panorama]",
	"[SteamNetSockets]",
	"[RenderPipelineCsgo]",
	"[VScript]",
	"[stringtables]",
	"[SignonState]",
	"[WorldRenderer]",
	"[AnimResource]",
	"[ResourceSystem]",
	"[SoundSystem]",
	"[Shooting]",
	"[HostStateManager]",
	"[Server]",
	"[BuildSparseShadowTree]",
	"[SteamAudio]",
	"execing selfbot",
	"execing movement/de-subticks/",
	"Invalid content height",
	"Certificate expires in",
	"**** Panel",
	"Interpreting bind command as:",
	"CCSGO_BlurTarget",
	"Entry player was not found",
	"CPlayerVoiceListener",
	"GameTypes: missing",
	"Unable to read",
	"failed to load file",
	"CNavGenParams",
	"failed to find",
	"Telling Steam not to update",
	"Telling Steam it is safe",
	"**** Unable",
	"ms Client",
	"ms FileSystem",
	"ms Prediction",
	"ms Frame",
	"ms SDL",
	"PlayerStatsUpdate",
	"used during construction differ",
	"Invalid image URL",
	"ReadSteamRemoteStorageFile",
	"CAnimGraphNetworkedVariables::",
	"CAsyncWriteInProgress::",
	"WriteSteamRemoteStorageFileAsync",
	"ChangeGameUIState",
	"This is usually a symptom of a general performance problem such as thread starvation.",
	"Obtained direct RTT measurements to relays in",
	"CS_App_Lifetime_Gamestats:",
	"Inventory filter setting",
	"Ping measurement completed after",
	"via direct route",
	"(This list may include POPs without any gameservers)",
	"Measured RTT to",
	"SDR ping location:",
	"Forcing SDR connection to",
	"Received SDR ticket for [",
	"Confirmation number",
	"Excessive frame time of ",
	"Present_RenderDevice",
	" not found in map ",
	"Unknown command: sellback",
	"CreateProceduralSfx:",
	"Ping measurement has been active for ",
	"    bind scancode",
	"Executing server command (",
	"ResetBreakpadAppId: ",
	"Logging into anonymous listen server account.",
	"Setting mapgroup to ",
	"Invalid counterterrorist spawnpoint",
	"Invalid terrorist spawnpoint",
	"Achievements disabled: cheats turned on in this app session.",
	"6ms Server ",
	"missing sounds dir. Fixing for now.",
	"[SoundSystemLowLevel]",
	"models/hostage/v_hostage_arm.vmdl :: draw",
]

REGION_FILTER = [
	"ord:",
	"atl:",
	"iad:",
	"dfw:",
	"dfw2:",
	"sea:",
	"lax:",
	"lhr:",
	"par:",
	"ams4:",
	"ams:",
	"sto:",
	"sto2:",
	"fra:",
	"waw:",
	"eat:",
	"hel:",
	"mad:",
	"vie:",
	"tyo:",
	"eze:",
	"seo:",
	"hkg4:",
	"can:",
	"cant:",
	"pwg:",
	"canm:",
	"tgdm:",
	"shb:",
	"pvgt:",
	"canu:",
	"pwj:",
	"pwz:",
	"pww:",
	"maa2:",
	"pwu:",
	"bom2:",
]

PRINT_FILTER = PRE_FILTER + REGION_FILTER


# https://regex101.com/r/pTapEF/5
csgo_regex = (
	r"(?:\d{2}\/){2}\d{4}\s-\s\d{2}:(?:\d{2}:){2}\s(?P<dead_status>\*DEAD\*)?\s?(?:\((?P<team>[^)]+)\))?\s?(?P<username>.*)‎\s(?:@\s(?P<location>.*))?\s?:(?:\s)*(?P<command>\S+)?\s(?P<args>\S+)?"
)

# https://regex101.com/r/1lYpb1/6
cs2_regex = r"\[(?P<team>ALL|CT|T)\]\s+(?P<username>.*)‎(?:﹫(?P<location>.*))?\s*(?P<dead_status>\[DEAD\])?:(?:\s)*(?P<command>\S+)?\s(?P<args>\S+)?"


if GAME == "csgo":
	COMMAND_REGEX = csgo_regex
else:
	COMMAND_REGEX = cs2_regex

CLIENT_ID = 872181511334543370

# TODO: change gsi library or add type definitions to everything
server = GSIServer(("127.0.0.1", 3000), GSI_TOKEN)

csgo_window_handle = win32gui.FindWindow("Valve001", None)

TEAMS = ["CT", "T", "Terrorist", "Counter-Terrorist"]

last_round = None
last_phase = None
nonce_signal = EventSignal()
