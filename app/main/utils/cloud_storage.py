import json
import os

from dotenv import load_dotenv
from google.cloud import storage
from google.oauth2 import service_account
from pydantic import BaseModel


class UploadMp3BodyDto(BaseModel):
    bucket_name: str
    destination: str
    mp3: bytes


class DownloadMp3BodyDto(BaseModel):
    bucket_name: str
    source: str


load_dotenv()

# get credentials from environment variable
credentials_json = os.getenv("GOOGLE_APPLICATION_CREDENTIALS_JSON") or "{}"
# convert to json
credentials = json.loads(credentials_json)
credentials = service_account.Credentials.from_service_account_info(credentials)


class CloudStorageLib:
    def __init__(self):
        self.storage_client = storage.Client(credentials=credentials)

    async def upload_mp3_data(self, data: UploadMp3BodyDto) -> None:
        print("upload_mp3_data")
        bucket_name = data.bucket_name
        destination = data.destination
        mp3_data = data.mp3

        bucket = self.storage_client.bucket(bucket_name)
        blob = bucket.blob(destination)

        blob.upload_from_string(mp3_data, content_type="audio/mpeg")
        print("upload_from_string")
        return None

    async def download_mp3_data(self, data) -> bytes:
        print("download_mp3_data")
        bucket_name = data.bucket_name
        source = data.source

        bucket = self.storage_client.bucket(bucket_name)
        blob = bucket.blob(source)

        return blob.download_as_string()
