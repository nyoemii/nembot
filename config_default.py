# "cs2" or "csgo"
GAME = "cs2"

CS2_CONSOLE_FILE = "C:\Program Files (x86)\Steam\steamapps\common\Counter-Strike Global Offensive\game\csgo\console.log"
# file that gets written to for command execution
CS2_EXEC_FILE = "C:\Program Files (x86)\Steam\steamapps\common\Counter-Strike Global Offensive\game\csgo\cfg\selfbot.cfg"

CSGO_CONSOLE_FILE = "C:\path\to\your\console.log"
# unused in csgo, just here bc i cannot be fucked to properly account for it
CSGO_EXEC_FILE = "D:\selfbot.cfg"

GSI_TOKEN = "S8RL9Z6Y22TYQK45JB4V8PHRJJMD9DS9"
PREFIX = "ɴᴇᴍʙᴏᴛ »"
COMMAND_PREFIX = "!"

# hehe jonathan (literally any filename works)
DATABASE_NAME = "jonathan.db"

# discord rpc
RPC_ENABLED = True
# auto translation of messages
LANGUAGE_DETECTION = False


OPENSHOCK_ENABLED = True

OPENSHOCK_STRENGTH_RANGE = 30, 75  # in percent, min 0, max 100
OPENSHOCK_DURATION_RANGE = 300, 3000  # in millseconds, min 300, max 30000
# Types: "Shock", "Vibrate", "Sound"
OPENSHOCK_TYPE = "Shock"
OPENSHOCK_API_TOKEN = ""
OPENSHOCK_API_URL = "https://api.openshock.app/2/shockers/control"
OPENSHOCK_SHOCKER_LIST = [
	"example-id-1",
	"example-id-2",
	"example-id-3",
	"example-id-4",
]
# Types: "random", "one", "all" (one chooses first in list)
OPENSHOCK_PUNISHMENT_TYPE = "random"


# specific to me, only works on classiccounter if you have my steamid (plugin may have also been removed from their servers)
HR_ENABLED = False
HR_FILE = "heartrate.txt"
HR_DIRECTORY = "E:/Media Library/"

# unused
DROP_KEY = "g"
SWITCH_HANDS_KEY = "c"


# don't change

if GAME == "csgo":
	CONSOLE_FILE = CSGO_CONSOLE_FILE
	EXEC_FILE = CSGO_EXEC_FILE
else:
	CONSOLE_FILE = CS2_CONSOLE_FILE
	EXEC_FILE = CS2_EXEC_FILE
