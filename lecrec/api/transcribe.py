# [START import_libraries]
import argparse
import base64
import json
import time
import wave

from googleapiclient import discovery
import httplib2
from oauth2client.client import GoogleCredentials
from functools import reduce

from api.wav import name_split, wav_split

# [START authenticating]


# Application default credentials provided by env variable
# GOOGLE_APPLICATION_CREDENTIALS
def get_speech_service():
    credentials = GoogleCredentials.from_stream('api/googleapi_auth/LecRec-a4f4c7931558.json').create_scoped(
        ['https://www.googleapis.com/auth/cloud-platform'])
    http = httplib2.Http()
    credentials.authorize(http)

    return discovery.build('speech', 'v1beta1', http=http)
# [END authenticating]


class MyFilename(str):
    pass


def _async_transcribe(filepath, filename, start_times, outpath='temp/'):
    """
    :param files:
    :type files: file pointer
    """
    wr=wave.open(filepath,"r")
    files = [
        MyFilename(
            outpath + name_split(filename, i)) for i in range(len(start_times))
        ]
    for file in files:
        with open(file, 'rb') as speech:
            # Base64 encode the binary audio file for inclusion in the request.
            file.speech_content = base64.b64encode(speech.read())

    # [START construct_request]

    service = get_speech_service()

    for file in files:
        file.service_request = service.speech().asyncrecognize(
            body={
                'config': {
                    # There are a bunch of config options you can specify. See
                    # https://goo.gl/KPZn97 for the full list.
                    'encoding': 'LINEAR16',  # raw 16-bit signed LE samples
                    'sampleRate': wr.getframerate(),  # 16 khz
                    # See http://g.co/cloud/speech/docs/languages for a list of
                    # supported languages.
                    'languageCode': 'ko-KR',  # a BCP-47 language tag
                },
                'audio': {
                    'content': file.speech_content.decode('UTF-8')
                    }
                })
    # [END construct_request]

    # [START send_request]
    for file in files:
        file.response = file.service_request.execute()
        # print(json.dumps(file.response))
        # [END send_request]

    for file in files:
        name = file.response['name']
        # Construct a GetOperation request.
        file.service_request = service.operations().get(name=name)

    done = [False for i in range(len(files))]
    while True:
        # Give the server a few seconds to process.
        # print('Waiting for server processing...')
        time.sleep(0.5)
        for idx, file in enumerate(files):
            # Get the long running operation with response.
            file.response = file.service_request.execute()

            if 'done' in file.response and file.response['done']:
                if not done[idx]:
                    print(idx, 'done')
                    done[idx] = True

        if reduce(lambda a,b: a and b, done, True):
            break

    start_times = iter(start_times)
    wr.close()

    # First print the raw json response
    for file in files:
        #print(json.dumps(file.response['response'], indent=2))

        # Now print the actual transcriptions
        if not 'response' in file.response:
            yield '', next(start_times)
        else:
            for result in file.response['response'].get('results', []):
                for alternative in result['alternatives']:
                    yield alternative['transcript'], next(start_times)
                    break


def async_transcribe(filepath, filename, start_times, outpath='temp/'):
    return list(_async_transcribe(filepath, filename, start_times, outpath))

if __name__ == '__main__':
    filename = 'little_prince.wav'
    start_times = wav_split(filename)
    l = async_transcribe(filename, start_times)
