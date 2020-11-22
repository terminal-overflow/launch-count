from datetime import datetime, timedelta
import time
from tkinter import *
import os

#change directory into launch-count/
os.chdir(f'{os.path.dirname(os.path.realpath(__file__))}/')

#file format: t-, launch year, launch month, launch day, launch hour, launch minute, launch second
comma = 0
file = open('info/info.txt', 'r')
if os.stat('info/info.txt').st_size > 0:
    for line in file:
        for letter in line:
            if letter == ',':
                comma += 1
        if comma < 6:
            print('Invalid entry')
            exit()
        comma = 0
    file.close()
    file = open('info/info.txt', 'r')
    dates = file.readlines()
    file.close()
    num = 0

    #mark positions in list to remove
    r = []
    for i in range(len(dates)):
        if dates[i].startswith('#'):
            r.append(i)
    #corrects remove position shift
    for i in range(len(r)):
        r[i] = r[i] - i

    if len(r) != len(dates):
        #remove
        for i in range(len(r)):
            dates.remove(dates[r[i]])

        for i in range(len(dates)):
            dates[i] = dates[i].strip()
            t_string, l_year, l_month, l_day, l_hour, l_minute, l_second = dates[num].split(',')
            #convert str to int
            l_year = int(l_year)
            l_month = int(l_month)
            l_day = int(l_day)
            l_hour = int(l_hour)
            l_minute = int(l_minute)
            l_second = int(l_second)

            #get days till
            days_till = (datetime(l_year, l_month, l_day, l_hour, l_minute, l_second) - datetime.now()).days
            if days_till < 0:
                if num +1 == len(dates):
                    extra_days = True
                    break
                else:
                    num += 1
    else:
        print('Invalid entry')
        exit()
else:
    print('Invalid entry')
    exit()

root = Tk()
root.title('World Times')
root.configure(background= 'black')

#changing font size relative to screen size
f_size = 80

#variables
seconds = 0
minutes = 0
hours = 0
days_after = 0
timer = '0:00:00'
extra_days = False
#flags
changed = False
#integration
t_label = None

days_till = str(days_till)
#start
def main_loop():
    global days_till
    global extra_days
    global days_after
    global changed
    global l_year, l_month, l_day, l_hour, l_minute, l_second
    global dates
    global t_string
    global num

    root.after(100, timer_loop)

    #get days
    days_till = int(days_till)
    t_string, l_year, l_month, l_day, l_hour, l_minute, l_second = dates[num].split(',')
    l_year = int(l_year)
    l_month = int(l_month)
    l_day = int(l_day)
    l_hour = int(l_hour)
    l_minute = int(l_minute)
    l_second = int(l_second)
    days_till = (datetime(l_year, l_month, l_day, l_hour, l_minute, l_second) - datetime.now()).days
    if days_till < 0:
        if num +1 == len(dates):
            extra_days = True
        else:
            num += 1
    #duplication for no overlapping
    t_string, l_year, l_month, l_day, l_hour, l_minute, l_second = dates[num].split(',')
    l_year = int(l_year)
    l_month = int(l_month)
    l_day = int(l_day)
    l_hour = int(l_hour)
    l_minute = int(l_minute)
    l_second = int(l_second)
    days_till = (datetime(l_year, l_month, l_day, l_hour, l_minute, l_second) - datetime.now()).days

    #optimise t_string
    t_string = t_string.title()
    t_string = t_string.replace('-', '')
    t_string = t_string.replace('+', '')

    #T± section
    if days_till >= 0:
        start = datetime.now().strftime('%H:%M:%S')
        end = datetime(l_year, l_month, l_day, l_hour, l_minute, l_second).strftime('%H:%M:%S')
        total_time = (datetime.strptime(end,'%H:%M:%S') - datetime.strptime(start,'%H:%M:%S'))
        total_time = str(total_time)

        if total_time.startswith('-'):
            total_time = total_time.replace(total_time[:8], '', 1)

    #labels
    if extra_days == True:
        t_string = f'{t_string}+'
    else:
        t_string = f'{t_string}-'

    ts_label = Label(root, text= t_string, width= 3, height= 2, padx= 10, foreground= 'white', background= 'black')
    ts_label.config(font= ('Arial', f_size + 5))

    t_label = Label(root, width= 8, height= 2, foreground= 'blue', background= 'black')
    t_label.config(font= ('Arial', f_size + 5))
    if extra_days == True or days_till < 0:
        t_label.config(text= timer, foreground= 'green')
    else:
        t_label.config(text= total_time)

    if t_label['text'] == '0:00:00' and days_till >= 0:
        days_till += 1

    days_after = int(days_after)
    if days_till == 1 or days_after == 1:
        days = ' Day'
    else:
        days = ' Days'

    days_till = str(days_till)
    day_label = Label(root, text= days_till + days, width= 8, height= 2, padx= 10, foreground= 'blue', background= 'black')
    day_label.config(font= ('Arial', f_size + 5))

    if extra_days == True:
        days_after = str(days_after)
        day_label.config(text= days_after + days)

    #config labels - colour schemes
    if days_till == '0':
        day_label.config(foreground= 'red')
        t_label.config(foreground= 'red')
    elif extra_days == True:
        day_label.config(foreground= 'green')

    #countdown flash
    end_time = False
    days_till = int(days_till)
    if days_till == 0:
        if total_time == '0:00:09':
            end_time = True
        elif total_time == '0:00:07':
            end_time = True
        elif total_time == '0:00:05':
            end_time = True
        elif total_time == '0:00:03':
            end_time = True
        elif total_time == '0:00:01':
            end_time = True

    if end_time == True:
        t_label.config(foreground= 'dark red')

    #T± labels
    ts_label.grid(row= 0, column= 0)
    day_label.grid(row= 0, column= 1)
    t_label.grid(row= 0, column= 2)

    #no slow down/overlapping
    root.after(100, main_loop)
    root.after(100, timer_loop)

    root.after(100, ts_label.destroy)
    root.after(100, t_label.destroy)
    root.after(100, day_label.destroy)

def timer_loop():
    global days_after
    global hours
    global minutes
    global seconds
    global extra_days
    global timer
    global days_till

    if extra_days == True:
        year_now = datetime.now().strftime('%Y')
        month_now = datetime.now().strftime('%m')
        day_now = datetime.now().strftime('%d')
        hour_now = datetime.now().strftime('%H')
        minute_now = datetime.now().strftime('%M')
        second_now = datetime.now().strftime('%S')

        year_now = int(year_now)
        month_now = int(month_now)
        day_now = int(day_now)
        hour_now = int(hour_now)
        minute_now = int(minute_now)
        second_now = int(second_now)

        launch_time = datetime(year= l_year, month= l_month, day= l_day, hour= l_hour, minute= l_minute, second= l_second)
        file_time = datetime(year= year_now, month= month_now, day= day_now, hour= hour_now, minute= minute_now, second= second_now)

        diff = file_time - launch_time
        diff = str(diff)
        if len(diff) > 8:
            days_after, whole_time = diff.split(', ')
            days_after, extra = days_after.split(' ')
            hours, minutes, seconds = whole_time.split(':')
        else:
            hours, minutes, seconds = diff.split(':')
            days_after = '0'

        seconds = int(seconds)
        if seconds < 10:
            seconds = str(seconds)
            seconds = f'0{seconds}'

        days_after = str(days_after)
        hours = str(hours)
        minutes = str(minutes)
        seconds = str(seconds)

        timer = f'{hours}:{minutes}:{seconds}'

timer_loop()
main_loop()
root.mainloop()
