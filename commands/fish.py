import asyncio
import json
import math
import random
from datetime import datetime
from enum import Enum

from command_execution import execute_command
from config import PREFIX


class TimeOfDay(Enum):
	Morning = 0
	Afternoon = 1
	Evening = 2
	Night = 3


class SeaWeatherCondition(Enum):
	ClearSkies = 0
	PartlyCloudy = 1
	Overcast = 2
	Fog = 3
	Rain = 4
	Thunderstorms = 5
	Windy = 6
	Calm = 7


class FishData:
	def __init__(self):
		self.Categories = []


class FishCategory:
	def __init__(self):
		self.Rarity = ""
		self.FishList = []


class Fish:
	def __init__(self):
		self.Name = ""
		self.Price = 0.0
		self.Weight = None


class FishWeight:
	def __init__(self):
		self.Min = 0.0
		self.Max = 0.0


async def cast_line(username):
	# time.sleep(1)
	# write_command(f"say {PREFIX} ♌︎ Player {username} is casting their line...")
	# press_key()
	weather = get_weather()
	# time.sleep(1)
	# write_command(f"say {PREFIX} {username}: ☁︎ You casted your line on {weather[1]} weather")
	# press_key()
	await asyncio.sleep(0.5)
	if random.randint(0, 2) == 0:
		await execute_command(
			f"say {PREFIX} {username}: (ó﹏ò｡) You didnt catch anything, try again later...",
			0.25,
		)
	else:
		fish_name, price, weight = get_fish_result(weather[0])
		await execute_command(
			f"say {PREFIX} {username}: 〈͜͡˒ ⋊ You caught a {fish_name}! ⚖️ It weighs {round(weight, 2)}kg and is worth around ${round(price, 2)}",
			0.25,
		)


async def cast_line_team(username):
	# time.sleep(1)
	# write_command(f"say {PREFIX} ♌︎ Player {username} is casting their line...")
	# press_key()
	weather = get_weather()
	# time.sleep(1)
	# write_command(f"say {PREFIX} {username}: ☁︎ You casted your line on {weather[1]} weather")
	# press_key()
	await asyncio.sleep(0.5)
	if random.randint(0, 2) == 0:
		await execute_command(
			f"say_team {PREFIX} {username}: (ó﹏ò｡) You didnt catch anything, try again later...",
			0.25,
		)
	else:
		fish_name, price, weight = get_fish_result(weather[0])
		await execute_command(
			f"say_team {PREFIX} {username}: 〈͜͡˒ ⋊ You caught a {fish_name}! ⚖️ It weighs {round(weight, 2)}kg and is worth around ${round(price, 2)}",
			0.25,
		)


def load_fish_db():
	with open("data/fishbase.json", "r") as file:
		json_data = file.read()
		fish_data = json.loads(json_data)
	return fish_data


def get_fish_result(sea_weather):
	fish_data = load_fish_db()
	if fish_data:
		rarity_modifier = get_rarity_modifier(sea_weather)
		rarity_roll = random.random()
		chosen_rarity = choose_rarity(rarity_roll, fish_data["Categories"], rarity_modifier)

		chosen_category = next(
			(category for category in fish_data["Categories"] if category["Rarity"] == chosen_rarity),
			None,
		)
		if chosen_category:
			fish_list = chosen_category["FishList"]
			chosen_fish = random.choice(fish_list)
			random_weight = random.uniform(chosen_fish["Weight"]["Min"], chosen_fish["Weight"]["Max"])
			usd_price = chosen_fish["Price"] * random_weight
			return chosen_fish["Name"], usd_price, random_weight
	else:
		raise ValueError("fishData was null")


def get_weather():
	forecasted_weather = forecast_sea_weather()
	weather_description = get_weather_description(forecasted_weather)
	return forecasted_weather, weather_description


def forecast_sea_weather():
	current_time_of_day = get_current_time_of_day()
	base_condition = {
		TimeOfDay.Morning: SeaWeatherCondition.ClearSkies,
		TimeOfDay.Afternoon: SeaWeatherCondition.PartlyCloudy,
		TimeOfDay.Evening: SeaWeatherCondition.Overcast,
		TimeOfDay.Night: SeaWeatherCondition.ClearSkies,
	}.get(current_time_of_day, SeaWeatherCondition.ClearSkies)

	if random.random() <= 0.25:
		base_condition = random.choice(list(SeaWeatherCondition))

	return base_condition


def get_current_time_of_day():
	current_hour = datetime.now().hour

	if 6 <= current_hour < 12:
		return TimeOfDay.Morning
	elif 12 <= current_hour < 18:
		return TimeOfDay.Afternoon
	elif 18 <= current_hour < 24:
		return TimeOfDay.Evening
	else:
		return TimeOfDay.Night


def get_weather_description(condition):
	return {
		SeaWeatherCondition.ClearSkies: "Clear skies with calm seas",
		SeaWeatherCondition.PartlyCloudy: "Partly cloudy skies with gentle breeze",
		SeaWeatherCondition.Overcast: "Overcast skies with potential for rain",
		SeaWeatherCondition.Fog: "Foggy conditions with reduced visibility",
		SeaWeatherCondition.Rain: "Rainfall with choppy seas",
		SeaWeatherCondition.Thunderstorms: "Thunderstorms with rough seas and lightning",
		SeaWeatherCondition.Windy: "Windy conditions with high waves",
		SeaWeatherCondition.Calm: "Calm seas with little to no wind",
	}.get(condition, "Unknown weather condition")


def get_rarity_modifier(sea_weather):
	return {
		SeaWeatherCondition.ClearSkies: 1.0,
		SeaWeatherCondition.PartlyCloudy: 1.1,
		SeaWeatherCondition.Overcast: 1.2,
		SeaWeatherCondition.Fog: 0.8,
		SeaWeatherCondition.Rain: 0.7,
		SeaWeatherCondition.Thunderstorms: 0.5,
		SeaWeatherCondition.Windy: 0.9,
		SeaWeatherCondition.Calm: 1.1,
	}.get(sea_weather, 1.0)


def choose_rarity(roll, categories, modifier):
	cumulative_chance = 0.0
	for category in categories:
		cumulative_chance += rarity_chance(category["Rarity"]) * modifier
		if roll <= cumulative_chance:
			return category["Rarity"]
	return categories[-1]["Rarity"]


def rarity_chance(rarity):
	return {
		"Common": 0.4,
		"Uncommon": 0.3,
		"Rare": 0.2,
		"Very Rare": 0.1,
		"Epic": 0.05,
		"Legendary": 0.025,
	}.get(rarity, 0.0)


def calculate_sell_price(tier, avg_size, loot_weight, sell_value, fish_type, quality, size_category):
	# Quality multipliers
	quality_multipliers = {
		"Normal": 1.0,
		"Shining": 1.8,
		"Glistening": 4.0,
		"Opulent": 6.0,
		"Radiant": 10.0,
		"Alpha": 15.0,
	}

	# Size multipliers
	size_multipliers = {
		"Avg Size x 0.1+": 1.75,
		"Avg Size x 0.25+": 0.6,
		"Avg Size x 0.5+": 0.8,
		"Avg Size+": 1.0,
		"Avg Size x 1.5+": 1.5,
		"Avg Size x 2+": 2.5,
		"Avg Size x 3+": 4.25,
	}

	# Check if the fish is alien or a junk object
	if fish_type in ["Alien", "Junk"]:
		base_value = sell_value
	else:
		# Base value calculation for other fish
		base_value = (5 * (1 + 0.25 * (tier - 1))) ** 2.5 - loot_weight

		# Adjust base value based on loot weight
		if loot_weight < 0.4:
			base_value *= 1.1
		if loot_weight < 0.15:
			base_value *= 1.25
		if loot_weight < 0.05:
			base_value *= 1.5

	# Get quality multiplier
	quality_multiplier = quality_multipliers.get(quality, 1.0)

	# Get size multiplier
	size_multiplier = size_multipliers.get(size_category, 1.0)

	# Final worth calculation
	final_worth = math.ceil(base_value * quality_multiplier * size_multiplier)

	return final_worth
