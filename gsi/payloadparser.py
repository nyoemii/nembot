class PayloadParser:
	def parse_payload(self, payload, gamestate):
		for item in payload:
			for i in payload[item]:
				try:
					setattr(getattr(gamestate, item), i, payload[item][i])
				except Exception as e:  # noqa: F841
					# print("Exception: " + str(e))
					pass
