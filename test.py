import praw
import operator
import numpy as np
import string
import unicodedata
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt

reddit = praw.Reddit(user_agent='pikv',
                     client_id='ixIkjWMxgYLbxA', client_secret='0KqTxCHUGGUfktFO-qIxqMbwVmE')

dictionary = dict()
commentArray = []

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
                            commentArray.append(comment.body)
                            count = count - 1

def store_Comments(commentArray):
    stop_words = set(stopwords.words("english"))
    for comment in commentArray:
        commentToken = word_tokenize(comment.lower())
        filteredArray = [w for w in commentToken if not w in stop_words]
        for word in filteredArray:
            if word not in string.punctuation:
                word = unicodedata.normalize('NFKD',word).encode('ascii', 'ignore')
                if word != '' and  len(word) < 15 and word != "n't":
                    dictionary[word] = dictionary.get(word,0) + 1

# A tolerance value on the number of words is needed so that the plot does not overpopulate
def plot_dict(numberOfWords):
    fullList = sorted(dictionary.items(), key=operator.itemgetter(1), reverse=True)
    sortedList = fullList[:numberOfWords]
    print(sortedList)
    x,y = zip(*sortedList)
    xs = np.arange(len(x))
    width = 1

    plt.bar(xs,y,width,align='center')
    plt.xticks(xs,x)
    plt.xticks(rotation=90)
    plt.yticks(y)
    plt.tight_layout()
    plt.savefig('netscore.png')

    plt.show()

def main():
    topic = str(raw_input('What would you like to find reddit posts about: '))
    subreddits = input('How many relevant subreddits relating to the topic would you like to go through: ')
    threads = input('How many threads would you like to search in the subreddits: ')
    comments = input('How many comments would you like to see: ')

    reddit_search(topic,subreddits,threads,comments)
    store_Comments(commentArray)
    plot_dict(10)

if __name__ == "__main__" :
    main()