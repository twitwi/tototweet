

from tototweet import toto
import sys

def go_tweet(filename):
    toto.tweet_next(filename, toto.auto_auth(filename))

def main(argv=None):
    if argv is None:
        argv = sys.argv
    if len(argv) == 1: # no parameters, just an example
        go_tweet('example.json')
    else:
        for f in argv[1:]:
            go_tweet(f)

if __name__ == '__main__':
    sys.exit(main())
