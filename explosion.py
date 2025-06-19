import asyncio
import traceback


from config import RPC_ENABLED
from globals import server
from loop.deathchecking import check_death
from loop.discord_rpc import DiscordManager


async def main_loop():
	"""
	Main loop for the bot, handles checking for commands, checking if the user is dead, and checking for round changes.
	"""
	while True:
		await check_death()
		await asyncio.sleep(0.05)


async def rpc_loop():
	"""
	Loop for updating the Discord RPC
	"""
	while True:
		await asyncio.sleep(1)
		presence = await DiscordManager.build_presence_from_data(server)
		await DiscordManager.update_presence(presence)


async def shutdown(server):
	"""
	Shutdown the server and observer.

	:param observer: The observer instance
	:param server: The server instance
	"""
	try:
		server.shutdown()

		tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
		[task.cancel() for task in tasks]
		await asyncio.gather(*tasks, return_exceptions=True)
	except Exception as e:
		print(f"Error during shutdown: {e}")


async def start_server():
	"""
	Start the server and initialize all necessary components.
	"""
	try:
		server.start_server()

		if RPC_ENABLED:
			await DiscordManager.initialize()

		await asyncio.gather(main_loop(), rpc_loop())
	except Exception as e:
		print("Error during startup.")
		print_traceback(e)
	finally:
		await shutdown(server)


def print_traceback(err):
	print("".join(traceback.format_exception(type(err), err, err.__traceback__)))


if __name__ == "__main__":
	try:
		asyncio.run(start_server())
	except KeyboardInterrupt:
		print("Shutting down...")
	except Exception as e:
		print(f"Error: {e}")
