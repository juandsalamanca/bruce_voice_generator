import streamlit as st
from elevenlabs.client import ElevenLabs
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import pydub
from pydub import AudioSegment
from io import BytesIO

with open('config.yaml') as file:
  config = yaml.load(file, Loader=SafeLoader)
	
authenticator = stauth.Authenticate(
	config['credentials'],
	config['cookie']['name'],
	config['cookie']['key'],
	config['cookie']['expiry_days'],
	config['preauthorized']
)

if not st.session_state.authentication_status:
  st.info('Please Login from the Home page.')
  home=st.button(label='Go home')
  if home:
    st.switch_page('voiss.py')
  st.stop()


st.header('Cloned Voice Generator')

st.sidebar.write("Select scenario")
sc11=st.sidebar.button('Scenario 11')
if sc11:
    st.switch_page('pages/10_scenario_11_AI_feedback.py')
sc13=st.sidebar.button(label='Scenario 13')
if sc13:
    st.switch_page('pages/13_scenario_13_AI_feedback.py')
sc34=st.sidebar.button(label='Scenario 34')
if sc34:
    st.switch_page('pages/8_scenario_34_AI_feedback.py')
sc35=st.sidebar.button(label='Scenario 35')
if sc35:
    st.switch_page('pages/11_scenario_35_AI_feedback.py')
sc37=st.sidebar.button(label='Scenario 37')
if sc37:
    st.switch_page('pages/14_scenario_37_AI_feedback.py')
sc57=st.sidebar.button(label='Scenario 57')
if sc57:
    st.switch_page('pages/17_scenario_57_AI_feedback.py')
sc84=st.sidebar.button(label='Scenario 84')
if sc84:
    st.switch_page('pages/16_scenario_84_AI_feedback.py')

response=st.sidebar.button(label="Response Tracking")
if response:
    st.switch_page('pages/tables.py') 
authenticator.logout('Logout', 'main')
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
