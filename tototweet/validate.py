
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from io import open

import json
import toto

def check_tweet_length(filename):
    data, tweets, ids = toto.data_tweets_ids(filename)
    for t in tweets:
        assert len(t['content']) < 120, (t, len(t['content']))

def check_tweet_ids(filename):
    data, tweets, ids = toto.data_tweets_ids(filename)
    assert len(set(ids)) == len(ids), "IDs should be unique, found duplicates " + str({k: v for k in set(ids) for v in [ids.count(k)] if v > 1})

def resave(filename):
    data, tweets, ids = toto.data_tweets_ids(filename)
    toto.save_feed_to_file(data, filename)

def check_all(filename, save=False):
    check_tweet_length(filename)
    check_tweet_ids(filename)
    if save:
        resave(filename)
