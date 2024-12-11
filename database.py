import asqlite

from config import DATABASE_NAME
from commands.fetch import find_recently_played


async def init_database():
	async with asqlite.connect(DATABASE_NAME) as connection:
		async with connection.cursor() as cursor:
			await cursor.execute(
				'''
				CREATE TABLE IF NOT EXISTS players (
					steamid INTEGER PRIMARY KEY,
					username TEXT,
					money TEXT DEFAULT 0
				)
				'''
			)
			await cursor.execute(
				'''
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
				'''
			)
			await cursor.execute(
				'''
				CREATE TABLE IF NOT EXISTS fish_caught (
					id INTEGER PRIMARY KEY AUTOINCREMENT,
					steamid INTEGER NOT NULL,
					username TEXT,
					fish TEXT,
					weight TEXT,
					price TEXT,
					rarity TEXT,
					timestamp TEXT
				)
				'''
			)
			await connection.commit()

async def insert_command(username, command, team, dead, location, timestamp):
	async with asqlite.connect(DATABASE_NAME) as connection:
		async with connection.cursor() as cursor:
			while True:
				await cursor.execute(
					'''
					SELECT steamid FROM players WHERE username = ?
					''',
					(username,)
				)
				steamid_row = await cursor.fetchone()
				if steamid_row is not None:
					steamid = int(steamid_row[0])
					break
				else:
					# print("Player not found in database.")
					# break
					await find_recently_played()
			await connection.commit()
	async with asqlite.connect(DATABASE_NAME) as connection:
		async with connection.cursor() as cursor:
			await cursor.execute(
				'''
				INSERT INTO commands_used (steamid, username, command, team, dead, location, timestamp)
				VALUES (?, ?, ?, ?, ?, ?, ?)
				''',
				(steamid, username, command, team, dead, location, timestamp)
			)
			await connection.commit()