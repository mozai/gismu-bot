#!/usr/bin/env python
" test the twitter authentication for @gismu "

import json
import twitter

cfg = json.load(open("secrets.json", 'r'))
API = twitter.Api(consumer_key=cfg["CON_KEY"],
                  consumer_secret=cfg["CON_SECRET"],
                  access_token_key=cfg["ACC_KEY"],
                  access_token_secret=cfg["ACC_SECRET"]
                  )

print("Verify credentials:")
print(API.VerifyCredentials())

print("Most Recent Status:")
print(API.GetUserTimeline(screen_name='gismu', count=1)[0])
