import aiohttp

from config import *
from globals import server

LAST_DEATH_COUNT = 3621

async def check_death():
	global LAST_DEATH_COUNT
	global CLIENT_STEAM_ID
	CLIENT_STEAM_ID = server.get_info("provider", "steamid")
	CURRENT_DEATH_COUNT = int(server.get_info("player", "match_stats", "deaths"))
	if server.get_info("player", "steamid") == CLIENT_STEAM_ID:
		if LAST_DEATH_COUNT == 3621:
			LAST_DEATH_COUNT = CURRENT_DEATH_COUNT
		if CURRENT_DEATH_COUNT < LAST_DEATH_COUNT:
			LAST_DEATH_COUNT = 0
		if CURRENT_DEATH_COUNT > LAST_DEATH_COUNT:
			LAST_DEATH_COUNT = CURRENT_DEATH_COUNT
			await on_death()

async def on_death():
	if SHOCKING_ENABLED:
		async with aiohttp.ClientSession() as session:
			try:
				async with session.post(
					API_URL,
					json={
						"shocks": [
							{
								"id": SHOCKER_ID,
								"type": "Shock",
								"intensity": DEATH_SHOCK_STRENGTH,
								"duration": DEATH_SHOCK_DURATION,
							}
						],
						"customName": "Counter Strike GSI Integration",
					},
					headers={"OpenShockToken": API_TOKEN}
				) as response:
					if response.status == 200:
						print("Shocker activated successfully.")
					else:
						print(
							f"Failed to activate shocker. Status code: {response}"
						)
			except aiohttp.ClientError as e:
				print(f"An error occurred: {e}")