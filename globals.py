import win32gui

from config import GAME, GSI_TOKEN
from gsi.server import GSIServer

server = GSIServer(("127.0.0.1", 3000), GSI_TOKEN)

csgo_window_handle = win32gui.FindWindow("Valve001", None)

TEAMS = ["CT", "T", "Terrorist", "Counter-Terrorist"]

last_round = None
last_phase = None

command_list = ["!disconnect", "!dc", "!q", "!quit", "!i", "!switchhands", "!play", "!flash", "!fish", "!〈͜͡˒", "!info", "!location", "!fact", "!drop", "!fetch"]

# https://regex101.com/r/pTapEF/3
csgo_regex = r"(?:\d{2}\/){2}\d{4}\s-\s\d{2}:(?:\d{2}:){2}\s(?P<dead_status>\*DEAD\*)?\s?(?:\((?P<team>[^)]+)\))?\s?(?P<username>.*)‎\s(?:@\s(?P<location>\w+))?\s?:(?:\s)*(?P<command>\S+)?\s(?P<args>\S+)?"

# https://regex101.com/r/1lYpb1/2
cs2_regex = r"\[(?P<team>ALL|CT|T)\]\s+(?P<username>.*)‎(?:﹫(?P<location>\w+))?\s*(?P<dead_status>\[DEAD\])?:(?:\s)?(?P<command>\S+)?\s(?P<args>\S+)?"

if GAME == "csgo":
	command_regex = csgo_regex
else:
	command_regex = cs2_regex


# List of strings to filter out of console output (if the line contains anything in this then it'll be filtered)
PRINT_FILTER = [
    "[InputSystem]",
    "[InputService]",
    "[NetSteamConn]",
    "[Networking]",
    "[Host]",
    "[VProf]",
    "[Client]",
    "**** Panel",
    "[CL CommandQueue]",
    "[SplitScreen]",
    "[RenderSystem]",
    "execing selfbot"
    ]
