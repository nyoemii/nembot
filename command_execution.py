import asyncio
import ctypes
import random
from ctypes import wintypes

import win32api

from config import EXEC_FILE, GAME
from globals import csgo_window_handle, command_nonce_list, nonce_signal

WM_COPYDATA = 0x004A


async def write_command(command):
	with open(EXEC_FILE, "w", encoding="utf-8") as f:
		f.write(command)


async def clear_command():
	with open(EXEC_FILE, "w", encoding="utf-8") as f:
		f.write("")


async def execute_command_csgo(command, delay=None):
	if delay is not None and delay != 3621:
		await asyncio.sleep(delay)
		send_message(csgo_window_handle, command)
	if delay == 3621:
		send_message(csgo_window_handle, command)
	else:
		await asyncio.sleep(0.25)
		send_message(csgo_window_handle, command)


async def generate_nonce(length: int) -> str:
	invisible_chars = [
		"\u200b",  # Zero-width space
		"\u200c",  # Zero-width non-joiner
		"\u200d",  # Zero-width joiner
		"\u200e",  # Left-to-right mark
		"\u200f",  # Right-to-left mark
		"\ufeff",  # Byte order mark
	]

	nonce = "".join(random.choice(invisible_chars) for _ in range(length))

	return nonce


def nonce_callback(data):
	return


# TODO: PLEASE HOW DO I STOP EXECUTION UNTIL THE CALLBACK IS FUCKING CALLED :(
async def execute_command_cs2(command, delay=None):
	nonce = await generate_nonce(4)
	command_nonce_list.append(nonce)
	if delay is not None and delay != 3621:
		await asyncio.sleep(delay)
	if delay == 3621:
		await write_command(command + nonce)
		await asyncio.sleep(0.050001)
		await clear_command()
	else:
		await asyncio.sleep(0.25)  # wait 0.25 seconds for chat delay, 0.15 should work but is very inconsistent... fuck valve
		await write_command(command + nonce)
		await asyncio.sleep(0.050001)
		await clear_command()

	nonce_signal.await_callback(nonce_callback)


async def execute_command(command, delay=None):
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


# TODO: if possible, switch to proper async instead of this lmfao
async def send_message_async(target_hwnd, message):
	loop = asyncio.get_event_loop()
	await loop.run_in_executor(None, send_message, target_hwnd, message)


def send_message(target_hwnd, message):
	message_bytes = (message + "\0").encode("utf-8")
	cds = COPYDATASTRUCT()
	cds.dwData = 0
	cds.cbData = len(message_bytes)
	cds.lpData = ctypes.cast(ctypes.create_string_buffer(message_bytes), wintypes.LPVOID)

	win32api.SendMessage(target_hwnd, WM_COPYDATA, 0, ctypes.addressof(cds))
