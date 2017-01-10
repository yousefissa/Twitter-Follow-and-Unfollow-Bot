Python3

# This is a twitter bot that allows you to do a few things:


1. Follow back users that follow you. 
2. Follow the followers of another user. 
3. Follow users based on a keyword. 
4. Follow users who retweeted a tweet.
5. Unfollow users that don't follow you back. 
6. Unfollow all users. 
7. Favorite tweets based on a keyword. 
8. Send a DM to users that follow you. 
9. Get follower and following count.
10. Quit. 


You will need tweepy, re and time installed.

## Config.py

You must put your auth info into config.py

## For Whitelisting:

Whitelisting a user means that the bot will NOT unfollow them. To whitelist a user, input one screen_name WITHOUT the @ sign per line below. Here are some examples. Input the names to the whitelisted.txt file.

## For Following Based on Keywords:

To follow users based on something they have tweeted, input keywords or keyword phrases in the keywords.txt file. Only put one keyword per line.

## For Sending DMs.

To send DMs, put the messages into the messages.txt file. The bot will send DMs to random users.
