from urllib import quote_plus
import urllib2,cookielib
import regex
import codecs
import lxml.etree as ET
from nltk.tokenize import sent_tokenize
import nltk
from multiprocessing.dummy import Pool as ThreadPool
from multiprocessing.dummy import Pool as ThreadPool
import time
searchedWord = ""

# pull data from google
def calculateParallel(func, numbers, threads=2):
	pool = ThreadPool(threads)
	results = pool.map(func, numbers)
	pool.close()
	pool.join()
	return results
	
# pull data from google
def calculateParallel(func, numbers, threads=2):
	pool = ThreadPool(threads)
	results = pool.map(func, numbers)
	pool.close()
	pool.join()
	return results	
	
def makeReq(i):
	time.sleep(1)
	bracetedRequest = "\""+searchedWord+"\" filetype:pdf"

	site = "https://www.google.co.il/search?q=" + quote_plus(bracetedRequest) + "&start=" + str(i*10)
	hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
		   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		   'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
		   'Accept-Encoding': 'none',
		   'Accept-Language': 'en-US,en;q=0.8',
		   'Connection': 'keep-alive',
		   'Host': 'www.google.com'}
	   
	req = urllib2.Request(site, headers = hdr)

	try:
		page = urllib2.urlopen(req)
	except urllib2.HTTPError, e:
		#x = 0/0
		#print e
		print e.fp.read()
		return ""
	data = page.read()
	return data
	
def createText(text):
	text = regex.sub("\[http[^]]+? ([^]]+)]", r"\1", text) 
	text = regex.sub("\[http[^]]+]", "", text) 
	text = regex.sub("(?s)<script.+?</script>", "", text) # remove scripts 
	text = regex.sub("(?s)<style.+?</style>", "", text) # remove scripts 
	text = regex.sub("(?s)<ref>.+?</ref>", "", text) # remove reference links
	text = regex.sub("(?s)<[^>]+>", "", text) # remove html tags
	text = regex.sub("&[a-z]+;", "", text) # remove html entities
	text = regex.sub("(?s){{.+?}}", "", text) # remove markup tags
	text = regex.sub("(?s){.+?}", "", text) # remove markup tags
	text = regex.sub("(?s)\[\[([^]]+\|)", "", text) # remove link target strings
	text = regex.sub("(?s)\[\[([^]]+\:.+?]])", "", text) # remove media links

	text = regex.sub("[']{5}", "", text) # remove italic+bold symbols
	text = regex.sub("[']{3}", "", text) # remove bold symbols
	text = regex.sub("[']{2}", "", text) # remove italic symbols

	text = regex.sub(u"[^ \r\n\p{latin}}\d'.?!]", " ", text)
	text = regex.sub(r'[^\x00-\x7F]+',' ', text)
	text = text.lower()

	text = regex.sub("[ ]{2,}", " ", text) # Squeeze spaces.
	paras = text.split("\n")
	
	nltk.download('averaged_perceptron_tagger')
	#nltk.download('punkt')
	final = ""
	for para in paras:
		if len(para) > 500:
			sents = [regex.sub("([.!?]+$)", r" \1", sent) for sent in sent_tokenize(para.strip())]
			final += " ".join(sents) + "\n"
	
	return text #or final?