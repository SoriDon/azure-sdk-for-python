# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------

import os
import pytest
import pathlib
import uuid
from devtools_testutils import AzureRecordedTestCase
from conftest import WHISPER_AZURE, OPENAI, WHISPER_ALL, configure, TTS_OPENAI, TTS_AZURE, TTS_AZURE_AD

audio_test_file = pathlib.Path(__file__).parent / "./assets/hello.m4a"
audio_long_test_file = pathlib.Path(__file__).parent / "./assets/wikipediaOcelot.wav"

class TestAudio(AzureRecordedTestCase):

    @configure
    @pytest.mark.parametrize("api_type", WHISPER_ALL)
    def test_transcribe(self, client, azure_openai_creds, api_type, **kwargs):

        result = client.audio.transcriptions.create(
            file=open(audio_test_file, "rb"),
            **kwargs,
        )
        assert result.text == "Hello."

    @configure
    @pytest.mark.parametrize("api_type", [WHISPER_AZURE, OPENAI])
    def test_transcribe_raw(self, client, azure_openai_creds, api_type, **kwargs):

        result = client.audio.transcriptions.create(
            # file=open(audio_test_file, "rb").read(),
            # use file tuple for now
            file=("hello.m4a", open(audio_test_file, "rb").read(), "application/octet-stream"),
            **kwargs,
        )
        assert result.text == "Hello."

    @configure
    @pytest.mark.parametrize("api_type", WHISPER_ALL)
    def test_translate(self, client, azure_openai_creds, api_type, **kwargs):

        result = client.audio.translations.create(
            file=open(audio_test_file, "rb"),
            **kwargs,
        )
        assert result.text == "Hello."

    @configure
    @pytest.mark.parametrize("api_type", [WHISPER_AZURE, OPENAI])
    def test_translate_raw(self, client, azure_openai_creds, api_type, **kwargs):

        result = client.audio.translations.create(
            # file=open(audio_test_file, "rb").read(),
            # use file tuple for now
            file=("hello.m4a", open(audio_test_file, "rb").read(), "application/octet-stream"),
            **kwargs,
        )
        assert result.text == "Hello."

    @configure
    @pytest.mark.parametrize("api_type", [WHISPER_AZURE, OPENAI])
    def test_transcribe_verbose(self, client, azure_openai_creds, api_type, **kwargs):

        result = client.audio.transcriptions.create(
            file=open(audio_long_test_file, "rb"),
            response_format="verbose_json",
            **kwargs,
        )
        assert result.text == "The ocelot, Lepardus paradalis, is a small wild cat native to the southwestern " \
            "United States, Mexico, and Central and South America. This medium-sized cat is characterized by " \
            "solid black spots and streaks on its coat, round ears, and white neck and undersides. It weighs " \
            "between 8 and 15.5 kilograms, 18 and 34 pounds, and reaches 40 to 50 centimeters – 16 to 20 inches " \
            "– at the shoulders. It was first described by Carl Linnaeus in 1758. Two subspecies are recognized, " \
            "L. p. paradalis and L. p. mitis. Typically active during twilight and at night, the ocelot tends to " \
            "be solitary and territorial. It is efficient at climbing, leaping, and swimming. It preys on small " \
            "terrestrial mammals such as armadillo, opossum, and lagomorphs."
        assert result.task == "transcribe"
        assert result.language == "english"
        assert result.duration == 56.25
        for segment in result.segments:
            assert segment["id"] is not None
            assert segment["seek"] is not None
            assert segment["start"] is not None
            assert segment["end"] is not None
            assert segment["text"] is not None
            assert segment["tokens"] is not None
            assert segment["temperature"] is not None
            assert segment["avg_logprob"] is not None
            assert segment["compression_ratio"] is not None
            assert segment["no_speech_prob"] is not None

    @configure
    @pytest.mark.parametrize("api_type", [WHISPER_AZURE, OPENAI])
    def test_transcribe_text(self, client, azure_openai_creds, api_type, **kwargs):

        result = client.audio.transcriptions.create(
            file=open(audio_test_file, "rb"),
            response_format="text",
            **kwargs,
        )
        assert result == "Hello.\n"

    @configure
    @pytest.mark.parametrize("api_type", [WHISPER_AZURE, OPENAI])
    def test_transcribe_srt(self, client, azure_openai_creds, api_type, **kwargs):

        result = client.audio.transcriptions.create(
            file=open(audio_test_file, "rb"),
            response_format="srt",
            **kwargs,
        )
        assert result == "1\n00:00:00,000 --> 00:00:02,000\nHello.\n\n\n"

    @configure
    @pytest.mark.parametrize("api_type", [WHISPER_AZURE, OPENAI])
    def test_transcribe_vtt(self, client, azure_openai_creds, api_type, **kwargs):

        result = client.audio.transcriptions.create(
            file=open(audio_test_file, "rb"),
            response_format="vtt",
            **kwargs,
        )
        assert result == "WEBVTT\n\n00:00:00.000 --> 00:00:02.000\nHello.\n\n"

    @configure
    @pytest.mark.parametrize("api_type", [WHISPER_AZURE, OPENAI])
    def test_translate_verbose(self, client, azure_openai_creds, api_type, **kwargs):

        result = client.audio.translations.create(
            file=open(audio_long_test_file, "rb"),
            response_format="verbose_json",
            **kwargs,
        )
        assert result.text == "The ocelot, Lepardus paradalis, is a small wild cat native to the southwestern " \
            "United States, Mexico, and Central and South America. This medium-sized cat is characterized by " \
            "solid black spots and streaks on its coat, round ears, and white neck and undersides. It weighs " \
            "between 8 and 15.5 kilograms, 18 and 34 pounds, and reaches 40 to 50 centimeters – 16 to 20 inches " \
            "– at the shoulders. It was first described by Carl Linnaeus in 1758. Two subspecies are recognized, " \
            "L. p. paradalis and L. p. mitis. Typically active during twilight and at night, the ocelot tends to " \
            "be solitary and territorial. It is efficient at climbing, leaping, and swimming. It preys on small " \
            "terrestrial mammals such as armadillo, opossum, and lagomorphs."
        assert result.task == "translate"
        assert result.language == "english"
        assert result.duration == 56.25
        for segment in result.segments:
            assert segment["id"] is not None
            assert segment["seek"] is not None
            assert segment["start"] is not None
            assert segment["end"] is not None
            assert segment["text"] is not None
            assert segment["tokens"] is not None
            assert segment["temperature"] is not None
            assert segment["avg_logprob"] is not None
            assert segment["compression_ratio"] is not None
            assert segment["no_speech_prob"] is not None

    @configure
    @pytest.mark.parametrize("api_type", [WHISPER_AZURE, OPENAI])
    def test_translate_text(self, client, azure_openai_creds, api_type, **kwargs):

        result = client.audio.translations.create(
            file=open(audio_test_file, "rb"),
            response_format="text",
            **kwargs,
        )
        assert result == "Hello.\n"

    @configure
    @pytest.mark.parametrize("api_type", [WHISPER_AZURE, OPENAI])
    def test_translate_srt(self, client, azure_openai_creds, api_type, **kwargs):

        result = client.audio.translations.create(
            file=open(audio_test_file, "rb"),
            response_format="srt",
            **kwargs,
        )
        assert result == "1\n00:00:00,000 --> 00:00:02,000\nHello.\n\n\n"

    @configure
    @pytest.mark.parametrize("api_type", [WHISPER_AZURE, OPENAI])
    def test_translate_vtt(self, client, azure_openai_creds, api_type, **kwargs):

        result = client.audio.translations.create(
            file=open(audio_test_file, "rb"),
            response_format="vtt",
            **kwargs,
        )
        assert result == "WEBVTT\n\n00:00:00.000 --> 00:00:02.000\nHello.\n\n"

    @configure
    @pytest.mark.parametrize("api_type", [WHISPER_AZURE, OPENAI])
    def test_transcribe_options(self, client, azure_openai_creds, api_type, **kwargs):

        result = client.audio.transcriptions.create(
            file=open(audio_test_file, "rb"),
            temperature=0,
            language="en",
            prompt="Transcribe the text exactly as spoken.",
            **kwargs,
        )
        assert result.text == "Hello"

    @configure
    @pytest.mark.parametrize("api_type", [WHISPER_AZURE, OPENAI])
    def test_translate_options(self, client, azure_openai_creds, api_type, **kwargs):

        result = client.audio.translations.create(
            file=open(audio_test_file, "rb"),
            temperature=0,
            prompt="Translate the text exactly as spoken.",
            **kwargs,
        )
        assert result.text == "Hello"

    @configure
    @pytest.mark.parametrize("api_type", [TTS_OPENAI, TTS_AZURE, TTS_AZURE_AD])
    def test_tts(self, client, azure_openai_creds, api_type, **kwargs):

        speech_file_path = pathlib.Path(__file__).parent / f"{uuid.uuid4()}.mp3"
        try:
            response = client.audio.speech.create(
                voice="alloy",
                input="The quick brown fox jumped over the lazy dog.",
                **kwargs,
            )
            assert response.encoding
            assert response.content
            assert response.text
            response.write_to_file(speech_file_path)
        finally:
            os.remove(speech_file_path)

    @configure
    @pytest.mark.parametrize("api_type", [TTS_OPENAI, TTS_AZURE])
    def test_tts_hd_streaming(self, client, azure_openai_creds, api_type, **kwargs):

        with client.audio.speech.with_streaming_response.create(
            voice="echo",
            input="The quick brown fox jumped over the lazy dog.",
            model="tts-1-hd"
        ) as response:
            response.read()


    @configure
    @pytest.mark.parametrize("api_type", [TTS_OPENAI, TTS_AZURE])
    def test_tts_response_format(self, client, azure_openai_creds, api_type, **kwargs):

        speech_file_path = pathlib.Path(__file__).parent / f"{uuid.uuid4()}.flac"
        try:
            response = client.audio.speech.create(
                voice="fable",
                input="The quick brown fox jumped over the lazy dog.",
                response_format="flac",
                **kwargs
            )
            assert response.encoding
            assert response.content
            assert response.text
            response.stream_to_file(speech_file_path)  # deprecated
        finally:
            os.remove(speech_file_path)

    @configure
    @pytest.mark.parametrize("api_type", [TTS_OPENAI, TTS_AZURE])
    def test_tts_speed(self, client, azure_openai_creds, api_type, **kwargs):

        speech_file_path = pathlib.Path(__file__).parent / f"{uuid.uuid4()}.mp3"
        try:
            response = client.audio.speech.create(
                voice="onyx",
                input="The quick brown fox jumped over the lazy dog.",
                speed=3.0,
                **kwargs
            )
            assert response.encoding
            assert response.content
            assert response.text
            response.write_to_file(speech_file_path)
        finally:
            os.remove(speech_file_path)
