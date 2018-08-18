from insta import *
from general import *

import csv
import datetime
import pandas as pd

# update the post counter
# check if 24 hours has passed and update the post counter
update_limits()

# username and password
username = "cherry.green.ch"
password = "Cherry_FB_2020"

# read the available messages in all lagnuages and create a dictionary
messages_dict = read_messages()

# create an object of the InstagramBot class
ig = InstagramBot(username, password, messages_dict)

# login instagram with the username and the password
ig.login()

# read the instagram pages that will be scraped
pages = read_pages()
# Todo: Delete this
pages = ['dimosbele', 'cocooning_biocosmetics']

# iterate through pages
# Todo: Delete [0:1]
for page in pages[0:1]:
    print("- Scrapping instagram page: ", page)
    # search the page and scrape the followers
    followers = ig.search_page(page)
    print('---- Number of followers found: ', len(followers))

    users_info_list = []
    cnt_follower = 1
    # Todo: Delete [0:3]
    for follower in followers[0:3]:
        # extract basic information of the follower: UserName, Name and isFollowing
        user_dict = user_basic_info(follower, page, cnt_follower)
        cnt_follower += 1
        users_info_list.append(user_dict)

    #print('users_info_list length: ', len(users_info_list))
    for user in users_info_list:
        print("--- Searching for follower: ", user)
        if user['IsFollowing'] == 'Follow':
            ig.search_user(user)


