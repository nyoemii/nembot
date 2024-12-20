import asqlite

from commands.fetch import find_recently_played
from config import DATABASE_NAME
from globals import server


async def init_database():
	async with asqlite.connect(DATABASE_NAME) as connection:
		async with connection.cursor() as cursor:
			await cursor.execute(
				"""
				CREATE TABLE IF NOT EXISTS players (
					steamid INTEGER PRIMARY KEY,
					username TEXT,
					money INTEGER DEFAULT 0
				)
				"""
			)
			await cursor.execute(
				"""
				CREATE TABLE IF NOT EXISTS commands_used (
					id INTEGER PRIMARY KEY AUTOINCREMENT,
					steamid INTEGER NOT NULL,
					username TEXT,
					command TEXT,
					team TEXT,
					dead TEXT,
					location TEXT,
					timestamp TEXT
				)
				"""
			)
			await cursor.execute(
				"""
				CREATE TABLE IF NOT EXISTS fish_caught (
					id INTEGER PRIMARY KEY AUTOINCREMENT,
					steamid INTEGER NOT NULL,
					username TEXT,
					fish_name TEXT,
					size INTEGER,
					price INTEGER,
					quality TEXT,
					timestamp TEXT
				)
				"""
			)
			await connection.commit()


async def insert_command(steamid, username, command, team, dead, location, timestamp):
	async with asqlite.connect(DATABASE_NAME) as connection:
		async with connection.cursor() as cursor:
			await cursor.execute(
				"""
				INSERT INTO commands_used (steamid, username, command, team, dead, location, timestamp)
				VALUES (?, ?, ?, ?, ?, ?, ?)
				""",
				(steamid, username, command, team, dead, location, timestamp),
			)
			await connection.commit()


async def check_if_player_exists(username):
	async with asqlite.connect(DATABASE_NAME) as connection:
		async with connection.cursor() as cursor:
			await cursor.execute(
				"""
				SELECT steamid FROM players WHERE username = ?
				""",
				(username,),
			)
			steamid_row = await cursor.fetchone()
			await connection.commit()
			if steamid_row:
				steamid_row = steamid_row[0]
			return steamid_row


async def insert_fish(fish_name, size, price, quality, steamid, username):
	async with asqlite.connect(DATABASE_NAME) as connection:
		async with connection.cursor() as cursor:
			await cursor.execute(
				"""
				INSERT INTO fish_caught (steamid, username, fish_name, size, price, quality, timestamp)
				VALUES (?, ?, ?, ?, ?, ?, ?)
				""",
				(steamid, username, fish_name, size, price, quality, server.get_info("provider", "timestamp")),
			)
			await connection.commit()


async def update_balance(steamid, amount):
	async with asqlite.connect(DATABASE_NAME) as connection:
		async with connection.cursor() as cursor:
			await cursor.execute(
				"""
				UPDATE players SET money = money + ? WHERE steamid = ?
				""",
				(amount, steamid),
			)
			await connection.commit()


async def get_balance(steamid):
	async with asqlite.connect(DATABASE_NAME) as connection:
		async with connection.cursor() as cursor:
			await cursor.execute(
				"""
				SELECT money FROM players WHERE steamid = ?
				""",
				(steamid,),
			)
			balance_row = await cursor.fetchone()
			await connection.commit()
			if balance_row:
				balance_row = balance_row[0]
			return balance_row
