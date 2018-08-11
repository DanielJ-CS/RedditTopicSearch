import praw


reddit = praw.Reddit(user_agent='pikv',
                     client_id='ixIkjWMxgYLbxA', client_secret='0KqTxCHUGGUfktFO-qIxqMbwVmE')

def reddit_search(keyword,numberofSubreddits,numberofThreads,numberofComments):
    topic = keyword
    top_subreddits = []
    amountofSubreddits = numberofSubreddits
    amountofComments = numberofComments
    amountofThreads = numberofThreads

    for array_subreddit in reddit.subreddits.search(topic):
        top_subreddits.append(array_subreddit.display_name)

    for subreddit in top_subreddits[:amountofSubreddits]:
        for submission in reddit.subreddit(subreddit).search(topic, limit=amountofThreads):
            count = amountofComments
            if not submission.stickied:
                print('UPVOTES: ', submission.ups)
                print('SUBREDDIT: ', subreddit)
                print('POST: ', submission.title)

                submission.comments.replace_more(limit=None)
                for comment in submission.comments.list():
                    if not comment.stickied:
                        if count > 0:
                            print('UPVOTES: ', comment.ups)
                            print('REPLY: ', comment.body)
                            count = count - 1


def main():
    topic = str(raw_input('What would you like to find reddit posts about: '))
    subreddits = input('How many relevant subreddits relating to the topic would you like to go through: ')
    threads = input('How many threads would you like to search in the subreddits: ')
    comments = input('How many comments would you like to see: ')

    reddit_search(topic,subreddits,threads,comments)

if __name__ == "__main__" :
    main()