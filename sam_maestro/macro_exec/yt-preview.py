#!/usr/bin/python3

import sys
import os
import subprocess
import argparse
import glob
import math
import re
import shutil
import codecs

import json
from collections import OrderedDict
import io

home = os.path.dirname(os.path.realpath(__file__))

height = 180
columns = 100
rows = 1
video_data_array = []
yt_video_out = '/tmp/video.mp4'

def move_file(file):
	destination = os.path.expanduser("~/_dev/blendertube.github.io/images/post-content")
	shutil.move(file, destination)

def clean_up_tmp():
	os.remove(yt_video_out)

def get_yt_video_url(file):
	# print(os.path.dirname(file))
	# print(os.path.expanduser("~/_dev/blendertube.github.io/_posts"))
	if os.path.dirname(file) != os.path.expanduser("~/_dev/blendertube.github.io/_posts"):
		return False

	with codecs.open(file, 'r', 'utf-8') as search:
		for line in search:
			try:
				if re.search('video_url:', line):
					video_url = line.rstrip()
				if re.search('video_id:', line):
					video_id = line.rstrip()
			except:
				break
		video_url = video_url.split('video_url:')[1].lstrip()
		video_id = video_id.split('video_id:')[1].lstrip()
	return [video_url, video_id]

def download_video(url):
	cmd = ['youtube-dl', '-f', '22', '-o', yt_video_out, str(url)]
	
	# download the video
	subprocess.call(cmd)

def extract_thumb(file):
	file = '/tmp/'+file+'-thumb.jpg'
	count_frames_cmd = """ffmpeg -nostats -i /tmp/video.mp4 -vcodec copy -f rawvideo -y /dev/null 2>&1 | grep frame | awk '{split($0,a,"fps")}END{print a[1]}' | sed 's/.*= *//'"""
	ps = subprocess.Popen(count_frames_cmd, shell=True, stdout=subprocess.PIPE)
	frames = ps.communicate()[0].decode('utf-8').strip()
	nth_frame = math.floor(int(frames) / 100)
	# print('extract every ' + str(nth_frame) + ' frames')

	extract_frames_cmd = ['ffmpeg', '-loglevel', 'panic', '-y', '-i', '/tmp/video.mp4', '-frames', '1', '-q:v', '1', '-vf', 'select=not(mod(n\,'+str(nth_frame)+'))', file]
	subprocess.call(extract_frames_cmd)
	move_file(file)

def extract_preview(file):
	file = '/tmp/'+file+'-preview.jpg'
	count_frames_cmd = """ffmpeg -nostats -i /tmp/video.mp4 -vcodec copy -f rawvideo -y /dev/null 2>&1 | grep frame | awk '{split($0,a,"fps")}END{print a[1]}' | sed 's/.*= *//'"""
	ps = subprocess.Popen(count_frames_cmd, shell=True, stdout=subprocess.PIPE)
	frames = ps.communicate()[0].decode('utf-8').strip()
	nth_frame = math.floor(int(frames) / 100)
	# print('extract every ' + str(nth_frame) + ' frames')

	extract_frames_cmd = ['ffmpeg', '-loglevel', 'panic', '-y', '-i', '/tmp/video.mp4', '-frames', '1', '-q:v', '1', '-vf', 'select=not(mod(n\,'+str(nth_frame)+')),scale=-1:'+str(height)+',tile='+str(columns)+'x'+str(rows), file]
	subprocess.call(extract_frames_cmd)
	move_file(file)

def check_arg(args=None):

# Command line options
# Currently, only the url option is used

	parser = argparse.ArgumentParser(description='download video')
	parser.add_argument('-u', '--url',
						help='video url',
						required='True')

	results = parser.parse_args(args)
	return (results.url)

if __name__ == '__main__':
	u = check_arg(sys.argv[1:])

	video_data_array = get_yt_video_url(u)
	# exit()

	if video_data_array == False:
		print("finder selection error!")
	else:
		download_video(video_data_array[0]) # pass in url
		extract_preview(video_data_array[1]) # pass in id
		extract_thumb(video_data_array[1]) # pass in id
		clean_up_tmp()