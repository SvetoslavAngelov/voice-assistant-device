import os
import pvporcupine
import numpy as np
import microphone_stream as ms
from threading import Thread
from dotenv import load_dotenv
from audio_utils import write_audio_file
from google_storage_utils import auth_service_account, upload_audio_file

def process_and_upload_recording(auth: object, bucket_name: str, audio_buffer: object, sample_rate: int):
    """
    Converts a list of audio chunks into a byte buffer, which is then converted into a *.wav byte buffer
    and uploaded to GCP. 
    """
    packed_audio = b''.join([np.array(chunk, dtype=np.int16).tobytes() for chunk in audio_buffer])
    audio_recording = write_audio_file(packed_audio, sample_rate)
    upload_audio_file(auth, bucket_name, audio_recording, 'test_recording.wav')
    
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

            if is_recording:
                audio_buffer.append(audio_chunk)

                if len(audio_buffer) >= BUFFER_SIZE:
                    t = Thread(target=process_and_upload_recording, args=[GOOGLE_APPLICATION_CREDENTIALS, GCS_BUCKET_NAME, audio_buffer, porcupine.sample_rate])
                    t.run()
                    audio_buffer = []
                    is_recording = False

if __name__ == "__main__":
    main()
