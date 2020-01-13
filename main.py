import sys, os
import datetime as dt
import random as rand
import pygame
import time
import speech_recognition as sr
from gtts import gTTS
from mutagen.mp3 import MP3 as mp3
# 1. Load words & sentences from list file
# 2. Display either one word or sentence randomly to ask an examinee to write down and speak out
# 3. Mark your answer and give you the result
## Pre-process ##
ARR_EN = list()
ARR_DE = list()
now = dt.datetime.now()
###############
### PRIMARY Setting ###
# SOURCE_FILE = "words/{:%Y%m%d}.txt".format(now)
# SOURCE_MP_FILE = "mp3_files/{:%Y%m%d}".format(now)
SOURCE_FILE = "words/20200111.txt"
SOURCE_MP_FILE = "mp3_files/20200111"
LANGUAGE = "de" #Deutsch
PROGRESS = "\r #Progress → {:d}/{:d}"
MENU_SPEAK = 1
MENU_WRITE = 2
#######################
### Functions ###
def load_file(source_file_name):
    with open(source_file_name) as f:
        flag = True
        for s in f.readlines():
            s = s.replace('\n','')
            if flag:
                ARR_DE.append(s)
                flag = False
            else:
                ARR_EN.append(s)
                flag = True
def create_mp3Files():
    arr_len = len(ARR_DE)
    index = 0
    if arr_len <= 0:
        print("Err:Word array is empty!!")
        exit()
    else:
        for s in ARR_DE:
            index += 1
            speech = gTTS(text=s, lang=LANGUAGE, slow=False)
            FILE_PATH = SOURCE_MP_FILE + "/{:03d}.mp3".format(index)
            speech.save(FILE_PATH)
            print(PROGRESS.format(index,arr_len), end='')
def convert_to_mp3(source_file_name, mp3_folder_name):
    if not os.path.exists(source_file_name):
        print('Err:Please insert source file into filepath:{:}!'.format(SOURCE_FILE))
        exit()
    else:
        print("Loading words from file......")
        load_file(source_file_name)
        print("Load complete!!")
        if not os.path.exists(mp3_folder_name):
            print("Start converting......")
            print("Creating MP3 files....")
            os.mkdir(mp3_folder_name)
            create_mp3Files()
            print("\nMP3 Conversion is complete!!")
        else:
            print("The mp3 folder already exists")
def play_mp3(file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    mp3_len = mp3(file_path).info.length
    pygame.mixer.music.play(1)
    time.sleep(mp3_len+0.1)
    pygame.mixer.music.stop()
def sound_recog():
    try:
        r = sr.Recognizer()
        ## Set record threshold ##
        r.dynamic_energy_threshold = False
        r.energy_threshold = 400
        r.operation_timeout = True
        ##########################
        with sr.Microphone() as source:
            print("Please say something!")
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
            print("↓↓↓↓Google thinks you spoke to him that ↓↓↓↓\n" + r.recognize_google(audio, language="de-DE"))
    except sr.UnknownValueError:
        print("Google could not understand what you had told")
        exit()
    except sr.RequestError as e:
        print("Google Error; {0}".format(e))
        exit()
def clean_screen():
    os.system("clear")
    print(MANUAL)
#################
##### Main ######
#################
convert_to_mp3(SOURCE_FILE, SOURCE_MP_FILE)
MANUAL = """
    ---Start---
    Display one word or sentence for each attempt randomly selected from the word list
    1. 'w' key indicates system asks you to translate Eng. sentence to Deutsch
    2. '?' key indicates system plays a Deutsch version of the sentence for you
    3. 's' key indicates system asks you to speak the sentence in Deutsch via microphone
    4. 'q' key indicates system terminates the program
    5. 'm' key indicates system clears screen of console and displays the manual again
    """
print(MANUAL)
rand_num = int(rand.random()*(len(ARR_DE)-1))
FILE_PATH = SOURCE_MP_FILE + "/{:03d}.mp3".format(rand_num+1)
while True:
    print("Problem >> {:s}".format(ARR_EN[rand_num]))
    print("Please input the key and press Enter key >> ", end='')
    key = input().strip()
    if key == 'm':
        clean_screen()
    elif key == '?':
        play_mp3(FILE_PATH)
        clean_screen()
    elif key == 's':
        print("Speak out in Deutsch for the sentence")
        sound_recog()
        print("Answer is [{:s}]".format(ARR_DE[rand_num]))
        input("Press Enter to continue......")
        clean_screen()
        rand_num = int(rand.random()*(len(ARR_DE)-1))
        FILE_PATH = SOURCE_MP_FILE + "/{:03d}.mp3".format(rand_num+1)
    elif key == 'w':
        print("Write an answer in Deutsch >> ", end='')
        answer = input()
        print("Answer is [{:s}]".format(ARR_DE[rand_num]))
        input("Press Enter to continue......")
        clean_screen()
        rand_num = int(rand.random()*(len(ARR_DE)-1))
        FILE_PATH = SOURCE_MP_FILE + "/{:03d}.mp3".format(rand_num+1)
    elif key == 'q':
        print("QUIT PROGRAM")
        exit()
    else:
        print("Err:Input a wrong key!")
        input("Press Enter to continue......")
        clean_screen()