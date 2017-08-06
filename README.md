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

## Setting up config.json file

This file is the heart of the bot. You must place your twitter auth info in the auth object. I've labeled what you have to put and where to the best of my abilities. 

Note: Make sure to clear all of the other fields if you do not want to follow based on keyword, whitelist, DM, etc! If you do, simply place your words in the corresponding list seperated by quotations and commas like what I have in the file right now.