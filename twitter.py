from twython.api import Twython


class AuthorizedTwitter:
    def __init__(self, consumer_token, consumer_secret, access_token, secret):
        self.t = Twython(consumer_token, consumer_secret, access_token, secret)

class Twitter:
    def __init__(self, consumer_token, consumer_secret):
        self.t = Twython(consumer_token, consumer_secret)
        self.consumer_token = consumer_token
        self.consumer_secret = consumer_secret

    def generate_access_token(self):
        auth = self.t.get_authentication_tokens()

        print("Please go to {auth_url} for a verification code.".format(**auth))
        verifier = input("Verification code: ")

        twitter = Twython(self.consumer_token, self.consumer_secret, auth['oauth_token'], auth['oauth_token_secret'])
        tokens = twitter.get_authorized_tokens(oauth_verifier=verifier)
        return tokens['oauth_token'], tokens['oauth_token_secret']

    def authenticate(self, access_token, secret):
        return AuthorizedTwitter(self.consumer_token, self.consumer_secret, access_token, secret)
