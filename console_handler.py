import asyncio
import os

from command_processing import parse
from globals import PRINT_FILTER, nonce_signal


async def listen(log_file):
	log_file.seek(0, os.SEEK_END)
	last_size = log_file.tell()

	while True:
		current_size = os.stat(log_file.name).st_size
		if current_size < last_size:
			log_file.seek(0, os.SEEK_SET)
			last_size = current_size

		line = log_file.readline()
		if not line:
			await asyncio.sleep(0.1)
			continue

		nonce_signal.handle_line(line)
		if not any(filter_text in line for filter_text in PRINT_FILTER):
			print(line.strip())
			await parse(line)
		last_size = log_file.tell()
