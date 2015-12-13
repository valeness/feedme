# FeedMe
Sends you an email at 8am every day with new rss feed updates, takes into account duplicates

Enter this command to edit the crontab to run this script every day at 8am

`crontab -e`

Then add this to the bottom

```

0 8 * * * python /path/to/script/rss.py

```
