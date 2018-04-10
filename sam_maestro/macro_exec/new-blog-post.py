#!/usr/bin/python3

import sys
import os
import subprocess
import argparse
import glob
import math
import re
import datetime
# from datetime import date

import json
from collections import OrderedDict
import io

from os import listdir
from os.path import isfile, join

home = os.path.expanduser("~/_dev/blendertube.github.io/_posts")

def convert_yt_title(d):
    title = d.replace(' - ', '-')
    title = title.replace(' ', '-')
    title = ''.join(c for c in title if c.isalnum() or c =='-' or c =='_')
    title = title.lower()
    return title

def convert_yt_date(d):
    date = d.replace(',', '')
    month, day, year = date.split(' ')
    yt_months_array = {'Jan':1,'Feb':2,'Mar':3,'Apr':4,'May':5,'Jun':6,'Jul':7,'Aug':8,'Sep':9,'Oct':10,'Nov':11,'Dec':12}
    # print(day)
    date = datetime.date(int(year),yt_months_array[month],int(day)).strftime('%Y-%m-%d')
    return date

def convert_yt_duration(d):
    length = d
    return length

'''
Track Height Locking in REAPER
Mar 28, 2018
REAPER Mania
/channel/UCq297H7Ca98HlB5mVFHGSsQ
https://www.youtube.com/watch?v=5P04TvRSwyk
476.801
'''

def parse_video_data(d):
    video_data_array = d.split('\n')

    video_title = video_data_array[0]
    video_id = convert_yt_title(video_title)
    video_date = convert_yt_date(video_data_array[1])
    video_creator = video_data_array[2]
    channel_url = video_data_array[3]
    video_url = video_data_array[4]
    video_length = convert_yt_duration(video_data_array[5])

    video_data_array = []
    video_data_array = [video_title, video_id, video_date, video_creator, channel_url, video_url, video_length]
    print(video_data_array)

    '''
    with open("2011-05-26-60 Snap and AlignTools.md") as search:
        url = ''
        for line in search:
            if re.search('video_link:', line):
                url = line.rstrip()
        url = url.split('video_link:')[1].lstrip()
        print(url)

    text = text.replace(' - ', '-')
    text = text.replace(' ', '-')
    text = ''.join(c for c in text if c.isalnum() or c =='-' or c =='_')
    video_title = text.lower()
    if not os.path.exists(video_title):
        os.makedirs(video_title)
    '''

def create_new_blog_post():
    isFile = os.path.isfile(join(home, "shamabi.md"))
    print(isFile)
    # blog_posts = [f for f in listdir(home) if isfile(join(home, f)) and f.endswith(".md")]
    # for f in blog_posts:
        # print(f)


        
def check_arg(args=None):

# Command line options
# Currently, only the url option is used

    parser = argparse.ArgumentParser(description='download video')
    parser.add_argument('-d', '--data',
                        help='video data',
                        required='True')

    results = parser.parse_args(args)
    return (results.data)

if __name__ == '__main__':
    data = check_arg(sys.argv[1:])
    parse_video_data(data)
    # create_new_blog_post()
