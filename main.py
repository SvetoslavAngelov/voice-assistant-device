import os
import asyncio
import pvporcupine
import numpy as np
import microphone_stream as ms
from dotenv import load_dotenv
from audio_utils import write_audio_file
from google_storage_utils import auth_service_account, upload_audio_file
    
def main() -> None:
    """
    Main function to initialize Porcupine, capture audio, and upload it to Google Cloud Storage
    when a wake word is detected.
    """

    load_dotenv()

    PORCUPINE_ACCESS_KEY = os.getenv('PORCUPINE_ACCESS_KEY')
    GCS_BUCKET_NAME = os.getenv('GCS_BUCKET_NAME')
    GOOGLE_APPLICATION_CREDENTIALS = auth_service_account()

    porcupine = pvporcupine.create(
        access_key=PORCUPINE_ACCESS_KEY,
        keywords=['picovoice'] 
     )

    # Fill the buffer with 4 seconds at 16000 bit rate and a frame length of 512 bits
    BUFFER_SIZE = int(( porcupine.sample_rate * 4 )/ porcupine.frame_length)
    
    with ms.MicrophoneStream(porcupine.sample_rate, porcupine.frame_length) as stream: 

        audio_buffer = []
        is_recording = False

        for audio_chunk in stream.generator():
            keyword_index = porcupine.process(audio_chunk)

            if keyword_index >= 0: 
                print('Wake up word detected\n')
                is_recording = True
                
                # Reset keyword index
                keyword_index = -1

            if is_recording:
                audio_buffer.append(audio_chunk)

                if len(audio_buffer) >= BUFFER_SIZE:
                    packed_audio = b''.join([np.array(chunk, dtype=np.int16).tobytes() for chunk in audio_buffer])
                    audio_recording = write_audio_file(packed_audio, porcupine.sample_rate)
                    #upload_audio_file(GOOGLE_APPLICATION_CREDENTIALS, GCS_BUCKET_NAME, audio_recording, 'test_recording.wav')
                    audio_buffer = []
                    is_recording = False

if __name__ == "__main__":
    main()
