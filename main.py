import os
import microphone_stream as ms 
import pvporcupine
import wave
from dotenv import load_dotenv

def write_audio_file(filename: str, audio_content: object, sample_rate: int):
    with wave.open(filename, 'wb') as wf: 
        wf.setnchannels(1)
        wf.setsamplewidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(audio_content)
    
def main() -> None:
    load_dotenv()

    PORCUPINE_ACCESS_KEY = os.getenv('PORCUPINE_ACCESS_KEY')

    porcupine = pvporcupine.create(
        access_key=PORCUPINE_ACCESS_KEY,
        keywords=['picovoice'] 
     )
    
    with ms.MicrophoneStream(porcupine.sample_rate, porcupine.frame_length) as stream: 
        for audio_chunk in stream.generator():
            keyword_index = porcupine.process(audio_chunk)

            if keyword_index >= 0: 
                print('Wake up word detected\n')

if __name__ == "__main__":
    main()
