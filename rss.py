import feedparser
import sys
import re
import smtplib

from email.mime.text import MIMEText
import creds

class Feed():
    def __init__(self):
        self.file = '/home/gary/scripts/rss/feedlist.csv'
        self.existing_file = '/home/gary/scripts/rss/existing.csv'
        self.feeds = []
        self.body = []
        self.existing = []

    def getFeeds(self):
        with open(self.file, 'r') as f:
            links = f.read()
            links = re.sub('[\s+]', '', links)
            self.feeds = links.split(',')
            #print(self.feeds)
    def getExisting(self):
        with open(self.existing_file, 'r') as f:
            links = f.read()
            links = re.sub('[\s+]', '', links)
            self.existing = links.split(',')
    def setExisting(self):
        with open(self.existing_file, 'a') as f:
            f.write(','.join(self.existing))
    def feedInfo(self):
        self.getFeeds()
        self.getExisting()
        for i in self.feeds:
            feed = feedparser.parse(i)

            if not feed['feed'].has_key('subtitle'):
                feed['feed']['subtitle'] = 'No Subtitle Available'

            feed_body = []
            feed_body.append("Title: {0}".format(feed['feed']['title']))
            feed_body.append("Link : {0}".format(feed['feed']['link']))
            feed_body.append(feed['feed']['subtitle'])
            entries = []
            counter = 1
            for i in feed['entries']:
                link = i['link'].encode('ascii', 'ignore')
                if counter == 6:
                    break
                if link in self.existing:
                    continue
                else:
                    counter += 1
                    self.existing.append(link)
                    entries.append("{0} | {1}".format(
                        i['title'].encode('ascii', 'ignore'),
                        link
                        ))
            feed_body.append("\t{0}".format('\n\t'.join(entries)))


            self.body.append('\n'.join(feed_body))
        #print('\n \n'.join(self.body))
        self.setExisting()
        self.sendEmail()

    def sendEmail(self):
        body = '\n \n'.join(self.body)
        msg = MIMEText(body)
        s = smtplib.SMTP(host='smtp.gmail.com', port=587)
        s.starttls()
        s.login(creds.user, creds.password)
        s.sendmail(creds.from_email, creds.to_email, msg.as_string())
        s.quit()

    def addFeed(self):
        url = sys.argv[2]
        print(url)
feed = Feed()
feed.feedInfo()
