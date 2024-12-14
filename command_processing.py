import asyncio
import re
from collections import deque

from command_execution import execute_command
from commands.fact import get_fact

# from commands.fish import cast_line, cast_line_team
from commands.webfishing import cast_line
from config import PREFIX
from database import insert_command
from globals import COMMAND_LIST, COMMAND_REGEX, TEAMS, server

COMMAND_QUEUE = deque()


async def parse(line):
	regex = re.search(COMMAND_REGEX, line, flags=re.UNICODE | re.VERBOSE)
	if regex:
		team = regex.group("team")
		username = regex.group("username")
		location = regex.group("location")
		dead = regex.group("dead_status")
		command = regex.group("command")
		args = regex.group("args")
	else:
		team = ""
		username = ""
		location = ""
		dead = ""
		command = ""
		args = ""

	# print(f"Team: {team}\nUsername: {username}\nLocation: {location}\nDead: {dead}\nCommand: {command}\nArgs: {args}")

	# * this doesn't account for commands that haven't been executed yet
	if command.lower() in COMMAND_LIST:
		timestamp = server.get_info("provider", "timestamp")
		command_data = command.replace("!", "")
		await insert_command(username, command_data, team, dead, location, timestamp)
		COMMAND_QUEUE.append((command, args, username, team, dead, location))


async def check_requirements():
	global should_process_commands
	# active_window_handle = win32gui.GetForegroundWindow()
	# _, pid = win32process.GetWindowThreadProcessId(active_window_handle)

	# if pid > 0:
	#     try:
	#         process = psutil.Process(pid)
	#         process_name = process.name()
	#     except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
	#         print("Unable to retrieve process info.")
	#         return False
	# else:
	#     print("Invalid PID or no valid window is currently focused.")
	#     return False

	if server.get_info("map", "phase") == "live":
		should_process_commands = True
		return True

	should_process_commands = False
	return False


async def process_commands():
	if await check_requirements():
		if COMMAND_QUEUE:
			cmd, arg, user, team, dead, location = COMMAND_QUEUE.popleft()
			await asyncio.sleep(0.25)
			await switchcase_commands(cmd, arg, user, team, dead, location)


async def switchcase_commands(cmd, arg, user, team, dead, location):
	# TODO: maybe pass user to commmand execution check if it's me so that execute_command_cs2 doesn't need wacky 3621 delay shit... it is kinda funny tho :3
	cmd = cmd.lower()
	match cmd:
		# case "!disconnect" | "!dc":
		#     await execute_command("disconnect", 0.5)
		# case "!quit" | "!q":
		#     await execute_command("quit", 0.5)
		case "!i":
			if team in TEAMS:
				if arg:
					inspect_link = re.search(
						r"steam:\/\/rungame\/730\/[0-9]+\/\+csgo_econ_action_preview%20([A-Za-z0-9]+)",
						arg,
					)
					if inspect_link:
						await execute_command(f"gameui_activate;csgo_econ_action_preview {inspect_link.group(1)}\n say {PREFIX} Opened inspect link on my client.")
					else:
						await execute_command(f"say {PREFIX} Invalid inspect link.")
				else:
					await execute_command(f"say {PREFIX} No inspect link provided.")
			else:
				pass
		case "!switchhands":
			if team in TEAMS:
				await execute_command(f"switchhands\nsay_team {PREFIX} Switched viewmodel.")
			else:
				pass
		case "!flash":
			if team in TEAMS:
				await execute_command(f"say_team {PREFIX} fuck you.")
				for _ in range(13):
					await execute_command("flashbangs", 3621)
					await asyncio.sleep(0.01 / 13)
			else:
				pass
		case "!fish" | "!〈͜͡˒":  # regex would need to be changed to properly match the fish kaomoji: !〈͜͡˒ ⋊
			if team in TEAMS:
				await cast_line(cmd, arg, user, team, dead, location)
			elif not dead:
				await cast_line(cmd, arg, user, team, dead, location)
			else:
				await execute_command(f"say {PREFIX} You cannot fish while dead.")
		case "!info":
			if team in TEAMS:
				await execute_command(f"say_team {PREFIX} github.com/Pandaptable/nembot, reads console.log and parses chat through it (aka not a cheat)")
			else:
				await execute_command(f"say {PREFIX} github.com/Pandaptable/nembot, reads console.log and parses chat through it (aka not a cheat)")
		case "!location":
			if team in TEAMS:
				message = "you're dead dumbass." if dead else f"Your current location: {location}"
				await execute_command(f"say_team {PREFIX} {message}")
		case "!fact":
			if team in TEAMS:
				fact = await get_fact()
				await execute_command(f"say_team {PREFIX} {fact}")
			else:
				fact = await get_fact()
				await execute_command(f"say {PREFIX} {fact}")
		case "!drop":
			if team in TEAMS:
				await execute_command("drop", 3621)  # funny 3621 placeholder for shit code to execute with 0 delay
			else:
				pass
		case "!help" | "!commands" | "!cmds":
			if team in TEAMS:
				await execute_command(f"say_team {PREFIX} !help | !fish or !〈͜͡˒ ⋊  | !fact | !i <inspect link> | !info (info on the bot) | !location | !drop | !flash | !switchhands")
			else:
				await execute_command(f"say {PREFIX} !help | !fish or !〈͜͡˒ ⋊  | !fact | !info (info on the bot)")
