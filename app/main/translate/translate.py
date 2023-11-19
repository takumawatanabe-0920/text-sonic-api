from google.cloud import translate_v2 as translate

import json
import os

from dotenv import load_dotenv
from google.oauth2 import service_account

load_dotenv()

# get credentials from environment variable
credentials_json = os.getenv("GOOGLE_APPLICATION_CREDENTIALS_JSON") or "{}"
# convert to json
credentials = json.loads(credentials_json)
credentials = service_account.Credentials.from_service_account_info(credentials)


class TranslateTextClient:
    def __init__(self):
        # Instantiates a client
        self.client = translate.Client(credentials=credentials)

    async def translate(self, text: str, target_language: str) -> str:
        result = self.client.translate(text, target_language=target_language)

        return result["translatedText"]
