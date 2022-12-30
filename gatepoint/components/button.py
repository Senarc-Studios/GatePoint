from typing import Union

class Button:
	def __init__(
		self,
		label: str,
		custom_id: str,
		url: str = None,
		style: int = None
	):
		if len(custom_id) > 100 or len(custom_id) == 0:
			raise ValueError("custom_id: Must be more than 0 characters and less than 100 characters.")

		self.label = label
		self.custom_id = custom_id
		self.style = 5 if url else style or 1
		self.url = url
