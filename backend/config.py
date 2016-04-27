import os

MAIL_SETTINGS = {
        'server': 'smtp.gmail.com',
        'port': 587,
        'username': 'gtgoodhealth@gmail.com',
        'password': 'GeorgeP@1927'
    }

TEST_DB_URI = 'mongodb://test:gthealthtest@ds015919.mlab.com:15919/gthealth_test'
ACTIVATION_LINK = 'localhost:4000/#/home/confirmation/{_id}/{token}'
PROD_ACTIVATION_LINK = 'www.george.gatech.edu/gthealth/#/home/confirmation/{_id}/{token}'

YIK_YAK_ID = 'E635177CFFEEBF2CD43831C603E3F4F5'

keywords = set(['depressed', 'depression', 'suicide', 'suicidal', 'kill',
                    'unhappy', 'counseling', 'counselor', 'psychiatrist',
                    'hate', 'death', 'die', 'heartbroken', 'lonely', 'hopeless',
                    'scared', 'suffer','failure', 'therapy', 'cry', 'alone', 'loser']);

secret_key = 'super secret'

SUBREDDITS = [
            {'name': 'McGill University', 'subreddit': 'mcgill', 'latitude': 45.5048, 'longitude': -73.5772},
            {'name': 'Georgia Tech', 'subreddit': 'gatech', 'latitude': 33.7756, 'longitude': -84.3963   },
            {'name': 'UT Austin', 'subreddit': 'UTAustin', 'latitude': 30.2849, 'longitude': -97.7341},
            {'name': 'Penn State University', 'subreddit': 'PennStateUniversity', 'latitude': 40.7982, 'longitude': -77.8599},
            {'name': 'Purdue', 'subreddit': 'purdue', 'latitude': 40.4237, 'longitude': -86.9212},
            {'name': 'UC Berkeley', 'subreddit': 'berkeley', 'latitude': 37.8719, 'longitude': -122.2585},
            {'name': 'CalPoly Ubispo', 'subreddit': 'CalPoly', 'latitude': 35.3050, 'longitude': -120.6625},
            {'name': 'UC Santa Barbara', 'subreddit': 'ucsantabarbara', 'latitude': 34.4140, 'longitude': -119.8489},
            {'name': 'North Carolina State University', 'subreddit': 'ncsu', 'latitude': 35.7847, 'longitude': -78.6821},
            {'name': 'York University', 'subreddit': 'yorku', 'latitude': 43.7735, 'longitude': -79.5019},
            {'name': 'Texas A&M', 'subreddit': 'aggies', 'latitude': 30.6191, 'longitude': -96.3359},
            {'name': 'Arizona State University', 'subreddit': 'asu', 'latitude': 33.4242, 'longitude': -111.9281},
            {'name': 'University of Central Florida', 'subreddit': 'ucf', 'latitude': 28.6024, 'longitude': -81.2001},
            {'name': 'University of British Columbia', 'subreddit': 'UBC', 'latitude': 49.2606, 'longitude': -123.2460},
            {'name': 'University of Maryland', 'subreddit': 'UMD', 'latitude': 38.9869, 'longitude': -76.9426},
            {'name': 'Rochester Institute of Technology', 'subreddit': 'rit', 'latitude': 43.0845, 'longitude': -77.6764},
            {'name': 'Ohio State University', 'subreddit': 'OSU', 'latitude': 40.0142, 'longitude': -83.0309},
            {'name': 'UC San Diego', 'subreddit': 'ucsd', 'latitude': 32.8801, 'longitude': -117.2340},
            {'name': 'University of Missouri', 'subreddit': 'mizzou', 'latitude': 38.9404, 'longitude': -92.3277},
            {'name': 'University of Georgia', 'subreddit': 'UGA', 'latitude': 33.9480, 'longitude': -83.3773}
      ]

class ConfigurationManager(object):

    def __init__(self):
        return
