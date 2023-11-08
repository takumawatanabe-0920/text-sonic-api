from google.cloud import texttospeech


class TextToSpeechClient:
    def __init__(self):
        # Instantiates a client
        self.client = texttospeech.TextToSpeechClient()
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
            # Write the response to the output file.
            out.write(response.audio_content)
            print(f'Audio content written to file "{output_filename}"')
