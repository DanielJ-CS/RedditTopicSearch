import praw


reddit = praw.Reddit(user_agent='pikv',
                     client_id='ixIkjWMxgYLbxA', client_secret='0KqTxCHUGGUfktFO-qIxqMbwVmE')

def main():
    topic = 'hifiman'
    top_subreddits = []
    amountofSubreddits = 3
    amountofComments = 3
    amountinSearch = 1

    for array_subreddit in reddit.subreddits.search(topic):
        top_subreddits.append(array_subreddit.display_name)

    for subreddit in top_subreddits[:amountofSubreddits]:
        for submission in reddit.subreddit(subreddit).search(topic,limit=amountinSearch):
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


if __name__ == "__main__" :
    main()