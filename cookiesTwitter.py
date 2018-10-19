from flask import Flask, jsonify, Blueprint, request
from flask_restful import Resource, Api, abort, reqparse
import json
import datetime

user = []
tweet = []

with open('user.json') as file:
    user = json.load(file)

with open('tweet.json') as file:
    tweet = json.load(file)

def emailExist(email):
    for data in user:
        if data["email"] == email:
            abort(400, message = "Email exist, please insert new email")

def usernameExist(username):
    for data in user:
        if data["username"]== username:
            abort(400, message = "Username exist")

def checkEmail(email):
    for data in user:
        if data["email"] == email:
            return email
    
    return "Email not exist"

def savedDataUser(user):
    with open('user.json', 'w') as outfile:
        json.dump(user, outfile)
        outfile.close()

def savedDataTweet(tweet):   
    with open('Tweet.json', 'w') as file:
        json.dump(tweet, file)
        file.close()

class readAllUser(Resource):
    def get(self):
        return user
    
class readOneUser(Resource):
    def get(self):
        args = request.args.get('username')
        for data in user['username']:
            if data['username'] == args:
                return data,200
    
        return "Error user not found"

class readTwitter(Resource):
    def get(self):
        return tweet

class signUp(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            "email",
            help = "Please insert email",
            required = True,
            location = ["json"]
        )
        self.reqparse.add_argument(
            "username",
            help = "Please insert username",
            required = True,
            location = ["json"]
        )
        self.reqparse.add_argument(
            "name",
            help = "Please insert name",
            required = True,
            location = ["json"]
        )
        self.reqparse.add_argument(
            "password",
            help = "Please insert password",
            required = True,
            location = ["json"]
        )
        super().__init__()

    def post(self):
        args = self.reqparse.parse_args()
        usernameExist(request.json["username"])
        emailExist(request.json["email"])
        user.append(request.json)
        savedDataUser(user)
        return "Thank you for applying for a Twitter Account"

class login(Resource):
    def post(self):
        req = request.json
        for data in user:
            if data["email"] == req ["email"]:
                if data["password"] == req["password"]:
                    return "Login success",200
        
        return "Error username or password incorrect",401

class twitter(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            "tweet",
            help = "Please insert your tweet",
            required = True,
            location = ["json"]
        )
        super().__init__()

    def post(self):
        data = request.json
        time = str(datetime.datetime.now())
        tmp = {}
        tmp ["datetime"] = time
        req = data.copy()
        req.update(tmp)
        args = self.reqparse.parse_args()
        checkEmail(data["email"])
        tweet.append(req)
        savedDataTweet(tweet)
        return "Success Tweeting"

class deleteTweet(Resource):
    def delete(self):
        req = request.json
        for data in tweet:
            if data["email"] == req["email"] and data["tweet"] == req["tweet"]:
                tweet.remove(data)
                savedDataTweet(tweet)
                return "Tweet deleted",200

        return "Tweet not found", 404

twitter_api = Blueprint ('/twitter', __name__)
api = Api(twitter_api)
api.add_resource(readTwitter, '/twitter')
api.add_resource(readAllUser, '/user')
api.add_resource(readOneUser, '/username')
api.add_resource(signUp, '/signup')
api.add_resource(login, '/login')
api.add_resource(twitter, '/tweet')
api.add_resource(deleteTweet, '/delete')


