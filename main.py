from alter import *
import nlp

import regex
import nltk
import pprint
import time

def joke(word, old_word):
	searchedWord = word

	temp_full_wav_path = os.path.join(temp_speech_path, temp_file_name + ".wav")
	temp_full_wav_path_res1 = os.path.join(temp_speech_path, "result" + ".wav")
	temp_full_wav_path_res2 = os.path.join(temp_speech_path, "result2" + ".wav")
	temp_full_wav_path_res3 = os.path.join(temp_speech_path, "result3" + ".wav")

	textToWav(searchedWord, temp_full_wav_path, text_to_speech_path)
	guassian_noise(temp_full_wav_path)
	#noise_wav(temp_full_wav_path)
	print("You said: " + searchedWord)
	words = wavToText(temp_full_wav_path, os.path.join(temp_speech_path, temp_file_name + ".txt"))
	newWord  = chooseOutput(words, searchedWord)
	searchedWord = newWord
	print "Sphinx thinks you said: " + searchedWord

	nlp.searchedWord = searchedWord

	results = nlp.calculateParallel(nlp.makeReq, range(4), 1)
	content = " ".join(results)
	text = nlp.createText(content)

	# sort by relevance
	raw = regex.findall(u"[^\s\d\w][\s\w]*"+ searchedWord +"[\s\w]*[^\s\d\w]", text)

	raw = [x[1:] for x in raw if len(x) <200 and len(x) > 30 and "www" not in x and not any(char.isdigit() for char in x) and "pdf" not in x]
	raw = list(set(raw))

	#pp.pprint(raw)
	ranked = [(float([x for (_,x) in nltk.pos_tag(y.split())].count('NN')) / len([x for (_,x) in nltk.pos_tag(y.split())]),y) for y in raw ]
	ranked = [(rank[0], rank[1].replace(searchedWord, '"' + searchedWord.upper() + '"')) for rank in ranked]
	pp = pprint.PrettyPrinter(indent = 4)
	best_rankes = sorted(ranked, key = lambda tup: abs(0.1 - tup[0]))[:3]
	print len(best_rankes)
	pp.pprint(best_rankes)
	textToWav(best_rankes[0][1], temp_full_wav_path_res1, text_to_speech_path)
	textToWav(best_rankes[1][1], temp_full_wav_path_res2, text_to_speech_path)
	textToWav(best_rankes[2][1], temp_full_wav_path_res3, text_to_speech_path)

	#may add text to speech
	
words = "A-E-S triple-DES hey-e-s ticipi stack udipi, reverse-engenring router switch arp forwarding routing system-call windows linux operating-system bit byte computer cookie ethernet fingerprint grep l-s script code jaavascript jaava pie-thon udp en-til-em r-s-hey".split(" ")
real_word = "AES"
for word in words:
	joke(word, real_word)
	time.sleep(2)
	break