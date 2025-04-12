import json

import aiohttp
from googletrans import Translator


# async def translate_message(message: str) -> tuple[str, str]:
# 	"""
# 	Translate a message using libretranslate.

# 	Args:
# 		message (str): The message to be translated.

# 	Returns:
# 		tuple[str, str]: A tuple containing the translated message and the detected language.

# 	"""
# 	url = "https://lt.vern.cc/translate"
# 	payload = {"q": message, "source": "auto", "target": "en", "format": "text", "alternatives": 3, "api_key": ""}
# 	headers = {"Content-Type": "application/json"}

# 	print(f"Translating message: {message}")

# 	async with aiohttp.ClientSession() as session:
# 		async with session.post(url, data=json.dumps(payload), headers=headers) as response:
# 			if response.status == 200:
# 				data = await response.json()
# 				# Assuming the API returns the translated text in a field called 'translatedText'
# 				translated_message = data.get("translatedText", "Translation not found")
# 				detected_language = data.get("detectedLanguage", "").get("language", "")
# 				return translated_message, detected_language
# 			else:
# 				print(f"Failed to translate message: {response.status}")
# 				return None


async def translate_message(message: str) -> tuple[str, str]:
	"""
	Translate a message using Google Translate.

	Args:
		message (str): The message to be translated.

	Returns:
		tuple[str, str]: A tuple containing the translated message and the detected language.

	"""
	async with Translator() as translator:
		translation = await translator.translate(message, dest="en")
		return translation.text, translation.src
