############################################################################
# File Name: music_player_class.py
# Description: an integrate music player class for better use
############################################################################
import os
import random

import pygame


class Music_Player:
  def __init__(self):
    self.load_music_files()
    pygame.mixer.music.set_volume(0.6)
    self.music_index=0

  def load_music_files(self):
    # load all music files
    self.music_list=[]
    for file in os.listdir('music_assets'):
      if file.endswith('.mp3'):
        self.music_list.append('music_assets/'+file)

  def play_random_music(self):
    # play random music
    index=random.randint(0,len(self.music_list)-1)
    self.play_music(index)

  def play_music(self,index):
    # play music
    self.stop_music()
    self.music_index=index
    pygame.mixer.music.load(self.music_list[index])
    # infinite loop
    pygame.mixer.music.play(-1)

  def stop_music(self):
    pygame.mixer.music.stop()

  def pause_music(self):
    pygame.mixer.music.pause()