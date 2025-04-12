import asyncio
import json

import aiohttp
from thefuzz import process

from command_execution import execute_command
from config import PREFIX


async def open_container(container_name, username, steamid, team):
	if not container_name:
		await execute_command(f"say {PREFIX} No container name provided")
		return
	containers = await load_containers()
	# fuzzy search for container
	print(container_name)
	container_matches = process.extract(container_name, [container["name"] for container in containers], limit=None)
	print(container_matches)
	# remove results that don't contain all words present in container_name
	filtered_matches = [name for name in container_matches if all(word.lower() in name[0].lower() for word in container_name.lower().split())]
	if not filtered_matches:
		await execute_command(f"say {PREFIX} No matching containers found")
		return
	matched_containers = [container for container in containers if container["name"] in [match[0] for match in filtered_matches]]
	print(matched_containers[0])
	# search through contains list to get all rarities available in a case, if contains_rare list also exists then add gold to rarity list
	contains = matched_containers[0]["contains"]
	rarity_list = []
	for item in contains:
		rarity_id = item["rarity"]["id"]
		if any(rarity_id.startswith(prefix) for prefix in ["rarity_rare", "rarity_mythical", "rarity_legendary", "rarity_ancient"]) and rarity_id not in rarity_list:
			rarity_list.append(rarity_id)
	if matched_containers[0]["contains_rare"] and "gold" not in rarity_list:
		rarity_list.append("gold")
	print(rarity_list)


async def load_containers() -> dict:
	async with aiohttp.ClientSession() as session:
		async with session.get("https://bymykel.github.io/CSGO-API/api/en/crates.json") as response:
			if response.status == 200:
				data = await response.json()
			else:
				raise Exception(f"Error: {response.status}")
	return data
