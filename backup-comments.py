#!/usr/bin/python3

# 2017-03-04 - initial version

import praw
import datetime, time, sys
from datetime import timezone

client_id     = 'YOUR_REDDIT/PRAW_CLIENT_ID'
client_secret = 'YOUR_REDDIT/PRAW_CLIENT_SECRET'
user_agent    = 'YOUR_USER_AGENT_STRING'
username      = 'YOUR_REDDIT_USERNAME'
password      = 'YOUR_REDDIT_PASSWORD'

reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
					 user_agent=user_agent,
					 username=username,
					 password=password)

template = """----------------------------------------------------------
Date: {}
Subreddit: {}

{}
"""

def utc_to_local(utc_dt):
	return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)


def comment2str(comment, delay=0):
	d = comment.__dict__
	dt = utc_to_local(datetime.datetime.fromtimestamp(d['created']))
	stamp = dt.strftime("%A, %F %r %Z")	 # Saturday, 2017-03-04 02:57:52 PM CST
	if delay > 0:
		time.sleep(delay)
	return template.format(stamp, d['subreddit'], d['body'])


def progress(n):
	if n%10 == 0:
		sys.stderr.write('{}... '.format(n))
		sys.stderr.flush()


def displayAllMatching(messageList, field, person):
	n = 1
	for message in messageList:
		if getattr(message, field) == person:
			progress(n)
			print(message2str(message, 0.4))
			n += 1
			if len(message.replies) > 0:
				for reply in message.replies:
					progress(n)
					print(message2str(reply, 0.2))
					n += 1
			print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-=-=-=-=-=-")


def main():
	username = reddit.user.me()
	n = 1
	for comment in username.comments.new(limit=None):
		progress(n)
		print(comment2str(comment, 0.2))
		n += 1


if __name__ == '__main__':
	main()
