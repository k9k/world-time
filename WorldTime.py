__author__ = 'kamil'

import requests
import datetime


def get_key():
    """gets key from key.ini"""
    import configparser
    config = configparser.ConfigParser()
    config.read("key.ini")
    api_key = config["KEY"]["api_key"]
    return api_key


def get_coordinates(name):
    """modified function from PostalCode.py"""
    url_city = "https://maps.googleapis.com/maps/api/geocode/json?address=" + str(name) + "&key=" + get_key()
    r = requests.get(url_city)
    lng = r.json()["results"][0]["geometry"]["location"]["lng"]
    lat = r.json()["results"][0]["geometry"]["location"]["lat"]
    return lat, lng


def get_data(lat, lng):
    """gets data from API"""
    timestamp = str(datetime.datetime.timestamp(datetime.datetime.now()))   #seconds from January 1, 1970
    url = "https://maps.googleapis.com/maps/api/timezone/json?location=" + str(lat) + "," + str(lng) \
          + "&timestamp=" + timestamp + "&key=" + get_key()
    r = requests.get(url)
    time_zone = r.json()['timeZoneId']
    offset = r.json()['rawOffset'] - 3600   #minus 3600 because my time is in UTC + 1 (Poland)
    return time_zone, offset


def get_time(act_hour, act_min, offset):
    """gets time of location, adds offset to actual time"""
    act_min += offset % 3600
    act_hour += int(offset/3600)
    while act_min > 60:
        act_min -= 60
    while act_hour > 24:
        act_hour -= 24
    return act_hour, act_min


def main():
    dec = "y"
    while dec is "y":
        location = input("What time is it in: ")
        lat, lng = get_coordinates(location)
        time_zone, offset = get_data(lat, lng)
        hour, minutes = datetime.datetime.now().hour, datetime.datetime.now().minute
        hour_loc, minutes_loc = get_time(hour, minutes, offset)

        print("Your actual time is:\n\t\t", hour, ":", minutes)
        print("In timezone: ", time_zone, "is:\n\t\t", hour_loc, ":", minutes_loc)

        dec = input("Check other location? y/n ")

main()