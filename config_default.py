GAME = "cs2"

# cs2 config
CS2_CONSOLE_FILE = "path/to/console.log"
# put at root of cfg folder
CS2_EXEC_FILE = "path/to/selfbot.cfg"

# unused atm, may use again later
DROP_KEY = "g"
SWITCH_HANDS_KEY = "c"

# csgo config
CSGO_CONSOLE_FILE = "path/to/console.log"
# unused, just for compatibility with shit code :3
CSGO_EXEC_FILE = "path/to/selfbot.cfg"

if GAME == "csgo":
	CONSOLE_FILE = CSGO_CONSOLE_FILE
	EXEC_FILE = CSGO_EXEC_FILE
else:
	CONSOLE_FILE = CS2_CONSOLE_FILE
	EXEC_FILE = CS2_EXEC_FILE


# hehe jonathan (you can change it to whatever, just make sure you keep it consistent)
DATABASE_NAME = "jonathan.db"

# recommend subtext here for the text
PREFIX = "ɴᴇᴍʙᴏᴛ »"

# https://openshock.org stuff
DEATH_SHOCK_STRENGTH = 60
DEATH_SHOCK_DURATION = 1500
SHOCKING_ENABLED = True

API_TOKEN = "your openshock api token"
API_URL = "https://api.openshock.app/2/shockers/control"
SHOCKER_ID = "your openshock shocker id"

RPC_ENABLED = True

# auto translation of chat messages
LANGUAGE_DETECTION = True

# token used for GSI in CS (put in auth field of your gamestate_integration_GSI.cfg)
GSI_TOKEN = "your gsi token"


# only usable on classiccounter if you have my steamid, aka irrelevant
HR_ENABLED = False
HR_FILE = "heartrate.txt"
HR_DIRECTORY = "E:/Media Library/"
