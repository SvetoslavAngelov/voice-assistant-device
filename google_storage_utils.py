import os
import io
from google.cloud import storage
from google.oauth2 import service_account

def auth_service_account():
    GOOGLE_APPLICATION_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    credentials = service_account.Credentials.from_service_account_file(GOOGLE_APPLICATION_CREDENTIALS)
    scoped_credentials = credentials.with_scopes(['https://www.googleapis.com/auth/cloud-platform'])
    project = credentials.project_id
    return scoped_credentials, project

async def upload_audio_file(auth: object, bucket_name: str, audio_buffer: object, destination_blob_name: str): 
    credentials, project = auth
    client = storage.Client(project=project, credentials=credentials)
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    wav_file = io.BytesIO(audio_buffer)

    try:
        blob.upload_from_file(wav_file, content_type='audio/wav')
        print(f'File {destination_blob_name} uploaded to {bucket_name}')
    except Exception as e:
        print(f'{e}')