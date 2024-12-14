import asyncio
import json
import os
import random

from godot_parser import load, parse

from commands.fetch import find_recently_played
from config import PREFIX
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


async def cast_line(cmd, arg, user, team, dead, location):
	# TODO: assign maps to tables and maybe other factors (steamid?)
	# fish_table = server.get_info("map", "name")
	fish_table = "lake"

	rolls = []

	for _ in range(3):
		roll = await roll_loot_table(fish_table)
		size = await roll_item_size(roll)
		rolls.append([roll, size])


async def generate_loot_tables(category, table):
	new_table = {"entries": {}, "total_weight": 0.0}

	for fish_category in fish_data:
		for item, data in item_data.items():
			if data["category"] == category and data["loot_table"] == table:
				new_table["total_weight"] += data["loot_weight"]
				new_table["entries"][item] = new_table["total_weight"]

	loot_tables[table] = new_table
	print(f"Generated Table {table} for category {category}")


async def roll_loot_table(table, max_tier=-1):
	table_data = loot_tables[table]
	table_total_weight = table_data["total_weight"]

	for _ in range(20):
		roll = random.uniform(0.0, table_total_weight)
		for item, cumulative_weight in table_data["entries"].items():
			if cumulative_weight > roll:
				data = item_data[item]
				if max_tier == -1 or data["tier"] <= max_tier:
					return data


async def roll_item_size(item):
	print(item)
	average_size = item["average_size"]
	deviation = average_size * 0.55
	average_size += average_size * 0.25

	roll = await stepify(random.gauss(average_size, deviation), 0.01)
	roll = round(abs(roll), 2)
	return roll


async def stepify(value, step):
	return round(value / step) * step


# TODO: add the json generation script
