from insta import *
from general import *

import csv
import datetime
import pandas as pd

# check if 24 hours has passed and update the post counter
update_limits()


username = "cherry.green.ch"
password = "Cherry_FB_2020"

df_messages = pd.read_excel("insta_info.xlsx", sheet_name="messages")
# create a list with category urls
eng_msgs = df_messages['English'].tolist()
fr_msgs = df_messages['French'].tolist()
ger_msgs = df_messages['German'].tolist()

messages_dict = {'eng': eng_msgs, 'fr':fr_msgs, 'ger':ger_msgs}
#print(messages_dict)

ig = InstagramBot(username, password, messages_dict)
ig.login()

# open and read .xlsx file with the pages to search
df_pages = pd.read_excel("insta_info.xlsx", sheet_name="pages")
# create a list with category urls
pages = df_pages['pages'].tolist()

print(pages)

pages = ['dimosbele', 'cocooning_biocosmetics']

for page in pages[0:1]:
    print("- Scrapping instagram page: ", page)
    followers = ig.search_page(page)
    print('---- Number of followers found: ', len(followers))
    #print(followers)
    users_info_list = []

    cnt_follower = 1
    for follower in followers[0:3]:
        #print("--- Handling follower: ", follower)

        # extract basic information of the follower: UserName, Name and isFollowing
        elmnts = follower.split('\n')
        #print(elmnts)
        user_dict = {}
        user_dict['UserName'] = elmnts[0]
        # some followers dont have Name. They have only useName and isFollowing.
        if elmnts[1] !=elmnts[-1]:
            user_dict['Name'] = elmnts[1]
        else:
            user_dict['Name'] = None

        user_dict['IsFollowing'] = elmnts[-1]
        #print(user_dict)
        # Write the basic info of the user to a csv
        with open('results/' + page +'.csv', 'a', encoding='utf-8') as file:
            w = csv.DictWriter(file, user_dict.keys(), lineterminator = '\n')
            if cnt_follower == 1:
                w.writeheader()
            w.writerow(user_dict)

        cnt_follower += 1
        users_info_list.append(user_dict)

    print('users_info_list length: ', len(users_info_list))
    for user in users_info_list:
        print("--- Searching for follower: ", user)
        if user['IsFollowing'] == 'Follow':
            ig.search_user(user)


