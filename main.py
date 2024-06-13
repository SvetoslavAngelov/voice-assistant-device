import os
import microphone_stream as ms 
import pvporcupine
import wave
from google.auth import default
from google.cloud import storage
from google.oauth2 import service_account
from dotenv import load_dotenv

def auth_service_account():
    GOOGLE_APPLICATION_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    credentials = service_account.Credentials.from_service_account_file(GOOGLE_APPLICATION_CREDENTIALS)
    scoped_credentials = credentials.with_scopes(['https://www.googleapis.com/auth/cloud-platform'])
    project = credentials.project_id
    return scoped_credentials, project

def write_to_gcs(bucket: str, source_file: str, destination_blob: str): 
    credentials, project = auth_service_account()
    client = storage.Client(project=project, credentials=credentials)
    bucket = client.bucket(bucket)
    blob = bucket.blob(destination_blob)

    blob.upload_from_filename(source_file)

    print(f'File {source_file} uploaded to {destination_blob}')

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
