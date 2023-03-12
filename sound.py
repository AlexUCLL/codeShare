from random import randint
import re
import os
import pygame
import glob

class SoundLibrary:

    def __init__(self):
        self.table = self.__create_table()

    def __find_audio_files(self):
        rootdir = "./sounds"
        rx = 'ogg'
        audio_files = []
        for root, dirs, files in os.walk(rootdir, topdown=False):
            for file in files:
                if re.match(r'.*\.ogg', file):
                    audio_files.append(re.sub(r'\\+', r'/', os.path.join(root,file)) )
        return audio_files

    def __derive_ids(self, path):
        string= re.sub(r'^\./sounds', '', path)
        string=re.sub(r'.ogg$', '', string)
        return string

    def __create_table(self):
        sounds = self.__find_audio_files()
        ids = []
        actual = []
        for sound in sounds:
            ids.append(self.__derive_ids(sound))
            actual.append(pygame.mixer.Sound(sound))
        table = dict(zip(ids, actual))
        return table

    def play_random_explosion(self):
        random = randint(1,6)
        string = "/explosions/" + str(random)
        self.table[string].play()
        
