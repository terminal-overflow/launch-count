from datetime import datetime, timedelta
import time
import pytz
from tkinter import *
import os

#change directory into launch-count/
os.chdir(f'{os.path.dirname(os.path.abspath(__file__))}/')

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
    #corrects position shift
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
        days_till = 'hidden'
else:
    file.close()
    days_till = 'hidden'

#open highlight locations
file = open('info/highlight.txt', 'r')
launch_loc = file.read()
if ',' in launch_loc:
    launch_loc = launch_loc.split(',')
else:
    launch_loc = launch_loc.split('\n')
file.close()

#mark positions in list to remove
r = []
for i in range(len(launch_loc)):
    if launch_loc[i].startswith('#'):
        r.append(i)
#corrects position shift
for i in range(len(r)):
    r[i] = r[i] - i

if len(r) != len(launch_loc):
    #remove
    for i in range(len(r)):
        launch_loc.remove(launch_loc[r[i]])
for i in range(len(launch_loc)):
    launch_loc[i] = launch_loc[i].lower()
    launch_loc[i] = launch_loc[i].strip()

#configure window
root = Tk()
root.title('World Times')
root.configure(background= 'black')
width_value = root.winfo_screenwidth()
height_value = root.winfo_screenheight()
root.geometry('%dx%d' % (width_value, height_value))
#changing font size relative to screen size
if width_value < 2560 and height_value < 1440:
    f_size = 20
else:
    f_size = 35

#full screen
s_full = False
def close(event):
    exit()
def f_screen(event):
    global s_full
    if s_full == True:
        s_full = False
        root.wm_attributes('-fullscreen', 'false')
    else:
        s_full = True
        root.wm_attributes('-fullscreen', 'true')
def f_close(event):
    global s_full
    s_full = False
    root.wm_attributes('-fullscreen', 'false')

#key binds
root.bind('q', close)
root.bind('f', f_screen)
root.bind('<Escape>', f_close)

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
#set timezone funtions
UTC_1 = pytz.timezone('Atlantic/Cape_Verde')
UTC_2 = pytz.timezone('Atlantic/South_Georgia')
UTC_3 = pytz.timezone('America/Godthab')
UTC_4 = pytz.timezone('Atlantic/Bermuda')
UTC_5 = pytz.timezone('America/New_York')
UTC_6 = pytz.timezone('America/Chicago')
UTC_7 = pytz.timezone('America/Denver')
UTC_8 = pytz.timezone('America/Los_Angeles')
UTC_9 = pytz.timezone('America/Juneau')
UTC_10 = pytz.timezone('Pacific/Honolulu')

UTC0_2 = pytz.timezone('Atlantic/Reykjavik')
UTC0 = pytz.timezone('Europe/London')
UTC1 = pytz.timezone('Europe/Paris')
UTC3 = pytz.timezone('Europe/Moscow')
UTC55 = pytz.timezone('Asia/Kolkata')
UTC6 = pytz.timezone('Asia/Almaty')
UTC8 = pytz.timezone('Asia/Shanghai')
UTC9 = pytz.timezone('Asia/Tokyo')
UTC11 = pytz.timezone('Australia/Sydney')
UTC12 = pytz.timezone('Pacific/Auckland')

#<= -1
datetime_utc_1 = datetime.now(UTC_1) #-1
datetime_utc_2 = datetime.now(UTC_2) #-2
datetime_utc_3 = datetime.now(UTC_3) #-3
datetime_utc_4 = datetime.now(UTC_4) #-4
datetime_utc_5 = datetime.now(UTC_5) #-5
datetime_utc_6 = datetime.now(UTC_6) #-6
datetime_utc_7 = datetime.now(UTC_7) #-7
datetime_utc_8 = datetime.now(UTC_8) #-8
datetime_utc_9 = datetime.now(UTC_9) #-9
datetime_utc_10 = datetime.now(UTC_10) #-10

#>= 0
datetime_utc0_2 = datetime.now(UTC0_2) #+0
datetime_utc0 = datetime.now(UTC0) #+0
datetime_utc1 = datetime.now(UTC1) #+1
datetime_utc3 = datetime.now(UTC3) #+3
datetime_utc55 = datetime.now(UTC55) #+5.5
datetime_utc6 = datetime.now(UTC6) #+6
datetime_utc8 = datetime.now(UTC8) #+8
datetime_utc9 = datetime.now(UTC9) #+9
datetime_utc11 = datetime.now(UTC11) #+11
datetime_utc12 = datetime.now(UTC12) #+12

#static text
title = Label(root, text= 'World Times', width= 15, height= 2, padx= 10, foreground= 'white', background= 'black')
title.config(font= ('Arial', f_size + 10))

#<= -1
cape_verde_txt = Label(root, text= 'Cape Verde:', width= 15, height= 2, padx= 5, foreground= 'white', background= 'black')
cape_verde_txt.config(font= ('Arial', f_size))

south_georgia_txt = Label(root, text= 'South Georgia:', width= 15, height= 2, padx= 5, foreground= 'white', background= 'black')
south_georgia_txt.config(font= ('Arial', f_size))

greenland_txt = Label(root, text= 'Greenland:', width= 15, height= 2, padx= 5, foreground= 'white', background= 'black')
greenland_txt.config(font= ('Arial', f_size))

french_guiana_txt = Label(root, text= 'French Guiana:', width= 15, height= 2, padx= 5, foreground= 'white', background= 'black')
french_guiana_txt.config(font= ('Arial', f_size))

new_york_txt = Label(root, text= 'New York:', width= 15, height= 2, padx= 5, foreground= 'white', background= 'black')
new_york_txt.config(font= ('Arial', f_size))

chicago_txt = Label(root, text= 'Chicago:', width= 15, height= 2, padx= 5, foreground= 'white', background= 'black')
chicago_txt.config(font= ('Arial', f_size))

denver_txt = Label(root, text= 'Denver:', width= 15, height= 2, padx= 5, foreground= 'white', background= 'black')
denver_txt.config(font= ('Arial', f_size))

los_angeles_txt = Label(root, text= 'Los Angeles:', width= 15, height= 2, padx= 5, foreground= 'white', background= 'black')
los_angeles_txt.config(font= ('Arial', f_size))

alaska_txt = Label(root, text= 'Alaska:', width= 15, height= 2, padx= 5, foreground= 'white', background= 'black')
alaska_txt.config(font= ('Arial', f_size))

hawaii_txt = Label(root, text= 'Hawaii:', width= 15, height= 2, padx= 5, foreground= 'white', background= 'black')
hawaii_txt.config(font= ('Arial', f_size))

#>= 0
iceland_txt = Label(root, text= 'Iceland:', width=15, height= 2, padx= 5, foreground= 'white', background= 'black')
iceland_txt.config(font= ('Arial', f_size))

england_txt = Label(root, text= 'England:', width=15, height= 2, padx= 5, foreground= 'white', background= 'black')
england_txt.config(font= ('Arial', f_size))

france_txt = Label(root, text= 'France:', width=15, height= 2, padx= 5, foreground= 'white', background= 'black')
france_txt.config(font= ('Arial', f_size))

moscow_txt = Label(root, text= 'Moscow:', width=15, height= 2, padx= 5, foreground= 'white', background= 'black')
moscow_txt.config(font= ('Arial', f_size))

india_txt = Label(root, text= 'India:', width=15, height= 2, padx= 5, foreground= 'white', background= 'black')
india_txt.config(font= ('Arial', f_size))

kazakhstan_txt = Label(root, text= 'Kazakhstan:', width=15, height= 2, padx= 5, foreground= 'white', background= 'black')
kazakhstan_txt.config(font= ('Arial', f_size))

china_txt = Label(root, text= 'China:', width=15, height= 2, padx= 5, foreground= 'white', background= 'black')
china_txt.config(font= ('Arial', f_size))

japan_txt = Label(root, text= 'Japan:', width=15, height= 2, padx= 5, foreground= 'white', background= 'black')
japan_txt.config(font= ('Arial', f_size))

australia_txt = Label(root, text= 'Australia:', width=15, height= 2, padx= 5, foreground= 'white', background= 'black')
australia_txt.config(font= ('Arial', f_size))

new_zealand_txt = Label(root, text= 'New Zealand:', width=15, height= 2, padx= 5, foreground= 'white', background= 'black')
new_zealand_txt.config(font= ('Arial', f_size))

#live time
#<= -1
cape_verde_label = Label(root, text= datetime_utc_1.strftime('%d:%m:%Y %H:%M:%S %Z %z'), width= 28, height= 2, foreground= 'green', background= 'black')
cape_verde_label.config(font= ('Arial', f_size))

south_georgia_label = Label(root, text= datetime_utc_2.strftime('%d:%m:%Y %H:%M:%S %Z %z'), width= 28, height= 2, foreground= 'green', background= 'black')
south_georgia_label.config(font= ('Arial', f_size))

greenland_label = Label(root, text= datetime_utc_3.strftime('%d:%m:%Y %H:%M:%S %Z %z'), width= 28, height= 2, foreground= 'green', background= 'black')
greenland_label.config(font= ('Arial', f_size))

french_guiana_label = Label(root, text= datetime_utc_4.strftime('%d:%m:%Y %H:%M:%S %Z %z'), width= 28, height= 2, foreground= 'green', background= 'black')
french_guiana_label.config(font= ('Arial', f_size))

new_york_label = Label(root, text= datetime_utc_5.strftime('%d:%m:%Y %H:%M:%S %Z %z'), width= 28, height= 2, foreground= 'green', background= 'black')
new_york_label.config(font= ('Arial', f_size))

chicago_label = Label(root, text= datetime_utc_6.strftime('%d:%m:%Y %H:%M:%S %Z %z'), width= 28, height= 2, foreground= 'green', background= 'black')
chicago_label.config(font= ('Arial', f_size))

denver_label = Label(root, text= datetime_utc_7.strftime('%d:%m:%Y %H:%M:%S %Z %z'), width= 28, height= 2, foreground= 'green', background= 'black')
denver_label.config(font= ('Arial', f_size))

los_angeles_label = Label(root, text= datetime_utc_8.strftime('%d:%m:%Y %H:%M:%S %Z %z'), width= 28, height= 2, foreground= 'green', background= 'black')
los_angeles_label.config(font= ('Arial', f_size))

alaska_label = Label(root, text= datetime_utc_9.strftime('%d:%m:%Y %H:%M:%S %Z %z'), width= 28, height= 2, foreground= 'green', background= 'black')
alaska_label.config(font= ('Arial', f_size))

hawaii_label = Label(root, text= datetime_utc_10.strftime('%d:%m:%Y %H:%M:%S %Z %z'), width= 28, height= 2, foreground= 'green', background= 'black')
hawaii_label.config(font= ('Arial', f_size))

#>= 0
iceland_label = Label(root, text= datetime_utc0_2.strftime('%d:%m:%Y %H:%M:%S %Z %z'), width= 28, height= 2, padx= 5, foreground= 'green', background= 'black')
iceland_label.config(font= ('Arial', f_size))

england_label = Label(root, text= datetime_utc0.strftime('%d:%m:%Y %H:%M:%S %Z %z'), width= 28, height= 2, padx= 5, foreground= 'green', background= 'black')
england_label.config(font= ('Arial', f_size))

france_label = Label(root, text= datetime_utc1.strftime('%d:%m:%Y %H:%M:%S %Z %z'), width= 28, height= 2, padx= 5, foreground= 'green', background= 'black')
france_label.config(font= ('Arial', f_size))

moscow_label = Label(root, text= datetime_utc3.strftime('%d:%m:%Y %H:%M:%S %Z %z'), width= 28, height= 2, padx= 5, foreground= 'green', background= 'black')
moscow_label.config(font= ('Arial', f_size))

india_label = Label(root, text= datetime_utc55.strftime('%d:%m:%Y %H:%M:%S %Z %z'), width= 28, height= 2, padx= 5, foreground= 'green', background= 'black')
india_label.config(font= ('Arial', f_size))

kazakhstan_label = Label(root, text= datetime_utc6.strftime('%d:%m:%Y %H:%M:%S %Z %z'), width= 28, height= 2, padx= 5, foreground= 'green', background= 'black')
kazakhstan_label.config(font= ('Arial', f_size))

china_label = Label(root, text= datetime_utc8.strftime('%d:%m:%Y %H:%M:%S %Z %z'), width= 28, height= 2, padx= 5, foreground= 'green', background= 'black')
china_label.config(font= ('Arial', f_size))

japan_label = Label(root, text= datetime_utc9.strftime('%d:%m:%Y %H:%M:%S %Z %z'), width= 28, height= 2, padx= 5, foreground= 'green', background= 'black')
japan_label.config(font= ('Arial', f_size))

australia_label = Label(root, text= datetime_utc11.strftime('%d:%m:%Y %H:%M:%S %Z %z'), width= 28, height= 2, padx= 5, foreground= 'green', background= 'black')
australia_label.config(font= ('Arial', f_size))

new_zealand_label = Label(root, text= datetime_utc12.strftime('%d:%m:%Y %H:%M:%S %Z %z'), width= 28, height= 2, padx= 5, foreground= 'green', background= 'black')
new_zealand_label.config(font= ('Arial', f_size))

#tkinter grid
title.grid(row= 0, column= 2, columnspan= 3)

#<= -1
cape_verde_txt.grid(row= 2, column= 0)
cape_verde_label.grid(row= 2, column= 1)

south_georgia_txt.grid(row= 3, column= 0)
south_georgia_label.grid(row= 3, column= 1)

greenland_txt.grid(row= 4, column= 0)
greenland_label.grid(row= 4, column= 1)

french_guiana_txt.grid(row= 5, column= 0)
french_guiana_label.grid(row= 5, column= 1)

new_york_txt.grid(row= 6, column= 0)
new_york_label.grid(row= 6, column= 1)

chicago_txt.grid(row= 7, column= 0)
chicago_label.grid(row= 7, column= 1)

denver_txt.grid(row= 8, column= 0)
denver_label.grid(row= 8, column= 1)

los_angeles_txt.grid(row= 9, column= 0)
los_angeles_label.grid(row= 9, column= 1)

alaska_txt.grid(row= 10, column= 0)
alaska_label.grid(row= 10, column= 1)

hawaii_txt.grid(row= 11, column= 0)
hawaii_label.grid(row= 11, column= 1)

#>= 0
iceland_txt.grid(row= 2, column= 5)
iceland_label.grid(row= 2, column= 6)

england_txt.grid(row= 3, column= 5)
england_label.grid(row= 3, column= 6)

france_txt.grid(row= 4, column= 5)
france_label.grid(row= 4, column= 6)

moscow_txt.grid(row= 5, column= 5)
moscow_label.grid(row= 5, column= 6)

india_txt.grid(row= 6, column= 5)
india_label.grid(row= 6, column= 6)

kazakhstan_txt.grid(row= 7, column= 5)
kazakhstan_label.grid(row= 7, column= 6)

china_txt.grid(row= 8, column= 5)
china_label.grid(row= 8, column= 6)

japan_txt.grid(row= 9, column= 5)
japan_label.grid(row= 9, column= 6)

australia_txt.grid(row= 10, column= 5)
australia_label.grid(row= 10, column= 6)

new_zealand_txt.grid(row= 11, column= 5)
new_zealand_label.grid(row= 11, column= 6)

def main_loop():
    global days_till
    global extra_days
    global days_after
    global changed
    global l_year, l_month, l_day, l_hour, l_minute, l_second
    global dates
    global t_string
    global num

    #dynamic font and window size change
    width_value = root.winfo_width()
    height_value = root.winfo_height()

    if width_value != 1 and height_value != 1:
        root.geometry('%dx%d' % (width_value, height_value))
    else:
        width_value = root.winfo_screenwidth()
        height_value = root.winfo_screenheight()
        root.geometry('%dx%d' % (width_value, height_value))

    #changing font size relative to screen size
    if width_value < 2560:
        f_size = 20
    else:
        f_size = 35

    root.after(100, timer_loop)

    #set timezone funtions
    #<= -1
    datetime_utc_1 = datetime.now(UTC_1) #-1
    datetime_utc_2 = datetime.now(UTC_2) #-2
    datetime_utc_3 = datetime.now(UTC_3) #-3
    datetime_utc_4 = datetime.now(UTC_4) #-4
    datetime_utc_5 = datetime.now(UTC_5) #-5
    datetime_utc_6 = datetime.now(UTC_6) #-6
    datetime_utc_7 = datetime.now(UTC_7) #-7
    datetime_utc_8 = datetime.now(UTC_8) #-8
    datetime_utc_9 = datetime.now(UTC_9) #-9
    datetime_utc_10 = datetime.now(UTC_10) #-10

    #>= 0
    datetime_utc0_2 = datetime.now(UTC0_2) #+0
    datetime_utc0 = datetime.now(UTC0) #+0
    datetime_utc1 = datetime.now(UTC1) #+1
    datetime_utc3 = datetime.now(UTC3) #+3
    datetime_utc55 = datetime.now(UTC55) #+5.5
    datetime_utc6 = datetime.now(UTC6) #+6
    datetime_utc8 = datetime.now(UTC8) #+8
    datetime_utc9 = datetime.now(UTC9) #+9
    datetime_utc11 = datetime.now(UTC11) #+11
    datetime_utc12 = datetime.now(UTC12) #+12

    #live time
    #<= -1
    title.config(font= ('Arial', f_size + 10))
    cape_verde_txt.config(font= ('Arial', f_size))
    cape_verde_label.config(text= datetime_utc_1.strftime('%d:%m:%Y %H:%M:%S %Z %z'), font= ('Arial', f_size))
    south_georgia_txt.config(font= ('Arial', f_size))
    south_georgia_label.config(text= datetime_utc_2.strftime('%d:%m:%Y %H:%M:%S %Z %z'), font= ('Arial', f_size))
    greenland_txt.config(font= ('Arial', f_size))
    greenland_label.config(text= datetime_utc_3.strftime('%d:%m:%Y %H:%M:%S %Z %z'), font= ('Arial', f_size))
    french_guiana_txt.config(font= ('Arial', f_size))
    french_guiana_label.config(text= datetime_utc_4.strftime('%d:%m:%Y %H:%M:%S %Z %z'), font= ('Arial', f_size))
    new_york_txt.config(font= ('Arial', f_size))
    new_york_label.config(text= datetime_utc_5.strftime('%d:%m:%Y %H:%M:%S %Z %z'), font= ('Arial', f_size))
    chicago_txt.config(font= ('Arial', f_size))
    chicago_label.config(text= datetime_utc_6.strftime('%d:%m:%Y %H:%M:%S %Z %z'), font= ('Arial', f_size))
    denver_txt.config(font= ('Arial', f_size))
    denver_label.config(text= datetime_utc_7.strftime('%d:%m:%Y %H:%M:%S %Z %z'), font= ('Arial', f_size))
    los_angeles_txt.config(font= ('Arial', f_size))
    los_angeles_label.config(text= datetime_utc_8.strftime('%d:%m:%Y %H:%M:%S %Z %z'), font= ('Arial', f_size))
    alaska_txt.config(font= ('Arial', f_size))
    alaska_label.config(text= datetime_utc_9.strftime('%d:%m:%Y %H:%M:%S %Z %z'), font= ('Arial', f_size))
    hawaii_txt.config(font= ('Arial', f_size))
    hawaii_label.config(text= datetime_utc_10.strftime('%d:%m:%Y %H:%M:%S %Z %z'), font= ('Arial', f_size))

    #>= 0
    iceland_txt.config(font= ('Arial', f_size))
    iceland_label.config(text= datetime_utc0_2.strftime('%d:%m:%Y %H:%M:%S %Z %z'), font= ('Arial', f_size))
    england_txt.config(font= ('Arial', f_size))
    england_label.config(text= datetime_utc0.strftime('%d:%m:%Y %H:%M:%S %Z %z'), font= ('Arial', f_size))
    france_txt.config(font= ('Arial', f_size))
    france_label.config(text= datetime_utc1.strftime('%d:%m:%Y %H:%M:%S %Z %z'), font= ('Arial', f_size))
    moscow_txt.config(font= ('Arial', f_size))
    moscow_label.config(text= datetime_utc3.strftime('%d:%m:%Y %H:%M:%S %Z %z'), font= ('Arial', f_size))
    india_txt.config(font= ('Arial', f_size))
    india_label.config(text= datetime_utc55.strftime('%d:%m:%Y %H:%M:%S %Z %z'), font= ('Arial', f_size))
    kazakhstan_txt.config(font= ('Arial', f_size))
    kazakhstan_label.config(text= datetime_utc6.strftime('%d:%m:%Y %H:%M:%S %Z %z'), font= ('Arial', f_size))
    china_txt.config(font= ('Arial', f_size))
    china_label.config(text= datetime_utc8.strftime('%d:%m:%Y %H:%M:%S %Z %z'), font= ('Arial', f_size))
    japan_txt.config(font= ('Arial', f_size))
    japan_label.config(text= datetime_utc9.strftime('%d:%m:%Y %H:%M:%S %Z %z'), font= ('Arial', f_size))
    australia_txt.config(font= ('Arial', f_size))
    australia_label.config(text= datetime_utc11.strftime('%d:%m:%Y %H:%M:%S %Z %z'), font= ('Arial', f_size))
    new_zealand_txt.config(font= ('Arial', f_size))
    new_zealand_label.config(text= datetime_utc12.strftime('%d:%m:%Y %H:%M:%S %Z %z'), font= ('Arial', f_size))

    #launch location highlight
    if launch_loc != '':
        if 'cape verde' in launch_loc:
            cape_verde_txt.config(foreground= 'yellow')
            cape_verde_label.config(foreground= 'yellow')
        if 'south georgia' in launch_loc or 'georgia' in launch_loc:
            south_georgia_txt.config(foreground= 'yellow')
            south_georgia_label.config(foreground= 'yellow')
        if 'greenland' in launch_loc:
            greenland_txt.config(foreground= 'yellow')
            greenland_label.config(foreground= 'yellow')
        if 'french guiana' in launch_loc or 'guiana' in launch_loc:
            french_guiana_txt.config(foreground= 'yellow')
            french_guiana_label.config(foreground= 'yellow')
        if 'new york' in launch_loc or 'eastern' in launch_loc:
            new_york_txt.config(foreground= 'yellow')
            new_york_label.config(foreground= 'yellow')
        if 'chicago' in launch_loc or 'central' in launch_loc:
            chicago_txt.config(foreground= 'yellow')
            chicago_label.config(foreground= 'yellow')
        if 'denver' in launch_loc or 'mountain' in launch_loc:
            denver_txt.config(foreground= 'yellow')
            denver_label.config(foreground= 'yellow')
        if 'los angeles' in launch_loc or 'pacific' in launch_loc:
            los_angeles_txt.config(foreground= 'yellow')
            los_angeles_label.config(foreground= 'yellow')
        if 'alaska' in launch_loc:
            alaska_txt.config(foreground= 'yellow')
            alaska_label.config(foreground= 'yellow')
        if 'hawaii' in launch_loc:
            hawaii_txt.config(foreground= 'yellow')
            hawaii_label.config(foreground= 'yellow')
        if 'iceland' in launch_loc:
            iceland_txt.config(foreground= 'yellow')
            iceland_label.config(foreground= 'yellow')
        if 'england' in launch_loc:
            england_txt.config(foreground= 'yellow')
            england_label.config(foreground= 'yellow')
        if 'france' in launch_loc:
            france_txt.config(foreground= 'yellow')
            france_label.config(foreground= 'yellow')
        if 'moscow' in launch_loc:
            moscow_txt.config(foreground= 'yellow')
            moscow_label.config(foreground= 'yellow')
        if 'india' in launch_loc:
            india_txt.config(foreground= 'yellow')
            india_label.config(foreground= 'yellow')
        if 'kazakhstan' in launch_loc:
            kazakhstan_txt.config(foreground= 'yellow')
            kazakhstan_label.config(foreground= 'yellow')
        if 'china' in launch_loc:
            china_txt.config(foreground= 'yellow')
            china_label.config(foreground= 'yellow')
        if 'japan' in launch_loc:
            japan_txt.config(foreground= 'yellow')
            japan_label.config(foreground= 'yellow')
        if 'australia' in launch_loc:
            australia_txt.config(foreground= 'yellow')
            australia_label.config(foreground= 'yellow')
        if 'new zealand' in launch_loc:
            new_zealand_txt.config(foreground= 'yellow')
            new_zealand_label.config(foreground= 'yellow')

    if days_till != 'hidden':
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
        elif days_till == 'hidden':
            t_label.config(text = '0:00:00')
        else:
            t_label.config(text= total_time)

        days_after = int(days_after)
        #make sure days are correct
        if t_label['text'] == '0:00:00' and days_till >= 0:
            days_till += 1

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

        if days_till == 'hidden':
            ts_label.config(foreground= 'black')
            t_label.config(foreground= 'black')
            day_label.config(foreground= 'black')

        #config labels - colour schemes
        if days_till == '0':
            day_label.config(foreground= 'red')
            t_label.config(foreground= 'red')
        elif extra_days == True:
            day_label.config(foreground= 'green')

        #countdown flash
        end_time = False
        days_till = int(days_till)
        if days_till != 'hidden' and days_till == 0:
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

        #display time of launch
        d_hour = l_hour

        if l_minute < 10 and l_minute >= 0:
            d_minute = f'0{l_minute}'
        else:
            d_minute = l_minute

        if l_second < 10 and l_second >= 0:
            d_second = f'0{l_second}'
        else:
            d_second = l_second

        hour_min = f'{d_hour}:{d_minute}:{d_second}'
        time_d = Label(root, text= hour_min, width= 15, height= 2, padx= 10, foreground= 'white', background= 'black')
        time_d.config(font= ('Arial', f_size))

        #T± labels
        if width_value < 2560:
            ts_label.grid(row= 2, column= 2)
            day_label.grid(row= 2, column= 3)
            t_label.grid(row= 2, column= 4)
            time_d.grid(row= 3, column= 2, columnspan= 3)
        else:
            ts_label.grid(row= 1, column= 2)
            day_label.grid(row= 1, column= 3)
            t_label.grid(row= 1, column= 4)
            time_d.grid(row= 2, column= 2, columnspan= 3)

    #no slow down/overlapping
    root.after(100, main_loop)

    if days_till != 'hidden':
        root.after(100, timer_loop)
        root.after(100, ts_label.destroy)
        root.after(100, t_label.destroy)
        root.after(100, day_label.destroy)
        root.after(100, time_d.destroy)

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
