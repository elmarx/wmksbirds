WM_LOCATION = 'Kassel'

try:
    from settings_local import *
except:
    # if not given, "birdlist" will do the "OAuth-Dance" for you
    ACCESS_TOKEN = None
    ACCESS_TOKEN_SECRET = None

    # go to https://apps.twitter.com and register an app to obtain the outh-token and -secret
    CONSUMER_TOKEN = None
    CONSUMER_SECRET = None

# dummy-usernames used in templates
DUMMY_NAMES = ['username', 'twitterhandle', 'me']

DEFAULT_URL = "http://webmontag.de/location/%s/index" % WM_LOCATION.lower()


