#!/usr/bin/env python3
# a bot that either follows or unfollows users
# author - yousefissa

# NOTE: You only have to change 1 thing: Change the user info below (screen name ,consumer_key, etc.)
# If you want to hardcode your message in, put it under senDM()
# Know your limits with this bot. Look at the twitter API limits so you don't get locked out.


import tweepy
from time import sleep
from re import search
from config import *
from itertools import cycle
from random import shuffle

# authorization from values inputted earlier, do not change.
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)


# ask the user what they want to do then runs the function accordingly
def main_menu():
    print('''
Please read the readme on Github before using this bot.

This is a bot that allows you to do a few things: 
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
    '''
          )

    userChoice = input('Enter the number of the action that you want to take: ')

    # Dictionary of user choices
    choices = {
        1: follow_back,
        2: follow_all,
        3: follow_keyword,
        4: follow_rters,
        5: unfollow_back,
        6: unfollow_all,
        7: fav_off_keyword,
        8: send_dm,
        9: get_count,
        10: quit
    }

    # tries running the function according to the number. restarts if given a non-number or number not in range.
    try:
        choices[int(userChoice)](*get_friends())
    except (ValueError, KeyError):
        print('Input not recognized. You probably did not enter a number. \n'
              'The program will restart. \n')
        main_menu()
    finally:
        Continue()


# function to get list of followers and followings, gets whitelisted users
def get_friends():
    # gets a list of your followers and following
    followers = api.followers_ids(screen_name)
    following = api.friends_ids(screen_name)
    total_followed = 0

    # gets a list of whitelisted users from a text file
    with open('Whitelisted.txt') as whitelistedText:
        whitelisted_users_old = whitelistedText.read().splitlines()
    whitelisted_users = []
    # convert screen names to user IDs
    for item in whitelisted_users_old:
        try:
            # gets info, then gets id.
            item = api.get_user(screen_name=item).id
            # adds the id into newlist.
            whitelisted_users.append(item)
        except tweepy.TweepError:
            pass
    # blacklist users to not folllow
    with open('blacklisted.txt') as blacklisted_text:
        blacklisted_users = blacklisted_text.read().splitlines()

    return followers, following, total_followed, whitelisted_users, blacklisted_users


# function to follow back users that follow you.
def follow_back(followers, following, total_followed, whitelisted_users, blacklisted_users):
    # Makes a list of  those you don't follow back.
    non_following = set(followers) - set(following) - set(blacklisted_users)

    print('Starting to follow users...')

    # starts following users.
    for f in non_following:
        try:
            api.create_friendship(f)
            total_followed += 1
            if total_followed % 10 == 0:
                print(str(total_followed) + ' users followed so far.')
            print('Followed user. Sleeping 10 seconds.')
            sleep(10)
        except (tweepy.RateLimitError, tweepy.TweepError) as e:
            error_handling(e)
    print(total_followed)
    

# function to follow the followers of another user.
def follow_all(followers, following, total_followed, whitelisted_users, blacklisted_users):
    their_name = input('Input their name. Do not use an @ sign. For example, for @POTUS, input just POTUS: ')
    their_followers = api.followers_ids(their_name)

    # Makes a list of nonmutual followings.
    their_followers_reduced = set(their_followers) - set(following) - set(blacklisted_users)
    # loops through their_followers and followers and adds non-mutual relationships to their_followers_reduced

    print('Starting to follow users...')
    # loops through the list and follows users.
    for f in their_followers_reduced:
        try:
            # follows the user.
            api.create_friendship(f)
            total_followed += 1
            if total_followed % 10 == 0:
                print(str(total_followed) + ' users followed so far.')
            print('Followed user. Sleeping 10 seconds.')
            sleep(10)
        except (tweepy.RateLimitError, tweepy.TweepError) as e:
            error_handling(e)
    print(total_followed)
    

# function to follow users based on a keyword:
def follow_keyword(followers, following, total_followed, whitelisted_users, blacklisted_users):
    with open('keywords.txt') as keywords_text:
        keywords = keywords_text.read().splitlines()
    for i in keywords:
        # gets search result
        search_results = api.search(q=i, count=100)
        searched_screen_names = [tweet.author._json['screen_name'] for tweet in search_results]
        searched_screen_names = list(set(searched_screen_names) - set(blacklisted_users))

        # only follows 100 of each keyword to avoid following non-relevant users.
        print('Starting to follow users who tweeted \'{}\''.format(i))
        for i in range(0, len(searched_screen_names) - 1):
            try:
                # follows the user.
                api.create_friendship(searched_screen_names[i])
                total_followed += 1
                if total_followed % 10 == 0:
                    print(str(total_followed) + ' users followed so far.')
                print('Followed user. Sleeping 10 seconds.')
                sleep(10)
            except (tweepy.RateLimitError, tweepy.TweepError) as e:
                error_handling(e)
    print(total_followed)
    


# function to follow users who retweeted a tweet.
def follow_rters(followers, following, total_followed, whitelisted_users, blacklisted_users):
    print('Per Twitter\'s API, this method only returns a max of 100 users per tweet. \n')

    # gets the tweet ID using regex
    tweet_url = input('Please input the full URL of the tweet: ')
    try:
        tweetID = search('/status/(\d+)', tweet_url).group(1)
    except tweepy.TweepError as e:
        print(e)
        print('Could not get tweet ID. Try again. ')
        follow_rters()

    # gets a list of users who retweeted a tweet
    RTUsers = api.retweeters(tweetID)
    RTUsers = set(RTUsers) - set(blacklisted_users)

    print('Starting to follow users.')

    # follows users:
    for f in RTUsers:
        try:
            api.create_friendship(f)
            total_followed += 1
            if total_followed % 10 == 0:
                print(str(total_followed) + ' users followed so far.')
            # sleeps so it doesn't follow too quickly.
            print('Followed user. Sleeping 10 seconds.')
            sleep(10)
        except (tweepy.RateLimitError, tweepy.TweepError) as e:
            error_handling(e)
    print(total_followed)
    


# function to unfollow users that don't follow you back.
def unfollow_back(followers, following, total_followed, whitelisted_users, blacklisted_users):
    print('Starting to unfollow users...')
    new_blacklisted_users = []
    # makes a new list of users who don't follow you back.
    non_mutuals = set(following) - set(followers) - set(whitelisted_users)
    for f in non_mutuals:
        try:
            # unfollows non follower.
            api.destroy_friendship(f)
            new_blacklisted_users.append(f)
            total_followed += 1
            if total_followed % 10 == 0:
                print(str(total_followed) + ' unfollowed so far.')
                # writes blacklisted users to file
                with open('blacklisted.txt', mode='a') as blacklisted_text: 
                    blacklisted_text.write('\n'.join(map(str,new_blacklisted_users)))
                    new_blacklisted_users = []
            # print sleeping, sleep.
            print('Unfollowed user. Sleeping 15 seconds.')
            sleep(15)
        except (tweepy.RateLimitError, tweepy.TweepError) as e:
            error_handling(e)
    print(total_followed)
    


# function to unfollow all users.
def unfollow_all(followers, following, total_followed, whitelisted_users, blacklisted_users):
    # whitelists some users.
    unfollowing_users = set(following) - set(whitelisted_users)
    new_blacklisted_users = []
    print('Starting to unfollow.')
    for f in unfollowing_users:
        # unfollows user
        api.destroy_friendship(f)
        new_blacklisted_users.append(f)
        # increment total_followed by 1
        total_followed += 1
        # print total unfollowed every 10
        if total_followed % 10 == 0:
            print(str(total_followed) + ' unfollowed so far.')
            with open('blacklisted.txt', mode='a') as blacklisted_text: 
                blacklisted_text.write('\n'.join(map(str,new_blacklisted_users)))
                new_blacklisted_users = []
        # print sleeping, sleep.
        print('Unfollowed user. Sleeping 8 seconds.')
        sleep(8)
    print(total_followed)
    


# Function to favorite tweets based on keywords
def fav_off_keyword(followers, following, total_followed, whitelisted_users, blacklisted_users):
    with open('keywords.txt') as keywords_text:
        keywords = keywords_text.read().splitlines()

    for i in keywords:
        # gets search result
        search_results = api.search(q=i, count=100)
        searched_tweet_ids = [tweet.id for tweet in search_results]

        # only follows 100 of each keyword to avoid following non-relevant users.
        print('Starting to favorite users who tweeted \'{}\''.format(i))
        for i in range(0, len(searched_tweet_ids) - 1):
            try:
                api.create_favorite(searched_tweet_ids[i])
                total_followed += 1
                if total_followed % 10 == 0:
                    print(str(total_followed) + ' tweets favorited so far.')
                print('Favorited tweet. Sleeping 12 seconds.')
                sleep(12)
            except (tweepy.RateLimitError, tweepy.TweepError) as e:
                error_handling(e)
    print(total_followed)
    


# TODO: allow the importing of text lists so messages don't get flagged as spam.
# Send a DM to users that follow you.
def send_dm(followers, following, total_followed, whitelisted_users, blacklisted_users):
    with open('messages.txt') as messages_text:
        messages = messages_text.read().splitlines()
    # users already dm'd
    with open('users_messaged.txt') as users_messaged_text:
        users_messaged = users_messaged_text.read().splitlines()
    followers = list(set(followers) - set(users_messaged))
    shuffle(followers)
    new_users_messaged = []
    greetings = ['Hey', 'Hi', 'Hello']
    # tries sending a message to your followers. switches greeting and message. 
    print('Starting to send messages... ')
    for user, message, greeting in zip(followers, cycle(messages), cycle(greetings)):
        try:
            username = api.get_user(user).screen_name
            # sends dm. 
            api.send_direct_message(user_id=user, text='{} {},\n{}'.format(greeting, username, message))
            new_users_messaged.append(user)
            total_followed += 1
            if total_followed % 5 == 0:
                print(str(total_followed) + ' messages sent so far.')
                with open('users_messaged.txt', mode='a') as users_messaged_text:
                    users_messaged_text.write('\n'.join(map(str,new_users_messaged)))
                    new_users_messaged = []
            print('Sent the user a DM. Sleeping 45 seconds.')
            sleep(45)
        except (tweepy.RateLimitError, tweepy.TweepError) as e:
            error_handling(e)
    print(total_followed)
    

# function to get follower/following count
def get_count(followers, following, total_followed, whitelisted_users, blacklisted_users):
    # prints the count.
    print('You follow {} users and {} users follow you.'.format(len(followers), len(followers)))
    print('This is sometimes inaccurate due to the nature of the API and updates. Be sure to double check. ')
    


# function to handle errors
def error_handling(e):
    error = type(e)
    if error == tweepy.RateLimitError:
        print('You\'ve hit a limit! Sleeping for 30 minutes.')
        sleep(60 * 30)
    if error == tweepy.TweepError:
        print('Uh oh. Could not complete task. Sleeping 10 seconds.')
        sleep(10)


# function to continue
def Continue():
    # asks the user if they want to keep calculating, converts to lower case
    keep_going = input('Do you want to keep going? Enter yes or no. \n'
                       '').lower()
    # evaluates user's response.
    if keep_going == 'yes':
        main_menu()
    elif keep_going == 'no':
        print('\n'
              'Thanks for using the Twitter bot!')
        quit()
    else:
        print('\n'
              'Input not recognized. Try again.')
        

# runs the main function, which runs everything else.
if __name__ == "__main__":  
    main_menu()
