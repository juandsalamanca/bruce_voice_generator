import streamlit as st
from elevenlabs.client import ElevenLabs
import yaml
import pydub
from pydub import AudioSegment
from io import BytesIO

st.header('Cloned Voice Generator')

@st.cache_data
def verified_tts(text):
  client = ElevenLabs(api_key=st.secrets["ELEVEN_LABS_KEY"])
  audio = client.text_to_speech.convert(
      text=text,
      voice_id="h4aPznjjOovo5zDdrhuY"
	  #No model param
  )

  audio_bytes = b"".join(chunk for chunk in audio)
  return audio_bytes

def adjust_volumne(audio_bytes, vol):
	
	audio = AudioSegment.from_file(BytesIO(audio_bytes), format="mp3")
	
	# Increase volume by 5 dB (use negative values to decrease)
	adjusted_audio = audio.apply_gain(vol)
	
	# Export to a BytesIO buffer instead of a file
	buffer = BytesIO()
	adjusted_audio.export(buffer, format="mp3")
	
	# Get the bytes
	adjusted_audio_bytes = buffer.getvalue()
	
	# Close the buffer
	buffer.close()

	return adjusted_audio_bytes

if "input_memory" not in st.session_state:
	st.session_state.input_memory = ""
if "audio_bytes" not in st.session_state:
	st.session_state.audio_bytes = None

vol = st.number_input("Enter the number of decibels by which the volume is increased (positive numbers) or decreased (negative numbers)", value=-10)
input = st.text_input("Enter the text you want transformed into audio")

button = st.button("Generate audio")

if button:
	raw_audio = verified_tts(input)
	st.session_state.audio_bytes = adjust_volumne(raw_audio, vol)
	
if st.session_state.audio_bytes != None:
	st.download_button(
        label="Download the mp3 file",
        data=st.session_state.audio_bytes,
        file_name=f"cloned.mp3",
        mime="text/csv",
    )
