import asyncio
import os

from watchdog.observers import Observer

from command_processing import check_requirements, parse, process_commands
from commands.fetch import find_recently_played
from commands.webfishing import generate_loot_tables, parse_files_in_directory
from config import CONSOLE_FILE, HR_DIRECTORY, HR_FILE
from database import init_database
from globals import PRINT_FILTER, server
from loop.deathchecking import check_death
from loop.discord_rpc import DiscordManager
from loop.heartrate import FileUpdateHandler
from loop.roundtracking import check_round


async def listen(log_file):
	log_file.seek(0, os.SEEK_END)
	last_size = log_file.tell()

	while True:
		current_size = os.stat(log_file.name).st_size
		if current_size < last_size:
			log_file.seek(0, os.SEEK_SET)
			last_size = current_size

		line = log_file.readline()
		if not line:
			await asyncio.sleep(0.1)
			continue

		if not any(filter_text in line for filter_text in PRINT_FILTER):
			print(line.strip())
			await parse(line)
		last_size = log_file.tell()


async def main_loop():
	while True:
		await check_death()
		await process_commands()
		await check_requirements()
		await check_round()
		await asyncio.sleep(0.05)


async def rpc_loop():
	while True:
		await asyncio.sleep(1)
		presence = DiscordManager.build_presence_from_data(server)
		await DiscordManager.update_presence(presence)


async def shutdown(observer, server):
	print("Shutting down...")
	observer.stop()
	server.shutdown()

	tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
	[task.cancel() for task in tasks]
	await asyncio.gather(*tasks, return_exceptions=True)
	observer.join()


async def start_server():
	server.start_server()

	await DiscordManager.initialize()

	event_handler = FileUpdateHandler(f"{HR_DIRECTORY + HR_FILE}")
	observer = Observer()
	observer.schedule(event_handler, HR_DIRECTORY, recursive=False)
	observer.start()

	await init_database()
	await find_recently_played()
	await parse_files_in_directory("data/webfishing", 1)
	await generate_loot_tables("fish", "lake")
	await generate_loot_tables("fish", "ocean")
	await generate_loot_tables("fish", "rain")
	await generate_loot_tables("fish", "alien")
	await generate_loot_tables("fish", "void")

	await generate_loot_tables("fish", "water_trash")

	# await generate_loot_tables("none", "seashell")
	# await generate_loot_tables("none", "trash")

	await generate_loot_tables("fish", "metal")

	try:
		log_file = open(CONSOLE_FILE, "r", encoding="utf-8")
		await asyncio.gather(main_loop(), rpc_loop(), listen(log_file))
	except asyncio.CancelledError:
		pass
	finally:
		await shutdown(observer, server)


if __name__ == "__main__":
	try:
		asyncio.run(start_server())
	except KeyboardInterrupt:
		print("Shutting down...")
