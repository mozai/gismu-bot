#!/usr/bin/env python
" posts the arguments as a status update to gismu@twitter "

import json
import sys
import twitter

if len(sys.argv) < 2:
    sys.stderr.write("Usage: %s \"new status message\"\n" % sys.argv[0])
    sys.exit(1)
NEWSTATUS = " ".join(sys.argv[1:]).strip()
if len(NEWSTATUS) == 0:
    sys.stderr.write("Message empty; skipping\n")
    sys.exit(1)

cfg = json.load(open("secrets.json", 'r'))
API = twitter.Api(consumer_key=cfg["CON_KEY"],
                  consumer_secret=cfg["CON_SECRET"],
                  access_token_key=cfg["ACC_KEY"],
                  access_token_secret=cfg["ACC_SECRET"]
                  )
API.PostUpdate(NEWSTATUS)
