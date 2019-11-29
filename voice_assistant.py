import os 
import pyttsx3
import speech_recognition as sr
from datetime import datetime
import webbrowser
import shutil
import wikipedia
import string
from PIL import Image
from google_images_download import google_images_download
import time 



#PYTHON TEXT TO SPEECH
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice',voices[0].id)


#SPEAK 

def speak(text):
	engine.say(text)
	print("ASSISTANT: ",text)
	engine.runAndWait()
	


#LISTEN
def listen():
	r = sr.Recognizer()
	with sr.Microphone() as source:
		print('listning...')
		audio = r.listen(source)
		said = ''

		try:
			said = r.recognize_google(audio)
			print('YOU: ' ,said)
		except Exception as e:
			print(e)
			pass

	return said



#NOTE THAT FUNCTION
def note_that(text):
	text =text.replace('note','')
	text =text.replace('that','')
	filename = str(datetime.now())
	filename = filename.replace('.',';')
	filename = filename.replace('-','')
	filename = filename.replace(':','')
	obj = open(filename+'.txt','w')
	obj.write(text)
	speak('noted')



def note_info():
	speak('give me some information about your note example some keywords')
	path = 'C:/Users/kunal kushwaha/python/'
	audio = listen()
	keywords = audio.split()
	ist = os.listdir(path)
	textfile = []

	for i in ist:
		if '.txt' in i:
			textfile.append(i)

	clone = []
	for i in textfile:
		clone.append(0)

	val = 0
	

	for i in textfile:
		for j in keywords:
			obj = open(i,'r')
			text = obj.read()
			if j in text:
				val += 1
		clone[textfile.index(i)] = val

	mno = max(clone)
	fo = textfile[clone.index(mno)]

	obj2 = open(fo,'r')
	main = obj2.read()
	speak('you told me that' ,main)




#WISH ME 
def wish():
	raw_time = str(datetime.time(datetime.now()))
	hour = int(raw_time[0]+raw_time[1])
	if hour < 12 :
		return 'good morning'
	elif hour < 16 and hour > 12:
		return 'good afternoon '
	elif hour < 24:
		return 'good evening'




#IMAGES SHOW 
def show_images():
	speak('what do you want to search')
	req = listen()
	search_queries =[req] 
	speak('wait for few seconds ')
	response = google_images_download.googleimagesdownload()
	arguments = {"keywords": req, "format": "jpg", "limit":1, "print_urls":False, "size": "medium", "aspect_ratio": "panoramic"} 
	try: 
		response.download(arguments) 
 
	except FileNotFoundError: 
		pass
		print('sorry cant download try again')
	image_name = os.listdir('C:/Users/kunal kushwaha/python/downloads/'+req+'/')[0]

	img = Image.open('C:/Users/kunal kushwaha/python/downloads/'+req+'/'+image_name)
	img.show()
	time.sleep(10)
	



#MAIN RUN
variable = True
while variable:
	audio = listen().lower()

	if'hello' in audio:
		speak('hello sir '+wish())

	elif 'open' in audio:
		audio = audio.replace('open','')
		audio = audio.replace(' ','')
		speak('opening '+audio)
		webbrowser.open(audio+'.com')



	elif 'wikipedia' in audio:
		audio = audio.replace('wikipedia','')
		print('getting results....')
		results = wikipedia.summary(audio,sentences = 3)
		print(results)
		speak(results)

	elif 'show' in audio:
		show_images()

	elif 'note' in audio:
		note_that(audio)

	elif 'keywords' in audio:
		note_info()

	elif 'stop' in audio:
		speak("bye sir ")
		path = 'C:/Users/kunal kushwaha/python/downloads/'
		for i in os.listdir(path):
			try:
				shutil.rmtree(path+i)
			except:
				pass

		variable = False
