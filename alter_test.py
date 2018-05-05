# This program consist of two parts:
# 1. Turning given text to speech (wav file output)
# 2. Turning speech back to text

import os
import speech_recognition as sr
import uuid
import datetime
from config import *
from noise import *
import time

temp_file_name = str(datetime.datetime.now()).replace(".","-").replace(" ","-").replace(":","-")
#starting_text = "Dogs are highly variable in height and weight."
"""starting_texts = ["Football is a family of team sports that involve, to varying degrees, kicking a ball with a foot to score a goal.", "Unqualified, the word football is understood to refer to whichever form of football is the most popular in the regional context in which the word appears", "Sports commonly called football in certain places include association football", "Various forms of football can be identified in history, often as popular peasant games", "everal of the football codes are the most popular team sports in the world."]"""

"""starting_texts2 = ["Basketball is a limited-contact sport played on a rectangular court", "While most often played as a team sport with five players on each side", "three-on-three, two-on-two, and one-on-one competitions are also common", "A pass is a method of moving the ball between players", "Dribbling is the act of bouncing the ball continuously with one hand", "A block is performed when, after a shot is attempted"]"""

"""starting_texts3 = "Variations of basketball are activities based on the game of basketball, using common basketball skills and equipment (primarily the ball and basket). Some variations are only superficial rules changes, while others are distinct games with varying degrees of basketball influences. Other variations include children's games, contests or activities meant to help players reinforce skills.".split(" ")"""

"""starting_texts4 = "The domestic cat is believed to have evolved from the Near Eastern wildcat, whose range covers vast portions of the Middle East westward to the Atlantic coast of Africa".split(" ")"""
starting_texts5 = "hey-e-s ticipi stack udipi, reverse-engenring router switch arp forwarding routing system-call windows linux operating-system bit byte computer cookie ethernet fingerprint grep l-s script code jaavascript jaava pie-thon udp en-til-em r-s-hey".split(" ")

def chooseOutput(output, original):
	for choice in output:
		if choice != original:
			return choice

def textToWav(text, wav_full_path, text_to_speech_path):
	run_command = 'echo ' + text + ' | cscript "' + text_to_speech_path + '" -w ' + wav_full_path + ' -voice "Microsoft Zira Desktop"'
	os.system(run_command)

def wavToText(wav_path, output_full_path):
	output = []
	r = sr.Recognizer()
	with sr.AudioFile(wav_path) as source:
		audio = r.record(source)  # read the entire audio file

	# recognize speech using Sphinx
	try:
		decoder = r.recognize_sphinx(audio, show_all=True)
		#print ('Best 10 hypothesis: ')
		for best, i in zip(decoder.nbest(), range(10)):
			output.append(best.hypstr)

		#output = decoder.hyp().hypstr
		#print("Sphinx thinks you said: " + output)
	except sr.UnknownValueError:
		print("Sphinx could not understand audio")
	except sr.RequestError as e:
		print("Sphinx error; {0}".format(e))

	return output	

# main
print "start!"
temp_full_wav_path = os.path.join(temp_speech_path, temp_file_name + ".wav")
for starting_text in starting_texts5:
	textToWav(starting_text, temp_full_wav_path, text_to_speech_path)
	guassian_noise(temp_full_wav_path)
	#noise_wav(temp_full_wav_path)
	print("You said: " + starting_text)
	output = wavToText(temp_full_wav_path, os.path.join(temp_speech_path, temp_file_name + ".txt"))
	output = chooseOutput(output, starting_text)
	print("Sphinx thinks you said: ", output)
