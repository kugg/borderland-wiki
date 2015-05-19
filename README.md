Wiki robot defence
------------------

A wiki cleaner for wiki.theborderland.se based on secritary from noisebridge.

This software can run on any Linux machine with Python2.7  and does not have
to be installed on the wiki server.

This sotware depends on cssselect (https://pypi.python.org/pypi/cssselect) and
pywikibot-compat (in repo).

Install it by making a
```
git clone https://github.com/SimonSapin/cssselect/
python cssselect/setup.py install --user
```
You may need to install python-mechanize and python-lxml
```
apt-get install python-mechanize python-lxml
```
This will install the cssselect library for your user.

Pywikibot is already in this repository you only have to set one environment
variable to have it configured.

Enter the directory where you have cloned this repository and run:

```
export PYWIKIBOT_DIR=$PWD
```
Running
-------

Create a login cookie by running:
```
python ./login.py -v -v
```

The account should now be authenticated using a cookie file.

Run the wiki cleaner!

```
./death_to_wikispammers.py
```

It will prompt you with the usernames from the registered user
list and ask you if they should be removed or not.

It will save the name of the latest account in /tmp
where you can retrieve it after 500 accounts have been handled.

Take the name from the last attempt and use it as an argument to
death_to_wikispammers.py to continue the next batch of 500 accounts.

Trouble?
--------

If you get an error similar to this one:
```
userlib.UserActionRefuse: You don't have permission to block
```
It means that your account in user-config.py does not have the correct previlegies.
Check your user-config.py on this line:
```
sysopnames['theborderland']['en'] = u'Secretary'
```
Verify that the same account exists on the wiki site and has account administrative privelegies.
You may also want to verify your cookie file.
```
python ./login.py -test
```

Good luck!

Details
-------

[Secretaribot](https://www.noisebridge.net/wiki/Secretaribot) is actually a few (quite small) python scripts, which, along with [Noisebot](https://www.noisebridge.net/wiki/Noisebot), help out the Noisebridge collective with housekeeping tasks.

This document is automagically created by make.py and README.intro in the
Secretaribot repository at [github](https://github.com/dannyob/secretaribot),
which is written out to the [Secretaribot's
page](https://www.noisebridge.net/wiki/Secretaribot) on the Noisebridge wiki. 

### General instructions ###

For the wiki tools, you'll need the
[pywikipediabot](http://pywikipediabot.sourceforge.net/) library stored
somewhere, and point the environment variable PYWIKIBOT_DIR at it. Copy the
'lib/noisebridge_family.py' into its 'families' directory.

### death_to_wikispammers ###

Usage: death_to_wikispammers [username]
Downloads a list of recently created users, starting at the username given.
One by one, shows their user page via STDOUT.
Delete user page and block for spam? it asks, [y/n]
If yes, deletes user page, blocks user for spamming
If no, goes onto next

### make_list_rss.py ###

Makes an RSS feed of all the noisebridge mailing lists.

Uses a noisebridge fork of mailman-archive-scraper, kept at
https://github.com/dannyob/mailman-archive-scraper/tree/noisebridge

and added as a git submodule to this collection.

### make_readme.py ###

Meta-helper script to write the README in this directory to the Secretaribot page on the NB wik.

### merge_blocked_users.py ###

Merge (and then delete) all blocked users into a single, uber-spam account.

'And nothing of value was lost'

### next_meeting.py ###

Creates the next meeting page from the template on the wiki.
Calculates the next ordinal number for the meeting ie (the 31811th Meeting etc)
Redirects 'Next meeting' and 'Last meeting' pages to point to correct minutes.

### pywikipediabot.py ###

Looks for and loads the pywikipediabot library from environment variable
$PYWIKIBOT_DIR.

### userlistpage.py ###

Utilities for getting lists of users from mediawiki installs

### www_watch.py ###

Goes out and checks a Wikipedia table full of links, and saves the etags from
the headers; by updating these etags on the page, it will trigger a mediawiki
page change whenever any of the other pages change. If you watch that page,
you'll be effectively watching all the other external pages.

### arooga.agi - call a bunch of people to 311 conf call ###

Usage: /etc/asterisk/agi-bin/arooga.cgi

Called by Asterisk dialplan, extracts callerid safely,
sends it onto an email alias, records info in syslog.
>>>>>>> d7c5120557327d93a7414afc736fd46b7fc08a51
