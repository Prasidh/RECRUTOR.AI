from llama_index import SimpleDirectoryReader, GPTListIndex, GPTSimpleVectorIndex, LLMPredictor, PromptHelper
import os
from TTS.api import TTS
import pyaudio
import wave
import speech_recognition as sr

os.environ["OPENAI_API_KEY"] = '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'

def chatbot(input_text):
    index = GPTSimpleVectorIndex.load_from_disk('index.json')
    response = index.query(input_text, response_mode="compact")
    return response.response

def play_audio(filename):
    # Set chunk size of 1024 samples per data frame
    chunk = 1024  

    # Open the sound file 
    wf = wave.open(filename, 'rb')

    # Create an interface to PortAudio
    p = pyaudio.PyAudio()

    # Open a .Stream object to write the WAV file to
    # 'output = True' indicates that the sound will be played rather than recorded
    stream = p.open(format = p.get_format_from_width(wf.getsampwidth()),
                    channels = wf.getnchannels(),
                    rate = wf.getframerate(),
                    output = True)

    # Read data in chunks
    data = wf.readframes(chunk)

    # Play the sound by writing the audio data to the stream
    while data != b'':
        stream.write(data)
        data = wf.readframes(chunk)

    # Close and terminate the stream
    stream.close()
    p.terminate()

tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DCA")

# Python program to translate
# speech to text and text to speech
 
# Initialize the recognizer
r = sr.Recognizer()

# Loop infinitely for user to
# speak
 
while(1):   
     
    # Exception handling to handle
    # exceptions at the runtime
    try:
         
        # use the microphone as source for input.
        with sr.Microphone() as source2:
             
            # wait for a second to let the recognizer
            # adjust the energy threshold based on
            # the surrounding noise level
            r.adjust_for_ambient_noise(source2, duration=0.2)
            
            #listens for the user's input
            print('Listening started, speak now...')
            audio2 = r.listen(source2,timeout=8,phrase_time_limit=8)
            
            # Using google to recognize audio
            print('Interpreting text...')
            chatgpt_input = r.recognize_google(audio2)
            chatgpt_input = chatgpt_input.lower()
            
            print("User input: ",chatgpt_input)
            chatgpt_output = chatbot(chatgpt_input)
            tts.tts_to_file(text=chatgpt_output)
            play_audio('output.wav')
             
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
         
    except sr.UnknownValueError:
        print("unknown error occurred")