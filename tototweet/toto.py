
import os.path
import json
from twitter import Twitter, OAuth, TwitterHTTPError

def rotate_from_file(filename, save=True, save_as=None,
                     k_dummy='dummy', k_tweets='tweets', k_id='id',
                     k_next_id='nextId', k_content='content'):
    def is_dummy(tweet):
        return tweet.has_key(k_dummy)
    
    data = json.load(open(filename))
    tweets = [t for t in data[k_tweets] if not is_dummy(t)]
    ids = [t[k_id] for t in tweets]

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
        data['nextId'] = nextnext_id
        if save_as is None:
            save_as = filename
        json.dump(data, open(save_as, 'w'), sort_keys = False, indent = 4, ensure_ascii=False)

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
    tweet_plain_text(content, oauth)
