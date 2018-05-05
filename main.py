from alter import *
import nlp

import regex
import nltk
import pprint
import time
searchedWord = "network"

temp_full_wav_path = os.path.join(temp_speech_path, temp_file_name + ".wav")
textToWav(searchedWord, temp_full_wav_path, text_to_speech_path)
#guassian_noise(temp_full_wav_path)
noise_wav(temp_full_wav_path)
print("You said: " + searchedWord)
words = wavToText(temp_full_wav_path, os.path.join(temp_speech_path, temp_file_name + ".txt"))
newWord  = chooseOutput(words, searchedWord)
searchedWord = newWord
print "Sphinx thinks you said: " + searchedWord

nlp.searchedWord = searchedWord

results = nlp.calculateParallel(nlp.makeReq, range(10), 1)
content = " ".join(results)
print "done!"
text = nlp.createText(content)

# sort by relevance
raw = regex.findall(u"[^\s\d\w][\s\w]*"+ searchedWord +"[\s\w]*[^\s\d\w]", text)

raw = [x[1:] for x in raw if len(x) <200 and len(x) > 30 and "www" not in x and not any(char.isdigit() for char in x) and "pdf" not in x]
raw = list(set(raw))

#pp.pprint(raw)
ranked = [(float([x for (_,x) in nltk.pos_tag(y.split())].count('NN'))/len([x for (_,x) in nltk.pos_tag(y.split())]),y) for y in raw ]
pp = pprint.PrettyPrinter(indent=4)
pp.pprint(sorted(ranked, key=lambda tup: abs(0.1-tup[0]))[:5])