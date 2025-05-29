from watchdog.events import FileSystemEventHandler

from command_execution import send_message_async
from config import HR_DIRECTORY, HR_FILE
from globals import csgo_window_handle, server


class FileUpdateHandler(FileSystemEventHandler):
	def __init__(self, file_path):
		self.file_path = file_path

	def on_modified(self, event):
		if (event.src_path) == self.file_path:
			file_updated()


def file_updated():
	with open(f"{HR_DIRECTORY + HR_FILE}", "r", encoding="utf-8") as f:
		heart_rate = f.read().splitlines()[0]
	if server.get_info("player", "activity") != "menu":
		if server.get_info("map", "phase") == "live":
			send_message_async(csgo_window_handle, "sm_fart Heartrate: " + heart_rate)
			print(f"Set HR to {heart_rate}")
