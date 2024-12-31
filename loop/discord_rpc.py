import asyncio

from pypresence import AioPresence

# yeah i'm gonna be totally honest i literally just asked chatgpt to adapt this from a C# RPC app to python (lazy)


class DiscordManager:
	CLIENT_ID = "1321313746362302464"
	client = None
	connected = False

	@classmethod
	async def initialize(cls):
		"""Initialize the Discord RPC client."""
		cls.client = AioPresence(cls.CLIENT_ID)
		try:
			await cls.client.connect()
			cls.connected = True
			print("[DISCORD] RPC Initialized and connected.")
		except Exception:
			cls.connected = False
			await asyncio.sleep(5)
			await cls.initialize()

	@classmethod
	async def update_presence(cls, presence):
		"""Update the Discord presence safely."""
		if not cls.connected:
			return
		try:
			await cls.client.update(**presence)
		except Exception:
			print("[DISCORD] Attempting to reconnect in 5 seconds...")
			await asyncio.sleep(5)
			await cls.initialize()

	@staticmethod
	async def build_presence_from_data(server):
		"""Build rich presence based on game data."""
		# Default presence set to menu.
		presence = {
			"details": "Main Menu",
			"state": "In Menu",
			"large_image": "menu",
			"large_text": "Menu",
		}

		# Retrieve game data from the server.
		provider = server.get_info("provider")
		map_data = server.get_info("map")
		player_data = server.get_info("player")

		# Handle bad or missing data early.
		if not (provider and map_data and player_data):
			return presence

		# Check if the player is actively playing.
		if player_data.get("activity") == "playing":
			map_name = map_data.get("name")
			mode = map_data.get("mode")
			phase = map_data.get("phase")

			presence.update({
				"large_image": map_name,
				"large_text": f"Playing on {map_name}",
			})

			fixed_mode_name = None

			# Define custom gamemode names.
			if mode == "scrimcomp2v2":
				fixed_mode_name = "Wingman"
			elif mode == "gungameprogressive":
				fixed_mode_name = "Armsrace"
			elif mode == "gungametrbomb":
				fixed_mode_name = "Demolition"
			elif mode == "cooperative":
				fixed_mode_name = "Guardian"
			elif mode == "coopmission":
				fixed_mode_name = "Co-Op Strike"
			elif mode == "survival":
				fixed_mode_name = "Danger Zone"

			mode_name = fixed_mode_name or mode.capitalize()

			if mode in ["casual", "competitive", "scrimcomp2v2"]:
				presence.update({
					"details": f"{player_data.get('activity', '').capitalize()} {mode_name}",
					"state": f"{phase.capitalize()} - CT: {map_data.get('team_ct', {}).get('score', 0)} | {map_data.get('team_t', {}).get('score', 0)} :T",
				})

				if provider.get("steamid") == player_data.get("steamid") and player_data.get("name") != "unconnected" and player_data["state"].get("health", 0) > 0:
					presence.update({
						"small_image": f"{player_data.get('team').lower()}_logo",
						"small_text": f"Playing as {player_data.get('team')}",
					})
				else:
					presence.update({
						"details": f"Watching {mode_name}",
						"small_image": mode,
						"small_text": "Spectating/Observing",
					})

			elif mode in ["gungameprogressive", "gungametrbomb", "deathmatch"]:
				presence.update({
					"details": f"{player_data.get('activity').capitalize()} {mode_name}",
					"state": f"{phase.capitalize()} - Kills: {player_data['match_stats'].get('kills', 0)}",
					"small_image": mode,
					"small_text": mode_name,
				})

			elif mode == "training":
				presence.update({"details": "Training"})

			elif mode in ["cooperative", "coopmission"]:
				presence.update({
					"details": f"{player_data.get('activity').capitalize()} {mode_name}",
					"state": f"Defending the objective - Kills: {player_data['match_stats'].get('kills', 0)}",
					"small_image": mode,
					"small_text": mode_name,
				})

			elif mode == "survival":
				state = "Alive" if player_data["state"].get("health", 0) > 0 else "Dead"
				presence.update({
					"details": f"{player_data.get('activity').capitalize()} {mode_name}",
					"state": f"Status: {state} - Kills: {player_data['match_stats'].get('kills', 0)}",
					"small_image": mode,
					"small_text": mode_name,
				})

			else:
				presence.update({
					"details": "Custom Gamemode",
					"state": "No Data",
					"small_image": "default",
				})

		return presence
