import json
import random

import aiohttp


async def get_fact():
	if random.random() <= 0.1:  # 10% chance for local fact
		fact = await get_local_fact()
	else:
		fact = await get_api_fact()
	return fact


async def get_api_fact():
	url = "https://uselessfacts.jsph.pl/api/v2/facts/random"

	async with aiohttp.ClientSession() as session:
		async with session.get(url) as response:
			if response.status == 200:
				data = await response.json()
				fact = data.get("text")
			else:
				fact = f"Error: {response.status}"
	return fact


async def get_local_fact():
	try:
		with open("data/facts.json", "r") as f:
			facts = json.load(f)
		fact = random.choice(facts) if facts else "No facts available."
	except Exception as e:
		fact = f"Error: {str(e)}"
	return fact
