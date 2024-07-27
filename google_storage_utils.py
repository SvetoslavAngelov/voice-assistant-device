import os
import io
from google.cloud import storage
from google.oauth2 import service_account
from typing import Any

def auth_service_account():
    GOOGLE_APPLICATION_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    credentials = service_account.Credentials.from_service_account_file(GOOGLE_APPLICATION_CREDENTIALS)
    scoped_credentials = credentials.with_scopes(['https://www.googleapis.com/auth/cloud-platform'])
    project = credentials.project_id
    return scoped_credentials, project

def upload_audio_file(auth: tuple[service_account.Credentials, Any | None], bucket_name: str, audio_buffer: str, destination_blob_name: str): 
    credentials, project = auth
    client = storage.Client(project=project, credentials=credentials)
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    wav_file = io.BytesIO(audio_buffer)
    blob.upload_from_filename(wav_file, content_type='audio/wav')

    print(f'File {destination_blob_name} uploaded to {bucket_name}')