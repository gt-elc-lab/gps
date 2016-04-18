import nltk
from datetime import datetime
import praw

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

    def crawl(self, subreddit='depression'):
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

    def crawl():
        pass



def download_corpus():
    """ Performs a search for depression related posts on all of our subreddits"""
    r = praw.Reddit(user_agent='gthealth')
    for school in config.SUBREDDITS:
        print 'Searching posts from %s' % (school['name'])
        query = ' OR '.join(config.keywords)
        samples = map(Crawler.sample_from_praw_submission,
            r.search(query, subreddit=school['subreddit'], limit=1000))
        print 'found %d results' % (len(samples))
        for sample in samples:
            sample.save()
    return


if __name__ == '__main__':
    RedditCrawler(SimpleClassifier()).crawl()
    # download_corpus()
    # samples = models.Sample.objects(label__exists=True)
    # print test_classifier(SimpleClassifier(), samples)

