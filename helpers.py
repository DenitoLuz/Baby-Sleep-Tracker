import os
import requests
import urllib.parse

from flask import redirect, render_template, request, session
from functools import wraps
import re
from datetime import datetime, timedelta
from datetime import date

import time
import copy

def dub_dig (num):
    if int (num) < 10:
        num = "0"+str(num)
    return str(num)


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def avg_nap(baby_rec):
    dates =[]
    for item in baby_rec:
        dates.append(item['date']) if item['date'] not in dates else dates


    all_naps =[]
    for item in dates:
        total_hours = 0
        total_mins = 0

        for element in baby_rec:
             if element['date'] == item:
                 found = re.search('^\d+', element['time'])

                 if found!= None:

                    hrs = re.search('^\d+(?=\:)', element['time']).group()
                    mins = re.search('(?<=\d\:)\d+(?=\:)', element['time']).group()
                    total_hours += int(hrs)
                    total_mins += int (mins)

        total_mins += total_hours*60
        all_naps.append(total_mins)

    total_nap_min = 0

    for nap in all_naps:
        total_nap_min += nap
        #total_nap_sec += int(re.search('(?<=\:\d:)\d+|(?<=\:\d\d:)\d+', nap).group())


    nap_min_avg = total_nap_min / len(all_naps)

    print ("allNaps = "+ str(all_naps))

    if nap_min_avg > 60:
        nap_hr_avg = nap_min_avg / 60
        nap_min_avg = round((nap_hr_avg-int(nap_hr_avg))*60)
    else:
        nap_hr_avg = 0
    nap_hr_avg = round(nap_hr_avg)
    print ("nap_hr_avg = "+ str(nap_hr_avg))
    print ("nap_min_avg = "+ str(nap_min_avg))
    if nap_hr_avg < 10:
        nap_hr_avg = "0"+str(round(nap_hr_avg))
    if nap_min_avg < 10:
        nap_min_avg = "0"+str(round(nap_min_avg))


    result = str(nap_hr_avg)+":"+str(nap_min_avg)+":00"
    print(result)
    return result

def update_baby_rec(baby_rec):
    for item in baby_rec:


        sleep = item['sleep']
        sleep_dt_obj = datetime.strptime(sleep, '%H:%M')
        wake = item['wake']
        wake_dt_obj = datetime.strptime(wake, '%H:%M')
        item ['time'] = str(wake_dt_obj - sleep_dt_obj)
        item ['time'] = re.sub('^-', '+', item ['time'])
    return baby_rec



def avg_session (baby_rec):
    total_min_day = 0
    total_hrs_day = 0
    avg_session_time = ""

    for item in baby_rec:

        #ONLY match those that are not saved as -1 day bla bla
        hour_day = re.search ('^\d+(?=\:)', item['time'] )
        min_day = re.search ('(?<=\d\:)\d+(?=\:)', item['time'] )

        # add to total
        if hour_day != None:
            total_hrs_day += int(hour_day.group())
            total_min_day += int(min_day.group())

    if min_day == 0 and hrs_day == 0:
        return "Not enough Data"

    total_min_day += (total_hrs_day*60)

    avg_minutes = total_min_day/len(baby_rec)
    avg_minutes = round(avg_minutes)
    avg_hours = 0

    if (avg_minutes > 59):
        avg_hours = avg_minutes/60
        avg_minutes = round((avg_hours-int(avg_hours))*60)
        avg_hours = int(avg_hours)

    if (avg_minutes < 10):
        avg_minutes = "0"+str(avg_minutes)

    if (avg_hours < 10):
        avg_hours = "0"+str(avg_hours)


        avg_session_time = str(avg_hours)+":"+str(avg_minutes) + ":00"
        print(avg_session_time)
    return avg_session_time

def three_top(baby_rec):
    baby_rec_cp = copy.deepcopy(baby_rec)

    fir_dt = datetime.strptime('17:00', '%H:%M')
    fir_sec = datetime.strptime('17:09', '%H:%M')
    diff = fir_dt-fir_sec
    # fir_thi = datetime.strptime(thi,'%H:%M')
    for cur in baby_rec:
        current = datetime.strptime(cur['sleep'],'%H:%M')
        counter = 0
        counter_frame = 0
        #print (current)
        for comp in baby_rec_cp:
            compare = datetime.strptime(comp['sleep'],'%H:%M')
            if compare == current:
                counter+=1
            time_diff = current - compare

            if time_diff > timedelta(days=-1, hours =23, minutes = 49) and time_diff < timedelta(days=0, hours =0, minutes = 11):
                counter_frame += 1
        cur['count'] = counter
        cur['frame'] = counter_frame

    highest = 0
    second = 0
    third = 0
    fir = {}
    sec = {}
    thi = {}
    loops = 0
    while loops < 2:
        for that in baby_rec:
            current = that['count']
            if current > highest:
                highest = current
                fir = that['sleep']
            elif current < highest and current >= second and that['sleep'] != fir:
                second = current
                sec = that['sleep']
            elif current < second and current >= third and that['sleep'] != sec:
                third = current
                thi = that['sleep']
        ranking =[{'time':'0'}]
        ranking[0]['time'] = str(fir)
        ranking[0]['count'] = str(highest)
        ranking.append({'time': str(sec), 'count':str(second)})
        ranking.append({'time':str(thi),'count':str(third)})
        loops += 1

    highest_f = 0
    second_f = 0
    third_f = 0
    fir_f = {}
    sec_f = {}
    thi_f = {}
    loops = 0
    while loops < 2:
        for that in baby_rec:
            current_f = that['frame']
            if current_f > highest_f:
                highest_f = current_f
                fir_f = that['sleep']
            elif current_f < highest_f and current_f >= second_f and that['sleep'] != fir_f:
                second_f = current_f
                sec_f = that['sleep']
            elif current_f < second_f and current_f >= third_f and that['sleep'] != sec_f:
                third_f = current_f
                thi_f = that['sleep']
        ranking_f =[{'time':'0'}]
        ranking_f[0]['time'] = str(fir_f)
        ranking_f[0]['count'] = str(highest_f)
        ranking_f.append({'time': str(sec_f), 'count':str(second_f)})
        ranking_f.append({'time':str(thi_f),'count':str(third_f)})
        loops += 1
    print (ranking_f)
    both = [ranking, ranking_f]
    return both

def get_night (baby_rec, type):
    night_sleeps = []
    for item in baby_rec:
        found  = re.search('^\+', item['time'])
        if found != None:
            night_sleeps.append(re.search('\d+:\d+', item[type]).group())

    sum_min = 0
    sum_hours = 0
    for each in night_sleeps:
        sum_hours += int(re.search('^\d+', each).group())
        sum_min += int(re.search('(?<=\:)\d+', each).group())

    sum_min += sum_hours*60
    avg_min = sum_min / len(night_sleeps)

    avg_hours = avg_min/60


    avg_min = round((avg_hours - int(avg_hours))*60)

    avg_hours = int(avg_hours)

    night_sleep = dub_dig(avg_hours)+":"+dub_dig(avg_min)+":00"
    return night_sleep



