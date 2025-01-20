import requests
import os
import traceback
from loguru import logger
BASE_URL = os.getenv('BASE_URL', 'http://10.10.70.20:8787/api/v1')
USER_NAME = os.getenv('USER_NAME', 'admin')
PASSWORD = os.getenv('PASSWORD', 'Angible123!')

def create_media_v1(base_url, user_name, password, file_path, data_params=None):
    try:
        login_url = f"{base_url}/login"
        payload = {'username': user_name, 'password': password}
        login_response = requests.post(login_url, data=payload)
        login_response.raise_for_status()
        media_url = f"{base_url}/media"
        headers = {'authorization': f'Token {login_response.json()["token"]}'}
        
        files = {}
        opened_file = open(file_path, 'rb')
        files['media_file'] = opened_file
        data_dict = {}
        if data_params:
            for key, value in data_params.items():
                data_dict[key] = value
        if data_dict:
            response = requests.post(url=media_url, files=files, headers=headers, data=data_dict)
        else:
            response = requests.post(url=media_url, files=files, headers=headers)
        response.raise_for_status()
        print(response.text)
    except Exception as e:
        traceback.print_exc()
    finally:
        opened_file.close()

def create_media_v2(base_url, user_name, password, file_path, data_params=None):
    response = None
    try:
        media_url = f"{base_url}/media"
        auth = (user_name, password)
        opened_file = open(file_path, 'rb')
        data_dict = {}
        if data_params:
            for key, value in data_params.items():
                data_dict[key] = value
        if data_dict:
            response = requests.post(url=media_url, files={'media_file': opened_file}, auth=auth, data=data_dict)
        else:
            response = requests.post(url=media_url, files={'media_file': opened_file}, auth=auth)
        response.raise_for_status()
    except Exception as e:
        traceback.print_exc()
    finally:
        opened_file.close()
    return response

def create_subtitles_by_token(base_url, user_name, password, file_path, friendly_token, language_id=None):
    response = None
    try:
        subtitle_url = f"{base_url}/subtitle/{friendly_token}"
        auth = (user_name, password)
        opened_file = open(file_path, 'rb')
        data_dict = {}
        if language_id:
            data_dict['language_id'] = language_id
        if data_dict:
            response = requests.post(url=subtitle_url, files={'subtitle_file': opened_file}, auth=auth, data=data_dict)
        else:
            response = requests.post(url=subtitle_url, files={'subtitle_file': opened_file}, auth=auth)
        response.raise_for_status()
    except Exception as e:
        logger.exception(e)
    finally:
        opened_file.close()
    return response

def create_media_and_upload_subtitles(base_url, user_name, password, media_file_path, subtitles_file_path, media_data_params=None, subtitle_data_params=None):
    media_response = None
    subtitle_response = None
    media_response = create_media_v2(base_url, user_name, password, media_file_path,media_data_params)
    logger.info(f"media_response: {media_response}")
    if media_response:
        media_friendly_token = media_response.json()['friendly_token']
        subtitle_response = create_subtitles_by_token(base_url, user_name, password, subtitles_file_path, media_friendly_token)
    if media_response:
        media_response = media_response.text
    if subtitle_response:
        subtitle_response = subtitle_response.text
    logger.info(f"media_response: {media_response}")
    logger.info(f"subtitle_response: {subtitle_response}")
    
        
if __name__ == "__main__":
    # create_media_v1(BASE_URL, USER_NAME, PASSWORD, '/path/to/file')
    # create_media_v2(BASE_URL, USER_NAME, PASSWORD, 'this_is_joe_central_00001090_v1.mp4', {'title': 'This is Joe Central!!!', 'description': 'This is a test video!!!', 'category': 'leon,joe'})
    create_media_and_upload_subtitles(BASE_URL, USER_NAME, PASSWORD, 'this_is_joe_central_00001090_v1.mp4', 'test.vtt', {'title': 'This is Joe Central!!!', 'description': 'This is a test videoooo!!!', 'category': 'leonnnn,joeeeee'})