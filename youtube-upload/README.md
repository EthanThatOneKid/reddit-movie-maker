# YouTube-Upload
> Upload a YouTube video from the command line

## Setup Summary
1. Using a python 2.7.x executable, `py -m pip install --user virtualenv`
1. Using the same python 2.7.x executable, `py -m virtualenv env`
1. Activate the env, `env\scripts\activate`
1. Download some dependencies, `pip install --upgrade google-api-python-client google-auth google-auth-oauthlib google-auth-httplib2`
1. Good to go 😊

## Call Example
```sh
python upload_video.py --file="/tmp/test_video_file.flv"
                       --title="Summer vacation in California"
                       --description="Had fun surfing in Santa Cruz"
                       --keywords="surfing,Santa Cruz"
                       --category="24"
                       --privacyStatus="public"
```

## References
* For env setup, refer to [this api-sample](https://github.com/youtube/api-samples/tree/07263305b59a7c3275bc7e925f9ce6cabf774022/python).
* For usage, refer to [this guide](https://developers.google.com/youtube/v3/guides/uploading_a_video).
* [Google API Creds](https://console.developers.google.com/apis/credentials)
