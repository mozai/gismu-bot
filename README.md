gismu-bot
=========
This is an automated agent that posts a "word-a-day" sort of thing to
Twitter for the language Lojban.  Twitter account is @gismu.

The four parts of speech in Lojban are gismu (root predicate-words),
lujvo (compound predicate-words), cmavo (structure-words),
and cmene (name-words).

It's actually not daily but every eight hours, so that it will cycle
over a year.  The lexicon I have contains 1436 gismu, and 8760 hours /
6 hours = 1430 words.  I've pre-processed the gismu list so that it
only states the word, one or two English translations (first literal,
then general-use), then the text of how the predicate is used.  The list
is sorted randomly and stored, to make sure of no repeats.


SETUP
-----
- install Bear's python-twitter module
  - cd $(mktemp -d)
  - git clone https://github.com/bear/python-twitter.git
  - cd python-twitter
  - sudo python setup.py install
- register a new app with twitter:
  - http://twitter.com/oauth_clients
  - API key: AAAAAAAAAAAAAAAAAAAA
  - Consumer key: AAAAAAAAAAAAAAAAAAAA
  - Consumer secret: SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS
  - write these into `secrets.json`
- prep the gismu list:
  - `perl -ne 'chomp; next if /^ \d+ /; $g = substr($_,1,5); $e = substr($_,20,42); $e =~ s/  +/ /g; $e =~ s/^ +| +$//g; $def = substr($_,62); $def =~ s/  .+//; $def =~ s/ \d\w \d\d\d$//; $line ="$g: $e. $def"; $line =~ s/"/\x27/g; die "$line\n" if length($line) > 140; print "$line\n";' /usr/share/lojban/gismu.txt | shuf > ./gismu_list.txt; /bin/rm -f gismu_list.txt.offset`
  - there should be no " marks in the gismu_list.txt file
  - for tradition's sake, put the gismu 'gismu' at the top of the list.  It's a good sign of when the stack rolls over.
- the crojob
  - `19 */8 * * *    ( cd gismu-bot && NEXT=$(./nextline gismu_list.txt); if [ -n "$NEXT" ];then ./post_tweet.py "$NEXT" ; else echo >&2 "End Of List reached"; fi )`


POST A NEW GISMU
----------------
    cd /usr/local/gismu-bot;
    NEXT=`./nextline gismu_list.txt`;
    [ "$NEXT" ] && ./gismu_tweet.py "$NEXT" || echo "no more gismu."


TODO
----
- pure python implementation of nextline.c
- re-shuffle the word list automatically when it reaches the end.
- support other platforms in case Twitter implodes
- is there an updated Lojban dictionary, in the 18 years since I made this?


LOG
---
* 2023 Mar.  Bear's python-twitter module changed, has a syntax error
  and some incompatible changes to method calls.
* 2022 Nov.  Twitter bought by whats-his-name.  Oh boy.
* 2021 Jul 07. reached the end, got the email warning.
  STILL haven't automated reshuffling the list.
* 2020 Apr 15. reached the end, got the email warning.
  Still haven't automated this.
* 2020 Jan 22. reached the end, got the email warning.  Opened the
  `gismu_list.txt` in vi, `:2,1341!shuf`, then deleted `*.offset`
  Still haven't automated this.
* 2018 Oct 29. reached the end, got the email warning.  Shuffled the
  list by hand, putting 'gismu' at the start and 'fanmo' at the end,
  then deleted `gismu_list.offset`.
* 2017 Aug 7. reached the end again, got the email warning.  Shuffled the
  list by hand, putting 'gismu' at the start and 'fanmo' at the end.
* 2016 Apr 8. Reminder to self: I say these are gismu, but not all the
  words in the reference `gismu.txt` list are gismu (CVCCV or CCVCV).
  Need to change the list before the next restart.
* 2014 Apr 3. Ran out again. Didn't notice until Sept 10. Really need
  to fix it so I get notified.  Reshuffled the list, put 'gismu' at
  the top, deleted `gismu_list.offset` to get it going again.
* 2013 Feb 17.  I ran out of gismu, but I didn't notice until Mar 25
  16h40. Erased the `*.offset` file, reshuffled the gismu list (except the
  first entry, 'gismu').  Retstart!
* 2012 Jun 11 18:46 EDT. Getting this error message: 'The Twitter REST
  API v1 is no longer active. Please migrate to API v1.1.'
  and Tweepy is gone!


