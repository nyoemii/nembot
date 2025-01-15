import win32con
import win32gui

from commands.fetch import find_recently_played
from config import GAME
from globals import csgo_window_handle, last_phase, last_round, server


async def check_round():
	"""
	Checks if the current round has changed and updates global variables accordingly.

	If the current round is 0, it will fetch the recently played players.

	Flashes the window if the game is CSGO and the round has changed.
	"""
	global last_round, last_phase
	current_phase = server.get_info("map", "phase")
	current_round = server.get_info("map", "round")

	if last_phase != current_phase:
		if current_phase == "gameover":
			last_round = None
		elif current_phase == "live" and last_round is None:
			if current_round == 0:
				print("Round 0 has started.")
				await find_recently_played()
			last_round = current_round

	last_phase = current_phase

	if current_phase == "live" and last_round is not None and current_round > last_round:
		print(f"Round {current_round} has started.")
		# await find_recently_played()
		# TODO: add round delay before(? currently it will flash at the end of a round, think it can be fixed by checking player info or smth idk..)
		if GAME == "csgo":
			win32gui.FlashWindow(csgo_window_handle, win32con.FLASHW_ALL)
			# TODO: after above todo, add cs2 window handle as well :3 (is dynamic... rip Valve001 in source 2....)
		if current_round == 0:
			await find_recently_played()
		last_round = current_round
