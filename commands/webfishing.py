import json
import math
import random

from unit_parse import parser

from command_execution import execute_command
from config import PREFIX
from database import insert_fish, update_balance
from globals import server


def load_json():
	with open("data/webfishing.json", "r", encoding="utf-8") as f:
		data = json.load(f)
	return data


def load_json_alt():
	with open("data/webfishing_alt.json", "r", encoding="utf-8") as f:
		data = json.load(f)
	return data


fish_data = load_json_alt()
item_data = load_json()
loot_tables = {}


class Rarity:
	blue = {
		"name": "Blue",
		"odds": 79.92,
		"color": "",
		"database_id": "blue",
		"price_mult": 1.0,
	}
	purple = {
		"name": "Purple",
		"odds": 15.98,
		"color": "\r",
		"database_id": "purple",
		"price_mult": 1.8,
	}
	pink = {
		"name": "Pink",
		"odds": 3.2,
		"color": "",
		"database_id": "pink",
		"price_mult": 4.0,
	}
	red = {
		"name": "Red",
		"odds": 0.64,
		"color": "",
		"database_id": "red",
		"price_mult": 6.0,
	}
	gold = {
		"name": "Gold",
		"odds": 0.26,
		"color": "",
		"database_id": "gold",
		"price_mult": 10.0,
	}
	contraband = {
		"name": "Contraband",
		"odds": 0.0256,
		"color": "",
		"database_id": "contraband",
		"price_mult": 15.0,
	}

	# blue = {
	# 		"name": "Mil-Spec Grade",
	# 		"odds": 79.92,
	# 		"color": "",
	# 		"database_id": "blue",
	# 		"price_mult": 1.0,
	# 	}
	# 	purple = {
	# 		"name": "Restricted",
	# 		"odds": 15.98,
	# 		"color": "\r",
	# 		"database_id": "purple",
	# 		"price_mult": 4.0,
	# 	}
	# 	pink = {
	# 		"name": "Classified",
	# 		"odds": 3.2,
	# 		"color": "",
	# 		"database_id": "pink",
	# 		"price_mult": 6.0,
	# 	}
	# 	red = {
	# 		"name": "Covert",
	# 		"odds": 0.64,
	# 		"color": "",
	# 		"database_id": "red",
	# 		"price_mult": 10.0,
	# 	}
	# 	gold = {
	# 		"name": "Exceedingly Rare",
	# 		"odds": 0.26,
	# 		"color": "",
	# 		"database_id": "gold",
	# 		"price_mult": 15.0,
	# 	}

	@classmethod
	def getattr(cls, quality):
		"""Retrieve rarity data dynamically by quality name."""
		if hasattr(cls, quality):
			return getattr(cls, quality)
		raise AttributeError(f"No such rarity: {quality}")


async def cast_line(steamid, username):
	catches = 1
	bonus = False
	# TODO: assign maps to tables and maybe other factors (steamid?)
	# fish_table = server.get_info("map", "name")
	fish_table = random.choice([
		"lake",
		"ocean",
		"deep",
		"rain",
		"alien",
		"void",
	])
	rod_cast_data = random.choice([
		"small",
		"sparkling",
		"large",
		"gold",
	])  # maybe implement double fish

	rolls = []

	for _ in range(3):
		roll = await roll_loot_table(fish_table)
		size_calc = await roll_item_size(roll)
		rolls.append([roll, size_calc])

	if rod_cast_data == "small":
		reroll_type = "small"
	if rod_cast_data == "sparkling":
		reroll_type = "tier"
	if rod_cast_data == "large":
		reroll_type = "large"
	if rod_cast_data == "gold":
		reroll_type = "rare"

	chosen = rolls[0]
	for roll in rolls:
		match reroll_type:
			case "none":
				chosen = roll
			case "small":
				if roll[1] < chosen[1]:
					chosen = roll
			case "large":
				if roll[1] > chosen[1]:
					chosen = roll
			case "tier":
				if roll[0]["tier"] > chosen[0]["tier"]:
					chosen = roll
			case "rare":
				if roll[0].get("rare"):
					chosen = roll

	fish_roll = chosen[0]
	size = chosen[1]

	quality = random.choices([Rarity.blue, Rarity.purple, Rarity.pink, Rarity.red, Rarity.gold], weights=[79.92, 15.98, 3.2, 0.64, 0.26])

	if rod_cast_data == "double" and random.random() < 0.15:
		catches = 2
		bonus = True

	for _ in range(catches):
		fish_name = fish_roll["item_name"]
		item_description = fish_roll["item_description"]
		catch_blurb = fish_roll["catch_blurb"]
		quality_name = quality[0]["name"]
		quality = quality[0]["database_id"]
		normalized_size = parser(f"{size} cm")
		price = await calculate_worth(fish_roll, quality, size)

		await insert_fish(fish_name, size, price, quality, steamid, username)
		await update_balance(steamid, price)
		await execute_command(f"say {PREFIX} {username}: 〈͜͡˒ ⋊ You caught a {quality_name} {fish_name}! {catch_blurb} It's {normalized_size} and is worth {price} ₶!", 0.5)


async def calculate_worth(fish_roll, quality, size):
	size_prefix = {
		0.1: 1.75,
		0.25: 0.6,
		0.5: 0.8,
		1.0: 1.0,
		1.5: 1.5,
		2.0: 2.5,
		3.0: 4.25,
	}

	average = fish_roll["average_size"]
	calc = size / average
	mult = 1.0

	for p in size_prefix.keys():
		if p > calc:
			break
		mult = size_prefix[p]

	idata = fish_roll

	value = idata["sell_value"]

	if idata["generate_worth"]:
		t = 1.0 + (0.25 * idata["tier"])
		w = idata["loot_weight"]
		value = pow(5 * t, 2.5 - w)

		if w < 0.4:
			value *= 1.1
		if w < 0.15:
			value *= 1.25
		if w < 0.05:
			value *= 1.5

	worth = math.ceil(value * mult * Rarity.getattr(quality)["price_mult"])

	return worth


async def generate_loot_tables(category, table):
	new_table = {"entries": {}, "total_weight": 0.0}
	total_weight = 0.0

	for item, data in item_data.items():
		if data["category"] == category and data["loot_table"] == table:
			total_weight += data["loot_weight"]
			new_table["entries"][item] = total_weight

	new_table["total_weight"] = total_weight
	loot_tables[table] = new_table
	print(f"Generated Table {table} for category {category}")


async def roll_loot_table(table, max_tier=-1):
	table_data = loot_tables[table]

	for _ in range(20):
		roll = random.uniform(0.0, loot_tables[table]["total_weight"])
		for item, cumulative_weight in table_data["entries"].items():
			if cumulative_weight > roll:
				data = item_data[item]
				if max_tier == -1 or data["tier"] <= max_tier:
					return data


async def roll_item_size(item):
	average_size = item["average_size"]
	deviation = average_size * 0.55
	average_size += average_size * 0.25

	roll = await stepify(random.gauss(average_size, deviation), 0.01)
	roll = round(abs(roll), 2)
	return roll


async def stepify(value, step):
	return round(value / step) * step


# TODO: add the json generation script instead of having already generated jsons, dynamically loading fish on every launch of the bot
