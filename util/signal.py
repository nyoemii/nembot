import asyncio


class EventSignal:
	def __init__(self):
		self._callbacks = []

	def connect(self, callback):
		"""Connects a callback function to the signal."""
		self._callbacks.append(callback)

	def disconnect(self, callback):
		"""Disconnects a callback function from the signal."""
		try:
			self._callbacks.remove(callback)
		except ValueError:
			pass  # Ignore if callback not found

	def emit(self, *args, **kwargs):
		"""Emits the signal, calling all connected callbacks."""
		for callback in self._callbacks:
			try:
				callback(*args, **kwargs)
			except Exception as e:
				print(f"Error in callback: {e}")  # Handle exceptions gracefully

	def await_callback(self, callback):
		def internal_callback(*args):
			self.disconnect(internal_callback)
			callback(*args)

		self.connect(internal_callback)
