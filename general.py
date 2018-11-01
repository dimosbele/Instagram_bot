import pandas as pd
import datetime
from dateutil.relativedelta import relativedelta
import csv

def update_limits():
    """
    Checks if the last post was done more than 24 hours ago and update the post counter and the date.
    :return: Nothing
    """
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # read the last update date
    limits_file = open("limits.txt", "r")
    lines = limits_file.read().split(',')
    limits_file.close()

    last_update_line = lines[2].split('=')
    last_update = last_update_line[1]
    print('The post counter was last updated at: ', last_update)

    start = datetime.datetime.strptime(now, '%Y-%m-%d %H:%M:%S')
    ends = datetime.datetime.strptime(last_update, '%Y-%m-%d %H:%M:%S')
    diff = relativedelta(start, ends)
    hours = diff.days*24 + diff.hours

    print('The post counter was last updated, ', hours, 'hours ago.')
    if hours>24:
        print('So,it needs to be updated')
        print('Updating post counter...')

        # write the updated inforamtion
        limits_file = open("limits.txt", "w")
        limits_file.write("posts_cnt=%s," % 0)
        limits_file.write("\n")
        limits_file.write("likes_cnt=%s," % 0)
        limits_file.write("\n")
        limits_file.write("last_update=%s" % now)
        limits_file.close()
    else:
        print('So, it should not be updated')

    limits_file.close()


def read_messages():
    """
    Reads the file with the available messages for the posts.
    :return: a dictionary with the available messages in 3 languages
    """
    # read the file with the available messages
    df_messages = pd.read_excel("insta_info.xlsx", sheet_name="messages")
    # create a list with the available messages for each language
    eng_msgs = df_messages['English'].tolist()
    fr_msgs = df_messages['French'].tolist()
    ger_msgs = df_messages['German'].tolist()

    # create a dictionary with all the available messages
    messages_dict = {'eng': eng_msgs, 'fr': fr_msgs, 'ger': ger_msgs}

    return messages_dict

def read_pages():
    """
    Reads the file with tha available pages that will be scraped
    :return: a list with the pages.
    """
    # open and read .xlsx file with the pages to search
    df_pages = pd.read_excel("insta_info.xlsx", sheet_name="pages")
    # create a list with category urls
    pages = df_pages['pages'].tolist()

    return pages


def user_basic_info(follower, page, cnt_follower):
    """

    :param follower: a item of a list with the users basic information that should be handled
    :param page: the name of the page where the user was found as a follower
    :param cnt_follower: counter in order to check if the headers must be writtern in the csv file
    :return: dictionary with the basic information of the follower: UserName, Name and isFollowing
    """
    # extract basic information of the follower: UserName, Name and isFollowing
    elmnts = follower.split('\n')
    print(elmnts)
    user_dict = {}
    user_dict['UserName'] = elmnts[0]
    # some followers dont have Name. They have only useName and isFollowing.
    if elmnts[1] != elmnts[-1]:
        user_dict['Name'] = elmnts[1]
    else:
        user_dict['Name'] = None

    user_dict['IsFollowing'] = elmnts[-1]

    # Write the basic info of the user to a csv
    with open('results/' + page + '.csv', 'a', encoding='utf-8') as file:
        w = csv.DictWriter(file, user_dict.keys(), lineterminator='\n')
        if cnt_follower == 1:
            w.writeheader()
        w.writerow(user_dict)

    return user_dict


def get_message(language, messages_dict):
    """
    Asks the user to select one of the available messages. Or type a new message.
    :param language: the language that was selected: 1, 2 or 3
    :param messages_dict: dictionary with the available messages in the 3 languages
    :return: the message that was finally selected.
    """
    if language == 1:
        print('Available English messages:')
        i = 1
        for msg in messages_dict['eng']:
            print(str(i) + ') ' + msg)
            i += 1
        print(str(len(messages_dict['eng']) + 1) + ') ' + 'Type your own message.')
        print(str(len(messages_dict['eng']) + 2) + ') ' + 'No message')
        try:
            message_id = int(input("Please, select one of the available messages: \n"))
            if message_id <= len(messages_dict['eng']):
                message = messages_dict['eng'][message_id - 1]
            elif message_id == (len(messages_dict['eng'])+1):
                message = input("Please, type your message: ")
            else:
                return 1
        except:
            return 1
    elif language == 2:
        print('Available French messages:')
        i = 1
        for msg in messages_dict['fr']:
            print(str(i) + ') ' + msg)
            i += 1
        print(str(len(messages_dict['fr']) + 1) + ') ' + 'Type your own message.')
        print(str(len(messages_dict['fr']) + 2) + ') ' + 'No message')
        try:
            message_id = int(input("Please, select one of the available messages: \n"))
            if message_id <= len(messages_dict['fr']):
                message = messages_dict['fr'][message_id - 1]
            elif message_id == (len(messages_dict['fr']) + 1):
                message = input("Please, type your message: ")
            else:
                return 1
        except:
            return 1
    elif language == 3:
        print('Available German messages:')
        i = 1
        for msg in messages_dict['ger']:
            print(str(i) + ') ' + msg)
            i += 1
        print(str(len(messages_dict['ger']) + 1) + ') ' + 'Type your own message.')
        print(str(len(messages_dict['ger']) + 2) + ') ' + 'No message')
        try:
            message_id = int(input("Please, select one of the available messages: \n"))
            if message_id <= len(messages_dict['ger']):
                message = messages_dict['ger'][message_id - 1]
            elif message_id == (len(messages_dict['ger']) + 1):
                message = input("Please, type your message: ")
            else:
                return 1
        except:
            return 1
    elif language not in [1,2,3]:
        return 1

    return message


def check_daily_limits(followers):
    # Consider Instagrams rate limits : 250 posts per day
    # limit: 225 posts/day

    # read the file with the post_counter that counts the number of posts and likes that we have done per day.
    # there is also the date of our last post.
    limits_file = open("limits.txt", "r")
    lines = limits_file.read().split(',')
    limits_file.close()

    # the posts counter
    posts_cnt_line = lines[0].split('=')
    posts_cnt = posts_cnt_line[1]
    posts_cnt = int(posts_cnt)

    # the number of likes
    likes_cnt_line = lines[1].split('=')
    likes_cnt = likes_cnt_line[1]
    likes_cnt = int(likes_cnt)

    # the last post/update date
    last_update_line = lines[2].split('=')
    last_update = last_update_line[1]

    # increase the post counter by one
    posts_cnt += 1

    # increase the post counter by 1 or 2
    if followers<=1000:
        likes_cnt += 1
    else:
        likes_cnt += 2

    print('Remaining posts for today:', 225 - posts_cnt, 'out of', 225)
    print('Remaining likes for today:', 500 - likes_cnt, 'out of', 500)
    if (posts_cnt > 225) | (likes_cnt > 500) :
        print('Sorry, you reached the daily limit of Instagram (225 posts/day & 500 likes/day)!')
        print('Please, try again after 24 hours!')
        return False

    # write the new counter value and the new date to the limits.txt
    limits_file = open("limits.txt", "w")
    limits_file.write("posts_cnt=%s," % posts_cnt)
    limits_file.write("\n")
    limits_file.write("likes_cnt=%s," % likes_cnt)
    limits_file.write("\n")
    limits_file.write("last_update=%s" % last_update)
    limits_file.close()

    return True


def read_file_to_set(filepath):
    """
    Write a file to a set
    :param filepath: path of the file
    :return: a set with the data from the file
    """
    with open(filepath, 'r') as f:
        lines = f.read().splitlines()

    return lines

def append_set_to_file(filepath, data):
    """
    Append a set to a file
    :param filepath: path of the file
    :param data: the set to be appended
    """

    with open(filepath, 'a') as f:
        for line in data:
            f.write("%s\n" % line)