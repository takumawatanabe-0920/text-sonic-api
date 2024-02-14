import json
import os
import base64
from google.oauth2 import service_account
from email.message import EmailMessage


from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from app.main.domain.mail.dto import GmailSendMessageDTO

# get credentials from environment variable
credentials_json = os.getenv("GOOGLE_APPLICATION_CREDENTIALS_JSON") or "{}"
# convert to json
credentials = json.loads(credentials_json)
credentials = service_account.Credentials.from_service_account_info(credentials)


class MailService:
    def __init__(self):
        self.client = build("gmail", "v1", credentials=credentials)

    def send_message(self, arg: GmailSendMessageDTO):
        try:
            message = EmailMessage()

            message.set_content("This is automated draft mail")

            message["To"] = "takumaozk0920@gmail.com"
            message["From"] = arg.From
            message["Subject"] = arg.Subject
            # message["Description"] = arg.Message

            # encoded message
            encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

            create_message = {"raw": encoded_message}
            # pylint: disable=E1101
            send_message = (
                self.client.users()
                .messages()
                .send(userId="me", body=create_message)
                .execute()
            )
            print(f'Message Id: {send_message["id"]}')
        except HttpError as error:
            print(f"An error occurred: {error}")
            send_message = None
        return send_message
