# -*- coding: utf-8 -*-
"""
Created on Sat Aug  5 15:18:57 2023

@author: bhuva
"""
import subprocess
import re
import random
import nltk
import numpy as np
from nltk.stem import WordNetLemmatizer
import training
import serial
import time
import vlc
from gtts import gTTS
import librosa
import soundfile as sf
from mutagen.wave import WAVE

#for arduino
s='/dev/ttyACM0'
ser=serial.Serial(s,9600)

#for pi pico
def send_data(serial_port, data):
    serial_port.write(data.encode())
pico_serial_port = serial.Serial("/dev/ttyS0", 9600, timeout=1)
#speaker
language='en'
def voice_creation(string):
    obj=gTTS(text=string,lang=language)
    obj.save('voice.wav')
def file_conversion(path):
    x,_=librosa.load(path,sr=16000)
    sf.write('tmp.wav',x,16000)
    audio=WAVE('tmp.wav')
    return audio.info.length
def play(path1):
    sound=vlc.MediaPlayer('voice.wav')
    sound.set_rate(1.25)
    sound.play()
lm = WordNetLemmatizer() #for getting words
def set_female_voice(text):
    try:
        subprocess.call(['espeak',text])
    except Exception as e:
        print(f"An error occurred: {e}")
def ourText(text):
  newtkns = nltk.word_tokenize(text)
  newtkns = [lm.lemmatize(word) for word in newtkns]
  return newtkns
 
def wordBag(text, vocab):
  newtkns = ourText(text)
  bagOwords = [0] * len(vocab)
  for w in newtkns:
    for idx, word in enumerate(vocab):
      if word == w:
        bagOwords[idx] = 1
  return np.array(bagOwords)

def Pclass(text, vocab, labels):
  bagOwords = wordBag(text, vocab)
  ourResult = training.ourNewModel.predict(np.array([bagOwords]))[0]
  newThresh = 0.2
  yp = [[idx, res] for idx, res in enumerate(ourResult) if res > newThresh]

  yp.sort(key=lambda x: x[1], reverse=True)
  newList = []
  for r in yp:
    newList.append(labels[r[0]])
  return newList

def getRes(firstlist, fJson):
  tag = firstlist[0]
  listOfIntents = fJson["intents"]
  for i in listOfIntents:
    if i["tag"] == tag:
      ourResult = random.choice(i["response"])
      break
  return ourResult
pattern=r'selfie|selvi|selbi|selbe|selbee|silbi|silby|sylbie|sylbi|silbe|silby|silbi'
while True:
    msg=""
    msg1=""
    while True:
            recieved_data=ser.read().decode()
            msg=msg+recieved_data
            print(msg)
            match=re.search(pattern,msg,re.IGNORECASE)
            if(match):
                msg1 = re.sub(pattern, "", msg)
                break
            
    print(msg1)
    intents = Pclass(msg1, training.newWords, training.ourClasses)
    ourResult = getRes(intents, training.data)
    print(ourResult,'intent:',intents[0])
    voice_creation(ourResult)
    d=file_conversion('voice.wav')       
    send_data(pico_serial_port, str(d))
    time.sleep(1)
    #sending data to pi pico regarding face
    data_to_send = intents[0]
    send_data(pico_serial_port, data_to_send)
    time.sleep(1)
    print(f"Sent: {data_to_send}")
    play(('tmp.wav'))