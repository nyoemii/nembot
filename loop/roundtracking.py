import win32con
import win32gui

# from commands.fetch import find_recently_played
from config import GAME
from globals import csgo_window_handle, last_phase, last_round, server


async def check_round():
	global last_round, last_phase
	current_phase = server.get_info("map", "phase")
	current_round = server.get_info("map", "round")

	if last_phase != current_phase:
		if current_phase == "gameover":
			last_round = None
		elif current_phase == "live" and last_round is None:
			if current_round == 0:
				print("Round 0 has started.")
			last_round = current_round

	last_phase = current_phase

	if current_phase == "live" and last_round is not None and current_round > last_round:
		print(f"Round {current_round} has started.")
		# await find_recently_played()
		# TODO: add round delay before(?)
		if GAME == "csgo":
			win32gui.FlashWindow(csgo_window_handle, win32con.FLASHW_ALL)
		last_round = current_round