import os
import struct
from google import genai
from google.genai import types

# --- Configuration for Vertex AI Gemini API ---
# REPLACE these with your actual Google Cloud Project ID and Location
PROJECT_ID = "gen-lang-client-0273245nnn"  #  

def save_wav_file(file_name, audio_data, sample_rate=24000):
    """Saves raw PCM audio data into a playable WAV file."""
    # (Your original save_wav_file function remains the same and is necessary
    # because the Gemini API returns raw audio data, not a WAV file.)
    try:
        num_channels = 1
        bits_per_sample = 16
        byte_rate = sample_rate * num_channels * (bits_per_sample // 8)
        block_align = num_channels * (bits_per_sample // 8)
        data_size = len(audio_data)
        chunk_size = 36 + data_size

        # WAV Header Construction
        header = struct.pack(
            "<4sI4s4sIHHIIHH4sI",
            b"RIFF", chunk_size, b"WAVE", b"fmt ", 16, 1, num_channels,
            sample_rate, byte_rate, block_align, bits_per_sample, b"data", data_size
        )
        
        with open(file_name, "wb") as f:
            f.write(header)
            f.write(audio_data)
            
        print(f"SUCCESS: Saved {len(audio_data)} bytes of audio to: {file_name}")
    except Exception as e:
        print(f"ERROR: Could not save file: {e}")


def generate_gemini_tts_on_vertex_ai():
    # --- CLIENT SETUP for Vertex AI ---
    try:
        # Initialize the client specifically for Vertex AI
        # This uses ADC for authentication (gcloud auth application-default login)
        client = genai.Client(
            vertexai=True
        )
    except Exception as e:
        print(f"\n[CRITICAL] Error initializing GenAI Client for Vertex AI. Check your PROJECT_ID, LOCATION, and authentication (gcloud auth).")
        print(f"Details: {e}")
        return

    # --- INPUT (Combined with Instructions) ---
    input_filename = "input.txt"
    if not os.path.exists(input_filename):
        with open(input_filename, "w", encoding="utf-8") as f:
            f.write("We are proud to present our new line of products. This has been a monumental effort by our entire team, and we believe it will set a new benchmark for quality and innovation in the market.")
    
    with open(input_filename, "r", encoding="utf-8") as f:
        text_input = f.read()

    # Apply your requested style/instruction directly in the prompt for Gemini TTS
    # This is the feature that Classic TTS (WaveNet/Studio) does not support.
    prompt = (
        "[Style: Warm, inviting, and respectful. Adopt a traditional Indian English accent suitable for ancient fables. The tone should be similar to an elder or guru sharing timeless wisdom.]\n"
        "[Instruction: Read the text with clear character distinction and dramatic flair. Maintain a steady, narrative pace. Vary pitch and pace for dialogue: Kings (authoritative, slightly deep), Scholars/Ministers (measured, wise), and Animals (distinctive, engaging). Emphasize and pronounce all Sanskrit/Indian terms (e.g., Panchatantra, Damanaka) clearly and correctly. Deliver wisdom quotes with a slowed, punchy, and deliberate cadence.]\n"
        #"[Style: Warm, friendly, authentic Indian English accent]\n"
        #"[Instruction: Read the following text enthusiastically and with self-esteem in Indian tone.]\n"
        f'"{text_input}"'
    )
    
    print(f"Read {len(text_input)} characters. Generating audio with Zephyr voice and custom instructions...")

    # --- CONFIG ---
    # Use the appropriate Gemini TTS model
    model = "gemini-2.5-pro-preview-tts"  # Also works with "gemini-2.5-flash-preview-tts"
    
    # The contents now contain the instruction-enhanced prompt
    contents = [types.Content(role="user", parts=[types.Part.from_text(text=prompt)])]
    
    # Configure for audio output and specify the Zephyr voice
    config = types.GenerateContentConfig(
        response_modalities=["audio"],
        speech_config=types.SpeechConfig(
            voice_config=types.VoiceConfig(
                prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name="Zephyr")
            )
        )
    )

    # --- GENERATION ---
    # (Rest of the generation logic from your original code)
    full_audio_buffer = bytearray()

    try:
        response_stream = client.models.generate_content_stream(
            model=model,
            contents=contents,
            config=config,
        )

        for chunk in response_stream:
            if chunk.candidates and chunk.candidates[0].content and chunk.candidates[0].content.parts:
                for part in chunk.candidates[0].content.parts:
                    if part.inline_data and part.inline_data.data:
                        full_audio_buffer.extend(part.inline_data.data)

        if len(full_audio_buffer) > 0:
            print(f"\nStream finished. Saving {len(full_audio_buffer)} bytes...")
            save_wav_file("zvertex_ai_audio.wav", full_audio_buffer)
        else:
            print("\n[ERROR] No audio data received. Check your prompt safety settings or API status.")

    except Exception as e:
        print(f"\n[EXCEPTION] Error: {e}")

if __name__ == "__main__":
    generate_gemini_tts_on_vertex_ai()
