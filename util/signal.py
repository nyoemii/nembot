import asyncio


class EventSignal:
	def __init__(self):
		self._pending: dict[str, asyncio.Event] = {}

	def register(self, nonce: str):
		self._pending[nonce] = asyncio.Event()

	def unregister(self, nonce: str):
		self._pending.pop(nonce, None)

	async def wait(self, nonce: str, *, timeout: float | None = None):
		if nonce not in self._pending:
			# Shortcut
			return
		elif timeout:
			return await asyncio.wait_for(self.wait(nonce), timeout)

		await self._pending[nonce].wait()

	def emit(self, nonce: str):
		lock = self._pending.pop(nonce, None)
		if not lock:
			# Not sure what to do here
			return
		lock.set()

	def handle_line(self, line: str):
		for nonce in list(self._pending):
			if nonce in line:
				self.emit(nonce)
