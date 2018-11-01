from insta import *
from general import *

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

# read the seller links that have been scraped in the past
already_scraped_users = read_file_to_set('backup/scraped_insta_users.txt')

# iterate through pages
# Todo: Delete [0:1]
for page in pages[0:1]:
#for page in pages:
    print("- Scrapping instagram page: ", page)
    # search the page and scrape the followers
    followers = ig.search_page(page)
    print('---- Number of followers found: ', len(followers))

    users_info_list = []
    cnt_follower = 1
    # Todo: Delete [0:3]
    # iterate through followers of this page
    for follower in followers[0:3]:
    #for follower in followers:
        # extract basic information of the follower: UserName, Name and isFollowing
        user_dict = user_basic_info(follower, page, cnt_follower)
        cnt_follower += 1

        # if this user has not been scraped in the past
        if user_dict['UserName'] in already_scraped_users:
            print('This user has been scraped in the past')
            #next_user = True
            continue
        else:
            #next_user = False
            append_set_to_file('backup/scraped_insta_users.txt', [user_dict['UserName']])

        users_info_list.append(user_dict)

    #if next_user == True:
        #break

    # iterate through followers of this page
    for user in users_info_list:
        print("--- Searching for follower: ", user)
        if user['IsFollowing'] == 'Follow':
            posted = ig.search_user(user)
            if posted == False:
                break
    if posted == False:
        break

# close the browser
ig.closeBrowser()

print("- End of process!")
