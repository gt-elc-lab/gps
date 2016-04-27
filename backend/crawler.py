import nltk
from datetime import datetime
import praw
import requests
from sentiment_analysis import SentimentHelper

import config
import models


class Classifier(object):
    """ Interface """

    def classify(submission):
        raise NotImplementedError()

class SimpleClassifier(Classifier):

    def classify(self, submission):
        tokens = nltk.tokenize.word_tokenize(submission.content)
        for word in tokens:
            if word in config.keywords:
                return True
        return False

class DTClassifier(Classifier):
    def classify(self, submission):
        if submission.content.count('depress') <= 0:
            return False
        else:
            if submission.content.count('psychiatry') <= 0:
                if submission.content.count('suicide') <= 0:
                    if SentimentHelper.compute_sentiment(submission.content)['neg'] <= 0.073:
                        return False
                    else:
                        if submission.content.count('suicide') <= 0:
                            if submission.content.count('depress') <= 1:
                                if submission.content.count('struggle') <= 0:
                                    if submission.content.count('help') <= 1:
                                        if submission.content.count('anxiety') <= 0:
                                            if SentimentHelper.compute_sentiment(submission.content)['pos'] <= 0.107:
                                                return True
                                            else:
                                                return False
                                        else:
                                            return False
                                    else:
                                        return True
                                else:
                                    return True
                            else:
                                return True
                        else:
                            return False
                else: 
                    return True
            else:
                return True
                
def test_classifier(classifier, samples):
    correct = sum(1.0 for sample in samples
        if sample.label == classifier.classify(sample))
    return correct / len(samples)


class Crawler(object):
    """ Super class for all crawlers"""

    def __init__(self, classifier):
        self.classifier = classifier

    def crawl():
        """
        Get data from the relevant source, filter by classification, then save
        to the database.
        """
        raise NotImplementedError()


class RedditCrawler(Crawler):

    def crawl(self, subreddit='gatech'):
        r = praw.Reddit(user_agent='gthealth')
        posts = [self.post_from_praw_submission(post)
            for post in r.get_subreddit(subreddit).get_new(limit=20)]
        for post in filter(self.classifier.classify, posts):
            post.save()

    @staticmethod
    def sample_from_praw_submission(submission):
        return models.Sample(r_id=submission.id,
                            title = submission.title,
                            content=submission.selftext,
                            date=datetime.utcfromtimestamp(
                                submission.created_utc),
                            subreddit=submission.subreddit.display_name)


    @staticmethod
    def post_from_praw_submission(submission):
        return models.Post(r_id=submission.id,
                           source='reddit',
                           author = submission.author.name,
                           url=submission.permalink,
                           content=submission.selftext,
                           title=submission.title,
                           created=datetime.utcfromtimestamp(
                            submission.created_utc),)

class YikYakCrawler(Crawler):

    def crawl(self, latitude=33.7756, longitude=-84.3963):
        self._login()
        posts = [self.post_from_yak(post)
            for post in self._get_new_yaks(latitude, longitude)]
        for post in filter(self.classifier.classify, posts):
            post.save()

    def _login(self):
        self.header = {
                'Referer' : 'https://www.yikyak.com/'
            }
        params = {
                'userID' : 'E635177CFFEEBF2CD43831C603E3F4F5'#config.YIK_YAK_ID
            }
        pin = requests.post('https://www.yikyak.com/api/auth/initPairing', 
                data=params, headers=self.header).json()['pin']
        params = {
                'countryCode': 'USA',
                'phoneNumber': '4079378010',
                'pin': pin
            }
        self.auth_token = requests.post('https://www.yikyak.com/api/auth/pair', 
                data=params, headers=self.header).json()
        self.header['x-access-token'] = self.auth_token

    def _get_new_yaks(self, latitude, longitude):
        params = {
                'userLat': latitude,
                'userLong': longitude,
                'lat': latitude,
                'long': longitude,
                'myHerd': 0
            }
        return requests.get('https://www.yikyak.com/api/proxy/v1/messages/all/new',
                params=params, headers=self.header)

    @staticmethod
    def post_from_yak(yak):
        return models.Post(r_id=yak['messageID'],
                           source='yikyak',
                           author = yak['posterID'],
                           url='yakwith.me/share/R/{}'.format(yak['messageID']),
                           content=yak['message'],
                           title=None,
                           created=datetime.utcfromtimestamp(
                            yak['gmt']),)

def download_corpus():
    """ Performs a search for depression related posts on all of our campuses"""
    r = praw.Reddit(user_agent='gthealth')
    for school in config.SUBREDDITS:
        print 'Searching posts from %s' % (school['name'])
        query = ' OR '.join(config.keywords)
        samples = map(Crawler.sample_from_praw_submission,
            r.search(query, subreddit=school['subreddit'], limit=1000))
        print 'found %d results' % (len(samples))
        for sample in samples:
            sample.save()


if __name__ == '__main__':
    RedditCrawler(SimpleClassifier()).crawl()
    YikYakCrawler(SimpleClassifier()).crawl()
    # download_corpus()
    # samples = models.Sample.objects(label__exists=True)
    # print test_classifier(SimpleClassifier(), samples)

