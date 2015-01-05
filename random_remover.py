import praw
import random
import time

r = praw.Reddit('Random remover')
r.login()

sub_name = raw_input('Enter subreddit name: ')
top_posts = int(raw_input('Enter number of top posts to choose from: '))
delay = int(raw_input('Enter time between removals (minutes): ')) * 60
deletion_time = int(raw_input('Enter time post is deleted (seconds): '))

subreddit = r.get_subreddit(sub_name)

running = subreddit.user_is_moderator

post_to_remove = None

while(running):
	try:
		posts = subreddit.get_hot(limit=top_posts)
		post_list = []
		for post in posts:
			post_list += [post]
		post_to_remove = post_list[random.randint(0,top_posts-1)]
		print 'Removing post: ' + post_to_remove.permalink
		post_to_remove.remove()
		time.sleep(deletion_time)
		print 'Approving post: ', post_to_remove.permalink
		post_to_remove.approve()
		post_to_remove = None
		print 'Sleeping for ' + str(delay) + ' seconds.'
		time.sleep(delay)
	except KeyboardInterrupt:
		if(post_to_remove != None):
			post_to_remove.approve()
		running = False
	except Exception as e:
		print e
		if(post_to_remove != None):
			post_to_remove.approve()