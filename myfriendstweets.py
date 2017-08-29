import tweepy #https://github.com/tweepy/tweepy
import csv
import os
import sys


#Twitter API credentials
consumer_key = ""
consumer_secret = ""
access_key = ""
access_secret = ""

#some twitter accounts use funny characters! fix that!
reload(sys)  
sys.setdefaultencoding('utf-8')

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
apis = tweepy.API(auth)

def get_all_tweets(sn,name):
    #Twitter only allows access to a users most recent 3240 tweets with this method

    #initialize a list to hold all the tweepy Tweets
    alltweets = []	

    #make initial request for most recent tweets n tweets n = 300
    s= 1
    print("trying %s:") % name.encode("utf-8")
    try:
        tweets = tweepy.Cursor(apis.user_timeline,id = sn).items(300)
        for status in tweets:
            print("appending status %s: %s") % (str(s),status.text.encode("utf-8"))
            alltweets.append(status)
            s+=1
        
    
        #transform the tweepy tweets into a 2D array that will populate the csv	
        outtweets = [[name, tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in alltweets]
    
        #write the csv	
        with open('_tweets.csv', 'ab') as f:
            writer = csv.writer(f)
            writer.writerow(["screen name","id","created_at","text"])
            writer.writerows(outtweets)
            return
    except Exception as e:
        print(e)
        os.system("pause")


if __name__ == '__main__':
    # will download most recent tweets of all your friends! yay!
    for friend in tweepy.Cursor(apis.friends).items():
        get_all_tweets(friend.id,friend.name)
