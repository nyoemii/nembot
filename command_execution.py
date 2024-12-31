import asyncio
import ctypes
import random
from ctypes import wintypes

import win32api

from config import EXEC_FILE, GAME
from globals import csgo_window_handle, nonce_signal

WM_COPYDATA = 0x004A


def write_command(command: str):
	with open(EXEC_FILE, "w", encoding="utf-8") as f:
		f.write(command)


def clear_command():
	with open(EXEC_FILE, "w", encoding="utf-8") as f:
		f.write("")


async def execute_command_csgo(command: str, delay: float | None = None):
	if delay is not None and delay != 3621:
		await asyncio.sleep(delay)
		await send_message_async(csgo_window_handle, command)
	if delay == 3621:
		await send_message_async(csgo_window_handle, command)
	else:
		await asyncio.sleep(0.25)
		await send_message_async(csgo_window_handle, command)


def generate_nonce(length: int) -> str:
	invisible_chars = [
		"\u200b",  # Zero-width space
		"\u200c",  # Zero-width non-joiner
		"\u0020",  # Space
		"\u2800",  # Braille blank
	]

	nonce = "".join(random.choice(invisible_chars) for _ in range(length))

	return nonce


async def execute_command_cs2(command: str, delay: float | None = None):
	nonce = generate_nonce(4)  # btw you could maybe have collisions here?
	nonce_signal.register(nonce)

	# Giving it 3 tries (change it if you want :D)
	for _ in range(3):
		if delay is not None and delay != 3621:
			await asyncio.sleep(delay)
		if delay == 3621:
			write_command(command + nonce)
			await asyncio.sleep(0.051)
			clear_command()
		else:
			await asyncio.sleep(0.25)  # wait 0.25 seconds for chat delay, 0.15 should work but is very inconsistent... fuck valve
			if "playerchatwheel" in command:
				write_command(command + f"\necholn {nonce}")
				await asyncio.sleep(0.0500001)
				clear_command()
			else:
				write_command(command + nonce)
				await asyncio.sleep(0.0500001)
				clear_command()

		try:
			await nonce_signal.wait(nonce, timeout=2.5)
		except asyncio.TimeoutError:
			continue
		else:
			break
	else:
		nonce_signal.unregister(nonce)
		print(f"Failed to run command {command}")
		# Do whatever you want here (e.g. log instead of throw)
		# raise RuntimeError(f"Failed to run command {command}")


async def execute_command(command: str, delay: float | None = None):
	if GAME == "csgo":
		await execute_command_csgo(command, delay)
	else:
		await execute_command_cs2(command, delay)


class COPYDATASTRUCT(ctypes.Structure):
	_fields_ = [
		("dwData", wintypes.LPARAM),
		("cbData", wintypes.DWORD),
		("lpData", wintypes.LPVOID),
	]


async def send_message_async(target_hwnd: str, message: str):
	loop = asyncio.get_event_loop()
	await loop.run_in_executor(None, send_message, target_hwnd, message)


def send_message(target_hwnd: str, message: str):
	message_bytes = (message + "\0").encode("utf-8")
	cds = COPYDATASTRUCT()
	cds.dwData = 0
	cds.cbData = len(message_bytes)
	cds.lpData = ctypes.cast(ctypes.create_string_buffer(message_bytes), wintypes.LPVOID)

	win32api.SendMessage(target_hwnd, WM_COPYDATA, 0, ctypes.addressof(cds))
