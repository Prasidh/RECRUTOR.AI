from llama_index import SimpleDirectoryReader, GPTListIndex, GPTSimpleVectorIndex, LLMPredictor, PromptHelper
import os
from TTS.api import TTS

os.environ["OPENAI_API_KEY"] = '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'

def chatbot(input_text):
    index = GPTSimpleVectorIndex.load_from_disk('index.json')
    response = index.query(input_text, response_mode="compact")
    return response.response

tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DCA")
tts.tts_to_file(text='')