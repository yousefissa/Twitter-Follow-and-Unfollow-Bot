# a bot that either follows or unfollows users
# author - yousefissa

# Know your limits with this bot. Look at the twitter API limits so you don't get locked out.

import tweepy, time




# ONLY THING TO CHANGE
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
    print('This is a bot that allows you to do a few things: \n'
          '1. Follow back users that follow you. \n'
          '2. Follow the followers of another user. \n'
          '3. Follow users based on a keyword. \n'
          '4. Unfollow users that don\'t follow you back. \n'
          '5. Unfollow all users. \n'
          '6. Get follower and following count. \n'
          )
    userChoice = input('Enter the number of the action that you want to take: ')


    # Dictionary of user choices
    choices = {
    1: followBack,
    2: followAll,
    3: followKeyword,
    4: unfollowBack,
    5: unfollowAll,
    6: getCount
    }

    # tries running the function according to the number. restarts if given a non-number or number not in range.
    try:
        choices[int(userChoice)]()
    except (ValueError, KeyError):
        print('Input not recognized. You probably did not enter a number. \n'
              'The program will restart. \n')
        mainMenu()



# function to get list of followers and followings
def getFriends():
    # gets a list of your followers and following
    followers = api.followers_ids(screen_name)
    following = api.friends_ids(screen_name)
    # resets total_followed everytime this is called. This is so that the user can keep track when they continue.
    total_followed = 0
    return followers, following, total_followed


# function to follow back users that follow you.
def followBack():
    # gets followers, following, total_followed
    followers, following, total_followed = getFriends()

     # Makes a list of  those you don't follow back.
    nonFollowing = set(followers) - set(following)

    print('Starting to follow.')

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
    followers, following, total_followed = getFriends()

    # gets a list of their followers
    theirName = input('Input their name. Do not use an @ sign. For example, for @POTUS, input just POTUS: ')
    theirFollowers = api.followers_ids(theirName)

    # Makes a list of nonmutual followings.
    theirFollowersReduced = set(theirFollowers) - set(following)
    # loops through theirFollowers and followers and adds non-mutual relationships to theirFollowersReduced

    print('Starting to follow.')
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

# function to unfollow users that don't follow you back.
def unfollowBack():
    # gets followers, following, total_followed
    followers, following, total_followed = getFriends()

    print('Starting to unfollow.')
    # loops through followers and following lists.
    for f in following:
        if f not in followers:
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
    # prints the total followed, then continues
    print(total_followed)
    getCount()
    Continue()

# function to unfollow all users.
def unfollowAll():
    # gets followers, following, total_followed
    followers, following, total_followed = getFriends()

    print('Starting to unfollow.')
    for f in following:
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



# function to get follower/following count
def getCount():
    # gets followers, following, total_followed
    followers, following, total_followed = getFriends()
    # prints the count.
    print('You follow {} users and {} users follow you.'.format(len(followers), len(followers)))
    print('This is sometimes inaccurate due to the nature of the API and time. Be sure to double check. ')
    Continue()



# function to continue
def Continue():
    # asks the user if they want to keep calculating.
    keepGoing = input('Do you want to keep going? Enter yes or no. \n'
                      '')
    keepGoing = keepGoing.lower()
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




