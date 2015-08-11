
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from io import open

import os.path
import random
import json
from twitter import Twitter, OAuth, TwitterHTTPError

k_dummy='dummy'
k_tweets='tweets'
k_id='id'
k_next_id='nextId'
k_content='content'

def read_feed_file(filename):
    return json.load(open(filename, 'r', encoding='utf-8'))

def save_feed_to_file(data, save_as):
     with open(save_as, 'w', encoding='utf-8') as f_out:
         srep = json.dumps(data, sort_keys=True, indent=4, ensure_ascii=False)
         f_out.write(srep)

def is_dummy(tweet, k_dummy='dummy'):
    return k_dummy in tweet

def data_tweets_ids(filename):
    data = read_feed_file(filename)
    tweets = [t for t in data[k_tweets] if not is_dummy(t, k_dummy)]
    ids = [t[k_id] for t in tweets]
    return data, tweets, ids

def rotate_from_file(filename, save=True, save_as=None):
    
    data, tweets, ids = toto.data_tweets_ids(filename)

    assert len(set(ids)) == len(ids), "IDs should be unique, found duplicates " + str({k: v for k in set(ids) for v in [ids.count(k)] if v > 1})

    next_id = data[k_next_id]
    next_i = ids.index(next_id)
    #print("Today, we tweet:")
    #print(next_id, tweets[next_i])
    #print("Next time, we'll tweet:")
    #print(nextnext_id, tweets[nextnext_i])
    if save:
        nextnext_i = (next_i + 1) % len(ids)
        nextnext_id = ids[nextnext_i]
        data[k_next_id] = nextnext_id
        if save_as is None:
            save_as = filename
        save_feed_to_file(data, save_as)

    t = tweets[next_i]
    return t[k_content], t

def oauth(OAUTH_TOKEN, OAUTH_SECRET, CONSUMER_KEY, CONSUMER_SECRET):
    return OAuth(OAUTH_TOKEN, OAUTH_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

def load_auth(for_file, auth_file):
    v = json.load(open(auth_file))[for_file]
    return oauth(v['OAUTH_TOKEN'], v['OAUTH_SECRET'], v['CONSUMER_KEY'], v['CONSUMER_SECRET'])

def auto_auth(for_file, private_auth_file=',,auth.json', default_auth_file='auth.json'):
    if os.path.isfile(private_auth_file):
        return load_auth(for_file, private_auth_file)
    else:
        return load_auth(for_file, default_auth_file)

def tweet_plain_text(text, oauth):
    t = Twitter(auth=oauth)
    t.statuses.update(status=text)

def tweet_next(filename, oauth):
    content, t = rotate_from_file(filename)
    try:
        tweet_plain_text(content, oauth)
    except Exception as e:
        if e.response_data['errors'][0]['code'] == 187: # duplicate tweet, retry once for now
            choices = ['⚡', '⭐', '☕', '✨', '⚓']
            augmented = content + random.choice(choices)
            print('Duplicate tweet found, retrying with: '+augmented)
            tweet_plain_text(augmented, oauth)
        else:
            raise
