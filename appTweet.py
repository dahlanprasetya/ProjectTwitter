from flask import Flask, request
from cookiesTwitter import twitter_api
import os

twitterApp = Flask(__name__)
twitterApp.register_blueprint(twitter_api, url_prefix = '/api/v1')

@twitterApp.route('/')
def hellow():
    return "Hello"

if __name__ == '__main__':
    twitterApp.run(debug = True, host = os.getenv("HOST"), port = os.getenv("TWEET"))