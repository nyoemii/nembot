import asyncio
import os
import traceback
import sys
import threading

from watchdog.observers import Observer

from commands.fetch import find_recently_played
from commands.webfishing import generate_loot_tables, parse_files_in_directory
from config import CONSOLE_FILE, HR_DIRECTORY, HR_ENABLED, HR_FILE, RPC_ENABLED
from console_handler import listen
from database import init_database
from globals import server, app, ui_instance, COMMAND_QUEUE
from loop.deathchecking import check_death
from loop.discord_rpc import DiscordManager
from loop.heartrate import FileUpdateHandler
from loop.roundtracking import check_round
from processor import check_requirements, process_commands
from util.ui import UI


async def main_loop():
	"""
	Main loop for the bot, handles checking for commands, checking if the user is dead, and checking for round changes.
	"""
	started = False
	while True:
		await check_death()
		await process_commands()
		await check_requirements()
		await check_round()
		ui_instance.update_command_status(f"{len(COMMAND_QUEUE)} commands in queue.")
		await asyncio.sleep(0.05)
		if not started:
			ui_instance.update_status("Bot started")
			started = True


async def rpc_loop():
	"""
	Loop for updating the Discord RPC
	"""
	while True:
		await asyncio.sleep(1)
		presence = await DiscordManager.build_presence_from_data(server)
		await DiscordManager.update_presence(presence)


async def shutdown(observer, server):
	"""
	Shutdown the server and observer.

	:param observer: The observer instance
	:param server: The server instance
	"""
	ui_instance.update_status("Shutting down...")
	try:
		observer.stop()
		server.shutdown()

		tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
		[task.cancel() for task in tasks]
		await asyncio.gather(*tasks, return_exceptions=True)
		if HR_ENABLED:
			observer.join()
	except Exception as e:
		print(f"Error during shutdown: {e}")


async def start_server(ui_instance: UI):
	"""
	Start the server and initialize all necessary components.
	"""
	ui_instance.update_status("Starting server...")
	try:
		# make sure steam dll exists
		if os.path.exists("./steam_api64.dll"):
			pass
		else:
			ui_instance.update_status("Steamworks API dll not found.")
			raise Exception("Steamworks API dll not found.")

		server.start_server()

		if RPC_ENABLED:
			ui_instance.update_status("Initializing Discord RPC...")
			await DiscordManager.initialize()

		ui_instance.update_status("Initializing event handler...")
		event_handler = FileUpdateHandler(f"{HR_DIRECTORY + HR_FILE}")
		observer = Observer()
		if HR_ENABLED:
			ui_instance.update_status("Starting Heart Rate observer...")
			observer.schedule(event_handler, HR_DIRECTORY, recursive=False)
			observer.start()

		ui_instance.update_status("Initializing database...")
		await init_database()
		await find_recently_played()
		ui_instance.update_status("Generating loot tables...")

		await parse_files_in_directory("data/webfishing", 1)
		await generate_loot_tables("fish", "lake")
		await generate_loot_tables("fish", "ocean")
		await generate_loot_tables("fish", "rain")
		await generate_loot_tables("fish", "alien")
		await generate_loot_tables("fish", "void")
		await generate_loot_tables("fish", "water_trash")
		await generate_loot_tables("fish", "metal")

		log_file = open(CONSOLE_FILE, "r", encoding="utf-8", errors="replace")

		ui_instance.update_status("Starting main loop...")
		await asyncio.gather(main_loop(), rpc_loop(), listen(log_file))
	except Exception as e:
		print("Error during startup.")
		print_traceback(e)
	finally:
		await shutdown(observer, server)


def print_traceback(err):
	print("".join(traceback.format_exception(type(err), err, err.__traceback__)))


def start_bot(ui_instance):
	try:
		asyncio.run(start_server(ui_instance))
	except KeyboardInterrupt:
		print("Shutting down...")
	except Exception as e:
		print(f"Error: {e}")


if __name__ == "__main__":
	bot_thread = threading.Thread(target=start_bot, args=(ui_instance,))
	bot_thread.daemon = True  # Ensure the thread exits when the main program exits
	bot_thread.start()
	exit_code = app.exec()
	sys.exit(exit_code)
