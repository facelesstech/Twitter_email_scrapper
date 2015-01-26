#!/usr/bin/env python

import twitter, time, re, os
from datetime import datetime, timedelta

class Spammer(object):

    def __init__(self):
        self.twitter_scrap_list = [] # List to hold the twitter email it scrapped
        self.spamfile = 'emails.txt' # Name of the file were saving the emails to
        self.load_txt_list = [] # List to hold the email we load from the txt file so we can re write them back to the txt file

    def searching_twitter(self):
        # Twitter access code to let you scrap twitter
        # Add your twitter dev keys here
        # Use this tutorial if you need help https://facelesstech.wordpress.com/2014/01/01/tweeting-from-python/
        api = twitter.Api(consumer_key='',
                  consumer_secret='',
                  access_token_key='',
                  access_token_secret='')

        self.search = '@gmail.com' # This is what the bot search for on twitter

        # Opens txt file and reads the last place it searched twitter
        fp = open("latest_twitter.txt", 'r')
        lastid = fp.read().strip()
        fp.close()

        self.results = api.GetSearch(self.search, since_id=lastid) # This search twitter via its api
        for statusObj in self.results:
            #screenname = statusObj.user.screen_name # This will get the @ name could be used in the spam email to personalise it

            
            tweet = statusObj.text.lower() # This pulls the twitter body

            self.twitter_scrap_list.append(tweet.encode('ascii', 'replace')) # The text part of the tweet found using the search

            # Writes the latest twitter position to the txt file
            fp = open("latest_twitter.txt", 'w')
            fp.write(str(max([x.id for x in self.results])))
            fp.close()

    def parsing_tweets(self):
        # do not currently know exact meaning of this expression but assuming
        # it means something like "[stuff]@[stuff][stuff1-4 letters]"
        mailsrch = re.compile(r'[\w\-][\w\-\.]+@[\w\-][\w\-\.]+[a-zA-Z]{1,4}')
        # "line" is a variable is set to a single line read from the file
        # ("text.txt"):
        for amount  in self.twitter_scrap_list:
            # this extends the previously named list via the "mailsrch" variable
            # which was named before
            self.load_txt_list.extend(mailsrch.findall(amount))
        
        # Opens txt file to write the parsed emails into
        fp = open(self.spamfile, 'w')
        fp.write(str(self.load_txt_list))
        fp.close()

    def sorting(self):
        try: # Trys to load the txt file but it theres nothing in it it doesnt
            self.load_txt_list = eval(open(self.spamfile).read()) 
            self.parsing_tweets()
        except:# If there isnt anything in the txt file then it goes on without it
            self.parsing_tweets()

    def counter(self):
        try: # Trys to load the txt file to count the emails
            fp = open(self.spamfile, 'r')
            self.newdict = eval(fp.read())
            fp.close()
        except: # If it doesn't find any emails in the file it uses this
            self.newdict = '0'

    def run(self):
        while 1:
            self.searching_twitter()
            # Let's you know you are searching for
            print "\nSearching twitter for %r" % self.search
            # Let's you know how many results it finds
            print 'Found %s results.' % (len(self.results))
            self.sorting()
            sleeping = 30
            self.counter()
            #realtime = sleeping / 60
            print "sleeping for %r seconds" % sleeping 
            now = datetime.now().time() # Current time
            setup_delta = datetime(2000, 1, 1, now.hour, now.minute, now.second) # Setting up current time in the right format
            adding_seconds = setup_delta + timedelta(seconds = 30) # Adds 30 seconds onto current time
            print "Scrips will next run at %s\nThere are %d emails scrapped so far\n" % (adding_seconds.time(), len(self.newdict))
            time.sleep(sleeping) # Sleeping

if __name__ == '__main__':
    spam = Spammer()
    try:
        load = open(spam.spamfile, 'r')
        spam.run()
    except:
        spam.run()


