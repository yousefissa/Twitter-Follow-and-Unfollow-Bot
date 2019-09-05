## NOTE: This code has not been updated in ~3 years, and although it may still work, I can't say that is efficient. This was a fun little project I made when learning to develop, and I have no plans to update it in the future. If you'd like to take ownership over this repository and clean it up, please shoot me an email. 


# Python Twitter Bot

This is a twitter bot that allows you to do automate a variety of twitter tasks!


1. Follow back users that follow you. 
2. Follow the followers of another user. 
3. Follow users based on a keyword. 
4. Follow users who retweeted a tweet.
5. Unfollow users that don't follow you back. 
6. Unfollow all users. 
7. Like tweets based on a keyword. 
8. Unlike all of your tweets.
9. Send a DM to users that follow you. 
10. Get follower and following count.

### Prerequisites
You will need tweepy, re and time installed. Simply run the corresponding pip command like: 

`pip install tweepy`

Additionally, you will need to set up your config.json file.

### Setting up config.json file

This file is the heart of the bot. You must place your twitter auth info in the auth object. I've labeled what you have to put and where to the best of my abilities. 

Note: Make sure to clear all of the other fields if you do not want to follow based on keyword, whitelist, DM, etc! If you do, simply place your words in the corresponding list seperated by quotations and commas like what I have in the file right now.

### Todo:

* Add the ability to unfavorite all tweets.
* Add a GUI.

## Authors

* **Yousef Issa** - [yousefissa](https://github.com/yousefissa)

## License

This project is licensed under the MIT License.

## Acknowledgments/Other

* Feel free to make edits or to comment on my code so that I can improve!
* Thanks for reading!
