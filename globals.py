import win32gui

from config import GAME, GSI_TOKEN
from gsi.server import GSIServer

# TODO: change gsi library or add type definitions to everything
server = GSIServer(("127.0.0.1", 3000), GSI_TOKEN)

csgo_window_handle = win32gui.FindWindow("Valve001", None)

TEAMS = ["CT", "T", "Terrorist", "Counter-Terrorist"]

last_round = None
last_phase = None

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
]

# https://regex101.com/r/pTapEF/5
csgo_regex = (
	r"(?:\d{2}\/){2}\d{4}\s-\s\d{2}:(?:\d{2}:){2}\s(?P<dead_status>\*DEAD\*)?\s?(?:\((?P<team>[^)]+)\))?\s?(?P<username>.*)‎\s(?:@\s(?P<location>.*))?\s?:(?:\s)*(?P<command>\S+)?\s(?P<args>\S+)?"
)

# https://regex101.com/r/1lYpb1/5
cs2_regex = r"\[(?P<team>ALL|CT|T)\]\s+(?P<username>.*)‎(?:﹫(?P<location>.*))?\s*(?P<dead_status>\[DEAD\])?:(?:\s)?(?P<command>\S+)?\s(?P<args>\S+)?"

if GAME == "csgo":
	COMMAND_REGEX = csgo_regex
else:
	COMMAND_REGEX = cs2_regex


# List of strings to filter out of console output (if the line contains anything in this then it'll be filtered)
PRINT_FILTER = [
	"[InputSystem]",
	"[InputService]",
	"[NetSteamConn]",
	"[Networking]",
	"[Host]",
	"[VProf]",
	"[Client]",
	"[EngineServiceManager][CL CommandQueue]",
	"[SplitScreen]",
	"[RenderSystem]",
	"[Panorama]",
	"[SteamNetSockets]",
	"[RenderPipelineCsgo]",
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
]
