from google.cloud import texttospeech
from google.oauth2 import service_account
import os

__dirname = os.path.abspath(os.path.dirname(__file__))

credentials = service_account.Credentials.from_service_account_file(
    os.path.join(__dirname, "credentials.json")
)


class TextToSpeechClient:
    def __init__(self):
        # Instantiates a client
        self.client = texttospeech.TextToSpeechClient(credentials=credentials)
        # voice gender ("neutral")
        self.voice = texttospeech.VoiceSelectionParams(
            language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
        )
        self.audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )

    def synthesize_speech(self, text, output_filename):
        # Set the text input to be synthesized
        synthesis_input = texttospeech.SynthesisInput(text=text)
        # Perform the text-to-speech request on the text input with the selected
        # voice parameters and audio file type
        response = self.client.synthesize_speech(
            input=synthesis_input, voice=self.voice, audio_config=self.audio_config
        )

        # The response's audio_content is binary.
        with open(output_filename, "wb") as out:
            print("output_filename", output_filename)
            # Write the response to the output file.
            out.write(response.audio_content)
            print(f'Audio content written to file "{output_filename}"')
