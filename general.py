import datetime
from dateutil.relativedelta import relativedelta

def update_limits():

    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # read the last update date
    limits_file = open("limits.txt", "r")
    lines = limits_file.read().split(',')
    limits_file.close()

    last_update_line = lines[1].split('=')
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
        limits_file.write("last_update=%s" % now)
        limits_file.close()
    else:
        print('So, it should not be updated')



    limits_file.close()
