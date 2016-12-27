# a bot that either follows or unfollows users
# author - yousefissa

# NOTE: You only have to change 1 thing: Change the user info below (screen name ,consumer_key, etc.)
# If you want to harcode your message in, put it under senDM()
# Know your limits with this bot. Look at the twitter API limits so you don't get locked out.


import tweepy, time
from re import search


# Change this!
# user info, change as necessary. Get this info from the twitter app page.
screen_name = ''
CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_TOKEN = ''
ACCESS_SECRET = ''




# authorization from values inputted earlier, do not change.
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)


# ask the user what they want to do then runs the function accordingly
def mainMenu():
    print('Please read the readme on Github before using this bot. \n'
          'This is a bot that allows you to do a few things: \n'
          '1. Follow back users that follow you. \n'
          '2. Follow the followers of another user. \n'
          '3. Follow users based on a keyword. \n'
          '4. Follow users who retweeted a tweet. \n'
          '5. Unfollow users that don\'t follow you back. \n'
          '6. Unfollow all users. \n'
          '7. Send a DM to users that follow you. \n'
          '8. Get follower and following count. \n'
          '9. Quit. '
          )
    userChoice = input('Enter the number of the action that you want to take: ')


    # Dictionary of user choices
    choices = {
    1: followBack,
    2: followAll,
    3: followKeyword,
    4: followRters,
    5: unfollowBack,
    6: unfollowAll,
    7: sendDM,
    8: getCount, 
    9: quit
    }

    # tries running the function according to the number. restarts if given a non-number or number not in range.
    try:
        choices[int(userChoice)]()
    except (ValueError, KeyError):
        print('Input not recognized. You probably did not enter a number. \n'
              'The program will restart. \n')
        mainMenu()



# function to get list of followers and followings, gets whitelisted users
def getFriends():
    # gets a list of your followers and following
    followers = api.followers_ids(screen_name)
    following = api.friends_ids(screen_name)
    # resets total_followed everytime this is called. This is so that the user can keep track when they continue.
    total_followed = 0

    # gets a list of whitelisted users from a text file
    with open('Whitelisted.txt') as whitelistedText:
        whitelistedUsersOld = whitelistedText.read().splitlines()

    # to not modify the iterated we're looping over, a new list is created.
    whitelistedUsers = []

    # convert screen names to user IDs
    for item in whitelistedUsersOld:
        # gets info, then gets id.
        item = api.get_user(screen_name=item).id
        # adds the id into newlist.
        whitelistedUsers.append(item)


    return followers, following, total_followed, whitelistedUsers


# function to follow back users that follow you.
def followBack():
    # gets followers, following, total_followed
    followers, following, total_followed, whitelistedUsers = getFriends()

     # Makes a list of  those you don't follow back.
    nonFollowing = set(followers) - set(following)

    print('Starting to follow users...')

    # starts following users.
    for f in nonFollowing:
        # follows the user if you don't already follow them back.
        api.create_friendship(f)

        # keep track of the total followed
        total_followed += 1
        # print total total every 10 follows
        if total_followed % 10 == 0:
            print(str(total_followed) + ' users followed so far.')

        # sleeps so it doesn't follow too quickly.
        print('Followed user. Sleeping 10 seconds.')
        time.sleep(10)


    # prints the total followed, then continues
    print(total_followed)
    getCount()
    Continue()





# function to follow the followers of another user.
def followAll():
    # gets followers, following, total_followed
    followers, following, total_followed, whitelistedUsers = getFriends()

    # gets a list of their followers
    theirName = input('Input their name. Do not use an @ sign. For example, for @POTUS, input just POTUS: ')
    theirFollowers = api.followers_ids(theirName)

    # Makes a list of nonmutual followings.
    theirFollowersReduced = set(theirFollowers) - set(following)
    # loops through theirFollowers and followers and adds non-mutual relationships to theirFollowersReduced

    print('Starting to follow users...')
    # loops through the list and follows users.
    for f in theirFollowersReduced:
        try:
            # follows the user.
            api.create_friendship(f)
            # keep track of the total followed
            total_followed += 1
            # print total total every 10 follows
            if total_followed % 10 == 0:
                print(str(total_followed) + ' users followed so far.')
            # sleeps so it doesn't follow too quickly.
            print('Followed user. Sleeping 10 seconds.')
            time.sleep(10)
        # most basic error handling.
        except:
            pass


    # prints the total followed, then continues
    print(total_followed)
    getCount()
    Continue()



# function to follow users based on a keyword:
def followKeyword():
    # TODO: implement function to follow based on keywords using search()
    print('This is coming soon.')
    Continue()



# function to follow users who retweeted a tweet.
def followRters():
    # gets followers, following, total_followed
    followers, following, total_followed, whitelistedUsers = getFriends()
    
    print('Per Twitter\'s API, this method only returns a max of 100 users per tweet. \n')

    # gets the tweet ID using regex
    tweetURL = input('Please input the full URL of the tweet: ')
    try:
        tweetID = search('/status/(\d+)', tweetURL).group(1)
    except:
        print('Could not get tweet ID. Try again. ')
        followRters()

    # gets a list of users who retweeted a tweet
    RTUsers = api.retweeters(tweetID)

    print('Starting to follow users.')

    # follows users:
    for f in RTUsers:
        try:
            # follows the user.
            api.create_friendship(f)
            # keep track of the total followed
            total_followed += 1
            # print total total every 10 follows
            if total_followed % 10 == 0:
                print(str(total_followed) + ' users followed so far.')
            # sleeps so it doesn't follow too quickly.
            print('Followed user. Sleeping 10 seconds.')
            time.sleep(10)
        # most basic error handling.
        except:
            print('Could not follow user.')


    # prints the total followed, then continues
    print(total_followed)
    getCount()
    Continue()









# function to unfollow users that don't follow you back.
def unfollowBack():
    # gets followers, following, total_followed
    followers, following, total_followed, whitelistedUsers = getFriends()

    print('Starting to unfollow users...')

    # makes a new list of users who don't follow you back.
    nonMutuals = set(following) - set(followers) - set(whitelistedUsers)
    for f in nonMutuals:
        try:
            # unfollows non follower.
            api.destroy_friendship(f)

            # increment total_followed by 1
            total_followed += 1
            # print total unfollowed every 10
            if total_followed % 10 == 0:
                print(str(total_followed) + ' unfollowed so far.')

            # print sleeping, sleep.
            print('Unfollowed user. Sleeping 2 seconds.')
            time.sleep(2)
        except:
            print('Could not follow users. Trying next user.')


    # prints the total followed, then continues
    print(total_followed)
    getCount()
    Continue()

# function to unfollow all users.
def unfollowAll():
    # gets followers, following, total_followed
    followers, following, total_followed, whitelistedUsers = getFriends()

    # whitelists some users.
    unfollowingUsers = set(following) - set(whitelistedUsers)

    print('Starting to unfollow.')
    for f in unfollowingUsers:
        # unfollows user
        api.destroy_friendship(f)
        # increment total_followed by 1
        total_followed += 1
        # print total unfollowed every 10
        if total_followed % 10 == 0:
            print(str(total_followed) + ' unfollowed so far.')

        # print sleeping, sleep.
        print('Unfollowed user. Sleeping 3 seconds.')
        time.sleep(3)
    # prints the total followed, then continues
    print(total_followed)
    getCount()
    Continue()


# TODO: allow the importing of text lists so messages don't get flagged as spam.
# Send a DM to users that follow you.
def sendDM():
    # gets followers, following, total_followed
    followers, following, total_followed, whitelistedUsers = getFriends()

    print('A message will be sent')

    # If you want to hardcode your message, remove the input from the message variable.
    # gets the message from the user. 
    message = input('Enter the message you want to send: \n')

    # tries sending a message to your followers. 
    print('Starting to send messages... ')
    for f in followers:
        try: 
            # sends dm. 
            api.send_direct_message(user_id=f, text=message)

            # increment total_followed by 1
            total_followed += 1
            # print total unfollowed every 10
            if total_followed % 10 == 0:
                print(str(total_followed) + ' messages sent so far.')

            print('Sent the user a DM. Sleeping 15 seconds.')
            time.sleep(15)

        except:
            print('Could not send a DM. Trying another user.')
    print(total_followed)
    getCount()
    Continue()



# function to get follower/following count
def getCount():
    # gets followers, following, total_followed
    followers, following, total_followed, whitelistedUsers = getFriends()
    # prints the count.
    print('You follow {} users and {} users follow you.'.format(len(followers), len(followers)))
    print('This is sometimes inaccurate due to the nature of the API and updates. Be sure to double check. ')
    Continue()



# function to continue
def Continue():
    # asks the user if they want to keep calculating, converts to lower case
    keepGoing = input('Do you want to keep going? Enter yes or no. \n'
                      '').lower()
    # evaluates user's response.
    if keepGoing == 'yes':
        mainMenu()
    elif keepGoing == 'no':
        print('\n'
              'Thanks for using the Twitter bot!')
        quit()
    else:
        print('\n'
              'Input not recognized. Try again.')
        Continue()



# runs the main function, which runs everything else.
mainMenu()




