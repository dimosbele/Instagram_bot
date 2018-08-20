from general import *

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

import datetime
import time
import random
import csv

class InstagramBot:

    def __init__(self, username, password, messages_dict):
        self.username = username
        self.password = password
        self.messages_dict = messages_dict
        self.driver = webdriver.Chrome('chromedriver.exe')
        #self.driver.set_window_size(700, 900)


    def closeBrowser(self):
        """
        Close the browser.
        :return: Nothing
        """
        self.driver.close()

    def login(self):
        """
        Login to instagram using the username and the password.
        :return: Nothing
        """
        driver = self.driver
        driver.get("https://www.instagram.com/")
        time.sleep(2)
        login_button = driver.find_element_by_xpath("//a[@href='/accounts/login/']")
        login_button.click()
        time.sleep(2)
        user_name_elem = driver.find_element_by_xpath("//input[@name='username']")
        user_name_elem.clear()
        user_name_elem.send_keys(self.username)
        passworword_elem = driver.find_element_by_xpath("//input[@name='password']")
        passworword_elem.clear()
        passworword_elem.send_keys(self.password)
        passworword_elem.send_keys(Keys.RETURN)
        time.sleep(2)



    def search_page(self, page):
        """
        The browser gets an instagram page and scrapes the basic informatiom of all the followers, from the pop up window.
        :param page: The name of the page. e.g. cocooning_biocosmetics
        :return: a list with all the followers basic information: UserName, Name and isFollowing
        """
        driver = self.driver
        print('--- Getting url: https://www.instagram.com/' + page)
        driver.get("https://www.instagram.com/" + page)
        time.sleep(2)

        # click the button to open the folloers pop up window
        driver.find_element_by_partial_link_text("follower").click()
        print('--- Opening followers pop up window.')
        time.sleep(5)

        # Scroll down followers page
        dialog = driver.find_element_by_xpath('/html/body/div[3]/div/div[2]/div/div[2]')
        # max scroll times
        scrolls = 300
        # counter to undersand when scrolled to the bottom
        pre_followers_cnt = 0
        for i in range(scrolls):
            #print('Scroll_id', i)
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", dialog)
            time.sleep(random.randint(500, 1000) / 1000)
            # every 5 scrolls, it checks if it has been scrolled to the bottom.
            if i%5==0:
                print('Checking if it scrolled to the bottom')
                followers_cnt = driver.find_elements_by_class_name('NroHT')
                #print('pre_followers_cnt = ', pre_followers_cnt)
                #print('followers_cnt = ', len(followers_cnt))
                # if the following is True: it can't scroll down any more.
                if pre_followers_cnt == len(followers_cnt):
                    print('-----Scrolled to the bottom.')
                    break
                pre_followers_cnt = len(followers_cnt)

        # Finally, scrape the followers
        print('--- Scrapping followers pop up window.')
        followers_elems = driver.find_elements_by_class_name('NroHT')

        # return a list with all the followers information
        return [e.text for e in followers_elems]


    def write_comment(self, comment_text):
        """
        Writes the message as a comment of the picture.
        :param comment_text:
        :return: comment_box_elem or False
        """
        try:
            time.sleep(3)
            #comment_button = lambda: self.driver.find_element_by_link_text('Comment')
            comment_button = lambda: self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/article/div[2]/section[1]/span[2]/button')
            comment_button().click()
        except NoSuchElementException as e:
            print(e)
            pass

        try:
            comment_box_elem = lambda: self.driver.find_element_by_xpath("//textarea[@aria-label='Add a comment…']")
            time.sleep(2)
            comment_box_elem().send_keys('')
            comment_box_elem().clear()
            for letter in comment_text:
                comment_box_elem().send_keys(letter)
                time.sleep((random.randint(1, 7) / 30))

            return comment_box_elem

        except StaleElementReferenceException and NoSuchElementException as e:
            print(e)
            return False


    def post_comment(self, comment_text):
        """
        Posts the message as a comment of the picture. It also checks if the comments was really posted.
        :param comment_text: The message that will be posted.
        :return: True or False
        """
        time.sleep(2)

        comment_box_elem = self.write_comment(comment_text)
        if comment_text in self.driver.page_source:
            comment_box_elem().send_keys(Keys.ENTER)
            try:
                post_button = lambda: self.driver.find_element_by_xpath("//button[@type='Post']")
                post_button().click()
                print('clicked post button')
            except NoSuchElementException:
                pass

        time.sleep(2)
        self.driver.refresh()
        if comment_text in self.driver.page_source:
            return True

        return False

    def search_user(self, user):
        """
        Opens the users profile in the browser and finds the most recent picture. Waits for the user to select a language and a message.
        Checks if the are available posts for today (225/day) looking in the details.txt and posts the message.
        :param user: the username of the user that we are looking for
        :return: Nothing
        """
        driver = self.driver
        messages_dict = self.messages_dict

        # open the user profile in the browser
        driver.get("https://www.instagram.com/" + user['UserName'])
        time.sleep(2)

        # scrape the users' page

        # the short description of the user
        description = driver.find_element_by_class_name("-vDIg")

        # numeric details are number of posts, followers and following
        numeric_details = driver.find_elements_by_class_name("Y8-fY ")
        numeric_details_list = [e.text for e in numeric_details]
        posts = numeric_details_list[0]
        followers = numeric_details_list[1]
        following = numeric_details_list[2]

        # create a dictionary with the details of the user
        user_details = {}
        user_details['UserName'] = user['UserName']
        user_details['Name'] = user['Name']
        user_details['User_Url'] = "https://www.instagram.com/" + user['UserName']
        user_details['Scrapping_date'] = datetime.datetime.now()
        user_details['posts'] = posts
        user_details['followers'] = followers
        user_details['following'] = following
        user_details['description'] = description.text

        # open the most recent picture of the user
        #link = driver.find_element_by_class_name('v1Nh3 kIKUG  _bz0w')
        links_tags = driver.find_elements_by_tag_name('a')
        links = [elem.get_attribute('href') for elem in links_tags if
                 'taken-by=' in elem.get_attribute('href')]

        # if the are available pictures, commend the first
        if len(links)>0:
            last_pic_href = links[0]
            print("---Commenting the first picture of user", user_details['User_Url'])
            print("----Picture URL: ", last_pic_href)

            # open the page with the most recent picture in the browser
            # ToDo: delete my picture
            driver.get(last_pic_href)
            #driver.get('https://www.instagram.com/p/BmWawZ6h4Fl/?taken-by=dimosbele')
            time.sleep(2)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # The user selects one of the available languages for the post: English, French, German
            language = int(input("Please, select the language: \n 1.English, \n 2.French, \n 3.German, \n 4.No message \n"))

            # The user selects one of the available messages in the language that was selected
            message = get_message(language, messages_dict)
            print('Thank you! You selected the following message: ', message)

            if message == 1:
                return 1

            # add the message information to the dictionary
            languages = ['English', 'French', 'German']
            user_details['Language'] = languages[language-1]
            user_details['Message'] = message


            # Consider Instagrams rate limits : 250 posts per day
            # limit: 225 posts/day

            # read the file with the post_counter that counts the number of posts that we have done per day.
            # there is also the date of our last post.
            limits_file = open("limits.txt", "r")
            lines = limits_file.read().split(',')
            limits_file.close()
            # the posts counter
            posts_cnt_line = lines[0].split('=')
            posts_cnt = posts_cnt_line[1]
            posts_cnt = int(posts_cnt)
            #the last post/update date
            last_update_line = lines[1].split('=')
            last_update = last_update_line[1]

            # increase the post counter by one
            posts_cnt += 1

            print('Remaining posts for today:', 225-posts_cnt, 'out of' , 225)
            if posts_cnt >225:
                print('Sorry, you reached the daily limit of Instagram (225 posts/day)!')
                print('Please, try again after 24 hours!')
                return 1

            # write the new counter value and the new date to the limits.txt
            limits_file = open("limits.txt", "w")
            limits_file.write("posts_cnt=%s," % posts_cnt)
            limits_file.write("\n")
            limits_file.write("last_update=%s" % last_update)
            limits_file.close()

            # post the comment to the most recent picture
            result = self.post_comment(message)

        else:
            user_details['Language'] = None
            user_details['Message'] = None

        # Write the basic info of the user to a csv
        with open('results/users.csv', 'a', encoding='utf-8') as file1:
            w = csv.DictWriter(file1, user_details.keys(), lineterminator = '\n')
            #if cnt_follower == 1:
            w.writeheader()
            w.writerow(user_details)