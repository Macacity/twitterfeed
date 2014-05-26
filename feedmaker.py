__author__ = 'LPC'
import twitter
from secrets import secrets
import os.path
from feedgen.feed import FeedGenerator
import datetime


MAX_FILE_LIVE_TIME = 3600

def get_tweets_with_links(user):


    filename = os.path.join(os.path.dirname(__file__), 'rss',  user + '_links.rss')
    threshold_time = datetime.datetime.now() - datetime.timedelta(seconds=MAX_FILE_LIVE_TIME)
    if os.path.isfile(filename) and datetime.datetime.fromtimestamp(os.path.getmtime(filename)) > threshold_time:
        with open(filename, 'r') as f:
            rss = f.read()
            if len(rss) > 0:
                return rss

    return make_rss(user, True)


def get_tweets(user):
    filename = os.path.join(os.path.dirname(__file__), 'rss',  user + '.rss')
    threshold_time = datetime.datetime.now() - datetime.timedelta(seconds=MAX_FILE_LIVE_TIME)
    if os.path.isfile(filename) and datetime.datetime.fromtimestamp(os.path.getmtime(filename)) > threshold_time:
        with open(filename, 'r') as f:
            rss = f.read()
            if len(rss) > 0:
                return rss

    return make_rss(user)


def make_rss(user, link=False):

    api = twitter.Api(**secrets)
    if link:
        filename = os.path.join(os.path.dirname(__file__), 'rss',  user + '_links.rss')

        try:
            statuses = [s for s in api.GetUserTimeline(None, user, count=50) if len(s.urls) > 0]
        except twitter.TwitterError as e:
            return str(e), 404

    else:
        filename = os.path.join(os.path.dirname(__file__), 'rss',  user + '.rss')

        try:
            statuses = api.GetUserTimeline(None, user)
        except twitter.TwitterError as e:
            return str(e), 404

    if len(statuses) == 0:
        return "No Tweets", 416

    fg = FeedGenerator()
    fg.title(user + ' on twitter')
    fg.description('RSS feed from a twitter stream')
    fg.link(href='http://twitter.com/' + statuses[0].GetUser().screen_name, rel='self')

    for status in statuses:
        fe = fg.add_entry()
        fe.title(status.GetUser().screen_name+': '+status.GetText())
        statusurl = 'http://twitter.com/' + statuses[0].GetUser().screen_name + '/status/' + status.GetIdStr()
        fe.guid(statusurl)
        fe.pubdate(status.created_at)

        if link:
            fe.link(href=status.urls[0].expanded_url, rel='alternate')
            fe.summary(status.GetText() + '\n' + status.urls[0].expanded_url)
        else:
            fe.link(href=statusurl, rel='alternate')
            fe.summary(status.GetText())

    fg.rss_file(filename)
    return fg.rss_str()